"""Pydantic schemas for API requests and responses."""
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The question to ask Netra",
        examples=["What is the significance of the Om mantra?"],
    )


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str = Field(..., description="Netra's response")
    context_used: str = Field(
        default="",
        description="Snippet of scripture context used (truncated)",
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Source URLs of the context",
    )


class LearnRequest(BaseModel):
    """Request schema for learn/ingest endpoint."""

    url: HttpUrl = Field(
        ...,
        description="URL of the scripture page to ingest",
        examples=["https://sacred-texts.com/tantra/page.html"],
    )


class LearnResponse(BaseModel):
    """Response schema for learn/ingest endpoint."""

    status: str = Field(..., description="Status of the operation")
    message: str = Field(..., description="Human-readable message")
    chunks_added: int = Field(
        default=0,
        description="Number of text chunks added to knowledge base",
    )


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: str = Field(default="healthy", description="Health status")
    version: str = Field(..., description="API version")
    llm_provider: str = Field(..., description="Active LLM provider")


class StatsResponse(BaseModel):
    """Response schema for knowledge base statistics."""

    total_chunks: int = Field(..., description="Total chunks in knowledge base")
    total_sources: int = Field(..., description="Unique source URLs")
    collection_name: str = Field(..., description="ChromaDB collection name")


class ErrorResponse(BaseModel):
    """Generic error response schema."""

    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
