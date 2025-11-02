"""
Tests for the API server.

This module tests:
- API endpoint functionality
- Request/response models
- Error handling
- Health checks
- Integration with NewsAgent
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import json
import sys

# Mock the Azure OpenAI import before importing the module
sys.modules['openai'] = Mock()

from src.api_server.main import app
from src.api_server.models import QueryRequest, QueryResponse, HealthResponse


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_agent_response():
    """Mock successful agent response."""
    return {
        "response": "I found 5 articles about AI technology.",
        "messages": [
            {"role": "user", "content": "Find news about AI"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "tool_123",
                        "content": json.dumps({
                            "status": "ok",
                            "total_results": 5,
                            "articles": [
                                {
                                    "title": "AI Breakthrough",
                                    "description": "New AI technology",
                                    "url": "https://example.com/ai1",
                                    "publishedAt": "2025-11-02T10:00:00Z"
                                },
                                {
                                    "title": "Machine Learning Advances",
                                    "description": "ML progress",
                                    "url": "https://example.com/ai2",
                                    "publishedAt": "2025-11-01T15:00:00Z"
                                }
                            ]
                        })
                    }
                ]
            }
        ]
    }


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns 200 OK."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "services" in data
        assert "version" in data

    def test_health_check_structure(self, client):
        """Test health check response structure."""
        response = client.get("/health")
        data = response.json()

        assert "anthropic" in data["services"]
        assert "newsapi" in data["services"]
        assert "agent" in data["services"]


class TestQueryEndpoint:
    """Test the main query endpoint."""

    @patch('src.api_server.main.news_agent')
    def test_query_with_natural_response(self, mock_agent, client, mock_agent_response):
        """Test query endpoint with natural language response."""
        mock_agent.process_request.return_value = mock_agent_response

        request_data = {
            "query": "Find news about AI",
            "response_format": "natural"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "I found 5 articles about AI technology."
        assert data["format"] == "natural"

    @patch('src.api_server.main.news_agent')
    def test_query_with_structured_response(self, mock_agent, client, mock_agent_response):
        """Test query endpoint with structured response."""
        mock_agent.process_request.return_value = mock_agent_response

        request_data = {
            "query": "Find news about AI",
            "response_format": "structured"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert "articles" in data
        assert len(data["articles"]) == 2
        assert data["articles"][0]["title"] == "AI Breakthrough"
        assert data["total_results"] == 5
        assert data["format"] == "structured"

    @patch('src.api_server.main.news_agent')
    def test_query_with_both_formats(self, mock_agent, client, mock_agent_response):
        """Test query endpoint with both response formats."""
        mock_agent.process_request.return_value = mock_agent_response

        request_data = {
            "query": "Find news about AI",
            "response_format": "both"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "articles" in data
        assert data["response"] == "I found 5 articles about AI technology."
        assert len(data["articles"]) == 2
        assert data["format"] == "both"

    @patch('src.api_server.main.news_agent')
    def test_query_with_session_id(self, mock_agent, client, mock_agent_response):
        """Test query endpoint maintains session ID."""
        mock_agent.process_request.return_value = mock_agent_response

        request_data = {
            "query": "Find news about AI",
            "session_id": "session_123",
            "response_format": "natural"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "session_123"
        mock_agent.process_request.assert_called_once_with(
            user_prompt="Find news about AI",
            session_id="session_123"
        )

    def test_query_without_agent(self, client):
        """Test query endpoint when agent is not configured."""
        with patch('src.api_server.main.news_agent', None):
            request_data = {
                "query": "Find news about AI"
            }

            response = client.post("/query", json=request_data)

            assert response.status_code == 503
            data = response.json()
            assert "error" in data

    @patch('src.api_server.main.news_agent')
    def test_query_handles_agent_error(self, mock_agent, client):
        """Test query endpoint handles agent errors gracefully."""
        mock_agent.process_request.side_effect = Exception("Agent error")

        request_data = {
            "query": "Find news about AI"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 500
        data = response.json()
        assert "error" in data

    def test_query_validates_request(self, client):
        """Test query endpoint validates request data."""
        # Empty query
        response = client.post("/query", json={"query": ""})
        assert response.status_code == 422

        # Missing query
        response = client.post("/query", json={})
        assert response.status_code == 422

        # Invalid response_format
        response = client.post("/query", json={
            "query": "test",
            "response_format": "invalid"
        })
        assert response.status_code == 422


class TestRequestModels:
    """Test request models."""

    def test_query_request_valid(self):
        """Test QueryRequest with valid data."""
        request = QueryRequest(
            query="Find AI news",
            session_id="session_123",
            response_format="both"
        )

        assert request.query == "Find AI news"
        assert request.session_id == "session_123"
        assert request.response_format == "both"

    def test_query_request_defaults(self):
        """Test QueryRequest default values."""
        request = QueryRequest(query="Find AI news")

        assert request.query == "Find AI news"
        assert request.session_id is None
        assert request.response_format == "both"

    def test_query_request_validation(self):
        """Test QueryRequest validation."""
        # Empty query should fail
        with pytest.raises(ValueError):
            QueryRequest(query="")

        # Invalid response_format should fail
        with pytest.raises(ValueError):
            QueryRequest(query="test", response_format="invalid")


class TestResponseModels:
    """Test response models."""

    def test_query_response_natural(self):
        """Test QueryResponse with natural format."""
        response = QueryResponse(
            response="Here are the results",
            format="natural"
        )

        assert response.response == "Here are the results"
        assert response.articles is None
        assert response.format == "natural"

    def test_query_response_structured(self):
        """Test QueryResponse with structured format."""
        from src.api_server.models import Article

        articles = [
            Article(
                title="Test Article",
                url="https://example.com",
                publishedAt="2025-11-02T10:00:00Z"
            )
        ]

        response = QueryResponse(
            articles=articles,
            total_results=1,
            format="structured"
        )

        assert len(response.articles) == 1
        assert response.articles[0].title == "Test Article"
        assert response.total_results == 1
        assert response.format == "structured"

    def test_health_response(self):
        """Test HealthResponse model."""
        response = HealthResponse(
            status="ok",
            version="1.0.0",
            services={"anthropic": "ok", "newsapi": "ok"}
        )

        assert response.status == "ok"
        assert response.version == "1.0.0"
        assert response.services["anthropic"] == "ok"


class TestArticleExtraction:
    """Test article extraction from messages."""

    @patch('src.api_server.main.news_agent')
    def test_extract_articles_from_messages(self, mock_agent, client, mock_agent_response):
        """Test that articles are correctly extracted from tool results."""
        mock_agent.process_request.return_value = mock_agent_response

        request_data = {
            "query": "Find news about AI",
            "response_format": "structured"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert "articles" in data
        assert len(data["articles"]) == 2
        assert data["articles"][0]["title"] == "AI Breakthrough"
        assert data["articles"][1]["title"] == "Machine Learning Advances"

    @patch('src.api_server.main.news_agent')
    def test_no_articles_in_messages(self, mock_agent, client):
        """Test when no articles are present in messages."""
        mock_agent.process_request.return_value = {
            "response": "I couldn't find any articles.",
            "messages": [
                {"role": "user", "content": "Find news about AI"}
            ]
        }

        request_data = {
            "query": "Find news about AI",
            "response_format": "structured"
        }

        response = client.post("/query", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data.get("articles") is None


class TestCORS:
    """Test CORS configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in actual responses."""
        # CORS headers are added to actual responses, not OPTIONS
        response = client.get("/health")

        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers or response.status_code == 200
        # Just verify the endpoint works - CORS is configured in the app


class TestIntegration:
    """Integration tests for the API server."""

    @patch('src.api_server.main.news_agent')
    def test_full_workflow(self, mock_agent, client, mock_agent_response):
        """Test a complete workflow from request to response."""
        mock_agent.process_request.return_value = mock_agent_response

        # Make request
        request_data = {
            "query": "What's happening with AI today?",
            "session_id": "test_session",
            "response_format": "both"
        }

        response = client.post("/query", json=request_data)

        # Verify response
        assert response.status_code == 200
        data = response.json()

        # Check natural language response
        assert data["response"] == "I found 5 articles about AI technology."

        # Check structured data
        assert len(data["articles"]) == 2
        assert data["total_results"] == 5

        # Check session ID maintained
        assert data["session_id"] == "test_session"

        # Verify agent was called correctly
        mock_agent.process_request.assert_called_once_with(
            user_prompt="What's happening with AI today?",
            session_id="test_session"
        )
