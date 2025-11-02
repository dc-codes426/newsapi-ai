"""
API request and response models.

Defines Pydantic models for the REST API endpoints.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for the query endpoint."""

    query: str = Field(
        ...,
        description="Natural language query for news search",
        min_length=1,
        example="Find me the latest news about artificial intelligence"
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID to maintain conversation context"
    )
    response_format: Literal["natural", "structured", "both"] = Field(
        default="both",
        description="Desired response format: 'natural' (text only), 'structured' (data only), or 'both'"
    )


class Article(BaseModel):
    """Article information extracted from tool results."""

    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    source: Optional[Dict[str, Any]] = None
    publishedAt: Optional[str] = None
    author: Optional[str] = None
    urlToImage: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for the query endpoint."""

    response: Optional[str] = Field(
        None,
        description="Natural language response from the AI agent"
    )
    articles: Optional[List[Article]] = Field(
        None,
        description="Structured article data if available"
    )
    total_results: Optional[int] = Field(
        None,
        description="Total number of results found"
    )
    session_id: Optional[str] = Field(
        None,
        description="Session ID for maintaining conversation context"
    )
    format: Literal["natural", "structured", "both"] = Field(
        default="both",
        description="Format of the response"
    )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(default="ok")
    version: str = Field(default="1.0.0")
    services: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of dependent services"
    )


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
