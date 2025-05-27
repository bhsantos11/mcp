#!/usr/bin/env python3
"""
Example usage of the Customer Analytics MCP Server.

This script demonstrates how to interact with the MCP server
to fetch customer data and generate insights.
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
            "CUSTOMER_API_URL": "https://api.example.com",
            "CUSTOMER_API_KEY": "demo-key"
        }
    )
    
    print("🚀 Starting Customer Analytics MCP Server Demo")
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
                
                # Example 1: Fetch customer data
                print("\n" + "=" * 50)
                print("📊 Example 1: Fetching Customer Data")
                print("=" * 50)
                
                customer_id = "1001"
                try:
                    content, mime_type = await session.read_resource(f"customer://{customer_id}")
                    customer_data = json.loads(content)
                    print(f"Customer: {customer_data['name']}")
                    print(f"Tier: {customer_data['customer_tier']}")
                    print(f"Total Spent: ${customer_data['total_spent']}")
                    print(f"Risk Score: {customer_data['risk_score']}")
                except Exception as e:
                    print(f"❌ Error fetching customer data: {e}")
                
                # Example 2: Get customer predictions
                print("\n" + "=" * 50)
                print("🔮 Example 2: Customer Predictions")
                print("=" * 50)
                
                try:
                    content, mime_type = await session.read_resource(f"customer://{customer_id}/predictions")
                    predictions = json.loads(content)
                    print(f"Churn Probability: {predictions['churn_probability']:.1%}")
                    print(f"Predicted LTV: ${predictions['predicted_lifetime_value']:,.2f}")
                    print(f"Recommended Categories: {', '.join(predictions['recommended_categories'])}")
                except Exception as e:
                    print(f"❌ Error fetching predictions: {e}")
                
                # Example 3: Calculate customer score
                print("\n" + "=" * 50)
                print("📈 Example 3: Customer Score Calculation")
                print("=" * 50)
                
                try:
                    result = await session.call_tool(
                        "calculate_customer_score",
                        arguments={
                            "total_spent": 2450.75,
                            "total_purchases": 15,
                            "days_since_last_purchase": 10,
                            "customer_tier": "gold"
                        }
                    )
                    score_data = json.loads(result.content[0].text)
                    print(f"Customer Score: {score_data['total_score']}/100")
                    print(f"Grade: {score_data['grade']}")
                    print("Recommendations:")
                    for rec in score_data['recommendations']:
                        print(f"  • {rec}")
                except Exception as e:
                    print(f"❌ Error calculating score: {e}")
                
                # Example 4: Generate customer insights
                print("\n" + "=" * 50)
                print("🧠 Example 4: Customer Insights")
                print("=" * 50)
                
                try:
                    result = await session.call_tool(
                        "generate_customer_insights",
                        arguments={"customer_id": customer_id}
                    )
                    insights = json.loads(result.content[0].text)
                    print(f"Analysis for: {insights['customer_name']}")
                    print("\nKey Metrics:")
                    for metric, value in insights['key_metrics'].items():
                        print(f"  • {metric.replace('_', ' ').title()}: {value}")
                    
                    if insights['behavioral_insights']:
                        print("\nBehavioral Insights:")
                        for insight in insights['behavioral_insights']:
                            print(f"  • {insight}")
                    
                    if insights['opportunities']:
                        print("\nOpportunities:")
                        for opportunity in insights['opportunities']:
                            print(f"  • {opportunity}")
                            
                except Exception as e:
                    print(f"❌ Error generating insights: {e}")
                
                # Example 5: Analyze customer segment
                print("\n" + "=" * 50)
                print("👥 Example 5: Customer Segment Analysis")
                print("=" * 50)
                
                try:
                    content, mime_type = await session.read_resource("analytics://segment/high_value")
                    segment_data = json.loads(content)
                    print(f"Segment: {segment_data['name']}")
                    print(f"Customer Count: {segment_data['customer_count']}")
                    print(f"Avg LTV: ${segment_data['avg_lifetime_value']:,.2f}")
                    print("Characteristics:")
                    for char in segment_data['characteristics']:
                        print(f"  • {char}")
                except Exception as e:
                    print(f"❌ Error fetching segment data: {e}")
                
                print("\n" + "=" * 50)
                print("✅ Demo completed successfully!")
                print("=" * 50)
                
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 