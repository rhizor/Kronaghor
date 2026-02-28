"""
Kronaghor - Configuration Module
Maneja la configuración de la aplicación.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str = "change-this-in-production"
    DEBUG: bool = True
    
    # Database
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración cacheada."""
    return Settings()
