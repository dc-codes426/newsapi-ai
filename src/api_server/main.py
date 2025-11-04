"""
FastAPI server for AI-powered news search.

This module provides a REST API endpoint that accepts natural language queries
and returns intelligent news search results using Claude AI.
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from anthropic import Anthropic
from pathlib import Path

from .models import QueryRequest, QueryResponse, HealthResponse, ErrorResponse, Article
from ..config import get_settings, setup_logging
from ..api_client import NewsAPIClient
from ..intent.news_agent import NewsAgent

# Setup logging
settings = get_settings()
setup_logging(log_level=settings.log_level, log_file="logs/api_server.log")
logger = logging.getLogger(__name__)


# Global clients (initialized in lifespan)
anthropic_client: Optional[Anthropic] = None
news_client: Optional[NewsAPIClient] = None
news_agent: Optional[NewsAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global anthropic_client, news_client, news_agent

    # Startup
    logger.info("Starting API server...")

    try:
        # Initialize clients
        if not settings.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY not set - agent functionality will be limited")
        else:
            anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Anthropic client initialized")

        if not settings.news_api_key:
            logger.warning("NEWS_API_KEY not set - news search will not work")
        else:
            news_client = NewsAPIClient(api_key=settings.news_api_key)
            logger.info("NewsAPI client initialized")

        # Initialize agent if both clients are available
        if anthropic_client and news_client:
            news_agent = NewsAgent(anthropic_client, news_client)
            logger.info("NewsAgent initialized")
        else:
            logger.warning("NewsAgent not initialized - missing API keys")

        logger.info(f"API server started on {settings.host}:{settings.port}")

    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("Shutting down API server...")
    if news_client:
        news_client.close()


# Create FastAPI app
app = FastAPI(
    title="NewsAPI AI",
    description="AI-powered news search using Claude AI and NewsAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from web/dist directory
static_dir = Path(__file__).parent.parent.parent / "web" / "dist"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")
    logger.info(f"Serving static assets from {static_dir / 'assets'}")


@app.get("/", include_in_schema=False)
async def serve_root():
    """Serve the React app root."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Frontend not built")


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    services = {
        "anthropic": "ok" if anthropic_client else "not_configured",
        "newsapi": "ok" if news_client else "not_configured",
        "agent": "ok" if news_agent else "not_configured"
    }

    return HealthResponse(
        status="ok",
        version="1.0.0",
        services=services
    )


@app.post("/query", response_model=QueryResponse, tags=["Search"])
async def query_news(request: QueryRequest):
    """
    Process a natural language news query using AI.

    The AI agent will:
    1. Understand your query
    2. Decide which tools to use (search news, get headlines, etc.)
    3. Execute the searches
    4. Return results in the requested format

    Args:
        request: Query request with natural language query and optional parameters

    Returns:
        QueryResponse with AI response and/or structured article data

    Raises:
        HTTPException: If agent is not configured or query processing fails
    """
    if not news_agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="News agent not configured. Please check API keys."
        )

    try:
        logger.info(f"Processing query: {request.query[:100]}...")

        # Generate session_id if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Process the request through the agent
        result = news_agent.process_request(
            user_prompt=request.query,
            session_id=session_id
        )

        # Extract natural language response
        natural_response = result.get("response", "")

        # Try to extract structured data from conversation messages
        articles_data = _extract_articles_from_messages(result.get("messages", []))

        # Build response based on requested format
        response = QueryResponse(
            session_id=session_id,  # Return the session_id (generated or provided)
            format=request.response_format
        )

        if request.response_format in ["natural", "both"]:
            response.response = natural_response

        if request.response_format in ["structured", "both"] and articles_data:
            response.articles = articles_data["articles"]
            response.total_results = articles_data.get("total_results")

        logger.info(f"Query processed successfully. Format: {request.response_format}")
        return response

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


def _extract_articles_from_messages(messages: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Extract article data from conversation messages.

    Looks for tool results in the conversation that contain article data.

    Args:
        messages: List of conversation messages

    Returns:
        Dictionary with articles and total_results, or None if no articles found
    """
    articles = []
    total_results = 0

    for message in messages:
        if message.get("role") != "user":
            continue

        content = message.get("content", [])
        if not isinstance(content, list):
            continue

        for item in content:
            if not isinstance(item, dict) or item.get("type") != "tool_result":
                continue

            # Parse the tool result content
            import json
            try:
                tool_content = item.get("content", "")
                if isinstance(tool_content, str):
                    tool_data = json.loads(tool_content)
                else:
                    tool_data = tool_content

                # Check if this result contains articles
                if "articles" in tool_data:
                    articles.extend(tool_data["articles"])
                    total_results = max(total_results, tool_data.get("total_results", 0))

            except (json.JSONDecodeError, Exception) as e:
                logger.debug(f"Could not parse tool result: {e}")
                continue

    if articles:
        # Convert to Article models
        article_models = [Article(**article) for article in articles]
        return {
            "articles": article_models,
            "total_results": total_results
        }

    return None


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ).dict()
    )


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Serve the React SPA for all non-API routes.
    This allows client-side routing to work properly.
    """
    # Skip if it's an API route
    if full_path.startswith(("query", "health", "docs", "openapi.json", "redoc")):
        raise HTTPException(status_code=404, detail="Not found")

    # Serve index.html for SPA routing
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    raise HTTPException(status_code=404, detail="Frontend not built")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api_server.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
        log_level=settings.log_level.lower()
    )
