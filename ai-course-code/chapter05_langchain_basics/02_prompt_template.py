"""
第5章-LangChain基础：Prompt Template
对应课程：第24课-Prompt-Template深入

功能：演示Prompt模板的各种用法
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotPromptTemplate
)
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取LLM实例"""
    return ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
    )


def demo_basic_template():
    """演示1：基础模板"""
    print("=" * 60)
    print("演示1：基础PromptTemplate")
    print("=" * 60)
    
    # 创建模板
    template = PromptTemplate(
        input_variables=["language", "topic"],
        template="用{language}写一个关于{topic}的函数"
    )
    
    # 填充变量
    prompt = template.format(language="Python", topic="快速排序")
    print(f"\n模板：用{{language}}写一个关于{{topic}}的函数")
    print(f"填充后：{prompt}")
    
    # 调用LLM
    llm = get_llm()
    response = llm.invoke(prompt)
    print(f"\nAI回复：\n{response.content}")


def demo_chat_prompt_template():
    """演示2：ChatPromptTemplate"""
    print("\n" + "=" * 60)
    print("演示2：ChatPromptTemplate")
    print("=" * 60)
    
    # 创建Chat模板（包含system和user）
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，回答要{style}"),
        ("user", "{question}")
    ])
    
    # 填充变量
    messages = template.format_messages(
        role="Python专家",
        style="简洁专业",
        question="什么是列表推导式？"
    )
    
    print("\n模板结构：")
    print("  system: 你是一个{role}，回答要{style}")
    print("  user: {question}")
    
    print("\n填充后的消息：")
    for msg in messages:
        print(f"  {msg.type}: {msg.content}")
    
    # 调用LLM
    llm = get_llm()
    response = llm.invoke(messages)
    print(f"\nAI回复：{response.content}")


def demo_few_shot_template():
    """演示3：Few-shot模板"""
    print("\n" + "=" * 60)
    print("演示3：Few-shot Template")
    print("=" * 60)
    
    # 定义示例
    examples = [
        {"input": "开心", "output": "正面"},
        {"input": "难过", "output": "负面"},
        {"input": "还行吧", "output": "中性"},
    ]
    
    # 单个示例的模板
    example_template = PromptTemplate(
        input_variables=["input", "output"],
        template="输入：{input}\n情感：{output}"
    )
    
    # Few-shot模板
    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_template,
        prefix="判断以下文本的情感（正面/负面/中性）：\n",
        suffix="\n输入：{text}\n情感：",
        input_variables=["text"]
    )
    
    # 生成prompt
    test_text = "这个产品太棒了！"
    prompt = few_shot_template.format(text=test_text)
    
    print("Few-shot模板生成的Prompt：")
    print("-" * 40)
    print(prompt)
    print("-" * 40)
    
    # 调用LLM
    llm = get_llm()
    response = llm.invoke(prompt)
    print(f"\nAI判断：{response.content}")


def demo_messages_placeholder():
    """演示4：MessagesPlaceholder（对话历史）"""
    print("\n" + "=" * 60)
    print("演示4：MessagesPlaceholder - 处理对话历史")
    print("=" * 60)
    
    # 创建支持对话历史的模板
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好的AI助手"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    
    # 模拟对话历史
    history = [
        HumanMessage(content="我叫小明"),
        AIMessage(content="你好小明！很高兴认识你！"),
    ]
    
    # 填充模板
    messages = template.format_messages(
        history=history,
        input="你还记得我叫什么吗？"
    )
    
    print("\n对话历史：")
    for msg in history:
        role = "用户" if isinstance(msg, HumanMessage) else "AI"
        print(f"  {role}：{msg.content}")
    
    print(f"\n新问题：你还记得我叫什么吗？")
    
    # 调用LLM
    llm = get_llm()
    response = llm.invoke(messages)
    print(f"AI回复：{response.content}")


def demo_template_chaining():
    """演示5：模板与Chain结合"""
    print("\n" + "=" * 60)
    print("演示5：模板 + Chain（LCEL）")
    print("=" * 60)
    
    from langchain_core.output_parsers import StrOutputParser
    
    # 创建模板
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个翻译专家，将{source_lang}翻译成{target_lang}"),
        ("user", "翻译：{text}")
    ])
    
    llm = get_llm()
    output_parser = StrOutputParser()
    
    # 使用LCEL创建Chain
    chain = template | llm | output_parser
    
    # 调用Chain
    result = chain.invoke({
        "source_lang": "中文",
        "target_lang": "英文",
        "text": "今天天气真好"
    })
    
    print("\n翻译任务：中文 → 英文")
    print(f"原文：今天天气真好")
    print(f"译文：{result}")


if __name__ == "__main__":
    demo_basic_template()
    demo_chat_prompt_template()
    demo_few_shot_template()
    demo_messages_placeholder()
    demo_template_chaining()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nPrompt Template核心知识：")
    print("  1. PromptTemplate：基础模板，单个字符串")
    print("  2. ChatPromptTemplate：对话模板，包含多条消息")
    print("  3. FewShotPromptTemplate：少样本学习模板")
    print("  4. MessagesPlaceholder：插入对话历史")
    print("  5. 模板 + LCEL：构建处理链")

