#!/bin/bash

echo "🔧 立即修复Docker网络问题..."

# 1. 停止当前构建
echo "⏹️  停止当前构建..."
docker compose down 2>/dev/null || true

# 2. 重启Docker服务（使镜像源配置生效）
echo "🔄 重启Docker服务（需要sudo权限）..."
if [ "$EUID" -eq 0 ]; then
    systemctl daemon-reload
    systemctl restart docker
    echo "✅ Docker服务已重启"
else
    echo "⚠️  需要sudo权限重启Docker，请运行："
    echo "   sudo systemctl restart docker"
    echo "   然后继续执行此脚本"
    read -p "按Enter继续..."
fi

# 3. 清理未完成的构建
echo "🧹 清理未完成的构建..."
docker system prune -f

# 4. 测试镜像源连接
echo "📡 测试镜像源连接..."
if curl -s -o /dev/null -w "%{http_code}" https://docker.mirrors.ustc.edu.cn/v2/ | grep -q "200\|401"; then
    echo "✅ 镜像源连接正常"
else
    echo "⚠️  镜像源连接异常，但继续尝试..."
fi

# 5. 重新构建（使用国内镜像）
echo "🚀 开始重新构建（使用国内镜像源）..."
echo "   这可能需要几分钟，请耐心等待..."
docker compose build --no-cache

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 构建成功！"
    echo ""
    echo "🚀 启动服务..."
    docker compose up -d
    
    echo ""
    echo "✅ 服务启动完成！"
    echo ""
    echo "📍 访问地址："
    echo "   前端: http://localhost:3000"
    echo "   后端API: http://localhost:8000"
    echo "   API文档: http://localhost:8000/docs"
else
    echo ""
    echo "❌ 构建失败，请检查网络连接或查看错误信息"
    echo ""
    echo "💡 其他解决方案："
    echo "   1. 检查网络连接"
    echo "   2. 尝试使用VPN"
    echo "   3. 手动拉取镜像："
    echo "      docker pull docker.mirrors.ustc.edu.cn/library/python:3.12-slim"
fi
