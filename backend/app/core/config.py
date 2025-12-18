"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./portfolio_optimizer.db"
    
    # Redis (optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Data Sources
    CASABLANCA_BOURSE_BASE_URL: str = "https://www.casablanca-bourse.com"
    ASFIM_BASE_URL: str = "https://www.asfim.ma"
    
    # Optimization Parameters
    DEFAULT_ALPHA: float = 0.05
    DEFAULT_REGULARIZATION_LAMBDA: float = 0.01
    MAX_PORTFOLIO_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

