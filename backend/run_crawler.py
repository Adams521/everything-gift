"""
运行爬虫脚本
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.crawlers.save_products import save_crawled_products

if __name__ == "__main__":
    print("🕷️  开始爬取商品数据...")
    asyncio.run(save_crawled_products())
    print("✅ 爬取完成！")
