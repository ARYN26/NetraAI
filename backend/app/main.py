"""
NetraAI - Tantric AI Knowledge System
FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi.errors import RateLimitExceeded
import sys

from app.config import settings
from app.services.rate_limiter import limiter
from app.api.routes import router
from app.api.auth import router as auth_router


from app.services.audit_logger import audit


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors."""
    client_ip = request.client.host if request.client else "unknown"
    audit.log_rate_limit(str(request.url.path), client_ip)
    logger.warning(f"Rate limit exceeded for IP: {client_ip}")
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "You are sending too many requests. Please slow down.",
            "retry_after": exc.detail,
        },
    )


# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)


def auto_seed_if_empty():
    """Check if knowledge base is empty and seed scriptures if needed."""
    try:
        from app.services.knowledge_base import KnowledgeBase
        from scripts.seed_scriptures import seed_scriptures

        kb = KnowledgeBase()
        if kb.is_empty():
            logger.info("Knowledge base is empty - seeding scriptures...")
            files, chunks = seed_scriptures(force=False)
            logger.success(f"Auto-seeded {chunks} chunks from {files} scripture files")
        else:
            logger.info(f"Knowledge base already has {kb.collection.count()} chunks")
    except Exception as e:
        logger.warning(f"Auto-seed failed (non-critical): {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Netra API...")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"ChromaDB Path: {settings.chroma_db_path}")

    # Auto-seed scriptures if knowledge base is empty
    auto_seed_if_empty()

    yield

    # Shutdown
    logger.info("Shutting down Netra API...")


# Create FastAPI application
app = FastAPI(
    title="Netra API",
    description="Tantric AI Knowledge System - Access scriptural wisdom through conversation",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS (tightened for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicit methods only
    allow_headers=["Content-Type", "Authorization"],  # Explicit headers only
    max_age=3600,  # Cache preflight for 1 hour
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

# Configure rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Include API routes
app.include_router(router)
app.include_router(auth_router)


@app.get("/")
async def root():
    """Root endpoint with welcome message."""
    return {
        "message": "Namaste. Welcome to Netra API.",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
