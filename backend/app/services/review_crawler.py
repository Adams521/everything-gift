"""
通用评价爬虫框架
支持多平台的商品评价数据爬取
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from playwright.async_api import async_playwright, Browser, Page
import asyncio
import re


class BaseReviewCrawler(ABC):
    """评价爬虫基类"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def init_browser(self, headless: bool = True):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=headless)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await context.new_page()
    
    async def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
    
    @abstractmethod
    async def crawl_reviews(
        self,
        product_id: str,
        platform_url: Optional[str] = None,
        max_reviews: int = 100
    ) -> Dict:
        """
        爬取商品评价
        
        Args:
            product_id: 商品ID
            platform_url: 商品链接
            max_reviews: 最大爬取评价数
        
        Returns:
            评价数据字典，包含：
            - review_count: 评价总数
            - good_review_count: 好评数
            - bad_review_count: 差评数
            - good_review_rate: 好评率
            - average_rating: 平均评分
            - reviews: 评价列表（可选）
        """
        pass
    
    def parse_rating(self, rating_text: str) -> Optional[float]:
        """解析评分文本为数字"""
        # 提取数字，如 "4.5分" -> 4.5
        match = re.search(r'(\d+\.?\d*)', rating_text)
        if match:
            return float(match.group(1))
        return None


class TaobaoReviewCrawler(BaseReviewCrawler):
    """淘宝评价爬虫"""
    
    async def crawl_reviews(
        self,
        product_id: str,
        platform_url: Optional[str] = None,
        max_reviews: int = 100
    ) -> Dict:
        """
        爬取淘宝商品评价
        
        注意：需要处理登录和反爬虫机制
        """
        if not self.page:
            await self.init_browser()
        
        try:
            # 构建评价页URL
            if not platform_url:
                platform_url = f"https://item.taobao.com/item.htm?id={product_id}"
            
            # 访问商品页面
            await self.page.goto(platform_url, wait_until="networkidle")
            await asyncio.sleep(2)  # 等待页面加载
            
            # 尝试获取评价数据
            # 注意：淘宝的评价数据可能需要登录才能查看完整数据
            review_data = {
                "review_count": 0,
                "good_review_count": 0,
                "bad_review_count": 0,
                "good_review_rate": None,
                "average_rating": None,
            }
            
            # 尝试从页面提取评价统计信息
            try:
                # 查找评价总数（需要根据实际页面结构调整选择器）
                review_count_elem = await self.page.query_selector(".tm-rate-counter")
                if review_count_elem:
                    review_count_text = await review_count_elem.inner_text()
                    review_count = int(re.search(r'\d+', review_count_text).group()) if re.search(r'\d+', review_count_text) else 0
                    review_data["review_count"] = review_count
                
                # 查找好评率
                good_rate_elem = await self.page.query_selector(".tm-rate-good")
                if good_rate_elem:
                    good_rate_text = await good_rate_elem.inner_text()
                    good_rate = self.parse_rating(good_rate_text)
                    if good_rate:
                        review_data["good_review_rate"] = good_rate / 100 if good_rate > 1 else good_rate
                        review_data["good_review_count"] = int(review_data["review_count"] * review_data["good_review_rate"])
                        review_data["bad_review_count"] = review_data["review_count"] - review_data["good_review_count"]
            except Exception as e:
                print(f"提取评价数据失败: {e}")
            
            return review_data
        
        except Exception as e:
            print(f"爬取淘宝评价失败: {e}")
            return {
                "review_count": None,
                "good_review_count": None,
                "bad_review_count": None,
                "good_review_rate": None,
                "average_rating": None,
            }
    
    async def __aenter__(self):
        await self.init_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_browser()


class JDReviewCrawler(BaseReviewCrawler):
    """京东评价爬虫"""
    
    async def crawl_reviews(
        self,
        product_id: str,
        platform_url: Optional[str] = None,
        max_reviews: int = 100
    ) -> Dict:
        """爬取京东商品评价"""
        if not self.page:
            await self.init_browser()
        
        try:
            # 构建评价页URL
            if not platform_url:
                platform_url = f"https://item.jd.com/{product_id}.html"
            
            # 访问商品页面
            await self.page.goto(platform_url, wait_until="networkidle")
            await asyncio.sleep(2)
            
            review_data = {
                "review_count": 0,
                "good_review_count": 0,
                "bad_review_count": 0,
                "good_review_rate": None,
                "average_rating": None,
            }
            
            # 尝试提取评价数据（需要根据实际页面结构调整）
            try:
                # 京东的评价数据通常在评论区域
                comment_count_elem = await self.page.query_selector("#comment-count")
                if comment_count_elem:
                    comment_text = await comment_count_elem.inner_text()
                    review_count = int(re.search(r'\d+', comment_text).group()) if re.search(r'\d+', comment_text) else 0
                    review_data["review_count"] = review_count
                
                # 查找好评率
                good_rate_elem = await self.page.query_selector(".percent")
                if good_rate_elem:
                    good_rate_text = await good_rate_elem.inner_text()
                    good_rate = self.parse_rating(good_rate_text)
                    if good_rate:
                        review_data["good_review_rate"] = good_rate / 100 if good_rate > 1 else good_rate
            except Exception as e:
                print(f"提取京东评价数据失败: {e}")
            
            return review_data
        
        except Exception as e:
            print(f"爬取京东评价失败: {e}")
            return {
                "review_count": None,
                "good_review_count": None,
                "bad_review_count": None,
                "good_review_rate": None,
                "average_rating": None,
            }
    
    async def __aenter__(self):
        await self.init_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_browser()


class ReviewCrawlerFactory:
    """评价爬虫工厂"""
    
    @staticmethod
    def create_crawler(platform: str) -> Optional[BaseReviewCrawler]:
        """创建对应平台的爬虫"""
        crawlers = {
            "taobao": TaobaoReviewCrawler,
            "jd": JDReviewCrawler,
            # 后续可以添加更多平台
        }
        
        crawler_class = crawlers.get(platform)
        if crawler_class:
            return crawler_class()
        return None


# 使用示例
async def example_usage():
    """使用示例"""
    # 爬取淘宝评价
    async with TaobaoReviewCrawler() as crawler:
        reviews = await crawler.crawl_reviews(
            product_id="123456789",
            platform_url="https://item.taobao.com/item.htm?id=123456789"
        )
        print(f"评价数据: {reviews}")
    
    # 使用工厂创建
    crawler = ReviewCrawlerFactory.create_crawler("taobao")
    if crawler:
        async with crawler:
            reviews = await crawler.crawl_reviews("123456789")
            print(f"评价数据: {reviews}")


if __name__ == "__main__":
    asyncio.run(example_usage())
