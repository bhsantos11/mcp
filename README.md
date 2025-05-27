# Messages MCP Server

A Model Context Protocol (MCP) server built with Python that provides access to messages from an external API endpoint. This server demonstrates how to integrate with external APIs using Authorization headers for authentication.

## Features

- **Messages Resource**: Fetch all messages from the configured API endpoint
- **Authorization Header Authentication**: Uses Bearer token authentication
- **Error Handling**: Comprehensive error handling for API requests
- **Response Metadata**: Includes response time and status information

## Installation

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd mcp-demo-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode (optional)
pip install -e .

# Run the server
python -m mcp_demo_server
```

### Development Installation

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

## Development

### Running in Development Mode

Use the MCP Inspector for testing and debugging:

```bash
# Install MCP CLI tools
pip install "mcp[cli]"

# Run with inspector
mcp dev src/mcp_demo_server/server.py
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=mcp_demo_server
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Usage

### Claude Desktop Integration

To use this server with Claude Desktop, add the following to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "mcp-demo-server": {
      "command": "python",
      "args": ["-m", "mcp_demo_server"],
      "cwd": "/path/to/mcp-demo-server"
    }
  }
}
```

### Available Resources

- `messages://{message_id}` - Fetch messages by ID from the API endpoint

### API Request Format

When you access the `messages://{message_id}` resource, the server makes a GET request like this:
```http
GET https://api-url.com/messages?id=12345
Authorization: Bearer your-token-here
Content-Type: application/json
```

## Architecture

The server is built using the FastMCP framework, which provides:

- **Automatic Protocol Handling**: JSON-RPC 2.0 message routing
- **Type Safety**: Full type hints and validation
- **Async Support**: Built on asyncio for high performance
- **Easy Testing**: Built-in development tools

## Configuration

The server can be configured through environment variables:

- `MCP_SERVER_NAME` - Server name (default: "Messages Server")
- `MCP_LOG_LEVEL` - Logging level (default: "INFO")
- `API_URL` - API endpoint URL (default: "https://api-url.com/messages")
- `AUTHORIZATION_TOKEN` - Authorization header token (default: "Bearer your-token-here")

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