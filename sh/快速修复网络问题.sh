#!/bin/bash

echo "🔧 配置Docker国内镜像源..."

# 检查是否有sudo权限
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  需要sudo权限，请运行: sudo ./快速修复网络问题.sh"
    exit 1
fi

# 备份原配置
if [ -f /etc/docker/daemon.json ]; then
    cp /etc/docker/daemon.json /etc/docker/daemon.json.bak
    echo "✅ 已备份原配置到 /etc/docker/daemon.json.bak"
fi

# 创建配置目录
mkdir -p /etc/docker

# 配置镜像加速器
cat > /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://dockerhub.azk8s.cn"
  ]
}
EOF

echo "✅ 已配置Docker镜像加速器"

# 重启Docker服务
echo "🔄 重启Docker服务..."
systemctl daemon-reload
systemctl restart docker

echo ""
echo "✅ 配置完成！"
echo ""
echo "📋 验证配置："
echo "   docker info | grep -A 5 'Registry Mirrors'"
echo ""
echo "🚀 现在可以重新构建："
echo "   docker compose build --no-cache"
echo "   或"
echo "   docker compose up -d"
