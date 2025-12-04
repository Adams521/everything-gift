from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.product import ProductResponse
from app.models.product import Product
from app.models.category import Category
from typing import List

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """根据筛选条件获取礼品推荐"""
    
    # 简单的推荐逻辑（后续可以接入AI）
    # 1. 根据预算筛选商品
    query = db.query(Product)
    
    if request.budget_min:
        query = query.filter(Product.price >= request.budget_min)
    if request.budget_max:
        query = query.filter(Product.price <= request.budget_max)
    
    # 2. 根据风格偏好匹配分类（简化版）
    categories = []
    if request.style:
        # 根据风格匹配分类
        category_map = {
            "实用型": ["电子产品", "家居用品", "健康设备"],
            "创意型": ["手办", "艺术品", "DIY工具"],
            "浪漫型": ["香水", "首饰", "花束"],
        }
        categories = category_map.get(request.style, [])
    
    # 3. 获取推荐商品（取前10个）
    products = query.limit(10).all()
    
    # 4. 生成推荐理由
    reasoning = f"根据您的筛选条件（"
    if request.recipient_type:
        reasoning += f"收礼人：{request.recipient_type}，"
    if request.occasion:
        reasoning += f"场景：{request.occasion}，"
    if request.budget_min and request.budget_max:
        reasoning += f"预算：{request.budget_min}-{request.budget_max}元，"
    if request.style:
        reasoning += f"风格：{request.style}，"
    reasoning = reasoning.rstrip("，") + "），为您推荐以下礼品。"
    
    return RecommendationResponse(
        categories=categories if categories else ["通用礼品"],
        products=[ProductResponse.model_validate(p) for p in products],
        reasoning=reasoning
    )
