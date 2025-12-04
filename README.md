# AI礼品推荐系统

基于AI的智能礼品推荐平台，帮助用户根据个性化条件选择最适合的礼品。

## 技术栈

### 前端
- **框架**: Next.js 15 + TypeScript
- **样式**: Tailwind CSS
- **UI组件**: shadcn/ui（待安装）

### 后端
- **框架**: FastAPI (Python 3.12)
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **ORM**: SQLAlchemy 2.0

### 部署
- **容器化**: Docker + Docker Compose
- **前端部署**: Vercel（推荐）
- **后端部署**: 阿里云/腾讯云轻量服务器

## 项目结构

```
gift/
├── frontend/          # Next.js前端应用
│   ├── app/           # App Router页面
│   ├── components/    # React组件
│   └── package.json
├── backend/           # FastAPI后端应用
│   ├── app/
│   │   ├── api/       # API路由
│   │   ├── core/      # 核心配置
│   │   ├── models/    # 数据库模型
│   │   ├── schemas/   # Pydantic模型
│   │   ├── services/  # 业务逻辑
│   │   └── crawlers/  # 爬虫模块
│   └── requirements.txt
├── database/          # 数据库迁移脚本
├── docker-compose.yml # Docker编排配置
└── README.md
```

## 快速开始

### 前置要求

- Docker & Docker Compose
- Node.js 20+ (如果本地运行前端)
- Python 3.12+ (如果本地运行后端)

### 使用Docker Compose（推荐）

1. **克隆项目**
   ```bash
   cd /home/jiaxidai/code/gift
   ```

2. **启动所有服务**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   - 前端: http://localhost:3000
   - 后端API: http://localhost:8000
   - API文档: http://localhost:8000/docs

4. **停止服务**
   ```bash
   docker-compose down
   ```

### 本地开发

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

#### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 数据库初始化

1. **创建数据库表**
   ```bash
   # 进入后端容器
   docker-compose exec backend bash
   
   # 运行Alembic迁移（待创建）
   alembic upgrade head
   ```

2. **初始化数据**
   ```bash
   # 运行初始化脚本（待创建）
   python scripts/init_data.py
   ```

## 开发任务

- [x] 项目架构设计与技术选型
- [x] 创建项目目录结构
- [x] 初始化前端项目（Next.js）
- [x] 初始化后端项目（FastAPI）
- [x] 配置Docker开发环境
- [ ] 设计数据库Schema
- [ ] 实现数据库迁移
- [ ] 搭建前端UI框架
- [ ] 开发数据爬取模块
- [ ] 实现AI推荐引擎
- [ ] 开发商品评级系统
- [ ] 配置云端部署

## 环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

## API文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 部署

### 前端部署（Vercel）

1. 连接GitHub仓库
2. 配置环境变量 `NEXT_PUBLIC_API_URL`
3. 自动部署

### 后端部署（阿里云）

1. 购买轻量应用服务器
2. 安装Docker
3. 上传代码并运行 `docker-compose up -d`

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
