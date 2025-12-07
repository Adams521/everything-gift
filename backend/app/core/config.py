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
    
    # Ollama配置
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME", "qwen3:4b")
    OLLAMA_ENABLED: bool = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# 验证并修复数据库 URL（处理可能的格式问题）
def validate_database_url(url: str) -> str:
    """验证并修复数据库连接 URL"""
    if not url or not isinstance(url, str):
        # 如果 URL 无效，尝试从环境变量重建
        db_user = os.getenv("POSTGRES_USER", "user")
        db_password = os.getenv("POSTGRES_PASSWORD", "password")
        db_host = os.getenv("POSTGRES_HOST", "postgres")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "giftdb")
        url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # 确保 URL 格式正确
    if not url.startswith(("postgresql://", "postgresql+psycopg2://")):
        # 如果格式不对，尝试修复
        if url.count("@") == 1 and url.count("/") >= 1:
            # 可能是缺少协议，尝试添加
            if not url.startswith("postgresql"):
                url = "postgresql://" + url
        else:
            # 完全重建
            db_user = os.getenv("POSTGRES_USER", "user")
            db_password = os.getenv("POSTGRES_PASSWORD", "password")
            db_host = os.getenv("POSTGRES_HOST", "postgres")
            db_port = os.getenv("POSTGRES_PORT", "5432")
            db_name = os.getenv("POSTGRES_DB", "giftdb")
            url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    return url

# 应用验证
settings.DATABASE_URL = validate_database_url(settings.DATABASE_URL)
