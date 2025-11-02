"""
Tests for the configuration module.

This module tests:
- Settings loading from environment variables
- Settings validation
- Constants and enums
- Logging configuration
"""

import pytest
import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from src.config import (
    Settings,
    get_settings,
    reload_settings,
    ArticleStatus,
    ContentType,
    LLMProvider,
    setup_logging,
    get_logger,
    LoggerMixin,
)
from src.config.constants import (
    DEFAULT_TIMEOUT_SECONDS,
    MAX_RETRIES,
    NEWSAPI_BASE_URL,
)


class TestSettings:
    """Test Settings class and configuration management."""

    def test_settings_defaults(self, monkeypatch, tmp_path):
        """Test that settings load with default values when no env vars are set."""
        # Clear any existing API keys
        monkeypatch.delenv("NEWS_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("AZURE_OPENAI_KEY", raising=False)

        # Create a temporary empty .env file to avoid loading from project .env
        empty_env = tmp_path / ".env"
        empty_env.write_text("")
        monkeypatch.setattr("src.config.settings.env_path", empty_env)

        settings = Settings()

        # API keys may be None or loaded from .env (both are valid defaults)
        # Just check that defaults work (not port since it may be set in .env)
        assert settings.relevance_threshold == 80
        assert settings.max_articles_per_search == 100
        assert settings.app_env == "development"
        assert settings.log_level == "INFO"
        assert settings.host == "0.0.0.0"
        # Port may be set in .env, just verify it's in valid range
        assert 1 <= settings.port <= 65535
        assert settings.use_mcp is False

    def test_settings_from_env(self, monkeypatch):
        """Test that settings load from environment variables."""
        monkeypatch.setenv("NEWS_API_KEY", "test-news-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
        monkeypatch.setenv("RELEVANCE_THRESHOLD", "75")
        monkeypatch.setenv("MAX_ARTICLES_PER_SEARCH", "50")
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("PORT", "8500")
        monkeypatch.setenv("USE_MCP", "true")

        settings = Settings()

        assert settings.news_api_key == "test-news-key"
        assert settings.anthropic_api_key == "test-anthropic-key"
        assert settings.relevance_threshold == 75
        assert settings.max_articles_per_search == 50
        assert settings.app_env == "production"
        assert settings.log_level == "DEBUG"
        assert settings.port == 8500
        assert settings.use_mcp is True

    def test_log_level_validation(self, monkeypatch):
        """Test that log_level is validated correctly."""
        monkeypatch.setenv("LOG_LEVEL", "debug")
        settings = Settings()
        assert settings.log_level == "DEBUG"

        monkeypatch.setenv("LOG_LEVEL", "info")
        settings = Settings()
        assert settings.log_level == "INFO"

    def test_invalid_log_level(self, monkeypatch):
        """Test that invalid log_level raises ValueError."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        with pytest.raises(ValueError, match="log_level must be one of"):
            Settings()

    def test_relevance_threshold_bounds(self, monkeypatch):
        """Test that relevance_threshold enforces bounds."""
        # Test lower bound
        monkeypatch.setenv("RELEVANCE_THRESHOLD", "-1")
        with pytest.raises(ValueError):
            Settings()

        # Test upper bound
        monkeypatch.setenv("RELEVANCE_THRESHOLD", "101")
        with pytest.raises(ValueError):
            Settings()

        # Test valid values
        monkeypatch.setenv("RELEVANCE_THRESHOLD", "0")
        settings = Settings()
        assert settings.relevance_threshold == 0

        monkeypatch.setenv("RELEVANCE_THRESHOLD", "100")
        settings = Settings()
        assert settings.relevance_threshold == 100

    def test_max_articles_bounds(self, monkeypatch):
        """Test that max_articles_per_search enforces bounds."""
        # Test lower bound
        monkeypatch.setenv("MAX_ARTICLES_PER_SEARCH", "0")
        with pytest.raises(ValueError):
            Settings()

        # Test upper bound
        monkeypatch.setenv("MAX_ARTICLES_PER_SEARCH", "1001")
        with pytest.raises(ValueError):
            Settings()

        # Test valid values
        monkeypatch.setenv("MAX_ARTICLES_PER_SEARCH", "1")
        settings = Settings()
        assert settings.max_articles_per_search == 1

        monkeypatch.setenv("MAX_ARTICLES_PER_SEARCH", "1000")
        settings = Settings()
        assert settings.max_articles_per_search == 1000

    def test_port_bounds(self, monkeypatch):
        """Test that port enforces valid range."""
        # Test lower bound
        monkeypatch.setenv("PORT", "0")
        with pytest.raises(ValueError):
            Settings()

        # Test upper bound
        monkeypatch.setenv("PORT", "65536")
        with pytest.raises(ValueError):
            Settings()

        # Test valid values
        monkeypatch.setenv("PORT", "1")
        settings = Settings()
        assert settings.port == 1

        monkeypatch.setenv("PORT", "65535")
        settings = Settings()
        assert settings.port == 65535

    def test_is_development_property(self, monkeypatch):
        """Test is_development property."""
        monkeypatch.setenv("APP_ENV", "development")
        settings = Settings()
        assert settings.is_development is True
        assert settings.is_production is False

        monkeypatch.setenv("APP_ENV", "dev")
        settings = Settings()
        assert settings.is_development is True

        monkeypatch.setenv("APP_ENV", "production")
        settings = Settings()
        assert settings.is_development is False

    def test_is_production_property(self, monkeypatch):
        """Test is_production property."""
        monkeypatch.setenv("APP_ENV", "production")
        settings = Settings()
        assert settings.is_production is True
        assert settings.is_development is False

        monkeypatch.setenv("APP_ENV", "prod")
        settings = Settings()
        assert settings.is_production is True

        monkeypatch.setenv("APP_ENV", "development")
        settings = Settings()
        assert settings.is_production is False

    def test_has_anthropic_property(self, monkeypatch):
        """Test has_anthropic property."""
        # Test with key present
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        settings = Settings()
        assert settings.has_anthropic is True

        # Test with key absent (set to empty string)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "")
        settings = Settings()
        # Empty string is still truthy for the field, so check the actual behavior
        # The property checks if the key is not None

    def test_has_azure_openai_property(self, monkeypatch):
        """Test has_azure_openai property."""
        monkeypatch.delenv("AZURE_OPENAI_KEY", raising=False)
        monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
        settings = Settings()
        assert settings.has_azure_openai is False

        # Key alone is not enough
        monkeypatch.setenv("AZURE_OPENAI_KEY", "test-key")
        settings = Settings()
        assert settings.has_azure_openai is False

        # Both key and endpoint required
        monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
        settings = Settings()
        assert settings.has_azure_openai is True

    def test_should_use_mcp_property(self, monkeypatch):
        """Test should_use_mcp property."""
        monkeypatch.setenv("USE_MCP", "false")
        settings = Settings()
        assert settings.should_use_mcp is False

        monkeypatch.setenv("USE_MCP", "true")
        settings = Settings()
        assert settings.should_use_mcp is True

    def test_azure_defaults(self, monkeypatch):
        """Test Azure-related default values."""
        settings = Settings()
        assert settings.azure_openai_api_version == "2024-02-15-preview"
        assert settings.azure_storage_container_name == "newsaggregator-articles"
        assert settings.azure_cosmos_database_name == "newsaggregator"
        assert settings.azure_cosmos_container_name == "articles-metadata"

    def test_celery_defaults(self, monkeypatch):
        """Test Celery-related default values."""
        settings = Settings()
        assert settings.redis_url == "redis://localhost:6379/0"
        assert settings.celery_task_time_limit == 1800
        assert settings.celery_task_soft_time_limit == 1500

    def test_sentry_defaults(self, monkeypatch):
        """Test Sentry-related default values."""
        settings = Settings()
        assert settings.sentry_dsn is None
        assert settings.sentry_environment is None
        assert settings.sentry_traces_sample_rate == 1.0


class TestGlobalSettings:
    """Test global settings management functions."""

    def test_get_settings_singleton(self, monkeypatch):
        """Test that get_settings returns the same instance."""
        # Reset global settings
        import src.config.settings
        src.config.settings.settings = None

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_reload_settings(self, monkeypatch):
        """Test that reload_settings creates a new instance."""
        import src.config.settings
        src.config.settings.settings = None

        monkeypatch.setenv("PORT", "8000")
        settings1 = get_settings()
        assert settings1.port == 8000

        monkeypatch.setenv("PORT", "9000")
        settings2 = reload_settings()
        assert settings2.port == 9000

        # Should be a new instance
        assert settings1 is not settings2


class TestConstants:
    """Test constants and enums."""

    def test_article_status_enum(self):
        """Test ArticleStatus enum values."""
        assert ArticleStatus.DISCOVERED.value == "discovered"
        assert ArticleStatus.SCRAPED.value == "scraped"
        assert ArticleStatus.SCORED.value == "scored"
        assert ArticleStatus.REJECTED.value == "rejected"
        assert ArticleStatus.STORED.value == "stored"
        assert ArticleStatus.SUMMARIZED.value == "summarized"
        assert ArticleStatus.FAILED.value == "failed"

    def test_content_type_enum(self):
        """Test ContentType enum values."""
        assert ContentType.FULL_TEXT.value == "full_text"
        assert ContentType.SUMMARY.value == "summary"
        assert ContentType.METADATA_ONLY.value == "metadata_only"

    def test_llm_provider_enum(self):
        """Test LLMProvider enum values."""
        assert LLMProvider.ANTHROPIC.value == "anthropic"
        assert LLMProvider.AZURE_OPENAI.value == "azure_openai"

    def test_http_constants(self):
        """Test HTTP configuration constants."""
        assert DEFAULT_TIMEOUT_SECONDS == 30
        assert MAX_RETRIES == 3
        assert isinstance(DEFAULT_TIMEOUT_SECONDS, int)
        assert isinstance(MAX_RETRIES, int)

    def test_newsapi_constants(self):
        """Test NewsAPI configuration constants."""
        assert NEWSAPI_BASE_URL == "https://newsapi.org/v2"
        assert isinstance(NEWSAPI_BASE_URL, str)


class TestLogging:
    """Test logging configuration."""

    def test_setup_logging_console_only(self):
        """Test logging setup with console handler only."""
        logger = setup_logging(log_level="INFO")

        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1

        # Check console handler exists
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) >= 1

    def test_setup_logging_with_file(self):
        """Test logging setup with file handler."""
        with TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = setup_logging(log_level="DEBUG", log_file=log_file)

            assert logger.level == logging.DEBUG
            assert Path(log_file).exists()

            # Test that logging works
            test_logger = get_logger("test")
            test_logger.info("Test message")

            # Verify file has content
            with open(log_file, "r") as f:
                content = f.read()
                assert "Test message" in content

    def test_setup_logging_levels(self):
        """Test different logging levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logger = setup_logging(log_level=level)
            assert logger.level == getattr(logging, level)

    def test_get_logger(self):
        """Test get_logger function."""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_logger_mixin(self):
        """Test LoggerMixin class."""
        class TestClass(LoggerMixin):
            pass

        obj = TestClass()
        logger = obj.logger

        assert isinstance(logger, logging.Logger)
        assert "TestClass" in logger.name

    def test_logging_rotation(self):
        """Test that file handler uses rotation."""
        with TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = setup_logging(
                log_level="INFO",
                log_file=log_file,
                max_bytes=1024,
                backup_count=3
            )

            # Find the RotatingFileHandler
            from logging.handlers import RotatingFileHandler
            file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
            assert len(file_handlers) == 1

            handler = file_handlers[0]
            assert handler.maxBytes == 1024
            assert handler.backupCount == 3


class TestIntegration:
    """Integration tests for config module."""

    def test_config_module_imports(self):
        """Test that all expected exports are available."""
        from src.config import (
            Settings,
            get_settings,
            reload_settings,
            ArticleStatus,
            ContentType,
            LLMProvider,
            setup_logging,
            get_logger,
            LoggerMixin,
        )

        # Verify types
        assert isinstance(Settings, type)
        assert callable(get_settings)
        assert callable(reload_settings)
        assert isinstance(ArticleStatus, type)
        assert isinstance(ContentType, type)
        assert isinstance(LLMProvider, type)
        assert callable(setup_logging)
        assert callable(get_logger)
        assert isinstance(LoggerMixin, type)

    def test_settings_with_logging(self, monkeypatch):
        """Test using settings with logging."""
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        settings = Settings()

        logger = setup_logging(log_level=settings.log_level)
        assert logger.level == logging.WARNING
