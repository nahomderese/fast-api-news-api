"""
Loads settings from environment variables with sensible defaults.
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Application settings
    app_name: str = Field(
        default="SWEN AI-Enriched News Pipeline",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    environment: str = Field(
        default="development",
        description="Environment (development/staging/production)"
    )
    
    # API settings
    api_prefix: str = Field(
        default="/api/v1",
        description="API route prefix"
    )
    host: str = Field(
        default="0.0.0.0",
        description="API host"
    )
    port: int = Field(
        default=8000,
        description="API port"
    )
    
    # AI Service settings
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API key for AI services"
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model to use (gemini-2.5-flash, gemini-1.5-pro, gemini-pro, etc.)"
    )
    use_mock_ai: bool = Field(
        default=True,
        description="Use mock AI service for development/testing"
    )
    
    # Brave Search API settings for media discovery
    brave_api_key: Optional[str] = Field(
        default=None,
        description="Brave Search API key for media discovery"
    )
    brave_image_search_url: str = Field(
        default="https://api.search.brave.com/res/v1/images/search",
        description="Brave Search API endpoint for image search"
    )
    brave_video_search_url: str = Field(
        default="https://api.search.brave.com/res/v1/videos/search",
        description="Brave Search API endpoint for video search"
    )
    
    # Database settings
    database_url: Optional[str] = Field(
        default=None,
        alias="DATABASE_URL",
        description="Database connection URL (postgresql+asyncpg://user:pass@host:port/db)"
    )
    db_host: str = Field(
        default="localhost",
        description="Database host"
    )
    db_port: int = Field(
        default=5432,
        description="Database port"
    )
    db_name: str = Field(
        default="swen_news",
        description="Database name"
    )
    db_user: str = Field(
        default="swen_user",
        description="Database user"
    )
    db_password: str = Field(
        default="",
        description="Database password"
    )
    
    # Database connection pool settings
    db_pool_size: int = Field(
        default=5,
        description="Database connection pool size"
    )
    db_max_overflow: int = Field(
        default=10,
        description="Maximum overflow connections beyond pool_size"
    )
    db_pool_timeout: int = Field(
        default=30,
        description="Timeout for getting connection from pool (seconds)"
    )
    db_pool_recycle: int = Field(
        default=3600,
        description="Recycle connections after this many seconds"
    )
    
    # CORS settings
    allowed_origins: str = Field(
        default="*",
        description="Allowed CORS origins (comma-separated or * for all)"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

