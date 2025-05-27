"""Main entry point for the MCP Demo Server."""

import asyncio
import logging
import os
import sys
from typing import Optional

from .server import mcp


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def main() -> None:
    """Main entry point for the server."""
    # Configure logging
    log_level = os.getenv("MCP_LOG_LEVEL", "INFO")
    setup_logging(log_level)
    
    # Set server name from environment
    server_name = os.getenv("MCP_SERVER_NAME", "Customer Analytics Server")
    mcp.name = server_name
    
    # Run the server
    try:
        mcp.run()
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 