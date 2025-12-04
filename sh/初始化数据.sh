#!/bin/bash

echo "🗄️  初始化数据库数据..."

# 初始化基础数据
echo "📝 创建分类和示例商品..."
docker compose exec -T backend python -c "
import sys
sys.path.insert(0, '/app')
from scripts.init_data import init_data
init_data()
"

# 运行爬虫添加更多商品
echo "🕷️  运行爬虫添加商品数据..."
docker compose exec -T backend python -c "
import sys
sys.path.insert(0, '/app')
from app.crawlers.save_products import save_crawled_products
import asyncio
asyncio.run(save_crawled_products())
"

echo ""
echo "✅ 数据初始化完成！"
echo ""
echo "📊 验证数据："
echo "   curl http://localhost:8000/api/v1/products?limit=5"
