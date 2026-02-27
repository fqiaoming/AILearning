"""
第6章-LangChain高级：Callback回调系统
对应课程：第33课-Callback系统与Chain监控

功能：监控Chain执行过程，添加日志、计时等功能
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from dotenv import load_dotenv
import os
import time
from typing import Any, Dict, List
from uuid import UUID

load_dotenv()


def get_llm():
    """获取LLM实例"""
    return ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
        temperature=0.7
    )


# ==================== 自定义Callback ====================

class TimingCallback(BaseCallbackHandler):
    """计时回调：记录LLM调用耗时"""
    
    def __init__(self):
        self.start_time = None
        self.total_time = 0
    
    def on_llm_start(
        self, 
        serialized: Dict[str, Any], 
        prompts: List[str], 
        **kwargs
    ) -> None:
        """LLM开始时调用"""
        self.start_time = time.time()
        print(f"[Timing] LLM开始调用...")
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """LLM结束时调用"""
        elapsed = time.time() - self.start_time
        self.total_time += elapsed
        print(f"[Timing] LLM调用完成，耗时：{elapsed:.2f}秒")


class LoggingCallback(BaseCallbackHandler):
    """日志回调：记录详细日志"""
    
    def on_llm_start(
        self, 
        serialized: Dict[str, Any], 
        prompts: List[str], 
        **kwargs
    ) -> None:
        print(f"[Log] 开始调用LLM")
        print(f"[Log] 模型：{serialized.get('name', 'unknown')}")
        print(f"[Log] Prompt长度：{len(prompts[0]) if prompts else 0}字符")
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        text = response.generations[0][0].text if response.generations else ""
        print(f"[Log] 输出长度：{len(text)}字符")
    
    def on_chain_start(
        self, 
        serialized: Dict[str, Any], 
        inputs: Dict[str, Any], 
        **kwargs
    ) -> None:
        print(f"[Log] Chain开始：{serialized.get('name', 'unknown')}")
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        print(f"[Log] Chain结束")


class TokenCountCallback(BaseCallbackHandler):
    """Token计数回调"""
    
    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            self.prompt_tokens += usage.get("prompt_tokens", 0)
            self.completion_tokens += usage.get("completion_tokens", 0)
            self.total_tokens += usage.get("total_tokens", 0)
            print(f"[Token] 本次使用：{usage.get('total_tokens', 'N/A')} tokens")
    
    def get_stats(self):
        return {
            "total": self.total_tokens,
            "prompt": self.prompt_tokens,
            "completion": self.completion_tokens
        }


# ==================== 演示 ====================

def demo_timing_callback():
    """演示1：计时回调"""
    print("=" * 60)
    print("演示1：计时回调 - 监控LLM调用耗时")
    print("=" * 60)
    
    timing = TimingCallback()
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("用一句话解释{topic}")
    chain = prompt | llm | StrOutputParser()
    
    # 使用回调
    result = chain.invoke(
        {"topic": "机器学习"},
        config={"callbacks": [timing]}
    )
    
    print(f"\n结果：{result}")
    print(f"总耗时：{timing.total_time:.2f}秒")


def demo_logging_callback():
    """演示2：日志回调"""
    print("\n" + "=" * 60)
    print("演示2：日志回调 - 记录详细执行过程")
    print("=" * 60)
    
    logging_cb = LoggingCallback()
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("用一句话解释{topic}")
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke(
        {"topic": "深度学习"},
        config={"callbacks": [logging_cb]}
    )
    
    print(f"\n结果：{result}")


def demo_multiple_callbacks():
    """演示3：组合多个回调"""
    print("\n" + "=" * 60)
    print("演示3：组合多个回调")
    print("=" * 60)
    
    timing = TimingCallback()
    logging_cb = LoggingCallback()
    token_cb = TokenCountCallback()
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("用一句话解释{topic}")
    chain = prompt | llm | StrOutputParser()
    
    # 使用多个回调
    result = chain.invoke(
        {"topic": "神经网络"},
        config={"callbacks": [timing, logging_cb, token_cb]}
    )
    
    print(f"\n结果：{result}")
    print(f"\n[统计]")
    print(f"  总耗时：{timing.total_time:.2f}秒")
    print(f"  Token统计：{token_cb.get_stats()}")


def demo_callback_usage():
    """演示4：回调的实际应用"""
    print("\n" + "=" * 60)
    print("演示4：Callback的实际应用场景")
    print("=" * 60)
    
    print("""
Callback的常见应用：

1. 性能监控
   - 记录每次调用耗时
   - 统计Token使用量
   - 追踪成本

2. 日志记录
   - 记录输入输出
   - 追踪错误
   - 审计日志

3. 实时反馈
   - 流式输出进度
   - 显示处理状态
   - 用户界面更新

4. 调试辅助
   - 打印中间结果
   - 验证数据流转
   - 定位问题

5. 数据收集
   - 收集训练数据
   - 记录用户行为
   - 质量监控
""")


if __name__ == "__main__":
    demo_timing_callback()
    demo_logging_callback()
    demo_multiple_callbacks()
    demo_callback_usage()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nCallback核心知识：")
    print("  1. Callback = Chain执行过程的钩子")
    print("  2. 继承BaseCallbackHandler实现自定义回调")
    print("  3. 通过config={'callbacks': [...]}传入")
    print("  4. 可以组合多个回调同时使用")

