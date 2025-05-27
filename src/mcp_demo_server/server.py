"""Customer Predictive Analytics MCP Server.

This server provides customer analytics capabilities including:
- Customer data retrieval by ID
- Predictive analytics and insights
- Customer segmentation
- Risk assessment
"""

import json
import logging
import os
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import httpx
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base

# Configure logging
logger = logging.getLogger(__name__)

# Mock customer database for demonstration
MOCK_CUSTOMERS = {
    "1001": {
        "id": "1001",
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "age": 34,
        "location": "New York, NY",
        "join_date": "2022-03-15",
        "total_purchases": 15,
        "total_spent": 2450.75,
        "last_purchase": "2024-01-15",
        "preferred_categories": ["electronics", "books"],
        "customer_tier": "gold",
        "risk_score": 0.15
    },
    "1002": {
        "id": "1002", 
        "name": "Bob Smith",
        "email": "bob.smith@email.com",
        "age": 28,
        "location": "San Francisco, CA",
        "join_date": "2023-01-20",
        "total_purchases": 8,
        "total_spent": 1200.50,
        "last_purchase": "2024-01-10",
        "preferred_categories": ["clothing", "sports"],
        "customer_tier": "silver",
        "risk_score": 0.25
    },
    "1003": {
        "id": "1003",
        "name": "Carol Davis",
        "email": "carol.davis@email.com", 
        "age": 45,
        "location": "Chicago, IL",
        "join_date": "2021-08-10",
        "total_purchases": 32,
        "total_spent": 5670.25,
        "last_purchase": "2024-01-20",
        "preferred_categories": ["home", "electronics", "books"],
        "customer_tier": "platinum",
        "risk_score": 0.05
    }
}


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage application lifecycle with customer analytics context."""
    logger.info("Initializing Customer Analytics Server...")
    
    # Initialize analytics context
    analytics_context = {
        "api_base_url": os.getenv("CUSTOMER_API_URL", "https://api.example.com"),
        "api_key": os.getenv("CUSTOMER_API_KEY", "demo-key"),
        "http_client": httpx.AsyncClient(timeout=30.0),
        "cache": {},
        "analytics_models": {
            "churn_prediction": "v1.2",
            "lifetime_value": "v2.1", 
            "recommendation": "v1.8"
        }
    }
    
    try:
        yield analytics_context
    finally:
        logger.info("Shutting down Customer Analytics Server...")
        await analytics_context["http_client"].aclose()


# Create the FastMCP server with lifespan management
mcp = FastMCP(
    name="Customer Analytics Server",
    dependencies=["httpx>=0.25.0", "python-dateutil>=2.8.0"],
    lifespan=app_lifespan
)


@mcp.resource("customer://{customer_id}")
def get_customer_data(customer_id: str) -> str:
    """Fetch comprehensive customer data by ID.
    
    This resource provides detailed customer information including:
    - Basic profile information
    - Purchase history summary
    - Customer tier and status
    - Risk assessment scores
    """
    logger.info(f"Fetching customer data for ID: {customer_id}")
    
    # In a real implementation, this would fetch from your customer API
    customer = MOCK_CUSTOMERS.get(customer_id)
    
    if not customer:
        return json.dumps({
            "error": f"Customer {customer_id} not found",
            "available_customers": list(MOCK_CUSTOMERS.keys())
        }, indent=2)
    
    # Add computed fields
    customer_data = customer.copy()
    customer_data["days_since_last_purchase"] = (
        datetime.now() - datetime.strptime(customer["last_purchase"], "%Y-%m-%d")
    ).days
    customer_data["average_order_value"] = round(
        customer["total_spent"] / customer["total_purchases"], 2
    )
    
    return json.dumps(customer_data, indent=2)


@mcp.resource("customer://{customer_id}/predictions")
def get_customer_predictions(customer_id: str) -> str:
    """Get predictive analytics for a specific customer.
    
    Provides AI-driven predictions including:
    - Churn probability
    - Lifetime value estimate
    - Next purchase prediction
    - Recommended products
    """
    logger.info(f"Generating predictions for customer ID: {customer_id}")
    
    customer = MOCK_CUSTOMERS.get(customer_id)
    if not customer:
        return json.dumps({"error": f"Customer {customer_id} not found"}, indent=2)
    
    # Mock predictive analytics (in real implementation, call ML models)
    predictions = {
        "customer_id": customer_id,
        "generated_at": datetime.now().isoformat(),
        "churn_probability": round(random.uniform(0.05, 0.45), 3),
        "predicted_lifetime_value": round(random.uniform(1000, 10000), 2),
        "next_purchase_probability_30_days": round(random.uniform(0.1, 0.8), 3),
        "recommended_categories": random.sample(
            ["electronics", "books", "clothing", "home", "sports", "beauty"], 3
        ),
        "optimal_contact_time": "Tuesday 2-4 PM",
        "preferred_channel": random.choice(["email", "sms", "push_notification"]),
        "model_versions": {
            "churn": "v1.2",
            "ltv": "v2.1",
            "recommendation": "v1.8"
        }
    }
    
    return json.dumps(predictions, indent=2)


@mcp.resource("analytics://segment/{segment_name}")
def get_customer_segment(segment_name: str) -> str:
    """Get customer segment analysis and characteristics.
    
    Available segments:
    - high_value: Customers with high lifetime value
    - at_risk: Customers with high churn probability
    - new_customers: Recently acquired customers
    - loyal: Long-term, consistent customers
    """
    logger.info(f"Fetching segment analysis for: {segment_name}")
    
    segments = {
        "high_value": {
            "name": "High Value Customers",
            "criteria": "Total spent > $3000 OR Customer tier = platinum",
            "customer_count": 1,
            "avg_lifetime_value": 5670.25,
            "avg_risk_score": 0.05,
            "characteristics": [
                "High purchase frequency",
                "Multiple category preferences", 
                "Low churn risk",
                "High engagement scores"
            ]
        },
        "at_risk": {
            "name": "At-Risk Customers", 
            "criteria": "Risk score > 0.2 OR Days since last purchase > 60",
            "customer_count": 1,
            "avg_lifetime_value": 1200.50,
            "avg_risk_score": 0.25,
            "characteristics": [
                "Declining purchase frequency",
                "Limited category engagement",
                "Higher price sensitivity",
                "Lower response rates"
            ]
        },
        "new_customers": {
            "name": "New Customers",
            "criteria": "Join date within last 6 months",
            "customer_count": 1, 
            "avg_lifetime_value": 1200.50,
            "avg_risk_score": 0.25,
            "characteristics": [
                "Still exploring preferences",
                "Higher engagement potential",
                "Price conscious",
                "Responsive to onboarding"
            ]
        },
        "loyal": {
            "name": "Loyal Customers",
            "criteria": "Customer for > 2 years AND Total purchases > 20",
            "customer_count": 1,
            "avg_lifetime_value": 5670.25,
            "avg_risk_score": 0.05,
            "characteristics": [
                "Consistent purchase patterns",
                "Brand advocates",
                "Low price sensitivity", 
                "High retention rate"
            ]
        }
    }
    
    segment = segments.get(segment_name)
    if not segment:
        return json.dumps({
            "error": f"Segment '{segment_name}' not found",
            "available_segments": list(segments.keys())
        }, indent=2)
    
    return json.dumps(segment, indent=2)


@mcp.tool()
async def fetch_customer_from_api(customer_id: str, ctx: Context) -> str:
    """Fetch customer data from external API endpoint.
    
    This tool demonstrates how to integrate with external customer APIs
    to retrieve real-time customer information.
    """
    logger.info(f"Fetching customer {customer_id} from external API")
    
    # Get the analytics context
    analytics_ctx = ctx.request_context.lifespan_context
    http_client = analytics_ctx["http_client"]
    api_base_url = analytics_ctx["api_base_url"]
    api_key = analytics_ctx["api_key"]
    
    try:
        # In a real implementation, this would call your actual customer API
        # For demo purposes, we'll simulate an API call
        await ctx.info(f"Calling API: {api_base_url}/customers/{customer_id}")
        
        # Simulate API delay
        import asyncio
        await asyncio.sleep(0.5)
        
        # Return mock data as if from API
        if customer_id in MOCK_CUSTOMERS:
            api_response = {
                "status": "success",
                "data": MOCK_CUSTOMERS[customer_id],
                "api_version": "v2.1",
                "response_time_ms": 245
            }
        else:
            api_response = {
                "status": "error", 
                "error": "Customer not found",
                "error_code": "CUSTOMER_NOT_FOUND"
            }
        
        return json.dumps(api_response, indent=2)
        
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return json.dumps({
            "status": "error",
            "error": f"API call failed: {str(e)}"
        }, indent=2)


@mcp.tool()
def calculate_customer_score(
    total_spent: float,
    total_purchases: int, 
    days_since_last_purchase: int,
    customer_tier: str = "bronze"
) -> str:
    """Calculate a comprehensive customer score based on multiple factors.
    
    The score considers:
    - Total spending amount
    - Purchase frequency
    - Recency of last purchase
    - Customer tier status
    """
    logger.info("Calculating customer score")
    
    # Base score from spending (0-40 points)
    spending_score = min(total_spent / 100, 40)
    
    # Purchase frequency score (0-30 points)
    frequency_score = min(total_purchases * 2, 30)
    
    # Recency score (0-20 points, decreases with time)
    recency_score = max(20 - (days_since_last_purchase / 5), 0)
    
    # Tier bonus (0-10 points)
    tier_bonuses = {"bronze": 0, "silver": 3, "gold": 6, "platinum": 10}
    tier_score = tier_bonuses.get(customer_tier.lower(), 0)
    
    total_score = spending_score + frequency_score + recency_score + tier_score
    
    # Determine grade
    if total_score >= 80:
        grade = "A+"
    elif total_score >= 70:
        grade = "A"
    elif total_score >= 60:
        grade = "B"
    elif total_score >= 50:
        grade = "C"
    else:
        grade = "D"
    
    result = {
        "total_score": round(total_score, 1),
        "grade": grade,
        "breakdown": {
            "spending_score": round(spending_score, 1),
            "frequency_score": round(frequency_score, 1), 
            "recency_score": round(recency_score, 1),
            "tier_score": tier_score
        },
        "recommendations": []
    }
    
    # Add recommendations based on score
    if total_score < 50:
        result["recommendations"].extend([
            "Consider re-engagement campaign",
            "Offer personalized discounts",
            "Review customer satisfaction"
        ])
    elif total_score < 70:
        result["recommendations"].extend([
            "Upsell opportunities available",
            "Encourage more frequent purchases",
            "Consider tier upgrade incentives"
        ])
    else:
        result["recommendations"].extend([
            "Excellent customer - maintain relationship",
            "Consider VIP treatment",
            "Leverage for referrals"
        ])
    
    return json.dumps(result, indent=2)


@mcp.tool()
async def generate_customer_insights(customer_id: str, ctx: Context) -> str:
    """Generate comprehensive AI-driven insights for a customer.
    
    This tool combines multiple data sources to provide actionable
    insights about customer behavior, preferences, and opportunities.
    """
    logger.info(f"Generating insights for customer {customer_id}")
    
    customer = MOCK_CUSTOMERS.get(customer_id)
    if not customer:
        return json.dumps({"error": f"Customer {customer_id} not found"}, indent=2)
    
    await ctx.info(f"Analyzing customer {customer['name']}")
    
    # Calculate derived metrics
    days_since_join = (datetime.now() - datetime.strptime(customer["join_date"], "%Y-%m-%d")).days
    avg_order_value = customer["total_spent"] / customer["total_purchases"]
    purchase_frequency = customer["total_purchases"] / (days_since_join / 30)  # per month
    
    insights = {
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "analysis_date": datetime.now().isoformat(),
        "key_metrics": {
            "customer_lifetime_days": days_since_join,
            "average_order_value": round(avg_order_value, 2),
            "monthly_purchase_frequency": round(purchase_frequency, 2),
            "total_clv": customer["total_spent"]
        },
        "behavioral_insights": [],
        "opportunities": [],
        "risk_factors": [],
        "recommendations": []
    }
    
    # Generate behavioral insights
    if avg_order_value > 150:
        insights["behavioral_insights"].append("High-value purchaser - prefers quality over quantity")
    if len(customer["preferred_categories"]) > 2:
        insights["behavioral_insights"].append("Diverse interests - good cross-sell candidate")
    if customer["customer_tier"] in ["gold", "platinum"]:
        insights["behavioral_insights"].append("Loyal customer with strong brand affinity")
    
    # Identify opportunities
    if purchase_frequency < 1:
        insights["opportunities"].append("Increase purchase frequency through targeted campaigns")
    if customer["customer_tier"] == "silver" and customer["total_spent"] > 2000:
        insights["opportunities"].append("Eligible for tier upgrade to Gold")
    
    # Risk factors
    days_since_last = (datetime.now() - datetime.strptime(customer["last_purchase"], "%Y-%m-%d")).days
    if days_since_last > 30:
        insights["risk_factors"].append(f"No purchase in {days_since_last} days - churn risk")
    if customer["risk_score"] > 0.2:
        insights["risk_factors"].append("High churn risk score - needs attention")
    
    # Recommendations
    insights["recommendations"].extend([
        f"Target with {customer['preferred_categories'][0]} category promotions",
        "Send personalized product recommendations",
        f"Optimal contact time: {random.choice(['Morning', 'Afternoon', 'Evening'])}"
    ])
    
    return json.dumps(insights, indent=2)


@mcp.prompt()
def analyze_customer_behavior(customer_id: str) -> str:
    """Analyze customer behavior patterns and provide strategic recommendations."""
    return f"""Please analyze the behavior patterns for customer ID {customer_id}. 

