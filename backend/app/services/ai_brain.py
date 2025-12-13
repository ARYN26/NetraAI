"""AI Brain - Orchestration layer for LLM interactions."""
from typing import Generator
from loguru import logger

from app.config import settings
from app.services.llm_provider import LLMProvider
from app.services.groq_provider import GroqProvider
from app.services.gemini_provider import GeminiProvider


# Netra's persona system prompt - STRICT topic boundaries
NETRA_SYSTEM_PROMPT = """You are Netra, a Tantric AI guide specializing in:
- Tantra, mantras, meditation, yoga
- Hindu/Buddhist spiritual philosophy
- Chakras, kundalini, energy work
- Scriptural texts (Vedas, Upanishads, Tantras, Shiva Purana, Vijnana Bhairava)
- Rituals, pujas, spiritual practices
- Sri Aurobindo and The Mother's teachings

RULES:
1. Answer ONLY from the scripture context provided below
2. For off-topic questions, politely decline without introducing yourself
3. Never discuss politics, games, technology, or non-spiritual topics
4. Keep responses concise and readable

FORMATTING:
- Write in flowing prose, not excessive bullet points
- Use simple paragraphs for explanations
- Only use bullet points sparingly for lists of items or steps
- Avoid heavy markdown formatting (no ** bold everywhere)
- Do NOT introduce yourself in responses - just answer directly

FOR RITUAL/PUJA QUESTIONS:
Provide steps covering: preparation, purification, invocation, main practice, and conclusion.
Include specific mantras in Sanskrit with transliteration when relevant.

GURU DIKSHA NOTICE:
When discussing mantras, rituals, or sadhana practices, end with:
"Note: Traditional practices are best learned through a qualified guru. This is for educational purposes."

Scripture Context:
{context}"""


class AIBrain:
    """
    AI Brain orchestrates interactions with LLM providers.

    Handles:
    - Provider selection (Groq/Gemini)
    - System prompt construction
    - Response generation
    """

    def __init__(self):
        """Initialize the AI Brain with configured provider."""
        self.provider = self._create_provider()
        logger.info(f"AIBrain initialized with {self.provider.provider_name}")

    def _create_provider(self) -> LLMProvider:
        """Create the appropriate LLM provider based on configuration."""
        provider_name = settings.llm_provider.lower()

        if provider_name == "groq":
            return GroqProvider()
        elif provider_name == "gemini":
            return GeminiProvider()
        else:
            logger.warning(f"Unknown provider '{provider_name}', defaulting to Groq")
            return GroqProvider()

    def _build_system_prompt(self, context: str) -> str:
        """Build the system prompt with scripture context."""
        if not context:
            context = "No specific scripture context available for this query."
        return NETRA_SYSTEM_PROMPT.format(context=context)

    def generate_response(self, question: str, context: str = "") -> str:
        """
        Generate a response to the user's question.

        Args:
            question: The user's question
            context: Scripture context from knowledge base

        Returns:
            Generated response from Netra
        """
        system_prompt = self._build_system_prompt(context)

        logger.debug(f"Generating response for: {question[:50]}...")
        response = self.provider.generate(system_prompt, question)

        return response

    def generate_response_stream(
        self, question: str, context: str = ""
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response to the user's question.

        Args:
            question: The user's question
            context: Scripture context from knowledge base

        Yields:
            Chunks of the generated response
        """
        system_prompt = self._build_system_prompt(context)

        logger.debug(f"Streaming response for: {question[:50]}...")
        yield from self.provider.generate_stream(system_prompt, question)
