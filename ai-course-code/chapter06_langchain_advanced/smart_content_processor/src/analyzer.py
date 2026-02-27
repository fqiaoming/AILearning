"""
文章类型分析器
对应课程：第36课-第6章综合实战项目

使用LLM判断文章类型（tech/news/general），作为Router的决策依据
涉及知识点：第31课-RouterChain动态路由
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from .config import config


class ArticleAnalyzer:
    """
    文章类型分析器
    
    将文章分为三类：
    - tech: 技术文章（编程、框架、算法等）
    - news: 新闻报道（时事、公告、发布等）
    - general: 普通文章（生活、随笔等）
    """

    def __init__(self):
        """初始化分析器"""
        if config.USE_LOCAL_MODEL:
            self.llm = ChatOpenAI(
                base_url=config.LM_STUDIO_BASE_URL,
                api_key=config.LM_STUDIO_API_KEY,
                model=config.LM_STUDIO_MODEL,
                temperature=0,
            )
        else:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        prompt = ChatPromptTemplate.from_template(
            "分析以下文章的类型，只返回一个词：tech（技术）、news（新闻）或 general（普通）\n\n"
            "文章内容：\n{article}\n\n类型："
        )

        self.chain = prompt | self.llm | StrOutputParser()

    def analyze(self, article: str, callbacks=None) -> str:
        """
        分析文章类型
        
        Args:
            article: 文章内容
            callbacks: LangChain回调列表
            
        Returns:
            "tech" / "news" / "general"
        """
        invoke_config = {}
        if callbacks:
            invoke_config["callbacks"] = callbacks

        try:
            result = self.chain.invoke(
                {"article": article[:500]},  # 只取前500字节省token
                config=invoke_config,
            )
            result = result.strip().lower()

            if "tech" in result:
                return "tech"
            elif "news" in result:
                return "news"
            return "general"

        except Exception as e:
            print(f"⚠️  文章分析失败，使用默认类型：{e}")
            return "general"
