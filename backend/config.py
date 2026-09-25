from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    COGNEE_API_KEY: str = "local"
    COGNEE_GRAPH_URL: str = "local"
    SARVAM_API_KEY: Optional[str] = ""
    N8N_WEBHOOK_URL: Optional[str] = "http://localhost:8000"
    ENVIRONMENT: str = "development"
    DEMO_MERCHANT_ID: str = "merchant_001"

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
