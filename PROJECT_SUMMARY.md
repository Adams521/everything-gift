# AI礼品推荐系统 - 项目总结文档

> **生成时间**: 2024年
> **用途**: 当AI context满了后，开启新context时快速了解项目上下文

---

## 📋 项目概述

**项目名称**: AI礼品推荐系统  
**项目类型**: 全栈Web应用（前后端分离）  
**核心功能**: 基于AI的智能礼品推荐平台，帮助用户根据个性化条件（收礼人、场景、预算、风格等）选择最适合的礼品

**当前状态**: ✅ **核心功能已完成，可正常使用**

---

## 🛠️ 技术栈

### 前端
- **框架**: Next.js 15 + TypeScript
- **样式**: Tailwind CSS
- **UI组件**: shadcn/ui（计划中）
- **React版本**: 19.0.0

### 后端
- **框架**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy 2.0
- **数据库迁移**: Alembic
- **认证**: python-jose + passlib
- **异步HTTP**: httpx

### 数据库与缓存
- **主数据库**: PostgreSQL 15
- **缓存**: Redis 7

### 爬虫技术
- **浏览器自动化**: Playwright
- **HTML解析**: BeautifulSoup4 + lxml
- **HTTP客户端**: httpx

### 部署
- **容器化**: Docker + Docker Compose
- **前端部署**: Vercel（推荐）
- **后端部署**: 阿里云/腾讯云轻量服务器

---

## 📁 项目结构

```
/workspace
├── backend/                    # FastAPI后端应用
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   ├── auth.py        # 用户认证API
│   │   │   ├── products.py    # 商品API
│   │   │   ├── categories.py  # 分类API
│   │   │   └── recommendations.py  # 推荐API
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 配置管理
│   │   │   ├── database.py    # 数据库连接
│   │   │   └── security.py    # 安全相关
│   │   ├── models/            # SQLAlchemy模型
│   │   │   ├── user.py        # 用户模型
│   │   │   ├── product.py     # 商品模型
│   │   │   ├── category.py    # 分类模型
│   │   │   ├── review.py      # 评价模型
│   │   │   └── rating.py      # 评级模型
│   │   ├── schemas/           # Pydantic模型
│   │   ├── services/          # 业务逻辑服务
│   │   │   ├── taobao_union.py  # 淘宝联盟API
│   │   │   └── jd_union.py      # 京东联盟API
│   │   ├── crawlers/          # 爬虫模块
│   │   │   ├── taobao_crawler.py    # 淘宝爬虫
│   │   │   ├── union_crawler.py     # 联盟爬虫
│   │   │   └── save_products.py     # 保存商品脚本
│   │   └── main.py            # FastAPI应用入口
│   ├── alembic/               # 数据库迁移
│   ├── requirements.txt      # Python依赖
│   └── Dockerfile            # Docker镜像配置
│
├── frontend/                  # Next.js前端应用
│   ├── app/                  # App Router页面
│   │   ├── page.tsx          # 首页
│   │   ├── login/            # 登录页
│   │   ├── register/         # 注册页
│   │   ├── recommend/        # 推荐表单页
│   │   ├── results/          # 推荐结果页
│   │   └── products/         # 商品列表页
│   ├── package.json
│   └── Dockerfile
│
├── docs/                      # 项目文档
│   ├── 完整功能说明.md
│   ├── 开发完成总结.md
│   ├── 技术方案.md
│   ├── 接入淘宝联盟和京东联盟.md
│   └── ...
│
├── docker-compose.yml         # Docker编排配置
├── .env.example              # 环境变量示例
└── README.md                 # 项目说明
```

---

## ✅ 已完成功能

### 1. 数据库 ✅
- ✅ 数据库表已创建（users, categories, products, reviews, ratings）
- ✅ 已有90个商品数据
- ✅ 已有8个礼品分类
- ✅ 使用Alembic进行数据库迁移管理

### 2. 后端API ✅
- ✅ `/api/v1/products` - 商品列表API（支持分页、筛选）
- ✅ `/api/v1/products/{id}` - 商品详情API
- ✅ `/api/v1/categories` - 分类列表API
- ✅ `/api/v1/recommendations` - 推荐API（根据筛选条件推荐商品）
- ✅ `/api/v1/auth/*` - 用户认证API（登录、注册）

### 3. 前端页面 ✅
- ✅ 首页 (`/`) - 项目介绍和导航
- ✅ 推荐页面 (`/recommend`) - 推荐表单页面
- ✅ 结果页面 (`/results`) - 推荐结果展示页面
- ✅ 商品列表页面 (`/products`) - 浏览所有商品
- ✅ 登录/注册页面 (`/login`, `/register`)

### 4. 爬虫功能 ✅
- ✅ 淘宝爬虫 (`backend/app/crawlers/taobao_crawler.py`)
- ✅ 联盟爬虫 (`backend/app/crawlers/union_crawler.py`)
- ✅ 数据保存脚本 (`backend/app/crawlers/save_products.py`)
- ✅ 支持淘宝联盟和京东联盟API接入

### 5. 推荐系统 ✅
- ✅ 根据预算范围筛选商品
- ✅ 根据风格偏好匹配分类
- ✅ 生成推荐理由
- ⚠️ 当前使用简单规则引擎，后续可接入AI（OpenAI API）

---

## 🗄️ 数据库设计

### 核心表结构

**users** - 用户表
- id, email, password_hash, created_at, updated_at

