"""Response caching service for minimizing API calls."""
import hashlib
from typing import Any, Optional

from cachetools import TTLCache
from loguru import logger

from app.config import settings


class ResponseCache:
    """In-memory cache for chat responses with TTL expiration."""

    def __init__(self, maxsize: Optional[int] = None, ttl: Optional[int] = None):
        """
        Initialize the cache.

        Args:
            maxsize: Maximum number of items to cache (default from settings)
            ttl: Time-to-live in seconds (default from settings)
        """
        self._maxsize = maxsize or settings.cache_max_size
        self._ttl = ttl or settings.cache_ttl_seconds
        self._cache: TTLCache = TTLCache(maxsize=self._maxsize, ttl=self._ttl)
        self._hits = 0
        self._misses = 0
        logger.info(f"ResponseCache initialized: maxsize={self._maxsize}, ttl={self._ttl}s")

    def _get_key(self, question: str) -> str:
        """Generate a cache key from a question."""
        normalized = question.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()

    def get(self, question: str) -> Optional[Any]:
        """
        Get a cached response for a question.

        Args:
            question: The user's question

        Returns:
            Cached response or None if not found
        """
        key = self._get_key(question)
        result = self._cache.get(key)
        if result is not None:
            self._hits += 1
            logger.debug(f"Cache HIT for question: {question[:50]}...")
        else:
            self._misses += 1
            logger.debug(f"Cache MISS for question: {question[:50]}...")
        return result

    def set(self, question: str, response: Any) -> None:
        """
        Cache a response for a question.

        Args:
            question: The user's question
            response: The response to cache
        """
        key = self._get_key(question)
        self._cache[key] = response
        logger.debug(f"Cached response for question: {question[:50]}...")

    def clear(self) -> None:
        """Clear all cached responses."""
        self._cache.clear()
        logger.info("Response cache cleared")

    @property
    def stats(self) -> dict:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        return {
            "size": len(self._cache),
            "max_size": self._maxsize,
            "ttl_seconds": self._ttl,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.1f}%",
        }
