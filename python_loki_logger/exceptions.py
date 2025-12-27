"""Custom exceptions for python_loki_logger."""


class LokiLoggerError(Exception):
    """Base exception for all Loki Logger errors."""

    pass


class LokiConnectionError(LokiLoggerError):
    """Raised when connection to Loki fails."""

    pass


class LokiPushError(LokiLoggerError):
    """Raised when pushing logs to Loki fails."""

    def __init__(self, message: str, status_code: int, response_text: str = ""):
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            response_text: Response text from Loki
        """
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"{message} (status_code={status_code})")


class LokiConfigurationError(LokiLoggerError):
    """Raised when there's a configuration error."""

    pass
