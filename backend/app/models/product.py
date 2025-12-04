from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
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
    crawl_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    category = relationship("Category", backref="products")
