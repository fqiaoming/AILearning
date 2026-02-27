"""
意图识别模块
对应课程：第28课-LangChain实战项目1

使用LangChain的Prompt Template + Output Parser实现结构化意图识别
技巧：Pydantic输出解析 + LCEL链式调用
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

from .config import config


class Intent(BaseModel):
    """意图模型 - 使用Pydantic定义结构化输出"""

    category: Literal["chat", "tool_call", "question", "complex"] = Field(
        description="意图类别：chat=闲聊, tool_call=工具调用, question=知识问答, complex=复杂任务"
    )
    confidence: float = Field(
        description="置信度，0-1之间",
        ge=0.0,
        le=1.0,
    )
    reason: str = Field(description="判断理由")


class IntentClassifier:
    """
    意图分类器
    
    使用LangChain的LCEL构建：Prompt → LLM → OutputParser
    支持4种意图：闲聊、工具调用、知识问答、复杂任务
    """

    def __init__(self):
        """初始化分类器，构建LCEL链"""
        # 根据配置选择模型
        if config.USE_LOCAL_MODEL:
            self.llm = ChatOpenAI(
                base_url=config.LOCAL_LLM_URL,
                api_key=config.LOCAL_LLM_API_KEY,
                model=config.LOCAL_MODEL,
                temperature=0.1,
            )
        else:
            self.llm = ChatOpenAI(
                model=config.PRIMARY_MODEL,
                temperature=0.1,
            )

        # Pydantic输出解析器
        self.parser = PydanticOutputParser(pydantic_object=Intent)

        # 提示词模板
        self.prompt = ChatPromptTemplate.from_template(
            """分析用户消息的意图。

意图类别：
- chat: 闲聊、打招呼、日常寒暄
- tool_call: 需要调用工具（天气查询、时间查询、数学计算等）
- question: 知识问答、概念解释、技术问题
- complex: 复杂任务，需要深度思考、多步骤分析

{format_instructions}

用户消息：{message}"""
        )

        # 构建LCEL链：Prompt → LLM → Parser
        self.chain = (
            self.prompt.partial(
                format_instructions=self.parser.get_format_instructions()
            )
            | self.llm
            | self.parser
        )

    def classify(self, message: str) -> Intent:
        """
        分类用户消息的意图
        
        Args:
            message: 用户输入文本
            
        Returns:
            Intent对象，包含category、confidence、reason
        """
        try:
            return self.chain.invoke({"message": message})
        except Exception as e:
            # 分类失败时返回默认意图（闲聊）
            return Intent(
                category="chat",
                confidence=0.5,
                reason=f"分类失败，使用默认意图：{e}",
            )


# 独立运行测试
if __name__ == "__main__":
    classifier = IntentClassifier()

    test_messages = [
        "你好呀",
        "现在几点了？",
        "什么是机器学习？",
        "帮我分析一下这个项目的优缺点",
        "北京天气怎么样",
        "123 + 456 等于多少",
    ]

    print("=" * 50)
    print("意图分类器测试")
    print("=" * 50)

    for msg in test_messages:
        intent = classifier.classify(msg)
        print(f"\n输入：{msg}")
        print(f"意图：{intent.category}（置信度：{intent.confidence:.2f}）")
        print(f"理由：{intent.reason}")
