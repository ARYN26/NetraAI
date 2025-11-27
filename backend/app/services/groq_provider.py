"""Groq LLM Provider implementation."""
from typing import Generator
from loguru import logger

from app.config import settings
from app.services.llm_provider import LLMProvider


class GroqProvider(LLMProvider):
    """LLM provider using Groq's API with Llama3."""

    def __init__(self):
        """Initialize Groq client."""
        try:
            from groq import Groq

            if not settings.groq_api_key:
                raise ValueError("GROQ_API_KEY is not set in environment")

            self.client = Groq(api_key=settings.groq_api_key, timeout=30.0)
            self.model = settings.groq_model
            logger.info(f"Groq provider initialized with model: {self.model}")

        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "groq"

    def generate(self, system_prompt: str, user_query: str) -> str:
        """
        Generate a response using Groq's API.

        Args:
            system_prompt: The system context/persona prompt
            user_query: The user's question

        Returns:
            The generated response text
        """
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )

            response = completion.choices[0].message.content
            logger.debug(f"Groq response length: {len(response)} chars")
            return response

        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise

    def generate_stream(
        self, system_prompt: str, user_query: str
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response using Groq's API.

        Args:
            system_prompt: The system context/persona prompt
            user_query: The user's question

        Yields:
            Chunks of the generated response
        """
        try:
            stream = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                stream=True,
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        except Exception as e:
            logger.error(f"Groq streaming error: {e}")
            raise
