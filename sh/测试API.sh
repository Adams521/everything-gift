#!/bin/bash

echo "🧪 测试API连接..."

echo ""
echo "1. 测试健康检查..."
curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "失败"

echo ""
echo "2. 测试商品列表API..."
curl -s 'http://localhost:8000/api/v1/products?limit=3' | python3 -m json.tool 2>/dev/null | head -30 || echo "失败"

echo ""
echo "3. 测试推荐API..."
curl -X POST 'http://localhost:8000/api/v1/recommendations' \
  -H 'Content-Type: application/json' \
  -d '{"budget_min":100,"budget_max":500,"style":"实用型"}' \
  2>/dev/null | python3 -m json.tool 2>/dev/null | head -30 || echo "失败"

echo ""
echo "✅ 测试完成"
