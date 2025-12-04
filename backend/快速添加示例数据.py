"""
快速添加示例数据到数据库
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models import Category, Product

# 创建表
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # 检查是否已有数据
    if db.query(Product).count() > 0:
        print(f"✅ 数据库中已有 {db.query(Product).count()} 个商品")
        db.close()
        exit(0)
    
    # 创建分类
    categories_data = [
        {"name": "电子产品", "description": "手机、耳机、智能手表等", "icon": "📱"},
        {"name": "美妆护肤", "description": "口红、香水、护肤品等", "icon": "💄"},
        {"name": "服饰配饰", "description": "衣服、包包、首饰等", "icon": "👗"},
        {"name": "家居用品", "description": "香薰、摆件、装饰品等", "icon": "🏠"},
        {"name": "食品饮料", "description": "巧克力、茶叶、酒类等", "icon": "🍫"},
    ]
    
    categories = []
    for cat_data in categories_data:
        cat = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not cat:
            cat = Category(**cat_data)
            db.add(cat)
            categories.append(cat)
        else:
            categories.append(cat)
    
    db.commit()
    for cat in categories:
        db.refresh(cat)
    
    # 创建商品
    products_data = [
        {"name": "AirPods Pro 2 无线降噪耳机", "price": 1899.0, "platform": "taobao", 
         "platform_url": "https://item.taobao.com/item.htm?id=123456789", 
         "category_id": categories[0].id, "description": "苹果AirPods Pro 2代，主动降噪，空间音频", 
         "image_url": "https://via.placeholder.com/300x300?text=AirPods"},
        {"name": "Dior 999 经典正红色口红", "price": 350.0, "platform": "taobao",
         "platform_url": "https://item.taobao.com/item.htm?id=987654321",
         "category_id": categories[1].id, "description": "迪奥999经典正红色，显白提气色",
         "image_url": "https://via.placeholder.com/300x300?text=Dior999"},
        {"name": "香薰蜡烛套装 多香味", "price": 128.0, "platform": "xiaohongshu",
         "platform_url": "https://www.xiaohongshu.com/explore/123456",
         "category_id": categories[3].id, "description": "精选多款香薰蜡烛，营造浪漫氛围",
         "image_url": "https://via.placeholder.com/300x300?text=Candle"},
        {"name": "智能运动手环", "price": 299.0, "platform": "taobao",
         "platform_url": "https://item.taobao.com/item.htm?id=111222333",
         "category_id": categories[0].id, "description": "多功能运动手环，心率监测，运动记录",
         "image_url": "https://via.placeholder.com/300x300?text=Watch"},
        {"name": "精美首饰盒", "price": 88.0, "platform": "taobao",
         "platform_url": "https://item.taobao.com/item.htm?id=444555666",
         "category_id": categories[2].id, "description": "实木首饰盒，多层设计，精美包装",
         "image_url": "https://via.placeholder.com/300x300?text=Jewelry"},
        {"name": "进口巧克力礼盒", "price": 168.0, "platform": "taobao",
         "platform_url": "https://item.taobao.com/item.htm?id=777888999",
         "category_id": categories[4].id, "description": "精选进口巧克力，精美礼盒包装",
         "image_url": "https://via.placeholder.com/300x300?text=Chocolate"},
        {"name": "创意书签套装", "price": 45.0, "platform": "xiaohongshu",
         "platform_url": "https://www.xiaohongshu.com/explore/789012",
         "category_id": categories[4].id, "description": "精美书签套装，多种款式",
         "image_url": "https://via.placeholder.com/300x300?text=Bookmark"},
        {"name": "瑜伽垫套装", "price": 199.0, "platform": "taobao",
         "platform_url": "https://item.taobao.com/item.htm?id=333444555",
         "category_id": categories[0].id, "description": "专业瑜伽垫，防滑设计",
         "image_url": "https://via.placeholder.com/300x300?text=Yoga"},
    ]
    
    for prod_data in products_data:
        product = Product(**prod_data)
        db.add(product)
    
    db.commit()
    print(f"✅ 成功创建 {len(products_data)} 个商品！")
    
except Exception as e:
    db.rollback()
    print(f"❌ 错误: {e}")
    raise
finally:
    db.close()
