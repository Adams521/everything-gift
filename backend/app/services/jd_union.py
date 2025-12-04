"""
京东联盟API接入
需要先申请京东联盟API权限
"""
import hashlib
import hmac
import time
import urllib.parse
from typing import List, Dict, Optional
import httpx
from app.core.config import settings

class JDUnionAPI:
    """京东联盟API客户端"""
    
    def __init__(self, app_key: str = None, app_secret: str = None, site_id: str = None):
        """
        初始化京东联盟API
        
        Args:
            app_key: 京东联盟App Key
            app_secret: 京东联盟App Secret
            site_id: 网站ID/APPID
        """
        self.app_key = app_key or getattr(settings, 'JD_UNION_APP_KEY', '')
        self.app_secret = app_secret or getattr(settings, 'JD_UNION_APP_SECRET', '')
        self.site_id = site_id or getattr(settings, 'JD_UNION_SITE_ID', '')
        self.api_url = "https://router.jd.com/api"
    
    def _generate_sign(self, params: dict) -> str:
        """生成签名"""
        # 京东联盟签名算法
        sorted_params = sorted(params.items())
        string_to_sign = self.app_secret
        for key, value in sorted_params:
            if key != "sign":
                string_to_sign += f"{key}{value}"
        string_to_sign += self.app_secret
        sign = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest().upper()
        return sign
    
    async def search_products(
        self,
        keyword: str,
        page_index: int = 1,
        page_size: int = 20,
        sort_name: str = "wlCommissionShare"  # 佣金比例
    ) -> List[Dict]:
        """
        搜索商品（使用京东联盟API）
        
        Args:
            keyword: 搜索关键词
            page_index: 页码
            page_size: 每页数量
            sort_name: 排序字段
        """
        if not self.app_key or not self.app_secret:
            # 如果没有配置API密钥，返回模拟数据
            return self._generate_mock_products(keyword)
        
        try:
            # 构建请求参数
            params = {
                "method": "jd.union.open.goods.query",
                "app_key": self.app_key,
                "access_token": "",  # 需要先获取access_token
                "timestamp": str(int(time.time() * 1000)),
                "format": "json",
                "v": "1.0",
                "sign_method": "md5",
                "goodsReqDTO": {
                    "keyword": keyword,
                    "pageIndex": page_index,
                    "pageSize": page_size,
                    "sortName": sort_name,
                }
            }
            
            # 生成签名
            params["sign"] = self._generate_sign(params)
            
            # 发送请求
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # 解析响应
                if "jd_union_open_goods_query_response" in data:
                    result = data["jd_union_open_goods_query_response"]["result"]["data"]
                    products = []
                    for item in result:
                        product = {
                            "name": item.get("skuName", ""),
                            "price": float(item.get("priceInfo", {}).get("price", 0)),
                            "image_url": item.get("imageInfo", {}).get("imageList", [{}])[0].get("url", ""),
                            "platform": "jd",
                            "platform_url": item.get("materialUrl", ""),
                            "description": item.get("comments", 0),  # 评论数
                            "shop_name": item.get("shopInfo", {}).get("shopName", ""),
                        }
                        products.append(product)
                    return products
                else:
                    print(f"API返回错误: {data}")
                    return self._generate_mock_products(keyword)
        
        except Exception as e:
            print(f"调用京东联盟API失败: {e}")
            return self._generate_mock_products(keyword)
    
    def _generate_mock_products(self, keyword: str) -> List[Dict]:
        """生成模拟商品数据（当API未配置时）"""
        import random
        products = []
        # 使用真实的占位图服务
        image_urls = [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop",
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop",
            "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=300&h=300&fit=crop",
        ]
        
        for i in range(10):
            products.append({
                "name": f"【京东自营】{keyword}精选{i+1}",
                "price": round(random.uniform(50, 2000), 2),
                "image_url": image_urls[i % len(image_urls)],
                "platform": "jd",
                "platform_url": f"https://item.jd.com/{random.randint(1000000, 9999999)}.html",
                "description": f"京东自营{keyword}，正品保证，快速配送。",
            })
        return products
