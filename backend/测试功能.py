"""
测试系统功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models import Product, Category

# 测试数据库
db = SessionLocal()
try:
    product_count = db.query(Product).count()
    category_count = db.query(Category).count()
    print(f"✅ 数据库连接正常")
    print(f"   商品数量: {product_count}")
    print(f"   分类数量: {category_count}")
    
    if product_count > 0:
        products = db.query(Product).limit(3).all()
        print(f"\n   示例商品:")
        for p in products:
            print(f"     - {p.name} (¥{p.price})")
finally:
    db.close()
