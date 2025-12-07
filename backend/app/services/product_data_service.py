"""
统一商品数据服务
整合API和爬虫，提供完整的商品数据获取接口
"""
from typing import Dict, Optional, List
from datetime import datetime
from app.services.taobao_union import TaobaoUnionAPI
from app.services.jd_union import JDUnionAPI
from app.core.database import SessionLocal
from app.models.product import Product


class ProductDataService:
    """统一商品数据服务"""
    
    def __init__(self):
        self.taobao_api = TaobaoUnionAPI()
        self.jd_api = JDUnionAPI()
        # 爬虫服务将在后续实现
        # self.review_crawler = ReviewCrawler()
    
    async def get_product_details(
        self,
        platform: str,
        product_id: Optional[str] = None,
        platform_url: Optional[str] = None,
        include_reviews: bool = False
    ) -> Optional[Dict]:
        """
        获取商品详细信息
        
        Args:
            platform: 平台名称（taobao, jd, pdd, xiaohongshu, douyin）
            product_id: 平台商品ID
            platform_url: 商品链接（如果product_id不可用）
            include_reviews: 是否包含详细评价数据（需要爬虫）
        
        Returns:
            商品详细信息字典
        """
        # 根据平台选择数据源
        if platform == "taobao":
            return await self._get_taobao_product(product_id, platform_url, include_reviews)
        elif platform == "jd":
            return await self._get_jd_product(product_id, platform_url, include_reviews)
        elif platform == "pdd":
            return await self._get_pdd_product(product_id, platform_url, include_reviews)
        elif platform == "xiaohongshu":
            return await self._get_xiaohongshu_product(product_id, platform_url, include_reviews)
        elif platform == "douyin":
            return await self._get_douyin_product(product_id, platform_url, include_reviews)
        else:
            raise ValueError(f"不支持的平台: {platform}")
    
    async def _get_taobao_product(
        self,
        product_id: Optional[str],
        platform_url: Optional[str],
        include_reviews: bool
    ) -> Optional[Dict]:
        """获取淘宝商品数据"""
        # 优先使用API
        if product_id:
            detail = await self.taobao_api.get_product_detail(product_id)
            if detail:
                # 如果需要评价数据，使用爬虫补充
                if include_reviews:
                    # review_data = await self.review_crawler.crawl_taobao_reviews(product_id)
                    # detail.update(review_data)
                    pass  # 待实现
                return detail
        
        # 如果API失败，尝试从数据库获取
        if product_id:
            db = SessionLocal()
            try:
                product = db.query(Product).filter(
                    Product.platform == "taobao",
                    Product.platform_product_id == product_id
                ).first()
                if product:
                    return self._product_to_dict(product)
            finally:
                db.close()
        
        return None
    
    async def _get_jd_product(
        self,
        product_id: Optional[str],
        platform_url: Optional[str],
        include_reviews: bool
    ) -> Optional[Dict]:
        """获取京东商品数据"""
        # 京东联盟API需要不同的调用方式
        # 这里先返回None，后续完善
        # 可以尝试从数据库获取
        if product_id:
            db = SessionLocal()
            try:
                product = db.query(Product).filter(
                    Product.platform == "jd",
                    Product.platform_product_id == product_id
                ).first()
                if product:
                    return self._product_to_dict(product)
            finally:
                db.close()
        
        return None
    
    async def _get_pdd_product(
        self,
        product_id: Optional[str],
        platform_url: Optional[str],
        include_reviews: bool
    ) -> Optional[Dict]:
        """获取拼多多商品数据（使用爬虫）"""
        # 待实现拼多多爬虫
        # 目前从数据库获取
        if product_id:
            db = SessionLocal()
            try:
                product = db.query(Product).filter(
                    Product.platform == "pdd",
                    Product.platform_product_id == product_id
                ).first()
                if product:
                    return self._product_to_dict(product)
            finally:
                db.close()
        
        return None
    
    async def _get_xiaohongshu_product(
        self,
        product_id: Optional[str],
        platform_url: Optional[str],
        include_reviews: bool
    ) -> Optional[Dict]:
        """获取小红书商品数据（使用爬虫）"""
        # 待实现小红书爬虫
        if product_id:
            db = SessionLocal()
            try:
                product = db.query(Product).filter(
                    Product.platform == "xiaohongshu",
                    Product.platform_product_id == product_id
                ).first()
                if product:
                    return self._product_to_dict(product)
            finally:
                db.close()
        
        return None
    
    async def _get_douyin_product(
        self,
        product_id: Optional[str],
        platform_url: Optional[str],
        include_reviews: bool
    ) -> Optional[Dict]:
        """获取抖音商品数据（使用爬虫）"""
        # 待实现抖音爬虫
        if product_id:
            db = SessionLocal()
            try:
                product = db.query(Product).filter(
                    Product.platform == "douyin",
                    Product.platform_product_id == product_id
                ).first()
                if product:
                    return self._product_to_dict(product)
            finally:
                db.close()
        
        return None
    
    def _product_to_dict(self, product: Product) -> Dict:
        """将Product模型转换为字典"""
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "original_price": product.original_price,
            "discount_price": product.discount_price,
            "image_url": product.image_url,
            "image_urls": product.image_urls,
            "video_url": product.video_url,
            "platform": product.platform,
            "platform_url": product.platform_url,
            "platform_product_id": product.platform_product_id,
            "description": product.description,
            "sales_count": product.sales_count,
            "sales_amount": product.sales_amount,
            "review_count": product.review_count,
            "good_review_count": product.good_review_count,
            "bad_review_count": product.bad_review_count,
            "good_review_rate": product.good_review_rate,
            "average_rating": product.average_rating,
            "shop_name": product.shop_name,
            "shop_url": product.shop_url,
            "specifications": product.specifications,
            "data_source": product.data_source,
            "last_updated": product.last_updated.isoformat() if product.last_updated else None,
        }
    
    async def save_product_data(self, product_data: Dict) -> Product:
        """
        保存商品数据到数据库
        
        Args:
            product_data: 商品数据字典
        
        Returns:
            保存的Product对象
        """
        db = SessionLocal()
        try:
            # 查找是否已存在
            if product_data.get("platform_product_id"):
                product = db.query(Product).filter(
                    Product.platform == product_data["platform"],
                    Product.platform_product_id == product_data["platform_product_id"]
                ).first()
            else:
                product = None
            
            if product:
                # 更新现有商品
                for key, value in product_data.items():
                    if hasattr(product, key) and value is not None:
                        setattr(product, key, value)
                product.last_updated = datetime.now()
            else:
                # 创建新商品
                product = Product(**product_data)
                product.last_updated = datetime.now()
                db.add(product)
            
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
