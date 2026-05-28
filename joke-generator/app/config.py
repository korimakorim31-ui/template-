"""Application configuration settings"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "Random Joke Generator API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    APP_PORT: int = 8001
    WORKERS: int = 4
    
    # Database
    DATABASE_URL: str = "sqlite:///./jokes.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Caching
    JOKE_CACHE_TTL: int = 3600
    CACHE_ENABLED: bool = True
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600
    RATE_LIMITING_ENABLED: bool = True
    
    # External APIs
    JOKE_API_TIMEOUT: int = 10
    JOKE_API_RETRIES: int = 3
    FALLBACK_ENABLED: bool = True
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    
    # Feature flags
    ENABLE_WEBSOCKET: bool = True
    ENABLE_TRANSLATIONS: bool = True
    ENABLE_USER_RATINGS: bool = True
    ENABLE_FAVORITES: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
