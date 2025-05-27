#!/usr/bin/env python3
"""
Example usage of the Messages MCP Server.

This script demonstrates how to interact with the MCP server
to fetch messages from an API endpoint.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Demonstrate MCP server usage."""
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_demo_server"],
        env={
            "MCP_LOG_LEVEL": "INFO",
            "API_URL": "https://api-url.com/messages",
            "AUTHORIZATION_TOKEN": "Bearer your-token-here"
        }
    )
    
    print("🚀 Starting Messages MCP Server Demo")
    print("=" * 50)
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Connected to MCP server")
                
                # List available resources
                print("\n📋 Available Resources:")
                resources = await session.list_resources()
                for resource in resources.resources:
                    print(f"  - {resource.uri}: {resource.description}")
                
                # List available tools
                print("\n🔧 Available Tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # List available prompts
                print("\n💬 Available Prompts:")
                prompts = await session.list_prompts()
                for prompt in prompts.prompts:
                    print(f"  - {prompt.name}: {prompt.description}")
                
                # Example: Fetch messages
                print("\n" + "=" * 50)
                print("📨 Fetching Messages from API")
                print("=" * 50)
                
                # Example message ID
                message_id = "12345"
                print(f"Fetching messages for ID: {message_id}")
                
                try:
                    content, mime_type = await session.read_resource(f"messages://{message_id}")
                    messages_response = json.loads(content)
                    
                    if messages_response["status"] == "success":
                        print(f"✅ Successfully fetched messages for ID: {messages_response['message_id']}")
                        print(f"Status Code: {messages_response['metadata']['status_code']}")
                        print(f"Message Count: {messages_response['metadata']['message_count']}")
                        if messages_response['metadata']['response_time_ms']:
                            print(f"Response Time: {messages_response['metadata']['response_time_ms']:.2f}ms")
                        
                        # Display first few messages if available
                        messages = messages_response["messages"]
                        if isinstance(messages, list) and messages:
                            print(f"\nFirst {min(3, len(messages))} messages:")
                            for i, message in enumerate(messages[:3]):
                                print(f"  {i+1}. {message}")
                        elif messages:
                            print(f"\nMessage data: {messages}")
                    else:
                        print(f"❌ Error: {messages_response['error']}")
                        print(f"Error Type: {messages_response['error_type']}")
                        
                except Exception as e:
                    print(f"❌ Error fetching messages: {e}")
                
                print("\n" + "=" * 50)
                print("✅ Demo completed successfully!")
                print("=" * 50)
                
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 