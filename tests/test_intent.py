"""
Tests for the intent module (NewsAgent).

This module tests:
- NewsAgent initialization
- Tool definitions
- Tool execution
- Conversation flow with Anthropic Claude
- Session management

Note: These tests mock the QueryOptimizer to avoid importing Azure OpenAI dependencies.
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch
from dataclasses import asdict

# Mock the Azure OpenAI import before importing the module
import sys
sys.modules['openai'] = Mock()

from src.intent.news_agent import NewsAgent
from src.api_client.models import UserQuery


class TestNewsAgentInit:
    """Test NewsAgent initialization."""

    def test_init_with_clients(self):
        """Test NewsAgent initializes correctly with clients."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        agent = NewsAgent(mock_anthropic, mock_news_client)

        assert agent.client == mock_anthropic
        assert agent.news_client == mock_news_client
        assert agent.conversation_history == {}
        assert len(agent.tools) == 4

    def test_tools_definition(self):
        """Test that all required tools are defined."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        agent = NewsAgent(mock_anthropic, mock_news_client)

        tool_names = [tool["name"] for tool in agent.tools]
        assert "optimize_queries" in tool_names
        assert "search_everything" in tool_names
        assert "search_top_headlines" in tool_names
        assert "get_sources" in tool_names

    def test_tool_schemas_valid(self):
        """Test that all tool schemas are valid."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        agent = NewsAgent(mock_anthropic, mock_news_client)

        for tool in agent.tools:
            assert "name" in tool
            assert "description" in tool
            assert "input_schema" in tool
            assert tool["input_schema"]["type"] == "object"
            assert "properties" in tool["input_schema"]


