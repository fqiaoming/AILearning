"""
第4章-OpenAI API：Token管理与成本优化
对应课程：第20课-Token管理与成本优化

功能：计算Token数量，估算成本，优化Token使用
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# tiktoken用于计算token数量
try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False
    print("提示：安装tiktoken可以精确计算token数量：pip install tiktoken")

load_dotenv()


def get_client():
    """获取AI客户端"""
    if os.getenv("OPENAI_API_KEY"):
        return OpenAI()
    else:
        return OpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        )


def get_model():
    """获取模型名称"""
    if os.getenv("OPENAI_API_KEY"):
        return "gpt-3.5-turbo"
    else:
        return os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")


# ==================== Token计算 ====================

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """计算文本的token数量"""
    if not HAS_TIKTOKEN:
        # 简单估算：中文约1.5字/token，英文约0.75词/token
        return len(text) // 2
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def count_messages_tokens(messages: list, model: str = "gpt-3.5-turbo") -> int:
    """计算消息列表的token数量"""
    total = 0
    for msg in messages:
        # 每条消息有额外的格式token
        total += 4  # 约4个token的格式开销
        total += count_tokens(msg.get("role", ""), model)
        total += count_tokens(msg.get("content", ""), model)
    total += 2  # 消息结束标记
    return total


# ==================== 成本计算 ====================

# 价格表（美元/1000 tokens）
PRICING = {
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "text-embedding-ada-002": {"input": 0.0001, "output": 0},
}


def estimate_cost(input_tokens: int, output_tokens: int, 
                  model: str = "gpt-3.5-turbo") -> float:
    """估算API调用成本（美元）"""
    if model not in PRICING:
        return 0.0
    
    price = PRICING[model]
    input_cost = (input_tokens / 1000) * price["input"]
    output_cost = (output_tokens / 1000) * price["output"]
    
    return input_cost + output_cost


def demo_token_counting():
    """演示Token计算"""
    print("=" * 60)
    print("Token计算演示")
    print("=" * 60)
    
    # 测试文本
    texts = [
        "Hello, world!",
        "你好，世界！",
        "Python是一种广泛使用的高级编程语言，它的设计理念强调代码的可读性。",
        "The quick brown fox jumps over the lazy dog.",
    ]
    
    print("\n【文本Token数量】")
    for text in texts:
        tokens = count_tokens(text)
        print(f"  '{text[:30]}...' → {tokens} tokens")
    
    # 消息列表
    messages = [
        {"role": "system", "content": "你是一个专业的Python程序员"},
        {"role": "user", "content": "写一个快速排序函数"},
    ]
    
    msg_tokens = count_messages_tokens(messages)
    print(f"\n【消息列表】")
    print(f"  System + User消息 → {msg_tokens} tokens")


def demo_cost_estimation():
    """演示成本估算"""
    print("\n" + "=" * 60)
    print("成本估算演示")
    print("=" * 60)
    
    # 模拟一次调用
    input_tokens = 100
    output_tokens = 500
    
    print(f"\n假设一次调用：输入{input_tokens}tokens，输出{output_tokens}tokens")
    print("\n【不同模型成本对比】")
    
    for model in ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]:
        cost = estimate_cost(input_tokens, output_tokens, model)
        print(f"  {model}: ${cost:.6f}")
    
    # 批量估算
    print("\n【批量调用成本估算】")
    calls_per_day = 1000
    
    for model in ["gpt-3.5-turbo", "gpt-4-turbo"]:
        cost_per_call = estimate_cost(input_tokens, output_tokens, model)
        daily_cost = cost_per_call * calls_per_day
        monthly_cost = daily_cost * 30
        print(f"\n  {model}:")
        print(f"    单次：${cost_per_call:.6f}")
        print(f"    日均（{calls_per_day}次）：${daily_cost:.2f}")
        print(f"    月均：${monthly_cost:.2f}")


def demo_optimization_tips():
    """演示优化技巧"""
    print("\n" + "=" * 60)
    print("Token优化技巧")
    print("=" * 60)
    
    print("""
✅ Token优化策略：

1. 精简System Prompt
   ❌ "你是一位经验丰富、知识渊博、态度友好的Python专家..."
   ✅ "你是Python专家，回答简洁专业"

2. 控制输出长度
   使用max_tokens参数
   在prompt中明确要求"100字以内"

3. 使用更高效的模型
   简单任务：gpt-3.5-turbo（便宜100倍）
   复杂任务：gpt-4-turbo

4. 智能路由
   根据任务复杂度选择模型
   80%简单任务用小模型

5. 缓存重复请求
   相同问题不重复调用
   使用Redis或内存缓存

6. 压缩上下文
   只保留必要的对话历史
   使用摘要而不是完整历史
""")
    
    # 演示prompt优化
    print("\n【Prompt优化示例】")
    
    verbose_prompt = """你是一位拥有20年经验的资深Python高级工程师和架构师，
你对Python语言有着深入的理解和丰富的实践经验，
能够编写高质量、高性能、易维护的代码。
请用你的专业知识来帮助用户解决问题。"""
    
    concise_prompt = "你是Python专家，回答简洁专业。"
    
    print(f"\n  冗长版本（{count_tokens(verbose_prompt)} tokens）：")
    print(f"    {verbose_prompt[:50]}...")
    
    print(f"\n  精简版本（{count_tokens(concise_prompt)} tokens）：")
    print(f"    {concise_prompt}")
    
    savings = count_tokens(verbose_prompt) - count_tokens(concise_prompt)
    print(f"\n  节省：{savings} tokens/次")


def demo_real_cost():
    """演示实际调用成本"""
    print("\n" + "=" * 60)
    print("实际调用成本演示")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个简洁的助手"},
            {"role": "user", "content": "用一句话解释什么是Python"}
        ],
        max_tokens=100
    )
    
    usage = response.usage
    print(f"\n实际调用结果：")
    print(f"  输入tokens：{usage.prompt_tokens}")
    print(f"  输出tokens：{usage.completion_tokens}")
    print(f"  总tokens：{usage.total_tokens}")
    
    if model in PRICING:
        cost = estimate_cost(usage.prompt_tokens, usage.completion_tokens, model)
        print(f"  估算成本：${cost:.6f}")
    
    print(f"\nAI回复：{response.choices[0].message.content}")


if __name__ == "__main__":
    demo_token_counting()
    demo_cost_estimation()
    demo_optimization_tips()
    demo_real_cost()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n成本控制核心要点：")
    print("  1. 了解Token计算方式")
    print("  2. 精简Prompt节省输入token")
    print("  3. 控制max_tokens节省输出token")
    print("  4. 根据任务选择合适的模型")
    print("  5. 实现缓存避免重复调用")

