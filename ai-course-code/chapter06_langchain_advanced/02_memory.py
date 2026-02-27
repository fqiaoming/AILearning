"""
第6章-LangChain高级：Memory对话记忆
对应课程：第32课-Memory与对话管理深入

功能：让AI记住对话历史，实现多轮对话
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
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


# ==================== 手动管理历史 ====================

def demo_manual_history():
    """演示1：手动管理对话历史"""
    print("=" * 60)
    print("演示1：手动管理对话历史")
    print("=" * 60)
    
    llm = get_llm()
    
    # 创建支持历史的模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好的AI助手，记住用户的信息"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    
    # 手动维护历史
    history = []
    
    # 第一轮对话
    print("\n[第1轮]")
    user_input1 = "我叫小明，我是一名Python程序员"
    print(f"用户：{user_input1}")
    
    response1 = chain.invoke({"history": history, "input": user_input1})
    print(f"AI：{response1.content}")
    
    # 更新历史
    history.append(HumanMessage(content=user_input1))
    history.append(AIMessage(content=response1.content))
    
    # 第二轮对话
    print("\n[第2轮]")
    user_input2 = "你还记得我叫什么名字吗？我的职业是什么？"
    print(f"用户：{user_input2}")
    
    response2 = chain.invoke({"history": history, "input": user_input2})
    print(f"AI：{response2.content}")


# ==================== 使用RunnableWithMessageHistory ====================

# 存储不同session的历史
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """获取指定session的历史"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def demo_runnable_with_history():
    """演示2：使用RunnableWithMessageHistory"""
    print("\n" + "=" * 60)
    print("演示2：RunnableWithMessageHistory - 自动管理历史")
    print("=" * 60)
    
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好的AI助手"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    
    # 包装成带历史管理的Chain
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    session_id = "user_123"
    
    # 第一轮
    print(f"\n[Session: {session_id}]")
    response1 = chain_with_history.invoke(
        {"input": "我叫张三，今年25岁"},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"用户：我叫张三，今年25岁")
    print(f"AI：{response1.content}")
    
    # 第二轮
    response2 = chain_with_history.invoke(
        {"input": "我多大了？"},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"\n用户：我多大了？")
    print(f"AI：{response2.content}")
    
    # 查看历史
    print(f"\n[历史记录]")
    history = get_session_history(session_id)
    for msg in history.messages:
        role = "用户" if isinstance(msg, HumanMessage) else "AI"
        print(f"  {role}：{msg.content[:50]}...")


# ==================== 不同类型的Memory ====================

def demo_memory_types():
    """演示3：不同类型的Memory"""
    print("\n" + "=" * 60)
    print("演示3：Memory类型介绍")
    print("=" * 60)
    
    print("""
LangChain支持多种Memory类型：

1. ConversationBufferMemory
   - 保存完整对话历史
   - 简单但可能超出token限制
   
2. ConversationBufferWindowMemory
   - 只保留最近K轮对话
   - 适合长对话场景
   
3. ConversationSummaryMemory
   - 保存对话摘要而非原文
   - 大幅节省token
   
4. ConversationSummaryBufferMemory
   - 最近对话保留原文，更早的压缩成摘要
   - 平衡信息和token
   
5. VectorStoreRetrieverMemory
   - 使用向量数据库存储
   - 支持语义检索相关历史
   
选择建议：
- 简单场景：BufferMemory
- 长对话：WindowMemory 或 SummaryBufferMemory
- 需要检索：VectorStoreRetrieverMemory
""")


def demo_sliding_window():
    """演示4：滑动窗口Memory"""
    print("\n" + "=" * 60)
    print("演示4：滑动窗口 - 只保留最近K轮")
    print("=" * 60)
    
    # 模拟滑动窗口
    max_history = 4  # 只保留最近4条消息
    history = []
    
    conversations = [
        "我叫小王",
        "我喜欢打篮球",
        "我今年30岁",
        "我在北京工作",
        "我最喜欢的颜色是蓝色"
    ]
    
    print(f"窗口大小：{max_history}条消息\n")
    
    for i, msg in enumerate(conversations, 1):
        # 添加新消息
        history.append({"role": "user", "content": msg})
        history.append({"role": "assistant", "content": f"好的，我记住了：{msg}"})
        
        # 滑动窗口：只保留最近K条
        if len(history) > max_history:
            history = history[-max_history:]
        
        print(f"[轮次{i}] 用户说：{msg}")
        print(f"  当前历史：{len(history)}条")
        print(f"  内容：{[h['content'][:15]+'...' for h in history]}")
        print()


if __name__ == "__main__":
    demo_manual_history()
    demo_runnable_with_history()
    demo_memory_types()
    demo_sliding_window()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nMemory核心知识：")
    print("  1. Memory = 让AI记住对话历史")
    print("  2. 手动管理：自己维护history列表")
    print("  3. 自动管理：RunnableWithMessageHistory")
    print("  4. 长对话要用滑动窗口或摘要，避免超token")

