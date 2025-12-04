# 修复 Tailwind CSS 配置

## 问题

Next.js 15 与 Tailwind CSS v4 的配置方式发生了变化，需要使用 `@tailwindcss/postcss` 插件。

## 已修复

1. ✅ 更新 `package.json`：
   - 添加 `@tailwindcss/postcss`
   - 降级 `tailwindcss` 到 v3.4.1（更稳定）

2. ✅ 更新 `postcss.config.js`：
   - 使用 `@tailwindcss/postcss` 代替 `tailwindcss`

3. ✅ 更新 `globals.css`：
   - 使用 `@import "tailwindcss"` 代替旧的指令

## 重新构建

```bash
# 停止服务
docker compose down

# 重新构建前端
docker compose build frontend

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f frontend
```

## 如果使用 Tailwind CSS v3（更稳定）

如果 v4 还有问题，可以完全使用 v3：

```json
// package.json
"tailwindcss": "^3.4.1"
```

```js
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## 验证

访问 http://localhost:3000，应该不再有构建错误。
