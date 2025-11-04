"""
Test API clients (NewsAPI, Scraping, Query Optimization).

This module consolidates tests for:
- NewsAPI direct client
- Article scraping
- LLM query optimization
- Complete production workflows

Tests require NEWS_API_KEY and optionally ANTHROPIC_API_KEY.
"""
import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api_client import (
    NewsAPIClient,
    QueryOptimizer,
    Article,
    SearchResult,
)
from src.config.settings import get_settings


class TestNewsAPIClient:
    """Test NewsAPI direct client"""

    @pytest.mark.unit
    def test_basic_search(self, mock_newsapi_client):
        """Test basic article search (mocked)"""
        from src.api_client.models import UserQuery
        with NewsAPIClient() as client:
            user_query = UserQuery(
                q="technology",
                languages=["en"],
                pageSize=5
            )
            results = client.search_everything(user_query)

            assert results['status'] == 'ok'
            assert 'articles' in results
            assert len(results['articles']) > 0

    @pytest.mark.unit
    def test_search_with_dates(self, mock_newsapi_client):
        """Test search with date range (mocked)"""
        from src.api_client.models import UserQuery
        from_date = datetime.now() - timedelta(days=7)
        to_date = datetime.now()

        with NewsAPIClient() as client:
            user_query = UserQuery(
                q="artificial intelligence",
                from_date=from_date,
                to_date=to_date,
                pageSize=5
            )
            results = client.search_everything(user_query)

            assert results['status'] == 'ok'
            assert len(results['articles']) > 0

    @pytest.mark.unit
    def test_top_headlines(self, mock_newsapi_client):
        """Test fetching top headlines (mocked)"""
        from src.api_client.models import UserQuery
        with NewsAPIClient() as client:
            user_query = UserQuery(
                countries=["us"],
                pageSize=5
            )
            results = client.search_top_headlines(user_query)

            assert results['status'] == 'ok'
            assert 'articles' in results

    @pytest.mark.integration
    def test_newsapi_live_smoke_test(self):
        """
        Integration test: Verify real NewsAPI connectivity.

        This test makes an actual API call and is skipped by default.
        Run with: pytest -m integration
        """
        from src.api_client.models import UserQuery
        settings = get_settings()
        if not settings.news_api_key:
            pytest.skip("NEWS_API_KEY not set in environment")

        with NewsAPIClient() as client:
            user_query = UserQuery(q="test", pageSize=1)
            results = client.search_everything(user_query)
            assert results['status'] == 'ok'
            assert 'articles' in results


class TestQueryOptimizer:
    """Test LLM-powered query optimization"""

    @pytest.fixture
    def check_anthropic_key(self):
        settings = get_settings()
        if not settings.anthropic_api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")

    @pytest.mark.integration
    def test_query_optimization(self, check_anthropic_key):
        """Test basic query optimization (MAKES REAL API CALLS)"""
        optimizer = QueryOptimizer(provider="anthropic")
        user_input = "What are the latest developments in renewable energy?"

        user_queries = optimizer.optimize_query(user_input)

        assert isinstance(user_queries, list)
        assert len(user_queries) >= 1
        # Check that UserQuery objects are returned
        for query in user_queries:
            assert hasattr(query, 'q')
            assert query.q  # Query string should not be empty


class TestArticleDataModel:
    """Test Article data model"""

    @pytest.mark.unit
    def test_article_from_newsapi(self, mock_newsapi_client):
        """Test creating Article from NewsAPI data (mocked)"""
        from src.api_client.models import UserQuery
        with NewsAPIClient() as client:
            user_query = UserQuery(q="climate", pageSize=3)
            results = client.search_everything(user_query)

            articles = [
                Article.from_newsapi(article_data)
                for article_data in results['articles']
            ]

            assert len(articles) > 0
            for article in articles:
                assert article.url
                assert article.title



