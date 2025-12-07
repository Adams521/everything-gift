#!/usr/bin/env python3
"""
数据库连接诊断和修复脚本
用于检查和修复 PostgreSQL 连接问题
"""
import os
import sys
from urllib.parse import urlparse, quote_plus

def check_database_url():
    """检查并验证数据库连接 URL"""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@postgres:5432/giftdb"
    )
    
    print(f"当前 DATABASE_URL: {database_url}")
    
    try:
        parsed = urlparse(database_url)
        print(f"解析结果:")
        print(f"  协议: {parsed.scheme}")
        print(f"  用户名: {parsed.username}")
        print(f"  主机: {parsed.hostname}")
        print(f"  端口: {parsed.port}")
        print(f"  数据库名: {parsed.path.lstrip('/')}")
        
        if parsed.path.lstrip('/') != 'giftdb':
            print(f"⚠️  警告: 数据库名不是 'giftdb'，而是 '{parsed.path.lstrip('/')}'")
            return False
        
        if parsed.username != 'user':
            print(f"⚠️  警告: 用户名不是 'user'，而是 '{parsed.username}'")
        
        if parsed.hostname != 'postgres':
            print(f"⚠️  警告: 主机名不是 'postgres'（容器名），而是 '{parsed.hostname}'")
        
        return True
    except Exception as e:
        print(f"❌ 解析 URL 时出错: {e}")
        return False

def generate_correct_url():
    """生成正确的数据库 URL"""
    db_user = os.getenv("POSTGRES_USER", "user")
    db_password = os.getenv("POSTGRES_PASSWORD", "password")
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "giftdb")
    
    # 对密码进行 URL 编码（如果包含特殊字符）
    encoded_password = quote_plus(db_password)
    
    url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    print(f"生成的正确 URL: {url}")
    return url

if __name__ == "__main__":
    print("=" * 60)
    print("数据库连接诊断工具")
    print("=" * 60)
    print()
    
    if not check_database_url():
        print()
        print("尝试生成正确的 URL...")
        correct_url = generate_correct_url()
        print()
        print("请设置环境变量:")
        print(f"export DATABASE_URL='{correct_url}'")
        sys.exit(1)
    
    print()
    print("✅ 数据库 URL 格式正确")
    print()
    print("如果仍然连接失败，请检查:")
    print("1. PostgreSQL 容器是否正在运行: docker-compose ps")
    print("2. 数据库是否已创建: docker-compose exec postgres psql -U user -l")
    print("3. 如果数据库不存在，运行: docker-compose exec postgres createdb -U user giftdb")

