# 使用原始Docker Hub（通过代理访问）
FROM python:3.12-slim

WORKDIR /app

# 配置pip使用国内镜像源（多个备用源）
# 这一层很少变化，放在前面以利用缓存
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host "pypi.tuna.tsinghua.edu.cn pypi.douban.com mirrors.aliyun.com" && \
    pip config set global.timeout 60

# 安装系统依赖（使用阿里云apt源加速）
# 系统依赖很少变化，放在前面
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list 2>/dev/null || true && \
    apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 升级pip到最新版本
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 复制依赖文件（单独一层，只有requirements.txt变化时才重新安装依赖）
# 这是增量构建的关键：依赖安装和代码复制分离
COPY requirements.txt .

# 安装Python依赖（使用已配置的国内源，增加超时时间）
# 只有当requirements.txt变化时，这一层才会重新构建
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt || \
    (echo "使用备用源重试..." && \
     pip install --no-cache-dir --default-timeout=100 \
     -i https://pypi.douban.com/simple/ \
     --trusted-host pypi.douban.com \
     -r requirements.txt)

# 复制应用代码（放在最后，代码变化时只重建这一层）
# 由于docker-compose.yml中使用了volumes挂载，实际运行时代码是实时同步的
# 但构建时仍需要复制，以便在没有挂载时也能运行
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令（使用--reload支持热重载）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
