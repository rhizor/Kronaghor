"""
Kronaghor - Configuration Module
Maneja la configuración de la aplicación.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str = ""  # Must be set in production
    DEBUG: bool = False
    
    # Test database
TEST_DATABASE_URL = "sqlite:///./test_kronaghor.db"

class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str = ""  # Must be set in production
    DEBUG: bool = False
    
    # Database - usar test db si existe
    DATABASE_URL: str = "sqlite:///./kronaghor.db"
    
    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_AI_PROVIDER: str = "openai"  # openai, grok, ollama
    
    # Cloud Storage
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    model_config = {"env_file": ".env", "case_sensitive": True}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate random key if not set (dev only)
        if not self.SECRET_KEY:
            if os.getenv("ENV", "dev") == "production":
                raise ValueError("SECRET_KEY must be set in production")
            self.SECRET_KEY = secrets.token_urlsafe(32)
    
    @property
    def is_production(self) -> bool:
        return os.getenv("ENV", "dev") == "production"


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración cacheada."""
    return Settings()
