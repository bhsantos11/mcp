"""Tests for the Messages MCP Server."""

import json
import pytest
from unittest.mock import AsyncMock, patch

from mcp_demo_server.server import get_messages


@pytest.mark.asyncio
class TestMessagesResource:
    """Test messages resource functionality."""

    async def test_get_messages_function_exists(self):
        """Test that the get_messages function exists and is callable."""
        assert callable(get_messages)
        
    # Note: Full testing would require mocking the Context object
    # and httpx client, which is more complex for this demo


if __name__ == "__main__":
    pytest.main([__file__]) 