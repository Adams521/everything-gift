from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    """用户角色枚举"""
    ADMIN = "admin"  # 管理员
    VIP = "vip"  # VIP用户
    USER = "user"  # 普通用户

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # 用户名
    email = Column(String, unique=True, index=True, nullable=True)  # 邮箱
    hashed_password = Column(String, nullable=False)  # 加密后的密码
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)  # 用户角色
    is_active = Column(String, default="true", nullable=False)  # 是否激活
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
