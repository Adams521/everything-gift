# 淘宝联盟和京东联盟API接入说明

## 🎯 目标

接入淘宝联盟和京东联盟，获取真实商品数据（包括图片、价格、详情等）。

## 📋 接入步骤

### 一、淘宝联盟接入

#### 1. 注册和申请

1. 访问：https://www.alimama.com/
2. 使用淘宝账号登录
3. 进入"媒体备案管理"，添加网站
4. 等待审核通过（1-3个工作日）
5. 申请API权限：
   - 点击"APPKEY申请"
   - 填写申请理由
   - 选择API权限
6. 获取凭证：
   - App Key
   - App Secret  
   - PID（推广位）

#### 2. 配置

在 `.env` 文件中添加：

```bash
TAOBAO_UNION_APP_KEY=your_app_key
TAOBAO_UNION_APP_SECRET=your_app_secret
TAOBAO_UNION_PID=mm_xxx_xxx_xxx
```

### 二、京东联盟接入

#### 1. 注册和申请

1. 访问：https://union.jd.com/
2. 使用京东账号登录
3. 进入"推广管理" -> "网站管理"，添加网站
4. 等待审核通过
5. 申请API权限，获取凭证

#### 2. 配置

在 `.env` 文件中添加：

```bash
JD_UNION_APP_KEY=your_app_key
JD_UNION_APP_SECRET=your_app_secret
JD_UNION_SITE_ID=your_site_id
```

## 💻 代码实现

### 已实现的文件

1. **淘宝联盟API**：`backend/app/services/taobao_union.py`
2. **京东联盟API**：`backend/app/services/jd_union.py`
3. **联盟爬虫**：`backend/app/crawlers/union_crawler.py`

### 使用方式

```python
from app.services.taobao_union import TaobaoUnionAPI
from app.services.jd_union import JDUnionAPI

# 淘宝联盟
taobao = TaobaoUnionAPI()
products = await taobao.search_products("生日礼物")

# 京东联盟
jd = JDUnionAPI()
products = await jd.search_products("生日礼物")
```

## 🖼️ 图片问题修复

### 已修复

1. ✅ 更新了爬虫代码，使用真实图片URL（Unsplash）
2. ✅ 创建了图片更新脚本
3. ✅ 前端添加了图片容错处理
4. ✅ 配置了Next.js图片域名白名单

### 运行图片更新

```bash
docker compose exec backend python 更新商品图片.py
```

## 🚀 使用联盟API

配置完成后，系统会自动使用联盟API：

```bash
# 运行爬虫（会自动检测是否配置了联盟API）
docker compose exec backend python -c "
import sys
sys.path.insert(0, '/app')
from app.crawlers.save_products import save_crawled_products
import asyncio
asyncio.run(save_crawled_products())
"
```

## ⚠️ 注意事项

1. **API限制**：注意调用频率限制
2. **数据更新**：定期更新商品数据
3. **合规使用**：遵守联盟使用规范
4. **佣金结算**：需要绑定收款账户

## 📚 参考文档

详细文档见：`docs/接入淘宝联盟和京东联盟.md`
