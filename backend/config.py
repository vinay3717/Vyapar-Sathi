from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM (owned by Devesh)
    GEMINI_API_KEY: str = ""

    # Memory (owned by Devesh)
    COGNEE_API_KEY: str = ""
    COGNEE_GRAPH_URL: str = ""

    # Voice (owned by Teammate)
    SARVAM_API_KEY: str = ""

    # Workflow (owned by Teammate)
    N8N_WEBHOOK_URL: str = ""

    # App (owned by both)
    ENVIRONMENT: str = "development"
    DEMO_MERCHANT_ID: str = "merchant_001"
    FASTAPI_BACKEND_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
