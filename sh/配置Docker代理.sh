#!/bin/bash

echo "🔧 配置Docker使用代理（7890端口）..."

if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  需要sudo权限"
    exit 1
fi

# 创建代理配置目录
mkdir -p /etc/systemd/system/docker.service.d

# 配置代理
cat > /etc/systemd/system/docker.service.d/http-proxy.conf <<'EOF'
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,docker.io,registry-1.docker.io"
EOF

echo "✅ 已配置Docker代理"

# 重启Docker
echo "🔄 重启Docker服务..."
systemctl daemon-reload
systemctl restart docker

echo ""
echo "✅ 配置完成！"
echo ""
echo "📋 验证配置："
echo "   docker info | grep -i proxy"
echo ""
echo "🚀 现在可以重新启动："
echo "   docker compose up -d"
