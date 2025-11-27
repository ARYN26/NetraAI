"""Application configuration using pydantic-settings."""
import os
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Allow extra env vars like TOKENIZERS_PARALLELISM
    )

    # API Keys
    groq_api_key: str = ""
    google_api_key: str = ""

    # Email (Gmail SMTP for OTP)
    smtp_email: str = ""
    smtp_password: str = ""  # Gmail App Password
    otp_expiry_minutes: int = 5

    # JWT Authentication
    jwt_secret_key: str = "netra-secret-key-change-in-production-12345"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Environment (development or production)
    environment: str = "development"

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Validate JWT secret key is not the default in production."""
        default_key = "netra-secret-key-change-in-production-12345"
        env = os.getenv("ENVIRONMENT", "development").lower()
        if v == default_key and env == "production":
            raise ValueError(
                "JWT_SECRET_KEY must be changed in production! "
                "Generate a secure key with: openssl rand -hex 32"
            )
        return v

    # LLM Configuration
    llm_provider: str = "groq"  # 'groq' or 'gemini'
    groq_model: str = "llama-3.1-8b-instant"
    gemini_model: str = "gemini-pro"

    # ChromaDB
    chroma_db_path: str = "./netra_db"
    chroma_collection_name: str = "scriptures"

    # Embedding Model
    embedding_model: str = "all-MiniLM-L6-v2"

    # Server Configuration
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    log_level: str = "INFO"

    # Rate Limiting (requests per minute per IP)
    rate_limit_per_minute: int = 20

    # Response Caching
    cache_max_size: int = 500  # Max cached responses
    cache_ttl_seconds: int = 86400  # 24 hours

    # Text Processing
    chunk_size: int = 1000
    chunk_overlap: int = 200
    search_results: int = 3

    # Relevance Filtering
    # Distance threshold for relevance (lower = more strict, 0.5-0.8 recommended)
    # If best match distance > threshold, question is considered off-topic
    relevance_threshold: float = 0.7

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
