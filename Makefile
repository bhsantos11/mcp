.PHONY: help install dev test lint format clean run dev-server example

# Default target
help:
	@echo "Customer Analytics MCP Server - Development Commands"
	@echo "=================================================="
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
	uv sync

# Install development dependencies
dev:
	uv sync --dev --all-extras

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=mcp_demo_server --cov-report=html --cov-report=term

# Run linting
lint:
	uv run ruff check src/ tests/
	uv run mypy src/

# Format code
format:
	uv run black src/ tests/ examples/
	uv run isort src/ tests/ examples/
	uv run ruff check --fix src/ tests/

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
	uv run mcp-demo-server

# Run server with MCP inspector for development
dev-server:
	uv run mcp dev src/mcp_demo_server/server.py

# Run usage example
example:
	uv run python examples/usage_example.py

# Build package
build:
	uv build

# Install package in development mode
install-dev:
	uv pip install -e .

# Check for security vulnerabilities
security:
	uv run safety check

# Generate requirements.txt (for compatibility)
requirements:
	uv export --format requirements-txt --output-file requirements.txt 