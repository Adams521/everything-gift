from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "AI礼品推荐系统"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@postgres:5432/giftdb"
    )
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")
    
    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*",  # 开发环境允许所有来源
    ]
    
    # API配置
    API_V1_PREFIX: str = "/api/v1"
    
    # 淘宝联盟配置
    TAOBAO_UNION_APP_KEY: str = os.getenv("TAOBAO_UNION_APP_KEY", "")
    TAOBAO_UNION_APP_SECRET: str = os.getenv("TAOBAO_UNION_APP_SECRET", "")
    TAOBAO_UNION_PID: str = os.getenv("TAOBAO_UNION_PID", "")
    
    # 京东联盟配置
    JD_UNION_APP_KEY: str = os.getenv("JD_UNION_APP_KEY", "")
    JD_UNION_APP_SECRET: str = os.getenv("JD_UNION_APP_SECRET", "")
    JD_UNION_SITE_ID: str = os.getenv("JD_UNION_SITE_ID", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
