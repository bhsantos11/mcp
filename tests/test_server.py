"""Tests for the Customer Analytics MCP Server."""

import json
import pytest
from unittest.mock import AsyncMock, patch

from mcp_demo_server.server import (
    get_customer_data,
    get_customer_predictions,
    get_customer_segment,
    calculate_customer_score,
    MOCK_CUSTOMERS,
)


class TestCustomerResources:
    """Test customer data resources."""

    def test_get_customer_data_valid_id(self):
        """Test fetching customer data with valid ID."""
        result = get_customer_data("1001")
        data = json.loads(result)
        
        assert data["id"] == "1001"
        assert data["name"] == "Alice Johnson"
        assert data["customer_tier"] == "gold"
        assert "days_since_last_purchase" in data
        assert "average_order_value" in data

    def test_get_customer_data_invalid_id(self):
        """Test fetching customer data with invalid ID."""
        result = get_customer_data("9999")
        data = json.loads(result)
        
        assert "error" in data
        assert "Customer 9999 not found" in data["error"]
        assert "available_customers" in data

    def test_get_customer_predictions_valid_id(self):
        """Test getting customer predictions with valid ID."""
        result = get_customer_predictions("1001")
        data = json.loads(result)
        
        assert data["customer_id"] == "1001"
        assert "churn_probability" in data
        assert "predicted_lifetime_value" in data
        assert "next_purchase_probability_30_days" in data
        assert "recommended_categories" in data
        assert isinstance(data["recommended_categories"], list)

    def test_get_customer_predictions_invalid_id(self):
        """Test getting customer predictions with invalid ID."""
        result = get_customer_predictions("9999")
        data = json.loads(result)
        
        assert "error" in data
        assert "Customer 9999 not found" in data["error"]

    def test_get_customer_segment_valid_segment(self):
        """Test getting customer segment data with valid segment."""
        result = get_customer_segment("high_value")
        data = json.loads(result)
        
        assert data["name"] == "High Value Customers"
        assert "criteria" in data
        assert "customer_count" in data
        assert "characteristics" in data
        assert isinstance(data["characteristics"], list)

    def test_get_customer_segment_invalid_segment(self):
        """Test getting customer segment data with invalid segment."""
        result = get_customer_segment("invalid_segment")
        data = json.loads(result)
        
        assert "error" in data
        assert "available_segments" in data


class TestCustomerTools:
    """Test customer analytics tools."""

    def test_calculate_customer_score_high_value(self):
        """Test customer score calculation for high-value customer."""
        result = calculate_customer_score(
            total_spent=5000.0,
            total_purchases=25,
            days_since_last_purchase=5,
            customer_tier="platinum"
        )
        data = json.loads(result)
        
        assert data["grade"] in ["A+", "A"]
        assert data["total_score"] > 70
        assert "breakdown" in data
        assert "recommendations" in data

    def test_calculate_customer_score_low_value(self):
        """Test customer score calculation for low-value customer."""
        result = calculate_customer_score(
            total_spent=100.0,
            total_purchases=2,
            days_since_last_purchase=90,
            customer_tier="bronze"
        )
        data = json.loads(result)
        
        assert data["grade"] in ["C", "D"]
        assert data["total_score"] < 50
        assert "re-engagement campaign" in str(data["recommendations"])

    def test_calculate_customer_score_breakdown(self):
        """Test that customer score breakdown is calculated correctly."""
        result = calculate_customer_score(
            total_spent=1000.0,
            total_purchases=10,
            days_since_last_purchase=10,
            customer_tier="gold"
        )
        data = json.loads(result)
        
        breakdown = data["breakdown"]
        assert "spending_score" in breakdown
        assert "frequency_score" in breakdown
        assert "recency_score" in breakdown
        assert "tier_score" in breakdown
        
        # Verify tier bonus
        assert breakdown["tier_score"] == 6  # Gold tier bonus


class TestMockData:
    """Test mock customer data integrity."""

    def test_mock_customers_structure(self):
        """Test that mock customer data has required fields."""
        required_fields = [
            "id", "name", "email", "age", "location", "join_date",
            "total_purchases", "total_spent", "last_purchase",
            "preferred_categories", "customer_tier", "risk_score"
        ]
        
        for customer_id, customer in MOCK_CUSTOMERS.items():
            for field in required_fields:
                assert field in customer, f"Missing field {field} in customer {customer_id}"

    def test_mock_customers_data_types(self):
        """Test that mock customer data has correct data types."""
        for customer_id, customer in MOCK_CUSTOMERS.items():
            assert isinstance(customer["id"], str)
            assert isinstance(customer["name"], str)
            assert isinstance(customer["email"], str)
            assert isinstance(customer["age"], int)
            assert isinstance(customer["total_purchases"], int)
            assert isinstance(customer["total_spent"], (int, float))
            assert isinstance(customer["preferred_categories"], list)
            assert isinstance(customer["risk_score"], (int, float))
            assert customer["customer_tier"] in ["bronze", "silver", "gold", "platinum"]


@pytest.mark.asyncio
class TestAsyncTools:
    """Test async tools and functions."""

    @patch('mcp_demo_server.server.MOCK_CUSTOMERS')
    async def test_generate_customer_insights_mock(self, mock_customers):
        """Test customer insights generation with mocked data."""
        # This would require more complex mocking of the Context object
        # For now, we'll test the basic structure
        mock_customers.get.return_value = MOCK_CUSTOMERS["1001"]
        
        # In a real test, we'd mock the Context and test the full function
        # This is a placeholder for more comprehensive async testing
        assert True  # Placeholder assertion


if __name__ == "__main__":
    pytest.main([__file__]) 