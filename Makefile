.PHONY: install dev-install test lint format type-check clean build publish

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=python_loki_logger --cov-report=html --cov-report=term

lint:
	flake8 python_loki_logger tests --max-line-length=88 --extend-ignore=E203

format:
	black python_loki_logger tests

format-check:
	black --check python_loki_logger tests

type-check:
	mypy python_loki_logger --ignore-missing-imports

check: format-check lint type-check test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine upload dist/*
