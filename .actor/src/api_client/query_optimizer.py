"""
LLM-powered query optimization for generating optimal search parameters

NOTE: This module is optional and primarily useful for programmatic/batch processing.
When using MCP servers, query optimization happens implicitly through the LLM.
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
from anthropic import Anthropic
from .models import UserQuery

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """LLM-powered query optimizer for news search"""

    OPTIMIZATION_PROMPT = """You are a news search expert. Your job is to transform user input into optimized search parameters for a news API.

User Input: {user_input}

Analyze the user's request and generate 1-5 search queries with optimal parameters. Each query should explore a different angle, perspective, or synonym for the topic.

Advanced search syntax is supported for the query string:
- Surround phrases with quotes (") for exact match
- Prepend words/phrases that must appear with + symbol. Eg: +bitcoin
- Prepend words that must not appear with - symbol. Eg: -bitcoin
- Use AND / OR / NOT keywords with optional parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin

Consider:
- What is the core topic or event?
- What are some alternative descriptions of the topic or event?

Optional Parameters (per query):
- searchIn: should results be in the title, description, content, or a combination of the three? Defaults to all
- sources: specific sources to include. Defaults to all.
- domains: specific web domains to include. Defaults to all.
- excludeDomains: specific web domains to exclude. Defaults to none.
- from_date: oldest article desired. Defaults to oldest allowed by plan.
- to_date: newest article desired. Defaults to newest allowed by plan.
- sortBy: publishedAt, relevancy, or popularity
- languages: ISO-639-1 codes: ar, de, en, es, fr, he, it, nl, no, pt, ru, sv, ud, zh
- countries: ISO 3166-1 alpha-2 codes
- categories: Options are: business, entertainment, general, health, science, sports, technology
- max_results: total number of results to request

Return a valid JSON object with an array of 1-5 queries. Each query should match this structure (all fields are optional except "q"):
{{
  "queries": [
    {{
      "q": "first optimized search query string",
      "searchIn": ["title", "description"],
      "sources": ["source name 1", "source name 2"],
      "domains": ["example.com"],
      "excludeDomains": ["exclude.com"],
      "from_date": "2025-01-01T00:00:00",
      "to_date": "2025-11-02T23:59:59",
      "sortBy": "publishedAt",
      "languages": ["en", "es"],
      "countries": ["us", "gb"],
      "categories": ["technology", "business"]
      "max_results": 100
    }},
    {{
      "q": "alternative angle on the same topic",
      "sortBy": "relevancy",
      "languages": ["en", "es"],
      "max_results": 100
    }},
    {{
      "q": "third perspective using synonyms",
      "categories": ["technology"],
      "sortBy": "popularity"
    }}
  ]
}}

Guidelines:
- Generate 1-5 queries exploring different angles of the user's request
- Only include optional fields if specifically mentioned or clearly relevant. Most fields will remain empty.
- Dates should be in ISO format (YYYY-MM-DDTHH:MM:SS)
- Each query can have different parameters based on what makes sense for that angle
- The "q" field is required for each query, all other fields are optional

Only return the JSON object, no other text."""

    def __init__(
        self,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        azure_endpoint: Optional[str] = None
    ):
        """
        Initialize the query optimizer.

        Args:
            provider: LLM provider ("anthropic" or "azure")
            api_key: API key for the provider
            model: Model name to use
            azure_endpoint: Azure OpenAI endpoint (for Azure provider)
        """
        self.provider = provider.lower()

        if self.provider == "anthropic":
            from ..config.settings import get_settings
            settings = get_settings()
            self.client = Anthropic(api_key=api_key or settings.anthropic_api_key)
            self.model = model or "claude-sonnet-4-5-20250929"
        elif self.provider == "azure":
            from ..config.settings import get_settings
            settings = get_settings()
            self.client = AzureOpenAI(
                api_key=api_key or settings.azure_openai_key,
                api_version=settings.azure_openai_api_version,
                azure_endpoint=azure_endpoint or settings.azure_openai_endpoint
            )
            self.model = model or settings.azure_openai_deployment_name
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def optimize_query(self, user_input: str) -> List[UserQuery]:
        """
        Transform user input into optimized search parameters.

        Args:
            user_input: Natural language user input

        Returns:
            List of UserQuery objects with optimized parameters
        """
        logger.info(f"Optimizing query: {user_input}")

        try:
            # Generate optimization using LLM
            prompt = self.OPTIMIZATION_PROMPT.format(user_input=user_input)
            response_text = self._call_llm(prompt)

            # Parse JSON response
            optimization = self._parse_response(response_text)

            # Convert to UserQuery objects
            user_queries = self._build_user_queries(optimization)

            logger.info(f"Generated {len(user_queries)} optimized queries")
            return user_queries

        except Exception as e:
            logger.error(f"Error optimizing query: {e}", exc_info=True)
            logger.warning(f"Falling back to basic query for input: {user_input[:100]}")
            # Fallback to basic query
            return self._fallback_queries(user_input)

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM provider"""
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response into structured data"""
        try:
            # Try to extract JSON from response
            # Handle cases where LLM might include markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            return json.loads(response_text)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Response text: {response_text}")
            raise

    def _build_user_queries(self, optimization: Dict[str, Any]) -> List[UserQuery]:
        """Build list of UserQuery objects from LLM JSON response"""

        # Extract queries array from LLM response
        queries_data = optimization.get('queries', [])

        user_queries = []

        for query_dict in queries_data:
            if not isinstance(query_dict, dict):
                continue

            # Extract query string (required)
            q = query_dict.get('q')
            if not q:
                logger.warning("Skipping query without 'q' field")
                continue

            # Parse dates if provided
            from_date = None
            to_date = None

            if 'from_date' in query_dict:
                try:
                    from_date = datetime.fromisoformat(query_dict['from_date'])
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid from_date format: {e}")

            if 'to_date' in query_dict:
                try:
                    to_date = datetime.fromisoformat(query_dict['to_date'])
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid to_date format: {e}")

            # Create UserQuery object
            # UserQuery validation will handle all the field validation
            user_query = UserQuery(
                q=q,
                searchIn=query_dict.get('searchIn'),
                sources=query_dict.get('sources'),
                domains=query_dict.get('domains'),
                excludeDomains=query_dict.get('excludeDomains'),
                from_date=from_date,
                to_date=to_date,
                sortBy=query_dict.get('sortBy'),
                languages=query_dict.get('languages'),
                countries=query_dict.get('countries'),
                categories=query_dict.get('categories'),
                pageSize=query_dict.get('pageSize', 100),
                max_results=query_dict.get('max_results', 100)
            )

            user_queries.append(user_query)

        return user_queries

    def _fallback_queries(self, user_input: str) -> List[UserQuery]:
        """Create a basic fallback query when LLM fails"""
        logger.warning(
            "Using fallback query - LLM optimization unavailable. "
            "This may be due to API key issues, rate limits, or service unavailability. "
            "Query will be less optimized."
        )

        # Return a simple UserQuery with just the user input as the query string
        return [UserQuery(q=user_input)]

    
