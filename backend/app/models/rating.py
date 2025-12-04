from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    overall_grade = Column(String, nullable=False)  # 优/良/差
    match_score = Column(Float, nullable=True)  # 匹配度评分 0-1
    quality_score = Column(Float, nullable=True)  # 质量评分 0-1
    price_score = Column(Float, nullable=True)  # 价格合理性评分 0-1
    reason = Column(Text, nullable=True)  # 评级理由
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    product = relationship("Product", backref="rating")
