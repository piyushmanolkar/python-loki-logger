# Contributing to Python Loki Logger

Thank you for your interest in contributing to Python Loki Logger! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/piyushmanolkar/python-loki-logger.git
cd python-loki-logger
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
make dev-install
# or
pip install -e ".[dev]"
```

## Running Tests

Run all tests:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

Run specific test file:
```bash
pytest tests/test_logger_init.py
```

Run tests by marker:
```bash
pytest -m unit
pytest -m integration
```

## Code Quality

### Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
make format  # Format code
make format-check  # Check formatting without modifying files
```

### Linting

We use [Flake8](https://flake8.pycqa.org/) for linting:

```bash
make lint
```

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for static type checking:

```bash
make type-check
```

### Run All Checks

Run all quality checks at once:

```bash
make check
```

## Making Changes

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and add tests to cover your code.

3. Run the full test suite and quality checks:
```bash
make check
```

4. Commit your changes:
```bash
git add .
git commit -m "Add feature: description of your changes"
```

5. Push to your fork and submit a pull request.

## Pull Request Guidelines

- **Write tests**: All new features and bug fixes should include tests.
- **Update documentation**: Update the README.md if you change functionality.
- **Follow code style**: Use Black for formatting and ensure Flake8 passes.
- **Write clear commit messages**: Describe what changed and why.
- **Keep PRs focused**: One feature or fix per pull request.
- **Add docstrings**: All public methods should have docstrings.

## Code Style Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all function parameters and return values
- Maximum line length is 88 characters (Black default)
- Use descriptive variable and function names
- Add docstrings to all public classes and methods

## Testing Guidelines

- Write unit tests for individual components
- Write integration tests for API interactions
- Use pytest fixtures for common test setup
- Mock external HTTP requests using `requests-mock`
- Aim for high test coverage (>90%)

## Reporting Bugs

When reporting bugs, please include:

- Python version
- Operating system
- Minimal code example to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages and stack traces

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Clearly describe the use case
- Explain why this feature would be useful
- Provide examples if possible

## Questions?

If you have questions about contributing, feel free to:

- Open an issue
- Start a discussion on GitHub

Thank you for contributing to Python Loki Logger!
