from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import products, categories, recommendations, auth

app = FastAPI(
    title="AI礼品推荐系统 API",
    description="基于AI的智能礼品推荐平台后端API",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(categories.router, prefix=settings.API_V1_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {"message": "AI礼品推荐系统 API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
