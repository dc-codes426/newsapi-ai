"""
Data models for news articles
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any, Iterator, Union
from enum import Enum
import hashlib
import logging
import validators
import itertools

logger = logging.getLogger(__name__)


# Validation Functions
def validate_query_string(q: str) -> str:
    """
    Validate and truncate query string if needed.

    Args:
        q: Query string to validate

    Returns:
        Validated/truncated query string
    """
    if len(q) > 500:
        logger.warning(f"Query truncated from {len(q)} to 500 characters")
        return q[:500]
    return q

def validate_searchIn(searchIn: Optional[List[str]]) -> Optional[List[str]]:
    if not searchIn:
        return None

    valid_fields = ['title','description','content']
    
    invalid_searchIns = [field for field in searchIn if field.lower() not in valid_fields]
    valid_searchIns = [field.lower() for field in searchIn if field.lower() in valid_fields]
    
    if invalid_searchIns:
        logger.warning(f"Invalid searchIn fields removed: {invalid_searchIns}. Allowed fields: {valid_fields}")

    if not valid_searchIns:
        logger.warning("No valid searchIn fields provided. Default is All")
        return None
    if set(valid_searchIns) == set(valid_fields):
        return None
    return valid_searchIns

def validate_domains(domains: List[str]) -> List[str]:
    if not domains:
        return None

    invalid_domains = [domain for domain in domains if not validators.domain(domain)]
    valid_domains = [domain for domain in domains if validators.domain(domain)]

    if invalid_domains:
        logger.warning(f"Invalid domains removed: {invalid_domains}")
    if not valid_domains:
        logger.warning(f"All domains invalid. Default is all available domains.")
    return valid_domains

def validate_sortBy(sortBy: str) -> str:
    if not sortBy:
        return None

    # Allowed fields are case-sensitive as per NewsAPI spec
    allowed_fields = ['relevancy', 'popularity', 'publishedAt']

    if sortBy not in allowed_fields:
        logger.warning(f"Invalid sortBy: {sortBy}. Allowed values: {allowed_fields}. Using default.")
        return None

    return sortBy

def validate_language_codes(language_codes: Optional[List[str]]) -> Optional[List[str]]:
    """
    Validate and filter ISO-639-1 language codes.

    Args:
        language_codes: List of language codes to validate

    Returns:
        List of valid language codes (lowercase), or None if all invalid or input is None
    """
    if not language_codes:
        return None

    allowed_langs = ['ar','de','en','es','fr','he','it','nl','no','pt','ru','sv','ud','zh']

    invalid_langs = [lang for lang in language_codes if lang.lower() not in allowed_langs]
    valid_langs = [lang.lower() for lang in language_codes if lang.lower() in allowed_langs]

    if invalid_langs:
        logger.warning(f"Invalid ISO-639-1 language codes removed: {invalid_langs}")

    if not valid_langs:
        logger.warning("All language codes were invalid, setting to Default:All")
        return None

    if set(valid_langs) == set(allowed_langs):
        return None
    return valid_langs


def validate_country_code(country_codes: Optional[List[str]]) -> Optional[List[str]]:
    """
    Validate and filter ISO 3166-1 alpha-2 country codes.

    Args:
        country_codes: List of country codes to validate

    Returns:
        List of valid country codes (lowercase), or None if all invalid or input is None
    """
    if not country_codes:
        return None

    # Valid country codes for NewsAPI
    valid_countries = [
        'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
        'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt',
        'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru',
        'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'
    ]

    invalid_codes = [code for code in country_codes if code.lower() not in valid_countries]
    valid_codes = [code.lower() for code in country_codes if code.lower() in valid_countries]

    if invalid_codes:
        logger.warning(f"Invalid country codes removed: {invalid_codes}. Must be ISO 3166-1 alpha-2 codes.")

    if not valid_codes:
        logger.warning("All country codes were invalid, setting to Default = All")
        return None

    if set(valid_codes) == set(valid_countries):
        return None

    return valid_codes

def validate_categories(categories: Optional[List[str]]) -> Optional[List[str]]:
    """
    Validate and filter NewsAPI category values.

    Args:
        categories: List of categories to validate

    Returns:
        List of valid categories (lowercase), or None if all invalid or input is None
    """
    if not categories:
        return None

    valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

    invalid_cats = [cat for cat in categories if cat.lower() not in valid_categories]
    valid_cats = [cat.lower() for cat in categories if cat.lower() in valid_categories]
    
    if invalid_cats:
        logger.warning(f"Invalid categories removed: {invalid_cats}. Allowed categories: {valid_categories}")

    if not valid_cats:
        logger.warning("All categories were invalid. Default is All")
        return None

    if set(valid_cats) == set(valid_categories):
        return None

    return valid_cats

# ============================================================================
# API-COMPLIANT QUERY CLASSES
# These classes are strict 1-to-1 mappings with NewsAPI endpoints
# ============================================================================

@dataclass
class EverythingQuery:
    """
    API-compliant query for NewsAPI /everything endpoint.
    All parameters strictly follow NewsAPI constraints.
    """
    q: str  # Required: search query (max 500 chars)
    searchIn: Optional[List[str]] = None  # title, description, content
    sources: Optional[List[str]] = None  # Max 20 sources
    domains: Optional[List[str]] = None
    excludeDomains: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    language: Optional[str] = None  # Single language code only
    sortBy: Optional[str] = None  # relevancy, popularity, publishedAt
    pageSize: Optional[int] = None  # Max 100
    page: Optional[int] = None

    def to_api_params(self) -> Dict[str, Any]:
        """Convert to NewsAPI query parameters."""
        params: Dict[str, Any] = {
            'q': self.q,
            'page': self.page if self.page else 1,
            'pageSize': min(self.pageSize, 100) if self.pageSize else 100
        }

        if self.searchIn:
            params['searchIn'] = ','.join(self.searchIn)

        if self.sources:
            params['sources'] = ','.join(self.sources[:20])  # Enforce max 20

        if self.domains:
            params['domains'] = ','.join(self.domains)

        if self.excludeDomains:
            params['excludeDomains'] = ','.join(self.excludeDomains)

        if self.from_date:
            params['from'] = self.from_date.strftime('%Y-%m-%d')

        if self.to_date:
            params['to'] = self.to_date.strftime('%Y-%m-%d')

        if self.language:
            params['language'] = self.language

        if self.sortBy:
            params['sortBy'] = self.sortBy

        return params

@dataclass
class TopHeadlinesQuery:
    """
    API-compliant query for NewsAPI /top-headlines endpoint.
    All parameters strictly follow NewsAPI constraints.
    """
    q: Optional[str] = None  # Optional: search query (max 500 chars)
    country: Optional[str] = None  # Single country code only
    category: Optional[str] = None  # Single category only
    sources: Optional[List[str]] = None  # Max 20 sources (cannot mix with country/category)
    pageSize: int = 100  # Max 100
    page: int = 1

    def to_api_params(self) -> Dict[str, Any]:
        """Convert to NewsAPI query parameters."""
        params: Dict[str, Any] = {
            'page': self.page,
            'pageSize': min(self.pageSize, 100)
        }

        if self.q:
            params['q'] = self.q

        if self.sources:
            params['sources'] = ','.join(self.sources[:20])  # Enforce max 20
        else:
            # Only add country/category if not using sources
            if self.country:
                params['country'] = self.country

            if self.category:
                params['category'] = self.category

        return params


@dataclass
class SourcesQuery:
    """
    API-compliant query for NewsAPI /sources endpoint.
    All parameters strictly follow NewsAPI constraints.
    """
    category: Optional[str] = None  # Single category only
    language: Optional[str] = None  # Single language code only
    country: Optional[str] = None  # Single country code only

    def to_api_params(self) -> Dict[str, Any]:
        """Convert to NewsAPI query parameters."""
        params: Dict[str, Any] = {}

        if self.category:
            params['category'] = self.category

        if self.language:
            params['language'] = self.language

        if self.country:
            params['country'] = self.country

        return params


# ============================================================================
# USER-FACING QUERY CLASS
# This class accepts flexible parameters and generates API-compliant queries
# ============================================================================

@dataclass
class UserQuery:
    """
    User-facing query class that can generate requests for all three NewsAPI endpoints.
    Accepts multiple values for languages, countries, categories, and unlimited sources.
    Automatically handles iteration and batching.
    """
    # Common parameters
    q: Optional[str] = None  # Search query

    # Everything endpoint parameters
    searchIn: Optional[List[str]] = None  # title, description, content
    sources: Optional[List[str]] = None  # Unlimited sources (will be chunked)
    domains: Optional[List[str]] = None
    excludeDomains: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    sortBy: Optional[str] = None  # relevancy, popularity, publishedAt

    # Multiple values supported (will iterate)
    languages: Optional[List[str]] = None  # Multiple languages
    countries: Optional[List[str]] = None  # Multiple countries
    categories: Optional[List[str]] = None  # Multiple categories

    # Pagination
    pageSize: int = 100
    max_results: int = 100  # Default limit on total results returned

    def __post_init__(self):
        """Validate and normalize user input"""
        # Validate query string if provided
        if self.q:
            self.q = validate_query_string(self.q)

        # Validate searchIn
        self.searchIn = validate_searchIn(self.searchIn)

        # Validate domains
        self.domains = validate_domains(self.domains)
        self.excludeDomains = validate_domains(self.excludeDomains)

        # Validate languages
        self.languages = validate_language_codes(self.languages)

        # Validate countries
        self.countries = validate_country_code(self.countries)

        # Validate categories
        self.categories = validate_categories(self.categories)

        # Validate sortBy
        self.sortBy = validate_sortBy(self.sortBy)

        # Convert date strings to datetime objects if needed
        if self.from_date and isinstance(self.from_date, str):
            self.from_date = datetime.fromisoformat(self.from_date.replace('Z', '+00:00'))

        if self.to_date and isinstance(self.to_date, str):
            self.to_date = datetime.fromisoformat(self.to_date.replace('Z', '+00:00'))

    def generate_everything_queries(self) -> Iterator[EverythingQuery]:
        """
        Generate EverythingQuery instances from user input.
        Handles chunking sources (max 20 per query) and iterating languages.
        """
        if not self.q:
            raise ValueError("Query 'q' is required for /everything endpoint")

        # Determine languages to iterate (default to None for API default)
        langs = self.languages if self.languages else [None]

        # Chunk sources into groups of 20
        if self.sources:
            source_chunks = [self.sources[i:i+20] for i in range(0, len(self.sources), 20)]
        else:
            source_chunks = [None]

        # Generate queries for each combination of language and source chunk
        for lang in langs:
            for source_chunk in source_chunks:
                yield EverythingQuery(
                    q=self.q,
                    searchIn=self.searchIn,
                    sources=source_chunk,
                    domains=self.domains,
                    excludeDomains=self.excludeDomains,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    language=lang,
                    sortBy=self.sortBy,
                    pageSize=self.pageSize,
                    page=1
                )

    def generate_headlines_queries(self) -> Iterator[TopHeadlinesQuery]:
        """
        Generate TopHeadlinesQuery instances from user input.
        Handles iterating countries/categories and chunking sources.
        """
        # If sources provided, chunk them and don't use country/category
        if self.sources:
            source_chunks = [self.sources[i:i+20] for i in range(0, len(self.sources), 20)]
            for source_chunk in source_chunks:
                yield TopHeadlinesQuery(
                    q=self.q,
                    sources=source_chunk,
                    pageSize=self.pageSize,
                    page=1
                )
        else:
            # Iterate through countries and categories
            countries = self.countries if self.countries else [None]
            categories = self.categories if self.categories else [None]

            for country in countries:
                for category in categories:
                    # Skip if both are None (need at least one parameter)
                    if country is None and category is None and self.q is None:
                        continue

                    yield TopHeadlinesQuery(
                        q=self.q,
                        country=country,
                        category=category,
                        pageSize=self.pageSize,
                        page=1
                    )

    def generate_sources_queries(self) -> Iterator[SourcesQuery]:
        """
        Generate SourcesQuery instances from user input.
        Iterates through all combinations of category, language, and country.
        """
        # Get all combinations
        categories = self.categories if self.categories else [None]
        languages = self.languages if self.languages else [None]
        countries = self.countries if self.countries else [None]

        for category, language, country in itertools.product(categories, languages, countries):
            if category is None and language is None and country is None:
                yield SourcesQuery()  # Get all sources
            else:
                yield SourcesQuery(
                    category=category,
                    language=language,
                    country=country
                )
@dataclass
class Source:
    id: str
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None

@dataclass
class Article:
    """Represents a news article"""

    # From NewsAPI
    title: str
    url: str
    source: Optional[Source] = None
    author: Optional[str] = None
    description: Optional[str] = None
    url_to_image: Optional[str] = None
    published_at: Optional[str] = None
    content: Optional[str] = None  # NewsAPI content snippet

    def __post_init__(self):
        # Convert string dates to datetime if needed
        if isinstance(self.published_at, str):
            self.published_at = datetime.fromisoformat(self.published_at)

    @classmethod
    def from_newsapi(cls, api_data: Dict[str, Any]) -> 'Article':
        """
        Create an Article from NewsAPI response data.

        Args:
            api_data: Article data from NewsAPI

        Returns:
            Article instance
        """
        source_data = api_data.get('source', {})
        source = None
        if source_data:
            source = Source(
                id=source_data.get('id', ''),
                name=source_data.get('name', ''),
                description=None,
                url=None,
                category=None,
                language=None,
                country=None
            )

        return cls(
            source=source,
            author=api_data.get('author'),
            title=api_data.get('title', ''),
            description=api_data.get('description'),
            url=api_data.get('url', ''),
            url_to_image=api_data.get('urlToImage'),
            published_at=api_data.get('publishedAt'),
            content=api_data.get('content')
        )

    def __repr__(self) -> str:
        return f"Article(title='{self.title[:50]}...', url='{self.url}')"


@dataclass
class SearchResult:
    """Represents the result of a news search"""

    query: UserQuery
    total_found: int = 0
    articles: List[Article] = field(default_factory=list)
    search_date: datetime = field(default_factory=datetime.utcnow)

    def add_article(self, article: Article) -> None:
        """Add an article to the results"""
        self.articles.append(article)
        self.total_found = len(self.articles)

