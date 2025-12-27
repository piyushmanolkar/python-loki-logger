"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def base_url():
    """Return a test base URL."""
    return "https://loki.example.com"


@pytest.fixture
def auth_tuple():
    """Return a test auth tuple."""
    return ("test_user", "test_password")


@pytest.fixture
def sample_labels():
    """Return sample labels for testing."""
    return {"app": "test-app", "environment": "test"}


@pytest.fixture
def sample_message():
    """Return a sample log message."""
    return "Test log message"


@pytest.fixture
def sample_extras():
    """Return sample extra data."""
    return {"user_id": "123", "request_id": "abc-def"}
