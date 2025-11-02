"""
Application-wide constants and enums.
"""

from enum import Enum


class ArticleStatus(Enum):
    """Status of an article in the system."""
    DISCOVERED = "discovered"
    SCRAPED = "scraped"
    SCORED = "scored"
    REJECTED = "rejected"
    STORED = "stored"
    SUMMARIZED = "summarized"
    FAILED = "failed"


class ContentType(Enum):
    """Type of content storage."""
    FULL_TEXT = "full_text"
    SUMMARY = "summary"
    METADATA_ONLY = "metadata_only"


class LLMProvider(Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"


# HTTP Configuration
DEFAULT_TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2

# NewsAPI Configuration
NEWSAPI_BASE_URL = "https://newsapi.org/v2"
NEWSAPI_PAGE_SIZE = 100
NEWSAPI_MAX_PAGES = 5

# Content Processing
SUMMARY_MAX_LENGTH = 500  # words
SUMMARY_MIN_LENGTH = 50  # words

# Storage Configuration
BLOB_CONTENT_TYPE = "text/html"
METADATA_CONTENT_TYPE = "application/json"

# Rate Limiting
NEWSAPI_REQUESTS_PER_MINUTE = 5
SCRAPING_REQUESTS_PER_SECOND = 1

# Cache TTL (seconds)
ARTICLE_CACHE_TTL = 3600  # 1 hour
METADATA_CACHE_TTL = 300  # 5 minutes

# Batch Processing
DEFAULT_BATCH_SIZE = 10
MAX_BATCH_SIZE = 50

# Error Messages
ERROR_NO_LLM_CONFIGURED = "No LLM provider configured. Please set ANTHROPIC_API_KEY or AZURE_OPENAI_KEY."
ERROR_INVALID_API_KEY = "Invalid API key provided."
ERROR_RATE_LIMIT_EXCEEDED = "Rate limit exceeded. Please try again later."
ERROR_ARTICLE_NOT_FOUND = "Article not found."
ERROR_STORAGE_FAILED = "Failed to store article."
ERROR_SCRAPING_FAILED = "Failed to scrape article content."

# Success Messages
SUCCESS_ARTICLE_STORED = "Article successfully stored."
SUCCESS_ARTICLE_SCORED = "Article successfully scored."
SUCCESS_SEARCH_COMPLETED = "Search completed successfully."


