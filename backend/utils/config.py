"""
Configuration settings for AssetFraction Backend
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Hedera Configuration
    HEDERA_NETWORK: str = "testnet"
    OPERATOR_ID: str
    OPERATOR_KEY: str
    TREASURY_ID: str
    TREASURY_KEY: str
    HCS_TOPIC_ID: str
    MIRROR_NODE_API: str = "https://testnet.mirrornode.hedera.com/api/v1"
    
    # JWT Configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./assetfraction.db"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Scheduler Configuration
    SCHEDULER_TIMEZONE: str = "UTC"
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
