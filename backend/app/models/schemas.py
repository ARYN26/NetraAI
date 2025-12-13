"""Pydantic schemas for API requests and responses."""
from typing import List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, HttpUrl, Field, field_validator


# Allowed domains for URL ingestion (SSRF protection)
ALLOWED_URL_DOMAINS = [
    "sacred-texts.com",
    "wisdomlib.org",
    "archive.org",
    "hinduwebsite.com",
    "swamij.com",
    "yogananda.com.au",
    "sivanandaonline.org",
    "dlshq.org",
    "ramakrishnavivekananda.info",
    "estudantedavedanta.net",
    "sriaurobindoashram.org",
]


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

    @field_validator("url")
    @classmethod
    def validate_url_domain(cls, v):
        """
        Validate URL is from allowed domains (SSRF protection).

        Prevents attackers from using the /learn endpoint to:
        - Scan internal networks (localhost, 192.168.x.x, etc.)
        - Access cloud metadata endpoints (169.254.169.254)
        - Probe internal services
        """
        parsed = urlparse(str(v))
        hostname = parsed.netloc.lower()

        # Block private/internal addresses
        blocked_patterns = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "169.254.",  # AWS metadata
            "10.",  # Private network
            "192.168.",  # Private network
            "172.16.",  # Private network
        ]
        for pattern in blocked_patterns:
            if hostname.startswith(pattern) or pattern in hostname:
                raise ValueError(f"Internal URLs are not allowed: {hostname}")

        # Check against whitelist
        if not any(hostname.endswith(domain) for domain in ALLOWED_URL_DOMAINS):
            allowed_list = ", ".join(ALLOWED_URL_DOMAINS[:3]) + "..."
            raise ValueError(
                f"URL domain '{hostname}' not in allowed list. "
                f"Allowed domains include: {allowed_list}"
            )

        return v


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
