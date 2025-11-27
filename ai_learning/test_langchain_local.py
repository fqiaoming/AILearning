"""测试LangChain v1.x + 本地LM Studio"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载配置（如果.env文件存在）
load_dotenv()

# 创建本地模型实例（连接到LM Studio）
# LangChain v1.x使用相同的ChatOpenAI接口
llm = ChatOpenAI(
    base_url=os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1"),
    api_key=os.getenv("LOCAL_LLM_API_KEY", "lm-studio"),
    moel=os.getenv("LOCAL_LLM_MODEL", "qwen2.5-7b-instruct"),
    temperature=0.7
)

# 测试对话
messages = [
    SystemMessage(content="你是一个专业的Python编程助手"),
    HumanMessage(content="请用Python写一个快速排序函数")
]

print("正在调用本地模型...")
print(f"LangChain版本: {__import__('langchain').__version__}")
response = llm.invoke(messages)

print("\n" + "="*50)
print("AI回答：")
print("="*50)
print(response.content)
