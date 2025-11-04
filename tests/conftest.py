"""
Pytest configuration and shared fixtures for newsapi-ai tests.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from types import SimpleNamespace


@pytest.fixture
def mock_newsapi_client(monkeypatch):
    """
    Mock NewsAPI client to avoid real API calls in unit tests.

    This fixture patches the requests.Session.get method used by NewsAPIClient
    to return mock data instead of making real HTTP requests.
    """
    mock_response_data = {
        'status': 'ok',
        'totalResults': 10,
        'articles': [
            {
                'source': {'id': 'techcrunch', 'name': 'TechCrunch'},
                'author': 'Test Author',
                'title': 'Test Article 1',
                'description': 'This is a test article description',
                'url': 'https://example.com/article1',
                'urlToImage': 'https://example.com/image1.jpg',
                'publishedAt': '2025-11-01T10:00:00Z',
                'content': 'Test article content...'
            },
            {
                'source': {'id': 'reuters', 'name': 'Reuters'},
                'author': 'Another Author',
                'title': 'Test Article 2',
                'description': 'Another test article',
                'url': 'https://example.com/article2',
                'urlToImage': 'https://example.com/image2.jpg',
                'publishedAt': '2025-11-02T12:00:00Z',
                'content': 'More test content...'
            },
            {
                'source': {'id': 'bbc-news', 'name': 'BBC News'},
                'author': 'BBC Reporter',
                'title': 'Test Article 3',
                'description': 'Third test article',
                'url': 'https://example.com/article3',
                'urlToImage': 'https://example.com/image3.jpg',
                'publishedAt': '2025-11-03T08:00:00Z',
                'content': 'BBC test content...'
            }
        ]
    }

    # Create a mock response object
    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = Mock()

    # Patch requests.Session.get to return our mock response
    with patch('requests.Session.get', return_value=mock_response):
        yield mock_response


@pytest.fixture
def mock_anthropic_client():
    """
    Mock Anthropic client for testing without real API calls.

    Returns a mock client that simulates Claude API responses.
    """
    from types import SimpleNamespace

    mock_client = Mock()

    # Mock the messages.create response
    mock_message = Mock()

    # Create a text block using SimpleNamespace so .text is a real string attribute
    mock_text_block = SimpleNamespace(
        text="This is a mocked AI response about the news query.",
        type="text"
    )

    mock_message.content = [mock_text_block]
    mock_message.stop_reason = "end_turn"

    mock_client.messages.create.return_value = mock_message

    return mock_client


@pytest.fixture
def sample_user_query():
    """
    Sample UserQuery object for testing.
    """
    from src.api_client.models import UserQuery
    return UserQuery(
        q="test query",
        languages=["en"],
        pageSize=10,
        max_results=100
    )


@pytest.fixture
def sample_articles():
    """
    Sample article data for testing.
    """
    return [
        {
            'source': {'id': 'test-source', 'name': 'Test Source'},
            'author': 'Test Author',
            'title': 'Sample Article 1',
            'description': 'This is a sample article for testing',
            'url': 'https://example.com/article1',
            'urlToImage': 'https://example.com/image1.jpg',
            'publishedAt': '2025-11-01T10:00:00Z',
            'content': 'Sample article content...'
        },
        {
            'source': {'id': 'another-source', 'name': 'Another Source'},
            'author': 'Another Author',
            'title': 'Sample Article 2',
            'description': 'Another sample article',
            'url': 'https://example.com/article2',
            'urlToImage': 'https://example.com/image2.jpg',
            'publishedAt': '2025-11-02T12:00:00Z',
            'content': 'More sample content...'
        }
    ]


# Helper functions for creating properly structured mocks

def create_text_block(text: str):
    """
    Create a text block for Anthropic API response mocking.

    Args:
        text: The text content of the block

    Returns:
        SimpleNamespace object with text and type attributes

    Usage:
        mock_text_block = create_text_block("Hello, world!")
        # Now mock_text_block.text is a real string, not a Mock
    """
    return SimpleNamespace(text=text, type="text")


def create_tool_block(name: str, input_data: dict, tool_id: str = "tool_123"):
    """
    Create a tool use block for Anthropic API response mocking.

    Args:
        name: The name of the tool
        input_data: The input parameters for the tool
        tool_id: The tool use ID (default: "tool_123")

    Returns:
        SimpleNamespace object with tool use attributes

    Usage:
        tool_block = create_tool_block("search_everything", {"q": "AI"})
    """
    return SimpleNamespace(
        type="tool_use",
        name=name,
        input=input_data,
        id=tool_id
    )
