"""
淘宝联盟API接入
需要先申请淘宝联盟API权限
"""
import hashlib
import hmac
import time
import urllib.parse
from typing import List, Dict, Optional
import httpx
from app.core.config import settings

class TaobaoUnionAPI:
    """淘宝联盟API客户端"""
    
    def __init__(self, app_key: str = None, app_secret: str = None, pid: str = None):
        """
        初始化淘宝联盟API
        
        Args:
            app_key: 淘宝联盟App Key
            app_secret: 淘宝联盟App Secret
            pid: 推广位PID（格式：mm_xxx_xxx_xxx）
        """
        self.app_key = app_key or getattr(settings, 'TAOBAO_UNION_APP_KEY', '')
        self.app_secret = app_secret or getattr(settings, 'TAOBAO_UNION_APP_SECRET', '')
        self.pid = pid or getattr(settings, 'TAOBAO_UNION_PID', '')
        self.api_url = "https://eco.taobao.com/router/rest"
    
    def _generate_sign(self, params: dict) -> str:
        """生成签名"""
        # 排序参数
        sorted_params = sorted(params.items())
        # 拼接字符串
        string_to_sign = self.app_secret
        for key, value in sorted_params:
            string_to_sign += f"{key}{value}"
        string_to_sign += self.app_secret
        # MD5加密
        sign = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest().upper()
        return sign
    
    async def search_products(
        self, 
        keyword: str, 
        page_no: int = 1,
        page_size: int = 20,
        sort: str = "total_sales_des"  # 销量降序
    ) -> List[Dict]:
        """
        搜索商品（使用淘宝联盟API）
        
        Args:
            keyword: 搜索关键词
            page_no: 页码
            page_size: 每页数量
            sort: 排序方式
        """
        if not self.app_key or not self.app_secret:
            # 如果没有配置API密钥，返回模拟数据
            return self._generate_mock_products(keyword)
        
        try:
            # 构建请求参数
            params = {
                "method": "taobao.tbk.dg.material.optional",
                "app_key": self.app_key,
                "timestamp": str(int(time.time() * 1000)),
                "format": "json",
                "v": "2.0",
                "sign_method": "md5",
                "q": keyword,
                "page_no": str(page_no),
                "page_size": str(page_size),
                "sort": sort,
                "has_coupon": "true",  # 只获取有优惠券的商品
            }
            
            # 生成签名
            params["sign"] = self._generate_sign(params)
            
            # 发送请求
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # 解析响应
                if "tbk_dg_material_optional_response" in data:
                    result = data["tbk_dg_material_optional_response"]["result_list"]["map_data"]
                    products = []
                    for item in result:
                        product = {
                            "name": item.get("title", ""),
                            "price": float(item.get("zk_final_price", 0)),
                            "image_url": item.get("pict_url", ""),  # 商品主图
                            "platform": "taobao",
                            "platform_url": item.get("item_url", ""),
                            "description": item.get("short_title", ""),
                            "coupon_info": item.get("coupon_info", ""),  # 优惠券信息
                            "volume": item.get("volume", 0),  # 销量
                            "shop_title": item.get("shop_title", ""),  # 店铺名称
                        }
                        products.append(product)
                    return products
                else:
                    print(f"API返回错误: {data}")
                    return self._generate_mock_products(keyword)
        
        except Exception as e:
            print(f"调用淘宝联盟API失败: {e}")
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
                "name": f"{keyword}精选商品{i+1}",
                "price": round(random.uniform(50, 2000), 2),
                "image_url": image_urls[i % len(image_urls)],
                "platform": "taobao",
                "platform_url": f"https://item.taobao.com/item.htm?id={random.randint(100000000, 999999999)}",
                "description": f"优质{keyword}，适合作为礼品赠送，品质保证。",
            })
        return products
    
    async def get_product_detail(self, item_id: str) -> Optional[Dict]:
        """获取商品详情"""
        if not self.app_key or not self.app_secret:
            return None
        
        try:
            params = {
                "method": "taobao.tbk.item.info.get",
                "app_key": self.app_key,
                "timestamp": str(int(time.time() * 1000)),
                "format": "json",
                "v": "2.0",
                "sign_method": "md5",
                "num_iids": item_id,
            }
            
            params["sign"] = self._generate_sign(params)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                if "tbk_item_info_get_response" in data:
                    return data["tbk_item_info_get_response"]
                return None
        
        except Exception as e:
            print(f"获取商品详情失败: {e}")
            return None
