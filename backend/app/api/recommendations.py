from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.core.database import get_db
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.product import ProductResponse
from app.models.product import Product
from app.models.category import Category
from app.services.ollama_service import ollama_service
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """根据筛选条件获取礼品推荐（使用AI模型分析）"""
    
    try:
        # 1. 使用AI模型分析用户请求，获取筛选条件和排序建议
        ai_analysis = ollama_service.analyze_user_request(
            recipient_type=request.recipient_type,
            age_range=request.age_range,
            gender=request.gender,
            relationship=request.relationship,
            occasion=request.occasion,
            budget_min=request.budget_min,
            budget_max=request.budget_max,
            style=request.style,
            mbti=request.mbti,
            zodiac=request.zodiac,
            interests=request.interests,
            user_query=request.user_query
        )
        
        filters = ai_analysis.get("filters", {})
        sort_by = ai_analysis.get("sort_by", "relevance")
        ai_reasoning = ai_analysis.get("reasoning", "")
        
        logger.info(f"AI分析结果: {ai_analysis}")
        
        # 2. 根据AI返回的筛选条件查询商品
        query = db.query(Product)
        
        # 价格筛选
        if filters.get("price_min"):
            query = query.filter(Product.price >= filters["price_min"])
        elif request.budget_min:  # 如果没有AI建议，使用用户输入
            query = query.filter(Product.price >= request.budget_min)
        
        if filters.get("price_max"):
            query = query.filter(Product.price <= filters["price_max"])
        elif request.budget_max:  # 如果没有AI建议，使用用户输入
            query = query.filter(Product.price <= request.budget_max)
        
        # 适用性别筛选
        if filters.get("suitable_gender"):
            query = query.filter(
                or_(
                    Product.suitable_gender == filters["suitable_gender"],
                    Product.suitable_gender == "unisex",
                    Product.suitable_gender.is_(None)
                )
            )
        
        # 适用年龄段筛选
        if filters.get("suitable_age_range"):
            query = query.filter(
                or_(
                    Product.suitable_age_range == filters["suitable_age_range"],
                    Product.suitable_age_range.is_(None)
                )
            )
        
        # 风格筛选
        if filters.get("style"):
            query = query.filter(
                or_(
                    Product.style == filters["style"],
                    Product.style.is_(None)
                )
            )
        elif request.style:  # 如果没有AI建议，使用用户输入
            query = query.filter(
                or_(
                    Product.style == request.style,
                    Product.style.is_(None)
                )
            )
        
        # 标签筛选（JSON字段，需要特殊处理）
        if filters.get("tags") and isinstance(filters["tags"], list):
            # 对于PostgreSQL的JSON字段，使用JSONB操作符
            # 这里简化处理，如果有标签匹配需求，可以进一步优化
            pass  # 暂时跳过标签筛选，因为需要更复杂的JSON查询
        
        # 适用场景筛选
        if filters.get("suitable_scenes") and isinstance(filters["suitable_scenes"], list):
            # 对于JSON字段的场景筛选，暂时跳过
            pass
        
        # 分类关键词匹配
        categories = []
        if filters.get("category_keywords") and isinstance(filters["category_keywords"], list):
            # 根据关键词查找分类
            category_query = db.query(Category).filter(
                or_(*[Category.name.like(f"%{keyword}%") for keyword in filters["category_keywords"]])
            )
            matched_categories = category_query.all()
            if matched_categories:
                category_ids = [cat.id for cat in matched_categories]
                query = query.filter(Product.category_id.in_(category_ids))
                categories = [cat.name for cat in matched_categories]
        
        # 3. 排序
        if sort_by == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort_by == "rating_desc":
            query = query.order_by(Product.rating.desc().nulls_last())
        elif sort_by == "sales_desc":
            query = query.order_by(Product.sales_count.desc().nulls_last())
        else:  # relevance 或其他
            # 默认排序：优先显示有评分和销量的商品
            query = query.order_by(
                Product.rating.desc().nulls_last(),
                Product.sales_count.desc().nulls_last(),
                Product.created_at.desc()
            )
        
        # 4. 获取推荐商品（取前10个）
        products = query.limit(10).all()
        
        # 5. 使用AI生成推荐理由
        if products:
            # 准备商品数据用于AI生成理由
            products_data = []
            for p in products:
                products_data.append({
                    "name": p.name,
                    "price": p.price,
                    "style": p.style,
                    "description": p.description or ""
                })
            
            # 准备用户请求数据
            user_request_data = {
                "user_query": request.user_query,
                "recipient_type": request.recipient_type,
                "age_range": request.age_range,
                "gender": request.gender,
                "relationship": request.relationship,
                "occasion": request.occasion,
                "budget_min": request.budget_min,
                "budget_max": request.budget_max,
                "style": request.style,
                "mbti": request.mbti,
                "zodiac": request.zodiac,
                "interests": request.interests
            }
            
            reasoning = ollama_service.generate_recommendation_reasoning(
                products_data,
                user_request_data
            )
        else:
            reasoning = "抱歉，没有找到符合您条件的商品，建议您调整筛选条件。"
        
        # 如果没有匹配的分类，使用默认分类
        if not categories:
            categories = ["通用礼品"]
        
        return RecommendationResponse(
            categories=categories,
            products=[ProductResponse.model_validate(p) for p in products],
            reasoning=reasoning
        )
        
    except Exception as e:
        logger.error(f"推荐API错误: {e}", exc_info=True)
        # 如果AI服务失败，回退到简单规则
        return await _fallback_recommendations(request, db)


async def _fallback_recommendations(
    request: RecommendationRequest,
    db: Session
) -> RecommendationResponse:
    """回退推荐逻辑（当AI服务不可用时使用）"""
    query = db.query(Product)
    
    # 根据预算筛选
    if request.budget_min:
        query = query.filter(Product.price >= request.budget_min)
    if request.budget_max:
        query = query.filter(Product.price <= request.budget_max)
    
    # 根据风格筛选
    categories = []
    if request.style:
        category_map = {
            "实用型": ["电子产品", "家居用品", "健康设备"],
            "创意型": ["手办", "艺术品", "DIY工具"],
            "浪漫型": ["香水", "首饰", "花束"],
        }
        categories = category_map.get(request.style, [])
        query = query.filter(
            or_(
                Product.style == request.style,
                Product.style.is_(None)
            )
        )
    
    # 排序并获取商品
    products = query.order_by(
        Product.rating.desc().nulls_last(),
        Product.created_at.desc()
    ).limit(10).all()
    
    # 生成简单推荐理由
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
