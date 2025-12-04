"""
更新数据库中商品的图片URL
将占位图替换为真实图片
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models import Product

# 使用Unsplash的真实图片（免费，无需API key）
IMAGE_URLS = [
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",  # 电子产品
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",  # 手表
    "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop",  # 购物
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop",  # 家居
    "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400&h=400&fit=crop",  # 食品
    "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop",  # 美妆
    "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop",  # 服饰
    "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=400&fit=crop",  # 包包
    "https://images.unsplash.com/photo-1572635196237-14b3f281fbaf?w=400&h=400&fit=crop",  # 眼镜
    "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop",  # 鞋子
]

def update_product_images():
    """更新商品图片"""
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        updated_count = 0
        
        for i, product in enumerate(products):
            # 如果图片URL为空或包含placeholder，则更新
            if not product.image_url or 'placeholder' in product.image_url.lower():
                product.image_url = IMAGE_URLS[i % len(IMAGE_URLS)]
                db.add(product)
                updated_count += 1
        
        db.commit()
        print(f"✅ 成功更新 {updated_count} 个商品的图片")
        
        # 显示示例
        sample_products = db.query(Product).limit(3).all()
        print("\n示例商品图片：")
        for p in sample_products:
            print(f"  - {p.name}: {p.image_url[:60]}...")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 更新失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_product_images()
