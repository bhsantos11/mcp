.PHONY: help install dev test lint format clean run dev-server example venv

# Default target
help:
	@echo "Customer Analytics MCP Server - Development Commands"
	@echo "=================================================="
	@echo "venv        - Create virtual environment"
	@echo "install     - Install dependencies"
	@echo "dev         - Install development dependencies"
	@echo "test        - Run tests"
	@echo "lint        - Run linting checks"
	@echo "format      - Format code"
	@echo "clean       - Clean build artifacts"
	@echo "run         - Run the MCP server"
	@echo "dev-server  - Run server with MCP inspector"
	@echo "example     - Run usage example"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev:
	pip install -r requirements-dev.txt
	pip install -e .

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=mcp_demo_server --cov-report=html --cov-report=term

# Run linting
lint:
	ruff check src/ tests/
	mypy src/

# Format code
format:
	black src/ tests/ examples/
	isort src/ tests/ examples/
	ruff check --fix src/ tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the MCP server
run:
	python -m mcp_demo_server

# Run server with MCP inspector for development
dev-server:
	mcp dev src/mcp_demo_server/server.py

# Run usage example
example:
	python examples/usage_example.py

# Build package
build:
	python setup.py sdist bdist_wheel

# Install package in development mode
install-dev:
	pip install -e .

# Check for security vulnerabilities
security:
	safety check

# Create virtual environment
venv:
	python -m venv venv
	@echo "Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)" 