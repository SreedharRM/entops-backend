import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env", ".env.local"],
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars like CONVEX_DEPLOYMENT
    )

    ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./entops.db"
    CONVEX_URL: str = os.getenv("CONVEX_URL", "https://your-convex-deployment.convex.cloud")
    CONVEX_API_KEY: str = os.getenv("CONVEX_API_KEY", "")

    # API Keys
    OUTREACH_API_KEY: str = os.getenv("OUTREACH_API_KEY", "demo-key")
    AUTUMN_API_KEY: str = os.getenv("AUTUMN_API_KEY", "demo-key")
    SLACK_API_KEY: str = os.getenv("SLACK_API_KEY", "demo-key")
    SALESFORCE_API_KEY: str = os.getenv("SALESFORCE_API_KEY", "demo-key")

    AGENTMAIL_API_KEY: str = "fe14c6b65b37a6174abc483730488cbec7edb9a2c1499ed8aecfe42e2e8d96e4"
    OPENAI_API_KEY: str = "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"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Task Configuration
    MAX_TASK_RETRIES: int = 3
    TASK_TIMEOUT_SECONDS: int = 300

settings = Settings()
