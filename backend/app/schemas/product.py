from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
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
    # 价格相关
    original_price: Optional[float] = None
    discount_price: Optional[float] = None
    
    # 图片和视频
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None
    
    # 平台商品ID
    platform_product_id: Optional[str] = None
    
    # 销量相关
    sales_count: Optional[int] = None
    sales_amount: Optional[float] = None
    
    # 评价相关
    review_count: Optional[int] = None
    good_review_count: Optional[int] = None
    bad_review_count: Optional[int] = None
    good_review_rate: Optional[float] = None
    average_rating: Optional[float] = None
    
    # 店铺信息
    shop_name: Optional[str] = None
    shop_url: Optional[str] = None
    
    # 商品规格
    specifications: Optional[Dict[str, Any]] = None
    
    # 数据来源
    data_source: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    
    # 价格相关
    original_price: Optional[float] = None
    discount_price: Optional[float] = None
    
    # 图片和视频
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None
    
    # 平台商品ID
    platform_product_id: Optional[str] = None
    
    # 销量相关
    sales_count: Optional[int] = None
    sales_amount: Optional[float] = None
    
    # 评价相关
    review_count: Optional[int] = None
    good_review_count: Optional[int] = None
    bad_review_count: Optional[int] = None
    good_review_rate: Optional[float] = None
    average_rating: Optional[float] = None
    
    # 店铺信息
    shop_name: Optional[str] = None
    shop_url: Optional[str] = None
    
    # 商品规格
    specifications: Optional[Dict[str, Any]] = None
    
    # 数据来源和元数据
    data_source: Optional[str] = None
    last_updated: Optional[datetime] = None
    crawl_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
