"""
将爬取的商品保存到数据库
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.product import Product
from app.models.category import Category
from app.crawlers.taobao_crawler import TaobaoCrawler, XiaohongshuCrawler
from app.crawlers.union_crawler import UnionCrawler


def get_or_create_category(db: Session, name: str) -> Category:
    """获取或创建分类"""
    category = db.query(Category).filter(Category.name == name).first()
    if not category:
        category = Category(name=name, description=f"{name}类礼品")
        db.add(category)
        db.commit()
        db.refresh(category)
    return category


async def save_crawled_products():
    """爬取并保存商品"""
    db: Session = SessionLocal()
    
    try:
        # 优先使用联盟API（如果配置了）
        union_crawler = UnionCrawler()
        use_union = hasattr(union_crawler.taobao_api, 'app_key') and union_crawler.taobao_api.app_key
        
        # 搜索关键词
        keywords = [
            "生日礼物",
            "情人节礼物",
            "母亲节礼物",
            "父亲节礼物",
            "圣诞节礼物",
        ]
        
        saved_count = 0
        
        # 如果配置了联盟API，优先使用
        if use_union:
            print("使用联盟API爬取商品...")
            all_products = await union_crawler.crawl_products(keywords)
            for prod_data in all_products:
                category = get_or_create_category(db, prod_data.get("category", "通用礼品"))
                existing = db.query(Product).filter(
                    Product.name == prod_data["name"],
                    Product.platform == prod_data["platform"]
                ).first()
                if not existing:
                    product = Product(
                        name=prod_data["name"],
                        price=prod_data.get("price"),
                        image_url=prod_data.get("image_url"),  # 使用真实图片URL
                        platform=prod_data["platform"],
                        platform_url=prod_data["platform_url"],
                        description=prod_data.get("description"),
                        category_id=category.id,
                    )
                    db.add(product)
                    saved_count += 1
            db.commit()
            print(f"\n✅ 成功保存 {saved_count} 个商品到数据库（来自联盟API）")
            return
        
        # 否则使用模拟爬虫
        taobao = TaobaoCrawler()
        xhs = XiaohongshuCrawler()
        
        for keyword in keywords:
            print(f"正在爬取: {keyword}")
            
            # 爬取淘宝商品
            try:
                taobao_products = await taobao.search_products(keyword)
                for prod_data in taobao_products:
                    # 获取或创建分类
                    category = get_or_create_category(db, prod_data.get("category", "通用礼品"))
                    
                    # 检查商品是否已存在
                    existing = db.query(Product).filter(
                        Product.name == prod_data["name"],
                        Product.platform == prod_data["platform"]
                    ).first()
                    
                    if not existing:
                        product = Product(
                            name=prod_data["name"],
                            price=prod_data.get("price"),
                            image_url=prod_data.get("image_url"),
                            platform=prod_data["platform"],
                            platform_url=prod_data["platform_url"],
                            description=prod_data.get("description"),
                            category_id=category.id,
                        )
                        db.add(product)
                        saved_count += 1
            except Exception as e:
                print(f"爬取淘宝商品失败: {e}")
            
            # 爬取小红书商品
            try:
                xhs_products = await xhs.search_products(keyword)
                for prod_data in xhs_products:
                    category = get_or_create_category(db, prod_data.get("category", "生活好物"))
                    
                    existing = db.query(Product).filter(
                        Product.name == prod_data["name"],
                        Product.platform == prod_data["platform"]
                    ).first()
                    
                    if not existing:
                        product = Product(
                            name=prod_data["name"],
                            price=prod_data.get("price"),
                            image_url=prod_data.get("image_url"),
                            platform=prod_data["platform"],
                            platform_url=prod_data["platform_url"],
                            description=prod_data.get("description"),
                            category_id=category.id,
                        )
                        db.add(product)
                        saved_count += 1
            except Exception as e:
                print(f"爬取小红书商品失败: {e}")
            
            # 提交批次
            db.commit()
            await asyncio.sleep(0.5)  # 延时
        
        print(f"\n✅ 成功保存 {saved_count} 个商品到数据库")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 保存失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(save_crawled_products())
