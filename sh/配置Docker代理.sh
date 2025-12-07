#!/bin/bash

# 配置 Docker 使用代理（用于加速镜像拉取）
# 支持自定义代理地址

set -e

echo "=========================================="
echo "配置 Docker 代理"
echo "=========================================="

# 检查是否有 sudo 权限
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  需要 sudo 权限，请运行: sudo bash sh/配置Docker代理.sh"
    exit 1
fi

# 获取代理地址
PROXY_HOST="${PROXY_HOST:-127.0.0.1}"
PROXY_PORT="${PROXY_PORT:-7890}"

# 如果通过参数传入
if [ -n "$1" ]; then
    PROXY_HOST=$(echo "$1" | cut -d: -f1)
    PROXY_PORT=$(echo "$1" | cut -d: -f2)
fi

PROXY_URL="http://${PROXY_HOST}:${PROXY_PORT}"

echo ""
echo "代理地址: $PROXY_URL"
echo "（可以通过环境变量 PROXY_HOST 和 PROXY_PORT 自定义）"
echo ""

# 创建代理配置目录
mkdir -p /etc/systemd/system/docker.service.d

# 备份原配置
if [ -f /etc/systemd/system/docker.service.d/http-proxy.conf ]; then
    cp /etc/systemd/system/docker.service.d/http-proxy.conf /etc/systemd/system/docker.service.d/http-proxy.conf.bak
    echo "✓ 已备份原配置"
fi

# 配置代理
cat > /etc/systemd/system/docker.service.d/http-proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=$PROXY_URL"
Environment="HTTPS_PROXY=$PROXY_URL"
Environment="NO_PROXY=localhost,127.0.0.1,*.local,169.254/16"
EOF

echo "✓ 已配置 Docker 代理"

# 重启 Docker
echo ""
echo "重启 Docker 服务..."
systemctl daemon-reload
systemctl restart docker

echo ""
echo "✅ 配置完成！"
echo ""
echo "验证配置："
docker info 2>/dev/null | grep -i proxy || echo "  未显示代理信息（可能需要等待几秒）"

echo ""
echo "现在可以使用代理拉取镜像："
echo "  docker compose up ollama"
echo ""
echo "取消代理配置："
echo "  sudo rm /etc/systemd/system/docker.service.d/http-proxy.conf"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl restart docker"
