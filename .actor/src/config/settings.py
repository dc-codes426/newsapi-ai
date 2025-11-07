"""
Application settings and configuration management.

Loads configuration from environment variables using pydantic-settings.
"""

from typing import Optional
from pathlib import Path
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Determine environment file path
env_path = Path(__file__).parent.parent.parent / '.env'

# Build settings config based on environment
if env_path.exists():
    # Local development - use .env file without overriding shell env vars
    load_dotenv(dotenv_path=env_path, override=False)
    settings_config = SettingsConfigDict(
        env_file=str(env_path),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
else:
    # Production (Azure) - only use environment variables
    settings_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore"
    )


class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = settings_config

    # News API Configuration
    news_api_key: Optional[str] = Field(None, description="NewsAPI key for fetching articles")

    # Additional News APIs (for MCP failover)
    the_news_api_key: Optional[str] = Field(None, description="TheNewsAPI key (optional)")
    news_data_api_key: Optional[str] = Field(None, description="NewsData.io API key (optional)")
    gnews_api_key: Optional[str] = Field(None, description="GNews API key (optional)")

    # MCP Configuration
    use_mcp: bool = Field(
        default=False,
        description="Use MCP servers for news aggregation (True) or direct API clients (False)"
    )

    # LLM API Configuration
    anthropic_api_key: Optional[str] = Field(None, description="Anthropic Claude API key")
    azure_openai_key: Optional[str] = Field(None, description="Azure OpenAI API key")
    azure_openai_endpoint: Optional[str] = Field(None, description="Azure OpenAI endpoint URL")
    azure_openai_api_version: str = Field(
        default="2024-02-15-preview",
        description="Azure OpenAI API version"
    )
    azure_openai_deployment_name: Optional[str] = Field(
        None,
        description="Azure OpenAI deployment/model name"
    )

    # Azure Storage Configuration
    azure_storage_connection_string: Optional[str] = Field(None, description="Azure Storage connection string")
    azure_storage_account_name: Optional[str] = Field(None, description="Azure Storage account name")
    azure_storage_container_name: str = Field(
        default="newsaggregator-articles",
        description="Azure Blob container name"
    )

    # Azure Cosmos DB Configuration
    azure_cosmos_connection_string: Optional[str] = Field(None, description="Azure Cosmos DB connection string")
    azure_cosmos_database_name: str = Field(
        default="newsaggregator",
        description="Cosmos DB database name"
    )
    azure_cosmos_container_name: str = Field(
        default="articles-metadata",
        description="Cosmos DB container name"
    )

    # Azure AD B2C Configuration (Optional for auth)
    azure_ad_b2c_tenant_name: Optional[str] = Field(None, description="Azure AD B2C tenant name")
    azure_ad_b2c_client_id: Optional[str] = Field(None, description="Azure AD B2C client ID")
    azure_ad_b2c_client_secret: Optional[str] = Field(None, description="Azure AD B2C client secret")

    # Application Configuration
    relevance_threshold: int = Field(
        default=80,
        ge=0,
        le=100,
        description="Minimum relevance score (0-100) for article inclusion"
    )
    max_articles_per_search: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of articles to fetch per search"
    )
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")

    # Web Application Settings
    host: str = Field(default="0.0.0.0", description="Host to bind the web server")
    port: int = Field(default=8000, ge=1, le=65535, description="Port to bind the web server")

    # Redis and Celery Configuration
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis URL for Celery broker and result backend"
    )
    celery_task_time_limit: int = Field(
        default=1800,
        description="Celery task time limit in seconds (default: 30 minutes)"
    )
    celery_task_soft_time_limit: int = Field(
        default=1500,
        description="Celery task soft time limit in seconds (default: 25 minutes)"
    )

    # Error Monitoring Configuration
    sentry_dsn: Optional[str] = Field(None, description="Sentry DSN for error monitoring")
    sentry_environment: Optional[str] = Field(None, description="Sentry environment (e.g., production, development)")
    sentry_traces_sample_rate: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Sentry traces sample rate for performance monitoring (0.0 to 1.0)"
    )

    @validator("log_level")
    def validate_log_level(cls, v):
        """Ensure log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v_upper

    @validator("azure_openai_key", "anthropic_api_key")
    def validate_llm_config(cls, v, values):
        """Ensure at least one LLM API key is provided."""
        # This validator runs for each field, so we check if ANY is set
        if not v and "anthropic_api_key" not in values and "azure_openai_key" not in values:
            return v
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env.lower() in ["development", "dev"]

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env.lower() in ["production", "prod"]

    @property
    def has_anthropic(self) -> bool:
        """Check if Anthropic API is configured."""
        return self.anthropic_api_key is not None

    @property
    def has_azure_openai(self) -> bool:
        """Check if Azure OpenAI is configured."""
        return self.azure_openai_key is not None and self.azure_openai_endpoint is not None

    @property
    def should_use_mcp(self) -> bool:
        """Check if MCP should be used (based on USE_MCP setting and development mode)."""
        return self.use_mcp


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create the global settings instance.

    Returns:
        Settings: The application settings
    """
    global settings
    if settings is None:
        settings = Settings()
    return settings


def reload_settings() -> Settings:
    """
    Reload settings from environment (useful for testing).

    Returns:
        Settings: The newly loaded settings
    """
    global settings
    settings = Settings()
    return settings
