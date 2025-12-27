"""Unit tests for LokiLogger initialization and configuration."""

import pytest

from python_loki_logger import LokiLogger, LokiConfigurationError


class TestLokiLoggerInit:
    """Test LokiLogger initialization."""

    @pytest.mark.unit
    def test_init_with_valid_baseurl(self, base_url):
        """Test initialization with valid base URL."""
        logger = LokiLogger(baseUrl=base_url)
        assert logger.baseUrl == base_url
        assert logger.pushUrl == "/loki/api/v1/push"
        assert logger.severity_label == "level"
        assert logger.auth is None

    @pytest.mark.unit
    def test_init_with_auth(self, base_url, auth_tuple):
        """Test initialization with authentication."""
        logger = LokiLogger(baseUrl=base_url, auth=auth_tuple)
        assert logger.auth == auth_tuple

    @pytest.mark.unit
    def test_init_with_custom_severity_label(self, base_url):
        """Test initialization with custom severity label."""
        logger = LokiLogger(baseUrl=base_url, severity_label="log_level")
        assert logger.severity_label == "log_level"

    @pytest.mark.unit
    def test_init_with_custom_push_url(self, base_url):
        """Test initialization with custom push URL."""
        custom_push = "/custom/push"
        logger = LokiLogger(baseUrl=base_url, pushUrl=custom_push)
        assert logger.pushUrl == custom_push

    @pytest.mark.unit
    def test_init_with_trailing_slash_raises_error(self):
        """Test that base URL with trailing slash raises error."""
        with pytest.raises(LokiConfigurationError, match="must not end with /"):
            LokiLogger(baseUrl="https://loki.example.com/")

    @pytest.mark.unit
    def test_init_with_empty_baseurl_raises_error(self):
        """Test that empty base URL raises error."""
        with pytest.raises(LokiConfigurationError, match="cannot be empty"):
            LokiLogger(baseUrl="")

    @pytest.mark.unit
    def test_init_with_invalid_push_url_raises_error(self, base_url):
        """Test that push URL not starting with / raises error."""
        with pytest.raises(LokiConfigurationError, match="must start with /"):
            LokiLogger(baseUrl=base_url, pushUrl="invalid")

    @pytest.mark.unit
    def test_init_all_parameters(self, base_url, auth_tuple):
        """Test initialization with all parameters."""
        logger = LokiLogger(
            baseUrl=base_url,
            auth=auth_tuple,
            severity_label="custom_level",
            pushUrl="/custom/api/push",
        )
        assert logger.baseUrl == base_url
        assert logger.auth == auth_tuple
        assert logger.severity_label == "custom_level"
        assert logger.pushUrl == "/custom/api/push"
