"""
Ollama服务 - 封装本地Ollama模型调用
用于分析用户输入并生成商品筛选和排序建议
"""
import ollama
from typing import Dict, List, Optional, Any
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class OllamaService:
    """Ollama服务类，用于调用本地Ollama模型"""
    
    def __init__(self, model_name: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化Ollama服务
        
        Args:
            model_name: 模型名称，默认从配置读取
            base_url: Ollama服务地址，默认从配置读取
        """
        self.model_name = model_name or settings.OLLAMA_MODEL_NAME
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.enabled = settings.OLLAMA_ENABLED
        self.client = None
        
        if self.enabled:
            # 尝试连接Ollama服务，如果配置的地址失败，尝试其他常见地址
            success = self._try_connect_ollama(self.base_url)
            
            # 如果配置的地址失败，尝试其他地址（适用于Docker环境）
            if not success:
                alternative_urls = [
                    "http://ollama:11434",  # Docker Compose 服务名（优先）
                    "http://host.docker.internal:11434",  # Docker Desktop / Docker 20.10+
                    "http://172.17.0.1:11434",  # Docker默认网关（Linux）
                    "http://localhost:11434",  # 本地运行
                ]
                
                for alt_url in alternative_urls:
                    if alt_url != self.base_url:
                        logger.info(f"尝试备用地址: {alt_url}")
                        if self._try_connect_ollama(alt_url):
                            self.base_url = alt_url
                            logger.info(f"使用备用地址连接成功: {alt_url}")
                            break
                
                if not self.client:
                    logger.warning("所有Ollama连接尝试均失败，将使用回退逻辑")
                    self.enabled = False
        else:
            logger.info("Ollama服务已禁用")
    
    def _try_connect_ollama(self, url: str) -> bool:
        """尝试连接Ollama服务"""
        try:
            self.client = ollama.Client(host=url)
            # 测试连接
            self.client.list()
            logger.info(f"Ollama服务已连接: {url}, 模型: {self.model_name}")
            return True
        except Exception as e:
            logger.debug(f"连接 {url} 失败: {e}")
            self.client = None
            return False
    
    def analyze_user_request(
        self, 
        recipient_type: Optional[str] = None,
        age_range: Optional[str] = None,
        gender: Optional[str] = None,
        relationship: Optional[str] = None,
        occasion: Optional[str] = None,
        budget_min: Optional[float] = None,
        budget_max: Optional[float] = None,
        style: Optional[str] = None,
        mbti: Optional[str] = None,
        zodiac: Optional[str] = None,
        interests: Optional[List[str]] = None,
        user_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分析用户请求，生成商品筛选和排序建议
        
        Returns:
            包含筛选条件和排序建议的字典
        """
        # 构建用户输入描述
        user_input = self._build_user_input_description(
            recipient_type, age_range, gender, relationship, occasion,
            budget_min, budget_max, style, mbti, zodiac, interests, user_query
        )
        
        # 构建提示词
        prompt = self._build_analysis_prompt(user_input)
        
        if not self.enabled or not self.client:
            return self._get_default_filters(budget_min, budget_max, style)
        
        try:
            # 调用Ollama模型
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,  # 降低温度以获得更稳定的输出
                    "top_p": 0.9,
                }
            )
            
            # 解析模型响应
            result = self._parse_model_response(response.get("response", ""))
            return result
            
        except Exception as e:
            logger.error(f"Ollama模型调用失败: {e}")
            # 返回默认的筛选条件
            return self._get_default_filters(
                budget_min, budget_max, style
            )
    
    def generate_recommendation_reasoning(
        self,
        products: List[Dict[str, Any]],
        user_request: Dict[str, Any]
    ) -> str:
        """
        为推荐的商品生成推荐理由
        
        Args:
            products: 推荐的商品列表
            user_request: 用户请求信息
            
        Returns:
            推荐理由文本
        """
        # 构建提示词
        prompt = self._build_reasoning_prompt(products, user_request)
        
        if not self.enabled or not self.client:
            return "根据您的筛选条件，为您推荐了以下商品。"
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.7,  # 稍高温度以获得更自然的文本
                    "top_p": 0.9,
                }
            )
            
            reasoning = response.get("response", "").strip()
            return reasoning if reasoning else "根据您的需求，为您推荐了以下商品。"
            
        except Exception as e:
            logger.error(f"生成推荐理由失败: {e}")
            return "根据您的筛选条件，为您推荐了以下商品。"
    
    def _build_user_input_description(
        self,
        recipient_type: Optional[str],
        age_range: Optional[str],
        gender: Optional[str],
        relationship: Optional[str],
        occasion: Optional[str],
        budget_min: Optional[float],
        budget_max: Optional[float],
        style: Optional[str],
        mbti: Optional[str],
        zodiac: Optional[str],
        interests: Optional[List[str]],
        user_query: Optional[str]
    ) -> str:
        """构建用户输入描述"""
        parts = []
        
        if user_query:
            parts.append(f"用户描述: {user_query}")
        
        if recipient_type:
            parts.append(f"收礼人类型: {recipient_type}")
        
        if age_range:
            parts.append(f"年龄段: {age_range}")
        
        if gender:
            parts.append(f"性别: {gender}")
        
        if relationship:
            parts.append(f"关系: {relationship}")
        
        if occasion:
            parts.append(f"场景: {occasion}")
        
        if budget_min and budget_max:
            parts.append(f"预算: {budget_min}-{budget_max}元")
        elif budget_min:
            parts.append(f"最低预算: {budget_min}元")
        elif budget_max:
            parts.append(f"最高预算: {budget_max}元")
        
        if style:
            parts.append(f"风格偏好: {style}")
        
        if mbti:
            parts.append(f"MBTI: {mbti}")
        
        if zodiac:
            parts.append(f"星座: {zodiac}")
        
        if interests:
            parts.append(f"兴趣爱好: {', '.join(interests)}")
        
        return "；".join(parts) if parts else "通用礼品推荐"
    
    def _build_analysis_prompt(self, user_input: str) -> str:
        """构建分析提示词"""
        return f"""你是一个专业的礼品推荐AI助手。请根据用户的以下需求，分析并返回JSON格式的商品筛选和排序建议。

用户需求：
{user_input}

请分析用户需求，并返回一个JSON对象，包含以下字段：
1. "filters": 筛选条件对象
   - "price_min": 最低价格（数字，可选）
   - "price_max": 最高价格（数字，可选）
   - "suitable_gender": 适用性别（"male", "female", "unisex"或null）
   - "suitable_age_range": 适用年龄段（字符串，如"18-25", "25-35", "35+"或null）
   - "style": 风格（"实用型", "创意型", "浪漫型"等或null）
   - "tags": 标签列表（字符串数组，如["实用", "创意", "浪漫"]或null）
   - "suitable_scenes": 适用场景列表（字符串数组，如["生日", "情人节"]或null）
   - "category_keywords": 分类关键词列表（字符串数组，用于匹配商品分类，如["电子产品", "首饰"]或null）

2. "sort_by": 排序方式（"price_asc", "price_desc", "rating_desc", "sales_desc"或"relevance"）
3. "reasoning": 简要说明筛选逻辑（字符串）

只返回JSON对象，不要包含其他文字说明。JSON格式示例：
{{
  "filters": {{
    "price_min": 100,
    "price_max": 500,
    "suitable_gender": "female",
    "style": "浪漫型",
    "tags": ["浪漫", "精致"],
    "suitable_scenes": ["情人节", "纪念日"]
  }},
  "sort_by": "relevance",
  "reasoning": "根据用户需求，推荐适合女性的浪漫型礼品，价格在100-500元之间"
}}
"""
    
    def _build_reasoning_prompt(self, products: List[Dict[str, Any]], user_request: Dict[str, Any]) -> str:
        """构建推荐理由生成提示词"""
        products_summary = []
        for i, product in enumerate(products[:5], 1):  # 只取前5个商品
            products_summary.append(
                f"{i}. {product.get('name', '')} - "
                f"价格: {product.get('price', 0)}元, "
                f"风格: {product.get('style', '')}, "
                f"描述: {product.get('description', '')[:50]}"
            )
        
        user_input = self._build_user_input_description(
            user_request.get('recipient_type'),
            user_request.get('age_range'),
            user_request.get('gender'),
            user_request.get('relationship'),
            user_request.get('occasion'),
            user_request.get('budget_min'),
            user_request.get('budget_max'),
            user_request.get('style'),
            user_request.get('mbti'),
            user_request.get('zodiac'),
            user_request.get('interests'),
            user_request.get('user_query')
        )
        
        return f"""你是一个专业的礼品推荐AI助手。请根据用户需求和推荐的商品，生成一段自然、友好的推荐理由（100-200字）。

用户需求：
{user_input}

推荐的商品：
{chr(10).join(products_summary)}

请生成推荐理由，说明为什么这些商品适合用户的需求。语言要自然、友好，不要使用列表格式。
"""
    
    def _parse_model_response(self, response_text: str) -> Dict[str, Any]:
        """解析模型响应，提取JSON"""
        try:
            # 尝试提取JSON部分
            response_text = response_text.strip()
            
            # 如果响应包含代码块，提取其中的JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            
            # 尝试找到JSON对象
            start_brace = response_text.find("{")
            end_brace = response_text.rfind("}")
            if start_brace != -1 and end_brace != -1:
                response_text = response_text[start_brace:end_brace + 1]
            
            # 解析JSON
            result = json.loads(response_text)
            return result
            
        except json.JSONDecodeError as e:
            logger.warning(f"解析模型响应失败: {e}, 响应内容: {response_text[:200]}")
            return {
                "filters": {},
                "sort_by": "relevance",
                "reasoning": "根据您的需求进行了商品筛选"
            }
    
    def _get_default_filters(
        self,
        budget_min: Optional[float],
        budget_max: Optional[float],
        style: Optional[str]
    ) -> Dict[str, Any]:
        """获取默认筛选条件"""
        filters = {}
        
        if budget_min:
            filters["price_min"] = budget_min
        if budget_max:
            filters["price_max"] = budget_max
        if style:
            filters["style"] = style
        
        return {
            "filters": filters,
            "sort_by": "relevance",
            "reasoning": "根据您的筛选条件进行了商品推荐"
        }


# 创建全局实例
ollama_service = OllamaService()

