"""
News API module for fetching and scraping articles

Use the factory functions (get_scraper) for automatic
selection between MCP and direct API clients based on configuration.
"""
# Direct API clients (for production/Azure deployment)
from .news_client import NewsAPIClient

# Data models
from .models import (
    Article,
    SearchResult,
    UserQuery,
    EverythingQuery,
    TopHeadlinesQuery,
    SourcesQuery
)

# Query optimization (deprecated - not needed with MCP)
from .query_optimizer import QueryOptimizer

__all__ = [
    # Direct API clients
    'NewsAPIClient',
    # Models
    'Article',
    'SearchResult',
    'UserQuery',
    'EverythingQuery',
    'TopHeadlinesQuery',
    'SourcesQuery',
    # Optimization (deprecated)
    'QueryOptimizer'
]
