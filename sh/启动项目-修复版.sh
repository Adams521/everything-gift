#!/bin/bash

echo "🚀 启动AI礼品推荐系统（使用Docker Compose V2）..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 使用Docker Compose V2（推荐）
if ! docker compose version > /dev/null 2>&1; then
    echo "❌ Docker Compose V2不可用，请更新Docker"
    echo "   或者尝试: sudo apt-get update && sudo apt-get install docker-compose-plugin"
    exit 1
fi

echo "✅ 使用 Docker Compose V2"
echo "📦 启动Docker服务..."
docker compose up -d

echo "⏳ 等待服务启动..."
sleep 5

echo "🗄️  初始化数据库..."
# 等待PostgreSQL就绪
until docker compose exec -T postgres pg_isready -U user > /dev/null 2>&1; do
    echo "等待PostgreSQL启动..."
    sleep 2
done

# 运行数据库迁移
echo "📊 运行数据库迁移..."
docker compose exec -T backend alembic upgrade head 2>/dev/null || {
    echo "⚠️  首次运行，创建初始迁移..."
    docker compose exec -T backend alembic revision --autogenerate -m "Initial migration" || true
    docker compose exec -T backend alembic upgrade head || true
}

# 初始化示例数据
echo "📝 初始化示例数据..."
docker compose exec -T backend python scripts/init_data.py || {
    echo "⚠️  数据初始化失败，可能需要先创建表"
}

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📍 访问地址："
echo "   前端: http://localhost:3000"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "📋 查看日志: docker compose logs -f"
echo "🛑 停止服务: docker compose down"
