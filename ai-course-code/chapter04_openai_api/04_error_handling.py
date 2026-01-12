"""
第4章-OpenAI API：错误处理与重试
对应课程：第19课-错误处理与重试策略

功能：处理API调用中的各种错误，实现自动重试
"""

from openai import OpenAI, APIError, RateLimitError, APITimeoutError
from dotenv import load_dotenv
import os
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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


# ==================== 基础错误处理 ====================

def chat_with_basic_error_handling(message: str):
    """基础错误处理"""
    client = get_client()
    model = get_model()
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            timeout=30  # 设置超时
        )
        return response.choices[0].message.content
        
    except RateLimitError as e:
        # 频率限制错误
        print(f"❌ 频率限制：{e}")
        print("💡 建议：等待一段时间后重试，或降低调用频率")
        return None
        
    except APITimeoutError as e:
        # 超时错误
        print(f"❌ 请求超时：{e}")
        print("💡 建议：检查网络连接，或增加timeout参数")
        return None
        
    except APIError as e:
        # 其他API错误
        print(f"❌ API错误：{e}")
        return None
        
    except Exception as e:
        # 未知错误
        print(f"❌ 未知错误：{type(e).__name__}: {e}")
        return None


# ==================== 自动重试 ====================

@retry(
    stop=stop_after_attempt(3),  # 最多重试3次
    wait=wait_exponential(multiplier=1, min=1, max=10),  # 指数退避
    retry=retry_if_exception_type((RateLimitError, APITimeoutError)),  # 只对特定错误重试
    before_sleep=lambda retry_state: print(f"⏳ 重试 {retry_state.attempt_number}/3...")
)
def chat_with_retry(message: str):
    """带自动重试的对话函数"""
    client = get_client()
    model = get_model()
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        timeout=30
    )
    return response.choices[0].message.content


# ==================== 自定义重试逻辑 ====================

def chat_with_custom_retry(message: str, max_retries: int = 3):
    """自定义重试逻辑"""
    client = get_client()
    model = get_model()
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                timeout=30
            )
            return response.choices[0].message.content
            
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避：1, 2, 4秒
                print(f"⏳ 频率限制，等待{wait_time}秒后重试... ({attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print("❌ 达到最大重试次数")
                raise
                
        except APITimeoutError:
            if attempt < max_retries - 1:
                print(f"⏳ 超时，立即重试... ({attempt + 1}/{max_retries})")
            else:
                print("❌ 达到最大重试次数")
                raise


def demo_error_handling():
    """演示错误处理"""
    print("=" * 60)
    print("错误处理演示")
    print("=" * 60)
    
    print("""
常见错误类型：
1. RateLimitError - 频率限制（调用太频繁）
2. APITimeoutError - 请求超时
3. AuthenticationError - 认证失败（API Key错误）
4. APIError - 其他API错误
""")
    
    # 正常调用
    print("【测试正常调用】")
    result = chat_with_basic_error_handling("你好")
    if result:
        print(f"✅ 成功：{result[:50]}...")
    
    # 使用带重试的函数
    print("\n【测试带重试的调用】")
    try:
        result = chat_with_retry("用一句话介绍Python")
        print(f"✅ 成功：{result}")
    except Exception as e:
        print(f"❌ 最终失败：{e}")


def demo_best_practices():
    """演示最佳实践"""
    print("\n" + "=" * 60)
    print("错误处理最佳实践")
    print("=" * 60)
    
    print("""
✅ 最佳实践：

1. 设置合理的timeout
   timeout=30  # 根据任务复杂度调整

2. 实现重试机制
   - 使用tenacity库
   - 指数退避策略
   - 限制最大重试次数

3. 区分可重试和不可重试的错误
   - RateLimitError: 可重试（等待后重试）
   - APITimeoutError: 可重试（可能是网络问题）
   - AuthenticationError: 不可重试（API Key错误）

4. 记录错误日志
   - 错误类型
   - 错误信息
   - 重试次数
   - 请求参数

5. 设置告警
   - 错误率超过阈值时告警
   - 连续失败时告警
""")


if __name__ == "__main__":
    demo_error_handling()
    demo_best_practices()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n核心要点：")
    print("  1. 使用try-except捕获特定异常")
    print("  2. 区分可重试和不可重试的错误")
    print("  3. 使用tenacity实现自动重试")
    print("  4. 指数退避避免雪崩")
    print("  5. 记录日志便于排查")

