"""Main logger implementation for pushing logs to Grafana Loki."""

import time
import json
from typing import Dict, Optional, Union, Tuple

import requests
from requests.exceptions import RequestException

from python_loki_logger.exceptions import (
    LokiConnectionError,
    LokiPushError,
    LokiConfigurationError,
)


class LokiLogger:
    """A logger for pushing logs to Grafana Loki.

    This class provides an easy-to-use interface for sending logs to a Grafana Loki
    instance with support for custom labels, severity levels, and authentication.

    Example:
        >>> logger = LokiLogger(baseUrl="https://loki.example.com")
        >>> logger.info("Application started", labels={"app": "my-app"})
        >>> logger.error("An error occurred", extras={"user_id": "123"})
    """

    def __init__(
        self,
        baseUrl: str,
        auth: Optional[Tuple[str, str]] = None,
        severity_label: str = "level",
        pushUrl: str = "/loki/api/v1/push",
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the Loki logger.

        Args:
            baseUrl: Base URL of the Loki instance (e.g.,
                "https://loki.example.com"). Must not end with a trailing slash.
            auth: Optional authentication tuple (username, password) for basic
                auth.
            severity_label: Label key to use for severity level. Defaults to
                "level".
            pushUrl: Path to the Loki push API endpoint. Defaults to
                "/loki/api/v1/push".
            labels: Optional global labels to include in all log messages.
                These labels will be merged with method-specific labels.
                Method labels take precedence if there are conflicts.

        Raises:
            LokiConfigurationError: If baseUrl is invalid or ends with a trailing slash.

        Example:
            >>> logger = LokiLogger(
            ...     baseUrl="https://loki.example.com",
            ...     auth=("username", "password"),
            ...     severity_label="log_level",
            ...     labels={"app": "my-app", "environment": "production"}
            ... )
        """
        if not baseUrl:
            raise LokiConfigurationError("baseUrl cannot be empty")

        if baseUrl.endswith("/"):
            raise LokiConfigurationError("baseUrl must not end with /")

        if not pushUrl.startswith("/"):
            raise LokiConfigurationError("pushUrl must start with /")

        self.baseUrl = baseUrl
        self.pushUrl = pushUrl
        self.severity_label = severity_label
        self.auth = auth
        self.global_labels = labels if labels is not None else {}

    def _call_api(
        self,
        level: str,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Internal method to push logs to Loki.

        Args:
            level: Severity level of the log (e.g., "info", "error", "debug").
            message: The log message. Can be a string or a dictionary.
            extras: Optional extra data to include in the log payload.
            labels: Optional labels to attach to the log stream. These will be merged
                   with global labels, with method labels taking precedence.

        Raises:
            LokiConnectionError: If connection to Loki fails.
            LokiPushError: If Loki returns a non-204 status code.
        """
        # Build payload
        payload: dict = {"message": message}
        if extras is not None:
            payload.update(extras)

        # Build labels: merge global labels with method-specific labels
        # Method labels override global labels if there are conflicts
        merged_labels = self.global_labels.copy()
        if labels is not None:
            merged_labels.update(labels)
        merged_labels[self.severity_label] = level

        # Build request body according to Loki API spec
        reqBody = {
            "streams": [
                {
                    "stream": merged_labels,
                    "values": [[str(time.time_ns()), json.dumps(payload)]],
                }
            ]
        }

        # Make request to Loki
        url = self.baseUrl + self.pushUrl
        try:
            if self.auth is not None:
                resp = requests.post(url, json=reqBody, auth=self.auth, timeout=10)
            else:
                resp = requests.post(url, json=reqBody, timeout=10)

            # Loki returns 204 No Content on success
            if resp.status_code != 204:
                raise LokiPushError(
                    "Failed to push log to Loki",
                    status_code=resp.status_code,
                    response_text=resp.text,
                )

        except RequestException as e:
            raise LokiConnectionError(
                f"Failed to connect to Loki at {url}: {str(e)}"
            ) from e

    def customLevel(
        self,
        level: str,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Log a message with a custom severity level.

        Args:
            level: Custom severity level (e.g., "critical", "trace", "fatal").
            message: The log message. Can be a string or a dictionary.
            extras: Optional extra data to include in the log payload.
            labels: Optional labels to attach to the log stream.

        Raises:
            LokiConnectionError: If connection to Loki fails.
            LokiPushError: If Loki returns a non-204 status code.

        Example:
            >>> logger.customLevel(
            ...     "critical", "Database is down", labels={"db": "postgres"}
            ... )
        """
        self._call_api(level, message, extras, labels)

    def error(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Log an error message.

        Args:
            message: The error message. Can be a string or a dictionary.
            extras: Optional extra data to include in the log payload.
            labels: Optional labels to attach to the log stream.

        Raises:
            LokiConnectionError: If connection to Loki fails.
            LokiPushError: If Loki returns a non-204 status code.

        Example:
            >>> logger.error("Database connection failed", extras={"db": "postgres"})
        """
        self._call_api("error", message, extras, labels)

    def info(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Log an info message.

        Args:
            message: The info message. Can be a string or a dictionary.
            extras: Optional extra data to include in the log payload.
            labels: Optional labels to attach to the log stream.

        Raises:
            LokiConnectionError: If connection to Loki fails.
            LokiPushError: If Loki returns a non-204 status code.

        Example:
            >>> logger.info("Application started", labels={"version": "1.0.0"})
        """
        self._call_api("info", message, extras, labels)

    def warn(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Log a warning message.

        Args:
            message: The warning message. Can be a string or a dictionary.
            extras: Optional extra data to include in the log payload.
            labels: Optional labels to attach to the log stream.

        Raises:
            LokiConnectionError: If connection to Loki fails.
            LokiPushError: If Loki returns a non-204 status code.

        Example:
            >>> logger.warn("Deprecated API called", extras={"endpoint": "/api/v1/old"})
        """
        self._call_api("warn", message, extras, labels)

    def debug(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Log a debug message.

        Args:
            message: The debug message. Can be a string or a dictionary.
            extras: Optional extra data to include in the log payload.
            labels: Optional labels to attach to the log stream.

        Raises:
            LokiConnectionError: If connection to Loki fails.
            LokiPushError: If Loki returns a non-204 status code.

        Example:
            >>> logger.debug("Processing request", extras={"request_id": "abc123"})
        """
        self._call_api("debug", message, extras, labels)