**gift_categories** - 礼品分类表
- id, name, description, icon

**products** - 商品信息表
- id, name, price, image_url, platform, platform_url, category_id, description, crawl_at, created_at, updated_at

**reviews** - 评价数据表
- id, product_id, rating, comment, created_at

**ratings** - 评级结果表
- id, product_id, overall_grade, match_score, quality_score, price_score, reason, created_at

### 当前数据状态
- **商品数量**: 90个
- **分类数量**: 8个
- **平台**: 淘宝、京东、小红书

---

## 🔌 API端点

### 基础信息
- **Base URL**: `http://localhost:8000`
- **API前缀**: `/api/v1`
- **API文档**: `http://localhost:8000/docs` (Swagger UI)

### 主要端点

#### 商品相关
- `GET /api/v1/products` - 获取商品列表（支持分页、筛选）
- `GET /api/v1/products/{id}` - 获取商品详情

#### 分类相关
- `GET /api/v1/categories` - 获取分类列表

#### 推荐相关
- `POST /api/v1/recommendations` - 获取礼品推荐
  - 请求参数：收礼人类型、场景、预算范围、风格偏好等
  - 返回：推荐商品列表和推荐理由

#### 认证相关
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录

---

## 🚀 部署信息

### 开发环境（Docker Compose）

**服务端口**:
- 前端: `http://localhost:3000`
- 后端API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

**启动命令**:
```bash
docker-compose up -d
```

**停止命令**:
```bash
docker-compose down
```

### 环境变量配置

主要环境变量（见 `.env.example`）:
- `DATABASE_URL` - PostgreSQL连接字符串
- `REDIS_URL` - Redis连接字符串
- `DEBUG` - 调试模式
- `NEXT_PUBLIC_API_URL` - 前端API地址
- `CORS_ORIGINS` - CORS允许的来源
- `TAOBAO_UNION_APP_KEY/SECRET/PID` - 淘宝联盟配置
- `JD_UNION_APP_KEY/SECRET/SITE_ID` - 京东联盟配置

---

## 📝 关键文件说明

### 后端关键文件

1. **`backend/app/main.py`** - FastAPI应用入口，注册所有路由
2. **`backend/app/core/config.py`** - 配置管理，读取环境变量
3. **`backend/app/core/database.py`** - 数据库连接和会话管理
4. **`backend/app/api/recommendations.py`** - 推荐API实现（当前使用规则引擎）
5. **`backend/app/models/product.py`** - 商品数据模型
6. **`backend/app/crawlers/union_crawler.py`** - 联盟爬虫（支持淘宝/京东）

### 前端关键文件

1. **`frontend/app/page.tsx`** - 首页
2. **`frontend/app/recommend/page.tsx`** - 推荐表单页面
3. **`frontend/app/results/page.tsx`** - 推荐结果展示页面
4. **`frontend/app/products/page.tsx`** - 商品列表页面

### 文档文件

1. **`docs/完整功能说明.md`** - 功能清单和问题排查指南
2. **`docs/开发完成总结.md`** - 开发完成状态总结
3. **`docs/技术方案.md`** - 技术选型和架构设计
4. **`docs/接入淘宝联盟和京东联盟.md`** - 联盟API接入指南

---

## 🔧 常用操作

### 运行爬虫添加商品
```bash
docker compose exec backend python run_crawler.py
```

### 检查数据库状态
```bash
docker compose exec backend python -c "
from app.core.database import SessionLocal
from app.models import Product
db = SessionLocal()
print(f'商品数: {db.query(Product).count()}')
db.close()
"
```

### 查看服务日志
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### 重启服务
```bash
docker compose restart
```

---

## 🎯 下一步计划 / 待优化项

### 功能增强
- [ ] 接入真实AI推荐（OpenAI API）
- [ ] 实现真实爬虫（使用Playwright处理反爬虫）
- [ ] 添加商品搜索功能
- [ ] 实现商品评级系统（多维度评分）
- [ ] 优化推荐算法

### 用户体验
- [ ] 完善前端UI（使用shadcn/ui组件）
- [ ] 添加加载动画和错误处理
- [ ] 优化移动端适配

### 技术优化
- [ ] 添加API响应缓存（Redis）
- [ ] 实现限流和防刷机制
- [ ] 添加监控和日志系统
- [ ] 性能优化（数据库索引、查询优化）

### 部署优化
- [ ] 配置CI/CD自动化部署
- [ ] 配置生产环境变量
- [ ] 添加HTTPS和域名配置

---

## 📚 重要文档链接

- **项目README**: `/workspace/README.md`
- **完整功能说明**: `/workspace/docs/完整功能说明.md`
- **开发完成总结**: `/workspace/docs/开发完成总结.md`
- **技术方案**: `/workspace/docs/技术方案.md`
- **联盟API接入**: `/workspace/docs/接入淘宝联盟和京东联盟.md`

---

## ⚠️ 注意事项

1. **爬虫使用**: 当前爬虫返回模拟数据，实际使用需要处理反爬虫机制或使用官方API
2. **推荐算法**: 当前使用简单规则引擎，后续可接入AI提升推荐质量
3. **图片显示**: 如果图片不显示，需要配置联盟API或更新图片URL
4. **环境变量**: 生产环境需要配置真实的数据库和API密钥

---

## 🔗 快速链接

- **前端访问**: http://localhost:3000
- **后端API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

---

**最后更新**: 2024年  
**项目状态**: ✅ 核心功能已完成，可正常使用