Focus on:
1. Purchase history and trends
2. Category preferences and cross-sell opportunities  
3. Customer lifecycle stage and tier progression
4. Risk factors and retention strategies
5. Personalization opportunities

Use the customer data and predictions resources to gather comprehensive information, then provide actionable insights and recommendations for improving customer engagement and lifetime value."""


@mcp.prompt()
def create_retention_strategy(customer_segment: str) -> List[base.Message]:
    """Create a customer retention strategy for a specific segment."""
    return [
        base.UserMessage(f"I need to create a retention strategy for the '{customer_segment}' customer segment."),
        base.UserMessage("Please analyze the segment characteristics and develop a comprehensive retention plan."),
        base.AssistantMessage("I'll help you create a targeted retention strategy. Let me analyze the segment data first."),
        base.UserMessage("Include specific tactics, timing, channels, and success metrics in your recommendations.")
    ]


@mcp.prompt()
def customer_health_check(customer_id: str) -> str:
    """Perform a comprehensive customer health assessment."""
    return f"""Perform a complete health check for customer {customer_id}.

Evaluate:
- Customer engagement levels
- Purchase behavior trends
- Risk indicators and warning signs
- Satisfaction and loyalty metrics
- Competitive threats
- Growth opportunities

Provide a health score (1-10) and specific action items to maintain or improve customer relationship health."""


if __name__ == "__main__":
    mcp.run() 