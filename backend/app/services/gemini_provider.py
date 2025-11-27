"""Google Gemini LLM Provider implementation."""
from typing import Generator
from loguru import logger

from app.config import settings
from app.services.llm_provider import LLMProvider


class GeminiProvider(LLMProvider):
    """LLM provider using Google's Gemini API."""

    def __init__(self):
        """Initialize Gemini client."""
        try:
            import google.generativeai as genai

            if not settings.google_api_key:
                raise ValueError("GOOGLE_API_KEY is not set in environment")

            genai.configure(api_key=settings.google_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            logger.info(f"Gemini provider initialized with model: {settings.gemini_model}")

        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "gemini"

    def generate(self, system_prompt: str, user_query: str) -> str:
        """
        Generate a response using Gemini's API.

        Args:
            system_prompt: The system context/persona prompt
            user_query: The user's question

        Returns:
            The generated response text
        """
        try:
            # Gemini uses a combined prompt approach
            full_prompt = f"{system_prompt}\n\nUser Query: {user_query}"

            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                },
            )

            result = response.text
            logger.debug(f"Gemini response length: {len(result)} chars")
            return result

        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise

    def generate_stream(
        self, system_prompt: str, user_query: str
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response using Gemini's API.

        Args:
            system_prompt: The system context/persona prompt
            user_query: The user's question

        Yields:
            Chunks of the generated response
        """
        try:
            full_prompt = f"{system_prompt}\n\nUser Query: {user_query}"

            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                },
                stream=True,
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Gemini streaming error: {e}")
            raise
