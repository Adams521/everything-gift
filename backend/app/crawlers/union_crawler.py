"""
使用淘宝联盟和京东联盟API爬取商品
"""
import asyncio
from typing import List, Dict
from app.services.taobao_union import TaobaoUnionAPI
from app.services.jd_union import JDUnionAPI

class UnionCrawler:
    """联盟API爬虫（淘宝联盟+京东联盟）"""
    
    def __init__(self):
        self.taobao_api = TaobaoUnionAPI()
        self.jd_api = JDUnionAPI()
    
    async def crawl_products(self, keywords: List[str]) -> List[Dict]:
        """
        爬取商品数据
        
        Args:
            keywords: 搜索关键词列表
        """
        all_products = []
        
        for keyword in keywords:
            # 从淘宝联盟获取
            try:
                taobao_products = await self.taobao_api.search_products(keyword)
                all_products.extend(taobao_products)
            except Exception as e:
                print(f"淘宝联盟爬取失败: {e}")
            
            # 从京东联盟获取
            try:
                jd_products = await self.jd_api.search_products(keyword)
                all_products.extend(jd_products)
            except Exception as e:
                print(f"京东联盟爬取失败: {e}")
            
            # 延时
            await asyncio.sleep(1)
        
        return all_products


async def main():
    """测试爬虫"""
    crawler = UnionCrawler()
    keywords = ["生日礼物", "情人节礼物", "母亲节礼物"]
    products = await crawler.crawl_products(keywords)
    print(f"爬取了 {len(products)} 个商品")
    for p in products[:3]:
        print(f"  - {p['name']} (¥{p['price']}) - {p.get('image_url', '无图片')[:50]}")


if __name__ == "__main__":
    asyncio.run(main())
