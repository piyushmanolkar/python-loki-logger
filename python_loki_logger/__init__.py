"""Python Loki Logger - A library for pushing logs to Grafana Loki."""

from python_loki_logger.Logger import LokiLogger
from python_loki_logger.exceptions import (
    LokiLoggerError,
    LokiConnectionError,
    LokiPushError,
    LokiConfigurationError,
)

__version__ = "3.0.0"
__all__ = [
    "LokiLogger",
    "LokiLoggerError",
    "LokiConnectionError",
    "LokiPushError",
    "LokiConfigurationError",
]
