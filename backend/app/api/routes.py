"""API route handlers for Netra."""
from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger

from app import __version__
from app.config import settings
from app.services.rate_limiter import limiter
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    StatsResponse,
)
from app.models.user import UserInDB
from app.services.ai_brain import AIBrain
from app.services.cache import ResponseCache
from app.services.knowledge_base import KnowledgeBase
from app.services.auth_service import get_current_active_user

router = APIRouter()

# Initialize services (lazy loading)
_knowledge_base = None
_ai_brain = None
_response_cache = None


def get_response_cache() -> ResponseCache:
    """Get or create ResponseCache instance."""
    global _response_cache
    if _response_cache is None:
        _response_cache = ResponseCache()
    return _response_cache


def get_knowledge_base() -> KnowledgeBase:
    """Get or create KnowledgeBase instance."""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base


def get_ai_brain() -> AIBrain:
    """Get or create AIBrain instance."""
    global _ai_brain
    if _ai_brain is None:
        _ai_brain = AIBrain()
    return _ai_brain


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        llm_provider=settings.llm_provider,
    )


@router.get("/stats", response_model=StatsResponse, tags=["System"])
async def get_stats(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get knowledge base statistics.

    Requires authentication.
    """
    kb = get_knowledge_base()
    stats = kb.get_stats()
    return StatsResponse(**stats)


@router.get("/cache-stats", tags=["System"])
async def get_cache_stats(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get response cache statistics.

    Requires authentication.
    """
    cache = get_response_cache()
    return cache.stats


# Off-topic response message
OFF_TOPIC_RESPONSE = (
    "I am Netra, devoted to the wisdom of Tantra and spiritual practices. "
    "This question falls outside my realm of knowledge. "
    "Please ask about mantras, meditation, yoga, or spiritual teachings."
)


@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, body: ChatRequest):
    """
    Ask Netra a question about tantric practices.

    The system will search the knowledge base for relevant scripture passages
    and generate a contextual response using the Netra persona.

    Off-topic questions (low relevance score) are rejected with a polite message.

    Rate limited to prevent API abuse. Responses are cached for efficiency.
    """
    logger.info(f"Chat request: {body.question[:50]}...")

    try:
        cache = get_response_cache()

        # Check cache first
        cached_response = cache.get(body.question)
        if cached_response:
            logger.info("Returning cached response")
            return cached_response

        kb = get_knowledge_base()
        brain = get_ai_brain()

        # Search for relevant context (now includes distance score)
        context, sources, best_distance = kb.search(body.question)

        logger.debug(f"Best distance score: {best_distance:.3f} (threshold: {settings.relevance_threshold})")

        # Check if the question is off-topic (distance too high = not relevant)
        if best_distance > settings.relevance_threshold or not context:
            logger.info(f"Off-topic question rejected (distance: {best_distance:.3f})")
            response = ChatResponse(
                response=OFF_TOPIC_RESPONSE,
                context_used="",
                sources=[],
            )
            # Cache off-topic responses too
            cache.set(body.question, response)
            return response

        # Generate response for on-topic questions
        ai_response = brain.generate_response(body.question, context)

        # Truncate context for response
        context_preview = context[:200] + "..." if len(context) > 200 else context

        response = ChatResponse(
            response=ai_response,
            context_used=context_preview,
            sources=sources,
        )

        # Cache the response
        cache.set(body.question, response)

        return response

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")
