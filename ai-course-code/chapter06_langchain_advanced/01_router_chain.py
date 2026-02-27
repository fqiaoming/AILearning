"""
第6章-LangChain高级：RouterChain
对应课程：第31课-RouterChain

功能：根据输入自动路由到不同的处理链
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取LLM实例"""
    return ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
        temperature=0.7
    )


# ==================== 定义专门的Chain ====================

def create_code_chain():
    """代码问题Chain"""
    prompt = ChatPromptTemplate.from_template("""你是一个专业的程序员。
请回答以下编程问题，给出代码示例和详细解释。

问题：{input}""")
    return prompt | get_llm() | StrOutputParser()


def create_math_chain():
    """数学问题Chain"""
    prompt = ChatPromptTemplate.from_template("""你是一个数学专家。
请一步步解答以下数学问题，展示完整的解题过程。

问题：{input}""")
    return prompt | get_llm() | StrOutputParser()


def create_general_chain():
    """通用问题Chain"""
    prompt = ChatPromptTemplate.from_template("""你是一个知识渊博的助手。
请回答以下问题。

问题：{input}""")
    return prompt | get_llm() | StrOutputParser()


# ==================== 路由逻辑 ====================

def classify_question(question: str) -> str:
    """分类问题类型"""
    llm = get_llm()
    
    classify_prompt = ChatPromptTemplate.from_template("""判断以下问题属于哪个类别：
- code：编程、代码相关问题
- math：数学计算、公式相关问题
- general：其他通用问题

问题：{question}

只回答类别名称（code/math/general）：""")
    
    chain = classify_prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question}).strip().lower()
    
    # 确保返回有效类别
    if "code" in result:
        return "code"
    elif "math" in result:
        return "math"
    else:
        return "general"


def route_question(input_dict: dict) -> str:
    """路由到对应的Chain"""
    question = input_dict["input"]
    category = classify_question(question)
    
    print(f"[路由] 问题类别：{category}")
    
    chains = {
        "code": create_code_chain(),
        "math": create_math_chain(),
        "general": create_general_chain()
    }
    
    chain = chains.get(category, chains["general"])
    return chain.invoke(input_dict)


def demo_router_chain():
    """演示RouterChain"""
    print("=" * 60)
    print("RouterChain演示 - 根据问题类型自动路由")
    print("=" * 60)
    
    # 测试问题
    test_questions = [
        "用Python写一个冒泡排序",
        "计算 (3+5) × 2 - 4 ÷ 2",
        "介绍一下人工智能的发展历史"
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"问题：{question}")
        print("-" * 60)
        
        result = route_question({"input": question})
        print(f"回答：{result[:200]}..." if len(result) > 200 else f"回答：{result}")


def demo_semantic_router():
    """演示语义路由（更智能的版本）"""
    print("\n" + "=" * 60)
    print("语义路由演示 - 使用embedding进行相似度匹配")
    print("=" * 60)
    
    print("""
语义路由的优势：
1. 不需要LLM分类，速度更快
2. 基于embedding相似度，更准确
3. 支持更多类别而不增加延迟

实现思路：
1. 为每个类别定义示例问题
2. 计算示例问题的embedding
3. 计算新问题的embedding
4. 找最相似的类别进行路由
""")


if __name__ == "__main__":
    demo_router_chain()
    demo_semantic_router()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nRouterChain核心知识：")
    print("  1. 路由 = 根据输入选择不同处理路径")
    print("  2. 可以用LLM分类来决定路由")
    print("  3. 也可以用embedding相似度路由（更快）")
    print("  4. 适合场景：多类型问答、多功能助手")

