from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    # 基础信息
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=True)  # 当前售价
    original_price = Column(Float, nullable=True)  # 原价
    discount_price = Column(Float, nullable=True)  # 折扣价
    image_url = Column(String, nullable=True)  # 主图URL（兼容旧数据）
    image_urls = Column(JSON, nullable=True)  # 商品图片列表
    video_url = Column(String, nullable=True)  # 商品视频URL
    platform = Column(String, nullable=False, index=True)  # taobao, jd, pdd, xiaohongshu, douyin等
    platform_url = Column(String, nullable=False)
    platform_product_id = Column(String, nullable=True, index=True)  # 平台商品ID（用于爬虫）
    category_id = Column(Integer, ForeignKey("gift_categories.id"), nullable=True)
    description = Column(Text, nullable=True)
    
    # 销量相关
    sales_count = Column(Integer, nullable=True)  # 销量（件数）
    sales_amount = Column(Float, nullable=True)  # 销售额（估算，元）
    
    # 评价相关
    review_count = Column(Integer, nullable=True)  # 评价总数
    good_review_count = Column(Integer, nullable=True)  # 好评数
    bad_review_count = Column(Integer, nullable=True)  # 差评数
    good_review_rate = Column(Float, nullable=True)  # 好评率（0-1之间）
    average_rating = Column(Float, nullable=True)  # 平均评分（1-5星）
    
    # 店铺信息
    shop_name = Column(String, nullable=True)  # 店铺名称
    shop_url = Column(String, nullable=True)  # 店铺链接
    
    # 商品参数
    specifications = Column(JSON, nullable=True)  # 商品规格参数（JSON格式，如：{"品牌": "xxx", "颜色": "xxx"}）
    
    # 数据来源和元数据
    data_source = Column(String, nullable=True)  # api/crawler 数据来源
    last_updated = Column(DateTime(timezone=True), nullable=True)  # 最后更新时间
    crawl_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    category = relationship("Category", backref="products")
