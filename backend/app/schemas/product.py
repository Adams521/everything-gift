from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Optional[float] = None
    image_url: Optional[str] = None
    platform: str
    platform_url: str
    category_id: Optional[int] = None
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    crawl_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
