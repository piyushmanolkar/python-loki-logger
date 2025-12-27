"""Integration tests for LokiLogger logging methods with mocked requests."""

import json
import pytest
import requests
import requests_mock

from python_loki_logger import (
    LokiLogger,
    LokiPushError,
    LokiConnectionError,
)


class TestLokiLoggerMethods:
    """Test LokiLogger logging methods."""

    @pytest.mark.integration
    def test_info_logs_successfully(self, base_url, sample_message):
        """Test that info() successfully sends logs to Loki."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.info(sample_message)

            assert m.call_count == 1
            request = m.request_history[0]
            body = request.json()

            # Verify the structure
            assert "streams" in body
            assert len(body["streams"]) == 1
            stream = body["streams"][0]
            assert "stream" in stream
            assert "values" in stream
            assert stream["stream"]["level"] == "info"

            # Verify the message in the values
            values = stream["values"][0]
            assert len(values) == 2  # timestamp and payload
            payload = json.loads(values[1])
            assert payload["message"] == sample_message

    @pytest.mark.integration
    def test_error_logs_successfully(self, base_url, sample_message):
        """Test that error() successfully sends logs to Loki."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.error(sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            assert body["streams"][0]["stream"]["level"] == "error"

    @pytest.mark.integration
    def test_warn_logs_successfully(self, base_url, sample_message):
        """Test that warn() successfully sends logs to Loki."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.warn(sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            assert body["streams"][0]["stream"]["level"] == "warn"

    @pytest.mark.integration
    def test_debug_logs_successfully(self, base_url, sample_message):
        """Test that debug() successfully sends logs to Loki."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.debug(sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            assert body["streams"][0]["stream"]["level"] == "debug"

    @pytest.mark.integration
    def test_custom_level_logs_successfully(self, base_url, sample_message):
        """Test that customLevel() successfully sends logs to Loki."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.customLevel("critical", sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            assert body["streams"][0]["stream"]["level"] == "critical"

    @pytest.mark.integration
    def test_log_with_labels(self, base_url, sample_message, sample_labels):
        """Test logging with custom labels."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.info(sample_message, labels=sample_labels)

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            # Should include both the severity label and custom labels
            assert stream_labels["level"] == "info"
            assert stream_labels["app"] == "test-app"
            assert stream_labels["environment"] == "test"

    @pytest.mark.integration
    def test_log_with_extras(self, base_url, sample_message, sample_extras):
        """Test logging with extra data."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            logger.info(sample_message, extras=sample_extras)

            assert m.call_count == 1
            body = m.request_history[0].json()
            values = body["streams"][0]["values"][0]
            payload = json.loads(values[1])

            # Should include message and extras
            assert payload["message"] == sample_message
            assert payload["user_id"] == "123"
            assert payload["request_id"] == "abc-def"

    @pytest.mark.integration
    def test_log_with_dict_message(self, base_url):
        """Test logging with a dictionary message."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)
            message = {"error": "Database error", "code": 500}
            logger.error(message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            values = body["streams"][0]["values"][0]
            payload = json.loads(values[1])

            assert payload["message"] == message

    @pytest.mark.integration
    def test_log_with_auth(self, base_url, auth_tuple, sample_message):
        """Test logging with authentication."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, auth=auth_tuple)
            logger.info(sample_message)

            assert m.call_count == 1
            request = m.request_history[0]

            # Verify auth header is present
            assert "Authorization" in request.headers

    @pytest.mark.integration
    def test_log_with_custom_severity_label(self, base_url, sample_message):
        """Test logging with custom severity label."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, severity_label="log_level")
            logger.info(sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            # Should use custom severity label
            assert "log_level" in stream_labels
            assert stream_labels["log_level"] == "info"
            assert "level" not in stream_labels


class TestLokiLoggerErrors:
    """Test error handling in LokiLogger."""

    @pytest.mark.integration
    def test_non_204_response_raises_error(self, base_url, sample_message):
        """Test that non-204 response raises LokiPushError."""
        with requests_mock.Mocker() as m:
            m.post(
                f"{base_url}/loki/api/v1/push",
                status_code=500,
                text="Internal Server Error",
            )

            logger = LokiLogger(baseUrl=base_url)

            with pytest.raises(LokiPushError) as exc_info:
                logger.info(sample_message)

            assert exc_info.value.status_code == 500
            assert "Internal Server Error" in exc_info.value.response_text

    @pytest.mark.integration
    def test_connection_error_raises_loki_connection_error(
        self, base_url, sample_message
    ):
        """Test that connection errors raise LokiConnectionError."""
        with requests_mock.Mocker() as m:
            m.post(
                f"{base_url}/loki/api/v1/push",
                exc=requests.exceptions.ConnectTimeout,
            )

            logger = LokiLogger(baseUrl=base_url)

            with pytest.raises(LokiConnectionError) as exc_info:
                logger.info(sample_message)

            assert "Failed to connect to Loki" in str(exc_info.value)

    @pytest.mark.integration
    def test_400_bad_request_raises_error(self, base_url, sample_message):
        """Test that 400 Bad Request raises LokiPushError."""
        with requests_mock.Mocker() as m:
            m.post(
                f"{base_url}/loki/api/v1/push",
                status_code=400,
                text="Bad Request: Invalid labels",
            )

            logger = LokiLogger(baseUrl=base_url)

            with pytest.raises(LokiPushError) as exc_info:
                logger.info(sample_message)

            assert exc_info.value.status_code == 400

    @pytest.mark.integration
    def test_all_log_levels_with_labels_and_extras(
        self, base_url, sample_message, sample_labels, sample_extras
    ):
        """Test all log levels work with labels and extras combined."""
        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url)

            # Test all log levels
            logger.debug(sample_message, extras=sample_extras, labels=sample_labels)
            logger.info(sample_message, extras=sample_extras, labels=sample_labels)
            logger.warn(sample_message, extras=sample_extras, labels=sample_labels)
            logger.error(sample_message, extras=sample_extras, labels=sample_labels)
            logger.customLevel(
                "critical", sample_message, extras=sample_extras, labels=sample_labels
            )

            # All 5 calls should have been made
            assert m.call_count == 5
