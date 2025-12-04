FROM node:20-alpine

WORKDIR /app

# 复制package文件（单独一层，只有package.json变化时才重新安装依赖）
# 这是增量构建的关键：依赖安装和代码复制分离
COPY package.json package-lock.json* ./

# 安装依赖（使用npm ci如果存在package-lock.json，否则用npm install）
# 只有当package.json或package-lock.json变化时，这一层才会重新构建
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# 复制应用代码（放在最后，代码变化时只重建这一层）
# 由于docker-compose.yml中使用了volumes挂载，实际运行时代码是实时同步的
# 但构建时仍需要复制，以便在没有挂载时也能运行
COPY . .

# 暴露端口
EXPOSE 3000

# 开发模式启动命令（支持热重载）
CMD ["npm", "run", "dev"]
