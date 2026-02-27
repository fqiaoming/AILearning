"""
内容处理Pipeline
对应课程：第36课-第6章综合实战项目

使用SequentialChain串联4个处理步骤：总结→关键词→翻译→配图建议
涉及知识点：第30课-SequentialChain串联
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain

from .config import config


class ContentProcessor:
    """
    内容处理Pipeline
    
    根据文章类型使用不同的提示词策略，通过SequentialChain串联4个步骤：
    1. 总结生成（根据类型定制）
    2. 关键词提取
    3. 英文翻译（翻译摘要）
    4. 配图建议
    """

    def __init__(self, article_type: str):
        """
        Args:
            article_type: 文章类型 ("tech" / "news" / "general")
        """
        self.article_type = article_type

        if config.USE_LOCAL_MODEL:
            self.llm = ChatOpenAI(
                base_url=config.LM_STUDIO_BASE_URL,
                api_key=config.LM_STUDIO_API_KEY,
                model=config.LM_STUDIO_MODEL,
                temperature=0.7,
            )
        else:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

        self._setup_pipeline()

    def _setup_pipeline(self):
        """构建SequentialChain处理流水线"""

        # 1. 总结生成 - 根据文章类型定制提示词
        summary_templates = {
            "tech": "你是技术文章编辑。从技术角度总结以下文章，突出核心技术点和创新之处（100字以内）：\n\n{article}",
            "news": "你是新闻编辑。用新闻导语的方式总结以下内容，突出5W要素（50字以内）：\n\n{article}",
            "general": "简要总结以下文章的主要内容（80字以内）：\n\n{article}",
        }
        summary_template = summary_templates.get(
            self.article_type, summary_templates["general"]
        )

        summary_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(summary_template),
            output_key="summary",
        )

        # 2. 关键词提取
        keywords_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(
                "从以下文章中提取5个最重要的关键词，用逗号分隔：\n\n{article}"
            ),
            output_key="keywords",
        )

        # 3. 英文翻译（翻译摘要，节省token）
        translation_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(
                "将以下中文翻译成英文：\n\n{summary}"
            ),
            output_key="translation",
        )

        # 4. 配图建议
        image_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(
                "基于以下摘要和关键词，给出3个配图建议（描述图片内容和风格）：\n\n"
                "摘要：{summary}\n关键词：{keywords}\n\n配图建议："
            ),
            output_key="image_suggestions",
        )

        # 组合成SequentialChain
        self.pipeline = SequentialChain(
            chains=[summary_chain, keywords_chain, translation_chain, image_chain],
            input_variables=["article"],
            output_variables=["summary", "keywords", "translation", "image_suggestions"],
            verbose=False,
        )

    def process(self, article: str, callbacks=None) -> dict:
        """
        处理文章
        
        Args:
            article: 文章内容
            callbacks: LangChain回调列表
            
        Returns:
            {
                "summary": 摘要,
                "keywords": 关键词,
                "translation": 英文翻译,
                "image_suggestions": 配图建议
            }
        """
        invoke_config = {}
        if callbacks:
            invoke_config["callbacks"] = callbacks

        return self.pipeline.invoke(
            {"article": article},
            config=invoke_config,
        )
