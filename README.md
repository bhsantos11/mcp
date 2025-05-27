# Customer Analytics MCP Server

A Model Context Protocol (MCP) server built with Python that provides customer predictive analytics and insights. This server demonstrates how to integrate customer data APIs with AI-powered analysis capabilities.

## Features

- **Customer Data Resources**: Fetch comprehensive customer information by ID
- **Predictive Analytics**: AI-driven predictions for churn, lifetime value, and purchase behavior
- **Customer Segmentation**: Analyze customer segments and characteristics
- **Risk Assessment**: Identify at-risk customers and retention opportunities
- **External API Integration**: Connect to customer data endpoints
- **Comprehensive Scoring**: Multi-factor customer scoring and grading system

## Installation

### Prerequisites

- Python 3.9 or higher
- `uv` package manager (recommended) or `pip`

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd mcp-demo-server

# Install dependencies
uv sync --dev --all-extras

# Run the server
uv run mcp-demo-server
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd mcp-demo-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run the server
mcp-demo-server
```

## Development

### Running in Development Mode

Use the MCP Inspector for testing and debugging:

```bash
# Install MCP CLI tools
uv add "mcp[cli]"

# Run with inspector
uv run mcp dev src/mcp_demo_server/server.py
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=mcp_demo_server
```

### Code Quality

```bash
# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## Usage

### Claude Desktop Integration

To use this server with Claude Desktop, add the following to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "mcp-demo-server": {
      "command": "uv",
      "args": ["run", "mcp-demo-server"],
      "cwd": "/path/to/mcp-demo-server"
    }
  }
}
```

### Available Resources

- `customer://{customer_id}` - Comprehensive customer data by ID
- `customer://{customer_id}/predictions` - AI-driven customer predictions
- `analytics://segment/{segment_name}` - Customer segment analysis

### Available Tools

- `fetch_customer_from_api` - Fetch customer data from external API endpoint
- `calculate_customer_score` - Calculate comprehensive customer score
- `generate_customer_insights` - Generate AI-driven customer insights

### Available Prompts

- `analyze_customer_behavior` - Analyze customer behavior patterns
- `create_retention_strategy` - Create customer retention strategy
- `customer_health_check` - Perform customer health assessment

## Architecture

The server is built using the FastMCP framework, which provides:

- **Automatic Protocol Handling**: JSON-RPC 2.0 message routing
- **Type Safety**: Full type hints and validation
- **Async Support**: Built on asyncio for high performance
- **Easy Testing**: Built-in development tools

## Configuration

The server can be configured through environment variables:

- `MCP_SERVER_NAME` - Server name (default: "Customer Analytics Server")
- `MCP_LOG_LEVEL` - Logging level (default: "INFO")
- `CUSTOMER_API_URL` - Base URL for customer API (default: "https://api.example.com")
- `CUSTOMER_API_KEY` - API key for customer service (default: "demo-key")

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop) 