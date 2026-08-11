import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "FloatChat Enterprise API"
    VERSION: str = "2.4.0"
    API_V1_STR: str = "/api/v1"

    # Server Port (Render supplies PORT via OS environment)
    PORT: int = 8000

    # Secret Key & JWT Settings
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database Settings (PostgreSQL with SQLite fallback)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./floatchat.db"
    )

    # AI & Groq LLM API Key
    GROQ_API_KEY: str = ""

    # Allowed CORS Origins
    # In production set to your Netlify URL, e.g.:
    # CORS_ORIGINS=https://your-app.netlify.app
    CORS_ORIGINS: Union[str, list[str]] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, list[str]]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Admin Security Passkey (loaded from env — never hard-coded)
    SECURITY_LOG_PASSKEY: str = ""

    # Secure key for gov/elevated-access verification.
    # Set FLOWCHAT_SECURITY_KEY in Render Environment Variables.
    # Never expose this in frontend / client-side code.
    FLOWCHAT_SECURITY_KEY: str = ""

    class Config:
        case_sensitive = True
        # Tries backend/.env for local dev, then .env at project root.
        # On Render, env vars are injected via OS environment — no file needed.
        env_file = ("backend/.env", ".env")
        env_file_encoding = "utf-8"

settings = Settings()
