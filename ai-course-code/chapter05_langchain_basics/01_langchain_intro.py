"""
第5章-LangChain基础：入门
对应课程：第23课-LangChain入门与核心概念

功能：演示LangChain的基本用法
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取LLM实例"""
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-3.5-turbo")
    else:
        # 使用本地LM Studio
        return ChatOpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
            model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
        )


def demo_basic_usage():
    """演示1：基础用法"""
    print("=" * 60)
    print("演示1：LangChain基础用法")
    print("=" * 60)
    
    llm = get_llm()
    
    # 方式1：直接调用（传入字符串）
    print("\n【方式1：直接传入字符串】")
    response = llm.invoke("你好，用一句话介绍LangChain")
    print(f"回复：{response.content}")
    
    # 方式2：使用Message对象
    print("\n【方式2：使用Message对象】")
    messages = [
        SystemMessage(content="你是一个Python专家"),
        HumanMessage(content="什么是装饰器？一句话解释")
    ]
    response = llm.invoke(messages)
    print(f"回复：{response.content}")


def demo_llm_parameters():
    """演示2：LLM参数配置"""
    print("\n" + "=" * 60)
    print("演示2：LLM参数配置")
    print("=" * 60)
    
    # 配置不同参数
    llm = get_llm()
    
    # 设置temperature
    llm_creative = ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
        temperature=0.9  # 更有创造性
    )
    
    llm_precise = ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
        temperature=0.1  # 更确定性
    )
    
    prompt = "给我的AI学习项目起一个创意名字"
    
    print(f"\n问题：{prompt}")
    print(f"\n创意模式(temp=0.9)：{llm_creative.invoke(prompt).content}")
    print(f"\n精确模式(temp=0.1)：{llm_precise.invoke(prompt).content}")


def demo_langchain_vs_openai():
    """演示3：LangChain vs 原生OpenAI"""
    print("\n" + "=" * 60)
    print("演示3：LangChain的价值")
    print("=" * 60)
    
    print("""
LangChain的核心价值：

1. 统一接口
   - 切换模型只需改一行代码
   - OpenAI、Claude、本地模型都用同样的接口

2. 组件化
   - Prompt Template：管理提示词
   - Output Parser：解析输出
   - Chain：组合多个步骤
   - Memory：管理对话历史

3. 生态丰富
   - 各种工具集成
   - 向量数据库
   - 文档加载器
   - Agent框架

4. 标准化
   - LCEL（LangChain Expression Language）
   - 声明式定义处理流程
""")


def demo_streaming():
    """演示4：流式输出"""
    print("\n" + "=" * 60)
    print("演示4：LangChain流式输出")
    print("=" * 60)
    
    llm = get_llm()
    
    print("\n流式输出演示：")
    print("AI：", end="", flush=True)
    
    for chunk in llm.stream("用100字介绍Python语言"):
        print(chunk.content, end="", flush=True)
    
    print()  # 换行


if __name__ == "__main__":
    demo_basic_usage()
    demo_llm_parameters()
    demo_langchain_vs_openai()
    demo_streaming()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nLangChain核心概念：")
    print("  1. ChatOpenAI：封装LLM调用")
    print("  2. Message：结构化消息")
    print("  3. invoke()：同步调用")
    print("  4. stream()：流式调用")

