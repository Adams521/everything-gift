# 配置Docker国内镜像源

## 问题
Docker构建时卡在下载镜像metadata，通常是网络问题（国内访问Docker Hub慢或被墙）。

## 解决方案

### 方案1：配置Docker镜像加速器（推荐）✅

编辑或创建 `/etc/docker/daemon.json`：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
EOF

# 重启Docker服务
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 方案2：使用阿里云镜像加速器

1. 登录阿里云容器镜像服务：https://cr.console.aliyun.com/
2. 获取专属加速地址
3. 配置到 `/etc/docker/daemon.json`

### 方案3：使用代理

如果有代理，可以配置Docker使用代理：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf <<-'EOF'
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 验证配置

```bash
docker info | grep -A 10 "Registry Mirrors"
```

## 重新构建

配置完成后，重新构建：

```bash
# 停止当前构建（Ctrl+C）
docker compose down

# 清理未完成的构建
docker system prune -f

# 重新构建
docker compose build --no-cache

# 或直接启动（会自动构建）
docker compose up -d
```

## 临时解决方案：使用国内镜像

如果配置镜像源后仍然很慢，可以修改Dockerfile使用国内镜像：

### 修改 backend/Dockerfile

```dockerfile
# 使用阿里云镜像
FROM registry.cn-hangzhou.aliyuncs.com/acs/python:3.12-slim
```

或者使用中科大镜像：

```dockerfile
FROM docker.mirrors.ustc.edu.cn/library/python:3.12-slim
```
