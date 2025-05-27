"""Messages MCP Server.

This server provides access to messages from an external API endpoint.
"""

import json
import logging
import os
from typing import Any, Dict
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import httpx
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage application lifecycle with messages API context."""
    logger.info("Initializing Messages Server...")
    
    # Initialize API context
    api_context = {
        "api_url": os.getenv("API_URL", "https://api-url.com/messages"),
        "authorization_token": os.getenv("AUTHORIZATION_TOKEN", "Bearer your-token-here"),
        "http_client": httpx.AsyncClient(timeout=30.0),
        "cache": {}
    }
    
    try:
        yield api_context
    finally:
        logger.info("Shutting down Messages Server...")
        await api_context["http_client"].aclose()


# Create the FastMCP server with lifespan management
mcp = FastMCP(
    name="Messages Server",
    dependencies=["httpx>=0.25.0"],
    lifespan=app_lifespan
)


@mcp.resource("messages://{message_id}")
async def get_messages(message_id: str, ctx: Context) -> str:
    """Fetch messages by ID from the API endpoint.
    
    This resource retrieves messages for a specific ID from the configured API endpoint
    using the Authorization header for authentication.
    """
    logger.info(f"Fetching messages for ID: {message_id}")
    
    # Get the API context
    api_ctx = ctx.request_context.lifespan_context
    http_client = api_ctx["http_client"]
    api_url = api_ctx["api_url"]
    auth_token = api_ctx["authorization_token"]
    
    try:
        # Make GET request to the messages endpoint
        headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }
        
        # Add the ID as a query parameter or path parameter
        # Assuming the API expects the ID as a query parameter
        params = {"id": message_id}
        
        await ctx.info(f"Making GET request to: {api_url} with ID: {message_id}")
        
        response = await http_client.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        # Return the response data
        messages_data = response.json()
        
        # Add metadata about the response
        result = {
            "status": "success",
            "message_id": message_id,
            "messages": messages_data,
            "metadata": {
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000 if response.elapsed else None,
                "message_count": len(messages_data) if isinstance(messages_data, list) else 1
            }
        }
        
        return json.dumps(result, indent=2)
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return json.dumps({
            "status": "error",
            "error": f"HTTP {e.response.status_code}: {e.response.text}",
            "error_type": "http_error"
        }, indent=2)
        
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return json.dumps({
            "status": "error",
            "error": f"Request failed: {str(e)}",
            "error_type": "request_error"
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return json.dumps({
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "error_type": "unexpected_error"
        }, indent=2)





if __name__ == "__main__":
    mcp.run() 