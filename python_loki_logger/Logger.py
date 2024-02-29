import time
import json
import requests
from typing import Dict, Optional, Union


class LokiLogger:

    def __init__(
        self,
        baseUrl: str,
        auth: tuple | None = None,
        severity_label: str = "level",
        pushUrl: str = "/loki/api/v1/push",
    ) -> None:
        if baseUrl.endswith("/"):
            raise ValueError("Base URL must not end with /")
        self.baseUrl = baseUrl
        self.pushUrl = pushUrl
        self.severity_label = severity_label
        self.auth = auth

    def __callApi(
        self,
        level: str,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        payload: dict = {"message": message}
        if extras is not None:
            payload.update(extras)
        if labels is None:
            labels = {}
        labels[self.severity_label] = level

        reqBody = {
            "streams": [
                {
                    "stream": labels,
                    "values": [[str(time.time_ns()), json.dumps(payload)]],
                }
            ]
        }

        try:
            if self.auth is not None:
                resp = requests.post(
                    self.baseUrl + self.pushUrl, json=reqBody, auth=self.auth
                )
            else:
                resp = requests.post(self.baseUrl + self.pushUrl, json=reqBody)

            if resp.status_code != 204:
                raise Exception("Something Went Wrong.")
        except Exception as e:
            raise e

    def customLevel(
        self,
        level: str,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.__callApi(
            level,
            message,
            extras,
            labels,
        )

    def error(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.__callApi(
            "error",
            message,
            extras,
            labels,
        )

    def info(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.__callApi(
            "info",
            message,
            extras,
            labels,
        )

    def warn(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.__callApi(
            "warn",
            message,
            extras,
            labels,
        )

    def debug(
        self,
        message: Union[str, dict],
        extras: Optional[dict] = None,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.__callApi(
            "debug",
            message,
            extras,
            labels,
        )
