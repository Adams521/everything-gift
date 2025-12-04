"""
创建管理员用户脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash

# 创建表
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # 检查是否已有管理员
    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if admin:
        print(f"✅ 管理员已存在: {admin.username}")
        db.close()
        exit(0)
    
    # 创建管理员
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),  # 默认密码
        role=UserRole.ADMIN,
        is_active="true"
    )
    db.add(admin)
    
    # 创建VIP用户示例
    vip_user = User(
        username="vip",
        email="vip@example.com",
        hashed_password=get_password_hash("vip123"),
        role=UserRole.VIP,
        is_active="true"
    )
    db.add(vip_user)
    
    db.commit()
    print("✅ 成功创建用户：")
    print(f"  管理员: admin / admin123")
    print(f"  VIP用户: vip / vip123")
    
except Exception as e:
    db.rollback()
    print(f"❌ 创建失败: {e}")
    raise
finally:
    db.close()

