"""
Application settings and configuration

NOTE: Claude Agent SDK API keys are managed separately from Claude Code
authentication via backend/config/key_manager.py and api_keys.json
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # CORS Configuration
    cors_origins: list = ["http://localhost:8000", "http://localhost:8080", "http://127.0.0.1:8000"]

    # WebSocket Configuration
    ws_heartbeat_interval: int = 30  # seconds
    ws_timeout: int = 300  # seconds

    # Agent Configuration
    max_conversation_history: int = 50  # Maximum messages to keep in memory
    stream_timeout: int = 120  # seconds

    # Healthcare Configuration
    enable_hipaa_logging: bool = True
    audit_log_path: str = "./logs/audit.log"

    # BYOK (Bring Your Own Key) Configuration
    allow_user_provided_keys: bool = True  # Allow users to provide their own API keys
    require_key_validation: bool = True  # Validate key format before use

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
