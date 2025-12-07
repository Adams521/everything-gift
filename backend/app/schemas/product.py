from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Optional[float] = None
    image_url: Optional[str] = None
    platform: str
    platform_url: str
    category_id: Optional[int] = None
    description: Optional[str] = None
    # 扩展的商品属性
    brand: Optional[str] = None
    material: Optional[str] = None
    suitable_scenes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    suitable_gender: Optional[str] = None
    suitable_age_range: Optional[str] = None
    style: Optional[str] = None
    rating: Optional[float] = None
    sales_count: Optional[int] = None
    stock_status: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    crawl_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
