from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, ARRAY, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    platform = Column(String, nullable=False)  # taobao, jd, xiaohongshu等
    platform_url = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("gift_categories.id"), nullable=True)
    description = Column(Text, nullable=True)
    
    # 扩展的商品属性字段
    brand = Column(String, nullable=True, index=True)  # 品牌
    material = Column(String, nullable=True)  # 材质
    suitable_scenes = Column(JSON, nullable=True)  # 适用场景，JSON数组格式，如["生日", "情人节", "纪念日"]
    tags = Column(JSON, nullable=True)  # 标签，JSON数组格式，如["实用", "创意", "浪漫"]
    suitable_gender = Column(String, nullable=True)  # 适用性别：male, female, unisex
    suitable_age_range = Column(String, nullable=True)  # 适用年龄段：如"18-25", "25-35", "35+"
    style = Column(String, nullable=True, index=True)  # 风格：实用型、创意型、浪漫型等
    rating = Column(Float, nullable=True)  # 商品评分（0-5分）
    sales_count = Column(Integer, nullable=True)  # 销量
    stock_status = Column(String, nullable=True)  # 库存状态：in_stock, out_of_stock, limited
    
    crawl_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    category = relationship("Category", backref="products")
