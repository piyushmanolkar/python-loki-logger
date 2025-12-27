"""Unit tests for custom exceptions."""

import pytest

from python_loki_logger.exceptions import (
    LokiLoggerError,
    LokiConnectionError,
    LokiPushError,
    LokiConfigurationError,
)


class TestExceptions:
    """Test custom exception classes."""

    @pytest.mark.unit
    def test_loki_logger_error_is_base_exception(self):
        """Test that LokiLoggerError is the base exception."""
        error = LokiLoggerError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    @pytest.mark.unit
    def test_loki_connection_error_inherits_from_base(self):
        """Test that LokiConnectionError inherits from LokiLoggerError."""
        error = LokiConnectionError("Connection failed")
        assert isinstance(error, LokiLoggerError)
        assert isinstance(error, Exception)
        assert str(error) == "Connection failed"

    @pytest.mark.unit
    def test_loki_push_error_with_status_code(self):
        """Test LokiPushError with status code."""
        error = LokiPushError("Push failed", status_code=500, response_text="Error")
        assert isinstance(error, LokiLoggerError)
        assert error.status_code == 500
        assert error.response_text == "Error"
        assert "status_code=500" in str(error)

    @pytest.mark.unit
    def test_loki_push_error_without_response_text(self):
        """Test LokiPushError without response text."""
        error = LokiPushError("Push failed", status_code=404)
        assert error.status_code == 404
        assert error.response_text == ""

    @pytest.mark.unit
    def test_loki_configuration_error_inherits_from_base(self):
        """Test that LokiConfigurationError inherits from LokiLoggerError."""
        error = LokiConfigurationError("Invalid config")
        assert isinstance(error, LokiLoggerError)
        assert isinstance(error, Exception)
        assert str(error) == "Invalid config"

    @pytest.mark.unit
    def test_all_exceptions_can_be_raised_and_caught(self):
        """Test that all exceptions can be raised and caught."""
        with pytest.raises(LokiLoggerError):
            raise LokiLoggerError("base error")

        with pytest.raises(LokiConnectionError):
            raise LokiConnectionError("connection error")

        with pytest.raises(LokiPushError):
            raise LokiPushError("push error", status_code=500)

        with pytest.raises(LokiConfigurationError):
            raise LokiConfigurationError("config error")

    @pytest.mark.unit
    def test_catch_specific_exception_as_base(self):
        """Test that specific exceptions can be caught as base exception."""
        try:
            raise LokiConnectionError("connection error")
        except LokiLoggerError as e:
            assert isinstance(e, LokiConnectionError)
            assert str(e) == "connection error"
