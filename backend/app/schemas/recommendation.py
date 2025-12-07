from pydantic import BaseModel
from typing import Optional, List
from app.schemas.product import ProductResponse

class RecommendationRequest(BaseModel):
    # 自然语言查询（可选，用于AI理解用户需求）
    user_query: Optional[str] = None  # 用户自然语言描述，如"想给女朋友买生日礼物，预算500元左右"
    
    # 人群维度
    recipient_type: Optional[str] = None  # 男/女友、父母、同事等
    age_range: Optional[str] = None  # 年龄段
    gender: Optional[str] = None  # 性别
    relationship: Optional[str] = None  # 关系亲密度
    
    # 场景用途
    occasion: Optional[str] = None  # 生日、纪念日、节日等
    
    # 预算价位
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    
    # 风格偏好
    style: Optional[str] = None  # 实用型、创意型、浪漫型等
    
    # 个性信息
    mbti: Optional[str] = None
    zodiac: Optional[str] = None
    interests: Optional[List[str]] = None

class RecommendationResponse(BaseModel):
    categories: List[str]  # 推荐的品类列表
    products: List[ProductResponse]  # 推荐的商品列表
    reasoning: str  # 推荐理由
