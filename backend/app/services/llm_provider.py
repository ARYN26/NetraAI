"""Abstract LLM Provider interface for swappable AI backends."""
from abc import ABC, abstractmethod
from typing import Generator


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, system_prompt: str, user_query: str) -> str:
        """
        Generate a response from the LLM.

        Args:
            system_prompt: The system context/persona prompt
            user_query: The user's question

        Returns:
            The generated response text
        """
        pass

    @abstractmethod
    def generate_stream(
        self, system_prompt: str, user_query: str
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response from the LLM.

        Args:
            system_prompt: The system context/persona prompt
            user_query: The user's question

        Yields:
            Chunks of the generated response
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of this provider."""
        pass