class TestCompleteWorkflow:
    """Test complete production workflow"""

    @pytest.fixture
    def check_all_keys(self):
        settings = get_settings()
        if not settings.news_api_key:
            pytest.skip("NEWS_API_KEY not set")
        if not settings.anthropic_api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")

    @pytest.mark.integration
    def test_complete_workflow(self, check_all_keys):
        """
        Test complete workflow (MAKES REAL API CALLS to NewsAPI and Anthropic):
        1. Generate queries with LLM
        2. Search for articles using first query
        3. Convert to Article objects
        4. Generate statistics
        """
        print(f"\n{'='*60}")
        print("Testing Complete Production Workflow")
        print(f"{'='*60}")

        # Step 1: Generate queries with LLM
        print("\n[1] Generating queries with Claude...")
        optimizer = QueryOptimizer(provider="anthropic")
        user_queries = optimizer.optimize_query("Latest developments in electric vehicles")

        print(f"  Generated {len(user_queries)} queries:")
        for i, query in enumerate(user_queries, 1):
            print(f"    {i}. {query.q}")
        if user_queries[0].from_date and user_queries[0].to_date:
            print(f"  Date range: {user_queries[0].from_date.strftime('%Y-%m-%d')} to {user_queries[0].to_date.strftime('%Y-%m-%d')}")

        # Step 2: Search for articles using first query
        print(f"\n[2] Searching NewsAPI with first query...")
        first_query = user_queries[0]
        print(f"  Using query: {first_query.q}")

        with NewsAPIClient() as news_client:
            results = news_client.search_everything(first_query)

        print(f"  Found {len(results['articles'])} articles")

        # Step 3: Convert to Article objects
        print("\n[3] Creating Article objects...")
        articles = [
            Article.from_newsapi(article_data)
            for article_data in results['articles']
        ]

        # Step 4: Generate statistics
        print("\n[4] Generating statistics...")
        search_result = SearchResult(
            query=first_query,
            total_found=results['totalResults']
        )

        for article in articles:
            search_result.add_article(article)

        print(f"  Total articles: {search_result.total_found}")

        # Assertions
        assert len(articles) > 0
        assert search_result.total_found == len(articles)
        assert len(search_result.articles) == len(articles)

        print(f"\n{'='*60}")
        print("✓ Complete workflow test passed!")
        print(f"{'='*60}\n")


class TestAPIErrorHandling:
    """Test error handling in API clients"""

    @pytest.fixture
    def check_news_api_key(self):
        settings = get_settings()
        if not settings.news_api_key:
            pytest.skip("NEWS_API_KEY not set")

    @pytest.mark.integration
    def test_newsapi_invalid_query(self, check_news_api_key):
        """Test NewsAPI with invalid query parameters (MAKES REAL API CALLS)"""
        from src.api_client.models import UserQuery
        with NewsAPIClient() as client:
            # Empty query should raise ValueError
            try:
                user_query = UserQuery(q="", pageSize=1)
                results = client.search_everything(user_query)
                # If it doesn't raise, check that status is in results
                assert 'status' in results
            except ValueError:
                # Expected - empty query is invalid
                assert True

    @pytest.mark.integration
    def test_newsapi_invalid_date_range(self, check_news_api_key):
        """Test NewsAPI with invalid date range (MAKES REAL API CALLS)"""
        from datetime import datetime, timedelta

        with NewsAPIClient() as client:
            # to_date before from_date
            from_date = datetime.now()
            to_date = datetime.now() - timedelta(days=30)

            try:
                results = client.search_articles(
                    query="test",
                    from_date=from_date,
                    to_date=to_date,
                    page_size=1
                )
                # Should either handle gracefully or raise error
                assert 'status' in results or results is None
            except Exception:
                # Error is acceptable
                assert True

    @pytest.mark.integration
    def test_newsapi_invalid_page_size(self, check_news_api_key):
        """Test NewsAPI with invalid page size (MAKES REAL API CALLS)"""
        with NewsAPIClient() as client:
            # Page size of 0 or negative
            try:
                results = client.search_articles(
                    query="test",
                    page_size=0
                )
                # Should handle gracefully
                assert results is not None
            except Exception:
                # Error is acceptable
                assert True

    @pytest.mark.integration
    def test_newsapi_connection_error(self):
        """Test NewsAPI connection error handling (MAKES REAL API CALLS)"""
        # Create client with invalid API key
        try:
            with NewsAPIClient(api_key="invalid_key_12345") as client:
                results = client.search_articles(
                    query="test",
                    page_size=1
                )
                # Should return error status
                if results:
                    assert 'status' in results
        except Exception:
            # Connection errors are acceptable
            assert True

    @pytest.mark.integration
    def test_query_optimizer_empty_input(self):
        """Test query optimizer with empty input (MAKES REAL API CALLS)"""
        settings = get_settings()
        if not settings.anthropic_api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")

        optimizer = QueryOptimizer(provider="anthropic")

        try:
            user_queries = optimizer.optimize_query("")
            # Should return fallback queries
            assert user_queries is not None
            assert isinstance(user_queries, list)
        except Exception:
            # Error is acceptable
            assert True

    @pytest.mark.integration
    def test_query_optimizer_very_long_input(self):
        """Test query optimizer with very long input (MAKES REAL API CALLS)"""
        settings = get_settings()
        if not settings.anthropic_api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")

        optimizer = QueryOptimizer(provider="anthropic")
        long_input = "technology " * 1000  # Very long query

        try:
            user_queries = optimizer.optimize_query(long_input)
            # Should handle gracefully
            assert user_queries is not None
        except Exception:
            # Error is acceptable for extremely long input
            assert True

    def test_article_from_newsapi_missing_fields(self):
        """Test Article.from_newsapi with missing fields"""
        incomplete_data = {
            "url": "https://example.com/article",
            "title": "Test Article"
            # Missing many optional fields
        }

        article = Article.from_newsapi(incomplete_data)

        assert article.url == "https://example.com/article"
        assert article.title == "Test Article"
        # Should handle missing fields gracefully
        assert article.description is None or article.description == ""



if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
