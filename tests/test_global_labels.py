"""Tests for global labels functionality."""

import pytest
import requests_mock

from python_loki_logger import LokiLogger


class TestGlobalLabels:
    """Test global labels functionality."""

    @pytest.mark.integration
    def test_logger_with_global_labels(self, base_url):
        """Test that logger can be initialized with global labels."""
        global_labels = {"app": "test-app", "environment": "test"}
        logger = LokiLogger(baseUrl=base_url, labels=global_labels)
        assert logger.global_labels == global_labels

    @pytest.mark.integration
    def test_logger_without_global_labels(self, base_url):
        """Test logger initializes with empty dict when no global labels."""
        logger = LokiLogger(baseUrl=base_url)
        assert logger.global_labels == {}

    @pytest.mark.integration
    def test_global_labels_included_in_all_requests(self, base_url, sample_message):
        """Test that global labels are included in all log requests."""
        global_labels = {"app": "test-app", "environment": "production"}

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, labels=global_labels)
            logger.info(sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            # Should include global labels and severity
            assert stream_labels["app"] == "test-app"
            assert stream_labels["environment"] == "production"
            assert stream_labels["level"] == "info"

    @pytest.mark.integration
    def test_method_labels_merge_with_global_labels(self, base_url, sample_message):
        """Test that method-specific labels merge with global labels."""
        global_labels = {"app": "test-app", "environment": "production"}
        method_labels = {"request_id": "abc123", "user_id": "456"}

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, labels=global_labels)
            logger.info(sample_message, labels=method_labels)

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            # Should include both global and method labels
            assert stream_labels["app"] == "test-app"
            assert stream_labels["environment"] == "production"
            assert stream_labels["request_id"] == "abc123"
            assert stream_labels["user_id"] == "456"
            assert stream_labels["level"] == "info"

    @pytest.mark.integration
    def test_method_labels_override_global_labels(self, base_url, sample_message):
        """Test that method labels override global labels on conflicts."""
        global_labels = {"app": "test-app", "environment": "production"}
        method_labels = {"environment": "staging"}  # Conflicts with global

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, labels=global_labels)
            logger.error(sample_message, labels=method_labels)

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            # Method label should override global label
            assert stream_labels["app"] == "test-app"
            assert stream_labels["environment"] == "staging"  # Overridden
            assert stream_labels["level"] == "error"

    @pytest.mark.integration
    def test_global_labels_work_with_all_log_methods(self, base_url, sample_message):
        """Test that global labels work with all logging methods."""
        global_labels = {"app": "test-app", "version": "1.0.0"}

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, labels=global_labels)

            # Test all log methods
            logger.debug(sample_message)
            logger.info(sample_message)
            logger.warn(sample_message)
            logger.error(sample_message)
            logger.customLevel("critical", sample_message)

            # All 5 requests should have been made
            assert m.call_count == 5

            # Verify all requests have global labels
            for request in m.request_history:
                body = request.json()
                stream_labels = body["streams"][0]["stream"]
                assert stream_labels["app"] == "test-app"
                assert stream_labels["version"] == "1.0.0"

    @pytest.mark.integration
    def test_global_labels_dont_modify_original_dict(self, base_url, sample_message):
        """Test that global labels dict is not modified by method calls."""
        global_labels = {"app": "test-app"}

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, labels=global_labels)
            logger.info(sample_message, labels={"request_id": "123"})

            # Original global_labels dict should not be modified
            assert global_labels == {"app": "test-app"}
            # Logger's internal copy should also remain unchanged
            assert logger.global_labels == {"app": "test-app"}

    @pytest.mark.integration
    def test_empty_method_labels_with_global_labels(self, base_url, sample_message):
        """Test logging with global labels but no method labels."""
        global_labels = {"app": "test-app", "team": "backend"}

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(baseUrl=base_url, labels=global_labels)
            logger.info(sample_message)  # No method labels

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            # Should only have global labels and severity
            assert stream_labels["app"] == "test-app"
            assert stream_labels["team"] == "backend"
            assert stream_labels["level"] == "info"
            assert len(stream_labels) == 3

    @pytest.mark.integration
    def test_global_labels_with_custom_severity_label(self, base_url, sample_message):
        """Test global labels work with custom severity label."""
        global_labels = {"app": "test-app"}

        with requests_mock.Mocker() as m:
            m.post(f"{base_url}/loki/api/v1/push", status_code=204)

            logger = LokiLogger(
                baseUrl=base_url, labels=global_labels, severity_label="log_level"
            )
            logger.info(sample_message)

            assert m.call_count == 1
            body = m.request_history[0].json()
            stream_labels = body["streams"][0]["stream"]

            assert stream_labels["app"] == "test-app"
            assert stream_labels["log_level"] == "info"
            assert "level" not in stream_labels

    @pytest.mark.unit
    def test_init_with_global_labels_all_parameters(self, base_url, auth_tuple):
        """Test initialization with global labels and all other parameters."""
        global_labels = {"app": "test-app", "env": "prod"}

        logger = LokiLogger(
            baseUrl=base_url,
            auth=auth_tuple,
            severity_label="log_level",
            pushUrl="/custom/push",
            labels=global_labels,
        )

        assert logger.baseUrl == base_url
        assert logger.auth == auth_tuple
        assert logger.severity_label == "log_level"
        assert logger.pushUrl == "/custom/push"
        assert logger.global_labels == global_labels