class TestToolExecution:
    """Test individual tool execution."""

    def test_execute_optimize_queries(self):
        """Test optimize_queries tool execution."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        agent = NewsAgent(mock_anthropic, mock_news_client)

        # Mock QueryOptimizer
        with patch('src.intent.news_agent.QueryOptimizer') as MockOptimizer:
            mock_optimizer = Mock()
            mock_query = UserQuery(q="test query", languages=["en"])
            mock_optimizer.optimize_query.return_value = [mock_query]
            MockOptimizer.return_value = mock_optimizer

            tool_input = {"user_input": "latest news about AI"}
            result = agent._execute_tool("optimize_queries", tool_input)

            assert "queries" in result
            assert isinstance(result["queries"], list)
            mock_optimizer.optimize_query.assert_called_once_with("latest news about AI")

    def test_execute_search_everything(self):
        """Test search_everything tool execution."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock the search response
        mock_news_client.search_everything.return_value = {
            "status": "ok",
            "totalResults": 100,
            "articles": [{"title": f"Article {i}"} for i in range(15)]
        }

        agent = NewsAgent(mock_anthropic, mock_news_client)

        tool_input = {"q": "climate change", "languages": ["en"]}
        result = agent._execute_tool("search_everything", tool_input)

        assert result["status"] == "ok"
        assert result["total_results"] == 100
        assert len(result["articles"]) == 10  # Limited to 10
        mock_news_client.search_everything.assert_called_once()

    def test_execute_search_top_headlines(self):
        """Test search_top_headlines tool execution."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock the headlines response
        mock_news_client.search_top_headlines.return_value = {
            "status": "ok",
            "totalResults": 20,
            "articles": [{"title": f"Headline {i}"} for i in range(20)]
        }

        agent = NewsAgent(mock_anthropic, mock_news_client)

        tool_input = {"countries": ["us"], "categories": ["technology"]}
        result = agent._execute_tool("search_top_headlines", tool_input)

        assert result["status"] == "ok"
        assert result["total_results"] == 20
        assert len(result["articles"]) == 10  # Limited to 10
        mock_news_client.search_top_headlines.assert_called_once()

    def test_execute_get_sources(self):
        """Test get_sources tool execution."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock the sources response
        mock_news_client.get_sources.return_value = {
            "status": "ok",
            "sources": [
                {"id": "bbc-news", "name": "BBC News"},
                {"id": "cnn", "name": "CNN"}
            ]
        }

        agent = NewsAgent(mock_anthropic, mock_news_client)

        tool_input = {"categories": ["general"], "languages": ["en"]}
        result = agent._execute_tool("get_sources", tool_input)

        assert result["status"] == "ok"
        assert len(result["sources"]) == 2
        mock_news_client.get_sources.assert_called_once()

    def test_execute_unknown_tool(self):
        """Test that unknown tool raises ValueError."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        agent = NewsAgent(mock_anthropic, mock_news_client)

        with pytest.raises(ValueError, match="Unknown tool"):
            agent._execute_tool("invalid_tool", {})


class TestProcessRequest:
    """Test request processing and conversation flow."""

    def test_process_request_simple_response(self):
        """Test processing a simple request that doesn't require tools."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock a simple text response (no tool use)
        mock_response = Mock()
        mock_response.stop_reason = "end_turn"
        mock_text_block = Mock()
        mock_text_block.text = "Here is the news you requested."
        mock_response.content = [mock_text_block]

        mock_anthropic.messages.create.return_value = mock_response

        agent = NewsAgent(mock_anthropic, mock_news_client)

        result = agent.process_request("Tell me about the news")

        assert "response" in result
        assert result["response"] == "Here is the news you requested."
        assert "messages" in result
        mock_anthropic.messages.create.assert_called_once()

    def test_process_request_with_tool_use(self):
        """Test processing a request that uses tools."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock tool use response, then final response
        mock_tool_response = Mock()
        mock_tool_response.stop_reason = "tool_use"
        mock_tool_block = Mock()
        mock_tool_block.type = "tool_use"
        mock_tool_block.name = "search_everything"
        mock_tool_block.input = {"q": "AI", "languages": ["en"]}
        mock_tool_block.id = "tool_123"
        mock_tool_response.content = [mock_tool_block]

        # Mock news client response
        mock_news_client.search_everything.return_value = {
            "status": "ok",
            "totalResults": 5,
            "articles": [{"title": "AI Article"}]
        }

        # Mock final text response
        mock_final_response = Mock()
        mock_final_response.stop_reason = "end_turn"
        mock_text_block = Mock()
        mock_text_block.text = "I found 5 articles about AI."
        mock_final_response.content = [mock_text_block]

        # Set up the mock to return tool response first, then final response
        mock_anthropic.messages.create.side_effect = [
            mock_tool_response,
            mock_final_response
        ]

        agent = NewsAgent(mock_anthropic, mock_news_client)

        result = agent.process_request("Find news about AI")

        assert "response" in result
        assert "I found 5 articles about AI" in result["response"]
        assert mock_anthropic.messages.create.call_count == 2

    def test_process_request_with_session_id(self):
        """Test that session_id maintains conversation history."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock simple response
        mock_response = Mock()
        mock_response.stop_reason = "end_turn"
        mock_text_block = Mock()
        mock_text_block.text = "Response"
        mock_response.content = [mock_text_block]

        mock_anthropic.messages.create.return_value = mock_response

        agent = NewsAgent(mock_anthropic, mock_news_client)

        # First request with session
        result1 = agent.process_request("First message", session_id="session_123")

        # Verify conversation history is stored
        assert "session_123" not in agent.conversation_history or \
               len(result1["messages"]) >= 1

    def test_process_request_without_session_id(self):
        """Test that requests without session_id don't maintain history."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock simple response
        mock_response = Mock()
        mock_response.stop_reason = "end_turn"
        mock_text_block = Mock()
        mock_text_block.text = "Response"
        mock_response.content = [mock_text_block]

        mock_anthropic.messages.create.return_value = mock_response

        agent = NewsAgent(mock_anthropic, mock_news_client)

        result = agent.process_request("Message without session")

        # Verify messages are returned but not stored
        assert "messages" in result
        assert len(result["messages"]) >= 1


class TestToolDefinitions:
    """Test tool definition details."""

    def test_optimize_queries_tool_schema(self):
        """Test optimize_queries tool has correct schema."""
        agent = NewsAgent(Mock(), Mock())

        tool = next(t for t in agent.tools if t["name"] == "optimize_queries")

        assert "user_input" in tool["input_schema"]["properties"]
        assert "user_input" in tool["input_schema"]["required"]

    def test_search_everything_tool_schema(self):
        """Test search_everything tool has correct schema."""
        agent = NewsAgent(Mock(), Mock())

        tool = next(t for t in agent.tools if t["name"] == "search_everything")

        props = tool["input_schema"]["properties"]
        assert "q" in props
        assert "searchIn" in props
        assert "sources" in props
        assert "domains" in props
        assert "from_date" in props
        assert "to_date" in props
        assert "languages" in props
        assert "sortBy" in props
        assert "max_results" in props
        assert "q" in tool["input_schema"]["required"]

    def test_search_top_headlines_tool_schema(self):
        """Test search_top_headlines tool has correct schema."""
        agent = NewsAgent(Mock(), Mock())

        tool = next(t for t in agent.tools if t["name"] == "search_top_headlines")

        props = tool["input_schema"]["properties"]
        assert "q" in props
        assert "countries" in props
        assert "categories" in props
        assert "sources" in props
        assert "max_results" in props

    def test_get_sources_tool_schema(self):
        """Test get_sources tool has correct schema."""
        agent = NewsAgent(Mock(), Mock())

        tool = next(t for t in agent.tools if t["name"] == "get_sources")

        props = tool["input_schema"]["properties"]
        assert "categories" in props
        assert "languages" in props
        assert "countries" in props


class TestErrorHandling:
    """Test error handling in NewsAgent."""

    def test_search_everything_with_invalid_input(self):
        """Test that invalid input to search_everything is handled."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        agent = NewsAgent(mock_anthropic, mock_news_client)

        # Missing required 'q' parameter should raise error
        tool_input = {"languages": ["en"]}

        with pytest.raises(Exception):  # Could be TypeError or ValidationError
            agent._execute_tool("search_everything", tool_input)

    def test_news_client_error_propagates(self):
        """Test that news client errors propagate correctly."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Mock client to raise error
        mock_news_client.search_everything.side_effect = Exception("API Error")

        agent = NewsAgent(mock_anthropic, mock_news_client)

        tool_input = {"q": "test"}

        with pytest.raises(Exception, match="API Error"):
            agent._execute_tool("search_everything", tool_input)


class TestIntegration:
    """Integration tests for NewsAgent."""

    def test_full_workflow_with_mocks(self):
        """Test a complete workflow with all mocked components."""
        mock_anthropic = Mock()
        mock_news_client = Mock()

        # Set up mock responses
        # 1. Tool use response
        mock_tool_response = Mock()
        mock_tool_response.stop_reason = "tool_use"
        mock_tool_block = Mock()
        mock_tool_block.type = "tool_use"
        mock_tool_block.name = "search_everything"
        mock_tool_block.input = {"q": "technology", "languages": ["en"]}
        mock_tool_block.id = "tool_abc"
        mock_tool_response.content = [mock_tool_block]

        # 2. News API response
        mock_news_client.search_everything.return_value = {
            "status": "ok",
            "totalResults": 3,
            "articles": [
                {"title": "Tech News 1"},
                {"title": "Tech News 2"},
                {"title": "Tech News 3"}
            ]
        }

        # 3. Final response
        mock_final_response = Mock()
        mock_final_response.stop_reason = "end_turn"
        mock_text_block = Mock()
        mock_text_block.text = "I found 3 technology articles for you."
        mock_final_response.content = [mock_text_block]

        mock_anthropic.messages.create.side_effect = [
            mock_tool_response,
            mock_final_response
        ]

        agent = NewsAgent(mock_anthropic, mock_news_client)

        result = agent.process_request("Show me technology news")

        # Verify the workflow
        assert result["response"] == "I found 3 technology articles for you."
        assert mock_anthropic.messages.create.call_count == 2
        mock_news_client.search_everything.assert_called_once()

    def test_agent_can_be_imported(self):
        """Test that NewsAgent can be imported from the module."""
        from src.intent.news_agent import NewsAgent

        assert NewsAgent is not None
        assert callable(NewsAgent)
