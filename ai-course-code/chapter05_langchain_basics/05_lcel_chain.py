"""
第5章-LangChain基础：LCEL与Chain
对应课程：第27课-Chain基础与LCEL深入

LCEL = LangChain Expression Language
用 | 管道符连接组件，构建处理链
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
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


def demo_basic_lcel():
    """演示1：LCEL基础"""
    print("=" * 60)
    print("演示1：LCEL基础 - 管道符连接")
    print("=" * 60)
    
    # LCEL的核心：用 | 连接组件
    prompt = ChatPromptTemplate.from_template("用一句话解释什么是{topic}")
    llm = get_llm()
    output_parser = StrOutputParser()
    
    # 创建Chain：prompt → llm → output_parser
    chain = prompt | llm | output_parser
    
    print("\nChain结构：prompt | llm | output_parser")
    print("执行：chain.invoke({'topic': 'Python'})")
    
    # 执行
    result = chain.invoke({"topic": "Python"})
    print(f"\n结果：{result}")


def demo_chain_components():
    """演示2：Chain的各种组件"""
    print("\n" + "=" * 60)
    print("演示2：Chain组件详解")
    print("=" * 60)
    
    print("""
LCEL常用组件：

1. ChatPromptTemplate - 构造输入
2. ChatOpenAI - 调用LLM
3. StrOutputParser - 提取字符串
4. JsonOutputParser - 解析JSON
5. RunnablePassthrough - 透传输入
6. RunnableLambda - 自定义函数

核心方法：
- invoke() - 同步调用
- stream() - 流式调用
- batch() - 批量调用
- ainvoke() - 异步调用
""")


def demo_runnable_passthrough():
    """演示3：RunnablePassthrough"""
    print("\n" + "=" * 60)
    print("演示3：RunnablePassthrough - 透传输入")
    print("=" * 60)
    
    # 场景：同时使用原始输入和处理后的结果
    prompt = ChatPromptTemplate.from_template(
        "原文：{original}\n翻译成英文，然后分析这句话的情感"
    )
    llm = get_llm()
    
    # RunnablePassthrough.assign() 可以添加新字段
    chain = (
        {"original": RunnablePassthrough()}  # 保留原始输入
        | prompt
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke("今天天气真好，心情很愉快！")
    print(f"\n原文：今天天气真好，心情很愉快！")
    print(f"结果：{result}")


def demo_runnable_lambda():
    """演示4：RunnableLambda - 自定义函数"""
    print("\n" + "=" * 60)
    print("演示4：RunnableLambda - 插入自定义处理")
    print("=" * 60)
    
    # 自定义处理函数
    def preprocess(text):
        """预处理：去除空格，转小写"""
        return text.strip().lower()
    
    def postprocess(result):
        """后处理：添加前缀"""
        return f"[AI回复] {result}"
    
    prompt = ChatPromptTemplate.from_template("简要解释：{input}")
    llm = get_llm()
    
    # 使用RunnableLambda包装自定义函数
    chain = (
        RunnableLambda(preprocess)  # 预处理
        | (lambda x: {"input": x})  # 转换为dict
        | prompt
        | llm
        | StrOutputParser()
        | RunnableLambda(postprocess)  # 后处理
    )
    
    result = chain.invoke("  PYTHON  ")
    print(f"\n输入：'  PYTHON  '")
    print(f"结果：{result}")


def demo_chain_streaming():
    """演示5：Chain流式输出"""
    print("\n" + "=" * 60)
    print("演示5：Chain流式输出")
    print("=" * 60)
    
    prompt = ChatPromptTemplate.from_template("用100字介绍{topic}")
    llm = get_llm()
    
    chain = prompt | llm | StrOutputParser()
    
    print("\n流式输出演示：")
    print("AI：", end="", flush=True)
    
    for chunk in chain.stream({"topic": "机器学习"}):
        print(chunk, end="", flush=True)
    
    print()  # 换行


def demo_chain_batch():
    """演示6：Chain批量调用"""
    print("\n" + "=" * 60)
    print("演示6：Chain批量调用")
    print("=" * 60)
    
    prompt = ChatPromptTemplate.from_template("用一句话解释{term}")
    llm = get_llm()
    
    chain = prompt | llm | StrOutputParser()
    
    # 批量调用
    terms = [
        {"term": "AI"},
        {"term": "机器学习"},
        {"term": "深度学习"},
    ]
    
    print("\n批量调用 chain.batch()：")
    results = chain.batch(terms)
    
    for term, result in zip(terms, results):
        print(f"\n  {term['term']}：{result[:50]}...")


def demo_practical_chain():
    """演示7：实用Chain示例 - 翻译+摘要"""
    print("\n" + "=" * 60)
    print("演示7：实用Chain - 翻译 + 摘要")
    print("=" * 60)
    
    # 翻译Chain
    translate_prompt = ChatPromptTemplate.from_template(
        "将以下中文翻译成英文，只输出译文：\n{text}"
    )
    
    # 摘要Chain
    summary_prompt = ChatPromptTemplate.from_template(
        "用一句话总结以下内容：\n{translated}"
    )
    
    llm = get_llm()
    
    # 组合Chain
    chain = (
        {"text": RunnablePassthrough()}
        | translate_prompt
        | llm
        | StrOutputParser()
        | (lambda x: {"translated": x})
        | summary_prompt
        | llm
        | StrOutputParser()
    )
    
    text = "Python是一种广泛使用的编程语言，以其简洁的语法和丰富的库而闻名。它适合初学者学习，也能满足专业开发者的需求。"
    
    print(f"\n原文：{text}")
    result = chain.invoke(text)
    print(f"\n翻译+摘要结果：{result}")


if __name__ == "__main__":
    demo_basic_lcel()
    demo_chain_components()
    demo_runnable_passthrough()
    demo_runnable_lambda()
    demo_chain_streaming()
    demo_chain_batch()
    demo_practical_chain()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nLCEL核心知识：")
    print("  1. | 管道符连接组件")
    print("  2. invoke() 同步调用")
    print("  3. stream() 流式调用")
    print("  4. batch() 批量调用")
    print("  5. RunnablePassthrough 透传")
    print("  6. RunnableLambda 自定义处理")

