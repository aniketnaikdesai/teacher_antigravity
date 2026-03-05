from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal


class Settings(BaseSettings):
    """
    Core application settings parsed from environment variables.
    Follows canonical configurations defined in GEMINI.md Sections 16, 18, 25.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App Environment
    APP_ENV: Literal["development", "production", "testing"] = "development"
    APP_NAME: str = "teacher_antigravity"

    # Provider Routing Models (Section 16 & 24)
    GEMINI_PRIMARY_MODEL_ID: str = "gemini-2.5-flash"  # Use stable production model
    GEMINI_REASONING_MODEL_ID: str = "gemini-2.5-pro"
    OLLAMA_FALLBACK_MODEL_ID: str = "llama3"
    OLLAMA_REASONING_MODEL_ID: str = "deepseek-coder"
    OLLAMA_API_BASE: str = "http://localhost:11434"

    # Stability Controls (Section 18 & 25)
    GEMINI_API_KEY: Optional[str] = None
    MAX_RETRIES: int = 2
    TIMEOUT_SECONDS: int = 30
    CACHE_TTL_SECONDS: int = 3600
    RATE_LIMIT_RPM: int = 60
    RATE_LIMIT_TPM: int = 100000

    # Safety Thresholds (Section 29)
    SAFETY_LEVEL: Literal["strict", "moderate", "lenient"] = "strict"

    @property
    def is_gemini_enabled(self) -> bool:
        """Helper to determine if Gemini is configured as the primary route."""
        return bool(self.GEMINI_API_KEY)


settings = Settings()
