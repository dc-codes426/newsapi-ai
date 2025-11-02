"""
News API client for fetching articles from NewsAPI.org

This is the production client for Azure deployment (USE_MCP=false).
For development with MCP servers, use MCPNewsClient instead.
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import requests
from .models import UserQuery, EverythingQuery, TopHeadlinesQuery, SourcesQuery, Article, SearchResult
from ..config.settings import get_settings

logger = logging.getLogger(__name__)


class NewsAPIClient:
    """Client for interacting with NewsAPI.org"""

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NewsAPI client.

        Args:
            api_key: NewsAPI key. If not provided, uses settings.news_api_key
        """
        settings = get_settings()
        self.api_key = api_key or settings.news_api_key
        if not self.api_key:
            raise ValueError("NewsAPI key is required")

        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': self.api_key,
            'User-Agent': 'NewsAggregator/1.0'
        })

    def search_everything(self, user_query: UserQuery) -> Dict[str, Any]:
        """
        Search for articles using the /everything endpoint with automatic pagination.

        Args:
            user_query: UserQuery object with search parameters

        Returns:
            Dict containing 'status', 'totalResults', and 'articles'
        """
        endpoint = f"{self.BASE_URL}/everything"

        try:
            all_articles = []
            total_results_across_queries = 0

            # Iterate through all generated API-compliant queries
            for api_query in user_query.generate_everything_queries():
                logger.info(f"Searching NewsAPI /everything for: {api_query.q} (language: {api_query.language or 'all'})")

                # Paginate through results for this specific query
                current_page = 1
                query_articles = []

                while True:
                    # Update page number
                    api_query.page = current_page
                    params = api_query.to_api_params()

                    response = self.session.get(endpoint, params=params, timeout=30)
                    response.raise_for_status()

                    data = response.json()

                    if data.get('status') != 'ok':
                        logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                        if current_page == 1:
                            # First page failed, skip this query
                            break
                        else:
                            # Subsequent page failed, use what we have
                            logger.warning(f"Error on page {current_page}, stopping pagination for this query")
                            break

                    page_articles = data.get('articles', [])
                    query_articles.extend(page_articles)
                    query_total = data.get('totalResults', 0)

                    logger.info(f"Page {current_page}: retrieved {len(page_articles)} articles")

                    # Stop pagination if:
                    # 1. Fewer than pageSize results (no more pages)
                    # 2. Collected all available results for this query
                    # 3. Reached max_results limit across all queries
                    if (len(page_articles) < api_query.pageSize or
                        len(query_articles) >= query_total or
                        len(all_articles) + len(query_articles) >= user_query.max_results):
                        break

                    current_page += 1

                # Add results from this query to total
                all_articles.extend(query_articles)
                total_results_across_queries += len(query_articles)

                logger.info(f"Collected {len(query_articles)} articles from this query variant")

                # Stop if we've reached the max_results limit
                if len(all_articles) >= user_query.max_results:
                    logger.info(f"Reached max_results limit of {user_query.max_results}")
                    break

            # Remove duplicates based on URL
            unique_articles = {}
            for article in all_articles:
                url = article.get('url')
                if url and url not in unique_articles:
                    unique_articles[url] = article

            final_articles = list(unique_articles.values())

            # Truncate to max_results if needed
            if len(final_articles) > user_query.max_results:
                final_articles = final_articles[:user_query.max_results]
                logger.info(f"Truncated to max_results limit of {user_query.max_results}")

            logger.info(f"Total: {len(final_articles)} unique articles (removed {len(all_articles) - len(final_articles)} duplicates)")

            return {
                'status': 'ok',
                'totalResults': len(final_articles),
                'articles': final_articles
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching articles from NewsAPI: {e}")
            return {'status': 'error', 'totalResults': 0, 'articles': []}

    def search_top_headlines(self, user_query: UserQuery) -> Dict[str, Any]:
        """
        Get top headlines using the /top-headlines endpoint with automatic pagination.

        Args:
            user_query: UserQuery object with search parameters

        Returns:
            Dict containing 'status', 'totalResults', and 'articles'
        """
        endpoint = f"{self.BASE_URL}/top-headlines"

        try:
            all_articles = []

            # Iterate through all generated API-compliant queries
            for api_query in user_query.generate_headlines_queries():
                # Build descriptive log message
                query_desc = api_query.q or f"{api_query.country or 'all'}/{api_query.category or 'all'}"
                logger.info(f"Fetching top headlines: {query_desc}")

                # Paginate through results for this specific query
                current_page = 1
                query_articles = []

                while True:
                    # Update page number
                    api_query.page = current_page
                    params = api_query.to_api_params()

                    response = self.session.get(endpoint, params=params, timeout=30)
                    response.raise_for_status()

                    data = response.json()

                    if data.get('status') != 'ok':
                        logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                        if current_page == 1:
                            # First page failed, skip this query
                            break
                        else:
                            # Subsequent page failed, use what we have
                            logger.warning(f"Error on page {current_page}, stopping pagination for this query")
                            break

                    page_articles = data.get('articles', [])
                    query_articles.extend(page_articles)
                    query_total = data.get('totalResults', 0)

                    logger.info(f"Page {current_page}: retrieved {len(page_articles)} articles")

                    # Stop pagination if:
                    # 1. Fewer than pageSize results (no more pages)
                    # 2. Collected all available results for this query
                    # 3. Reached max_results limit across all queries
                    if (len(page_articles) < api_query.pageSize or
                        len(query_articles) >= query_total or
                        len(all_articles) + len(query_articles) >= user_query.max_results):
                        break

                    current_page += 1

                # Add results from this query to total
                all_articles.extend(query_articles)
                logger.info(f"Collected {len(query_articles)} articles from this query variant")

                # Stop if we've reached the max_results limit
                if len(all_articles) >= user_query.max_results:
                    logger.info(f"Reached max_results limit of {user_query.max_results}")
                    break

            # Remove duplicates based on URL
            unique_articles = {}
            for article in all_articles:
                url = article.get('url')
                if url and url not in unique_articles:
                    unique_articles[url] = article

            final_articles = list(unique_articles.values())

            # Truncate to max_results if needed
            if len(final_articles) > user_query.max_results:
                final_articles = final_articles[:user_query.max_results]
                logger.info(f"Truncated to max_results limit of {user_query.max_results}")

            logger.info(f"Total: {len(final_articles)} unique articles (removed {len(all_articles) - len(final_articles)} duplicates)")

            return {
                'status': 'ok',
                'totalResults': len(final_articles),
                'articles': final_articles
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching top headlines from NewsAPI: {e}")
            return {'status': 'error', 'totalResults': 0, 'articles': []}

    def get_sources(self, user_query: UserQuery) -> Dict[str, Any]:
        """
        Get available news sources using the /sources endpoint.

        Args:
            user_query: UserQuery object with filter parameters

        Returns:
            Dict containing 'status' and 'sources'
        """
        endpoint = f"{self.BASE_URL}/sources"

        try:
            all_sources = []

            # Iterate through all generated API-compliant queries
            for api_query in user_query.generate_sources_queries():
                # Build descriptive log message
                filters = []
                if api_query.category:
                    filters.append(f"category={api_query.category}")
                if api_query.language:
                    filters.append(f"language={api_query.language}")
                if api_query.country:
                    filters.append(f"country={api_query.country}")

                filter_str = ", ".join(filters) if filters else "all"
                logger.info(f"Fetching sources: {filter_str}")

                params = api_query.to_api_params()

                response = self.session.get(endpoint, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()

                if data.get('status') != 'ok':
                    logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                    continue  # Skip this query and try the next one

                sources = data.get('sources', [])
                all_sources.extend(sources)
                logger.info(f"Retrieved {len(sources)} sources")

            # Remove duplicates based on source ID
            unique_sources = {}
            for source in all_sources:
                source_id = source.get('id')
                if source_id and source_id not in unique_sources:
                    unique_sources[source_id] = source

            final_sources = list(unique_sources.values())

            logger.info(f"Total: {len(final_sources)} unique sources (removed {len(all_sources) - len(final_sources)} duplicates)")

            return {
                'status': 'ok',
                'sources': final_sources
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching sources from NewsAPI: {e}")
            return {'status': 'error', 'sources': []}

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
