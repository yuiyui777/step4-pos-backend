from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # データベース
    DATABASE_URL: str
    
    # アプリケーション
    APP_NAME: str = "POS API"
    DEBUG: bool = False
    
    # CORS設定
    FRONTEND_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

