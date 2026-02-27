"""
智能路由系统
对应课程：第36课-第6章综合实战项目

根据文章类型自动路由到对应的处理Pipeline
涉及知识点：第31课-RouterChain动态路由
"""

from .analyzer import ArticleAnalyzer
from .processor import ContentProcessor


class SmartRouter:
    """
    智能路由器
    
    流程：
    1. ArticleAnalyzer 分析文章类型
    2. 根据类型获取/创建对应的 ContentProcessor
    3. 执行处理并返回结果
    """

    def __init__(self):
        self.analyzer = ArticleAnalyzer()
        # 缓存已创建的processor，避免重复初始化
        self.processors = {}

    def route_and_process(self, article: str, callbacks=None) -> dict:
        """
        分析文章类型并路由到对应处理器
        
        Args:
            article: 文章内容
            callbacks: LangChain回调列表
            
        Returns:
            处理结果dict，包含 article_type, summary, keywords, translation, image_suggestions
        """
        # 1. 分析文章类型
        article_type = self.analyzer.analyze(article, callbacks)

        # 2. 获取或创建对应的processor（懒加载 + 缓存）
        if article_type not in self.processors:
            self.processors[article_type] = ContentProcessor(article_type)

        processor = self.processors[article_type]

        # 3. 处理文章
        result = processor.process(article, callbacks)

        # 4. 附加元数据
        result["article_type"] = article_type

        return result
