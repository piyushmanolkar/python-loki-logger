# Python Loki Logger

[![Tests](https://github.com/piyushmanolkar/python-loki-logger/workflows/Tests/badge.svg)](https://github.com/piyushmanolkar/python-loki-logger/actions)
[![PyPI version](https://badge.fury.io/py/python-loki-logger.svg)](https://badge.fury.io/py/python-loki-logger)
[![Python Versions](https://img.shields.io/pypi/pyversions/python-loki-logger.svg)](https://pypi.org/project/python-loki-logger/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, production-ready Python library for pushing logs to Grafana Loki with a clean, intuitive API.

## Features

- **Simple & Intuitive API**: Easy integration with your existing projects
- **Multiple Severity Levels**: Built-in support for debug, info, warn, error, and custom levels
- **Global Labels**: Define labels once in the constructor to include in all log messages
- **Custom Labels**: Attach custom labels to your logs for better filtering and querying
- **Extra Data Support**: Include additional context with your log messages
- **Authentication**: Built-in support for basic authentication
- **Type Hints**: Full type annotation support for better IDE integration
- **Comprehensive Error Handling**: Custom exceptions for different error scenarios
- **Well Tested**: 90%+ test coverage with unit and integration tests
- **Production Ready**: Robust error handling and input validation

## Installation

Install via pip:

```bash
pip install python-loki-logger
```

For development:

```bash
pip install python-loki-logger[dev]
```

## Quick Start

```python
from python_loki_logger import LokiLogger

# Initialize the logger with optional global labels
logger = LokiLogger(
    baseUrl="https://loki.example.com",
    labels={"app": "my-app", "environment": "production"}
)

# Log messages - global labels are automatically included
logger.info("Application started successfully")
logger.error("An error occurred", extras={"user_id": "123"})
logger.debug("Debug information", labels={"request_id": "abc-123"})
```

## Usage Examples

### Basic Logging

```python
from python_loki_logger import LokiLogger

logger = LokiLogger(baseUrl="https://loki.example.com")

# Different severity levels
logger.debug("Debug message")
logger.info("Info message")
logger.warn("Warning message")
logger.error("Error message")
```

### With Authentication

```python
logger = LokiLogger(
    baseUrl="https://loki.example.com",
    auth=("username", "password")
)

logger.info("Authenticated log message")
```

### With Custom Labels

```python
logger = LokiLogger(baseUrl="https://loki.example.com")

logger.info(
    "Request processed",
    labels={
        "app": "my-app",
        "environment": "production",
        "version": "1.0.0"
    }
)
```

### With Extra Data

```python
logger.error(
    "Failed to process payment",
    extras={
        "user_id": "12345",
        "transaction_id": "txn_abc123",
        "amount": 99.99
    }
)
```

### With Dictionary Messages

```python
logger.error({
    "event": "payment_failed",
    "error_code": "INSUFFICIENT_FUNDS",
    "retry_count": 3
})
```

### Custom Severity Levels

```python
logger.customLevel(
    "critical",
    "Database connection lost",
    labels={"service": "database"}
)
```

### Custom Severity Label

```python
# Use a different label key for severity
logger = LokiLogger(
    baseUrl="https://loki.example.com",
    severity_label="log_level"
)

logger.info("This will use 'log_level' instead of 'level'")
```

### Global Labels

Define labels once in the constructor that will be included in all log messages:

```python
# Initialize logger with global labels
logger = LokiLogger(
    baseUrl="https://loki.example.com",
    labels={
        "app": "my-application",
        "environment": "production",
        "version": "1.0.0"
    }
)

# All logs will automatically include the global labels
logger.info("User logged in", labels={"user_id": "12345"})
# Results in labels: {app, environment, version, user_id, level}

logger.error("Payment failed", labels={"transaction_id": "txn_789"})
# Results in labels: {app, environment, version, transaction_id, level}
```

**Label Precedence:** Method-specific labels override global labels if there are conflicts:

```python
logger = LokiLogger(
    baseUrl="https://loki.example.com",
    labels={"environment": "production", "app": "my-app"}
)

# Override the environment label for this specific log
logger.info("Testing in staging", labels={"environment": "staging"})
# Results in: {app: "my-app", environment: "staging", level: "info"}
```

## Error Handling

The library provides specific exceptions for different error scenarios:

```python
from python_loki_logger import (
    LokiLogger,
    LokiConfigurationError,
    LokiConnectionError,
    LokiPushError
)

try:
    logger = LokiLogger(baseUrl="https://loki.example.com/")  # Trailing slash
except LokiConfigurationError as e:
    print(f"Configuration error: {e}")

try:
    logger = LokiLogger(baseUrl="https://loki.example.com")
    logger.info("Test message")
except LokiConnectionError as e:
    print(f"Connection failed: {e}")
except LokiPushError as e:
    print(f"Failed to push log. Status code: {e.status_code}")
```

## API Reference

### `LokiLogger`

#### `__init__(baseUrl, auth=None, severity_label="level", pushUrl="/loki/api/v1/push", labels=None)`

Initialize a new Loki logger instance.

**Parameters:**
- `baseUrl` (str): Base URL of your Loki instance. Must not end with `/`.
- `auth` (tuple, optional): Authentication tuple `(username, password)` for basic auth.
- `severity_label` (str, optional): Label key for severity level. Default: `"level"`.
- `pushUrl` (str, optional): Loki push API endpoint path. Default: `"/loki/api/v1/push"`.
- `labels` (dict, optional): Global labels to include in all log messages. Method-specific labels will be merged with these, with method labels taking precedence on conflicts.

**Raises:**
- `LokiConfigurationError`: If configuration is invalid.

#### `info(message, extras=None, labels=None)`

Log an info-level message.

**Parameters:**
- `message` (str | dict): Log message or dictionary.
- `extras` (dict, optional): Additional data to include.
- `labels` (dict, optional): Custom labels for this log.

**Raises:**
- `LokiConnectionError`: If connection fails.
- `LokiPushError`: If Loki returns an error.

#### `error(message, extras=None, labels=None)`

Log an error-level message. Same parameters as `info()`.

#### `warn(message, extras=None, labels=None)`

Log a warning-level message. Same parameters as `info()`.

#### `debug(message, extras=None, labels=None)`

Log a debug-level message. Same parameters as `info()`.

#### `customLevel(level, message, extras=None, labels=None)`

Log a message with a custom severity level.

**Parameters:**
- `level` (str): Custom severity level (e.g., "critical", "trace").
- Other parameters same as `info()`.

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/piyushmanolkar/python-loki-logger.git
cd python-loki-logger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make dev-install
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific tests
pytest tests/test_logger_init.py
pytest -m unit
pytest -m integration
```

### Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Type checking
make type-check

# Run all checks
make check
```

## Requirements

- Python >= 3.8
- requests >= 2.25.0

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Before submitting a PR:
1. Add tests for new features
2. Ensure all tests pass (`make test`)
3. Run code quality checks (`make check`)
4. Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 3.0.0
- **New Feature**: Global labels support - define labels once in constructor for all log messages
- Complete refactoring with improved code quality
- Added comprehensive test suite (90%+ coverage)
- Added custom exception classes
- Improved type hints and documentation
- Added input validation
- Better error messages
- CI/CD with GitHub Actions
- Modern packaging with pyproject.toml

## Support

- **Issues**: [GitHub Issues](https://github.com/piyushmanolkar/python-loki-logger/issues)
- **Discussions**: [GitHub Discussions](https://github.com/piyushmanolkar/python-loki-logger/discussions)

## Acknowledgments

Thank you to all contributors who have helped make this library better!

---

**Made with ❤️ by the Python community**
