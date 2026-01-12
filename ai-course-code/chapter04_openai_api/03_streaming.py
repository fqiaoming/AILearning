"""
第4章-OpenAI API：Streaming流式响应
对应课程：第18课-Streaming与异步处理

功能：实现打字机效果的实时输出
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import asyncio

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


def demo_non_streaming():
    """演示1：非流式响应（等待完成才返回）"""
    print("=" * 60)
    print("演示1：非流式响应")
    print("=" * 60)
    print("（需要等AI生成完毕才能看到结果）\n")
    
    client = get_client()
    model = get_model()
    
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "用100字介绍Python语言"}
        ]
    )
    
    end_time = time.time()
    
    print(f"AI：{response.choices[0].message.content}")
    print(f"\n⏱️ 总耗时：{end_time - start_time:.2f}秒")
    print("（用户需要等待这么久才能看到任何内容）")


def demo_streaming():
    """演示2：流式响应（边生成边输出）"""
    print("\n" + "=" * 60)
    print("演示2：流式响应")
    print("=" * 60)
    print("（实时输出，打字机效果）\n")
    
    client = get_client()
    model = get_model()
    
    start_time = time.time()
    first_token_time = None
    
    print("AI：", end="", flush=True)
    
    # 使用stream=True开启流式
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "用100字介绍Python语言"}
        ],
        stream=True  # 关键参数
    )
    
    full_content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            
            # 记录首个token的时间
            if first_token_time is None:
                first_token_time = time.time()
            
            print(content, end="", flush=True)
            full_content += content
    
    end_time = time.time()
    
    print(f"\n\n⏱️ 首个token延迟：{first_token_time - start_time:.2f}秒")
    print(f"⏱️ 总耗时：{end_time - start_time:.2f}秒")
    print("（用户几乎立即就能看到内容开始输出）")


def demo_streaming_with_callback():
    """演示3：流式响应 + 回调处理"""
    print("\n" + "=" * 60)
    print("演示3：流式响应 + 回调处理")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    # 定义回调函数
    def on_token(token: str):
        """每收到一个token时调用"""
        print(f"[收到token] {repr(token)}")
    
    def on_complete(full_text: str):
        """生成完成时调用"""
        print(f"\n[生成完成] 总长度：{len(full_text)}字")
    
    print("\n开始生成：\n")
    
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "数到5"}
        ],
        stream=True
    )
    
    full_content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            on_token(content)
            full_content += content
    
    on_complete(full_content)


def chat_streaming(user_message: str):
    """封装好的流式对话函数"""
    client = get_client()
    model = get_model()
    
    print(f"用户：{user_message}")
    print("AI：", end="", flush=True)
    
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )
    
    full_content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_content += content
    
    print()  # 换行
    return full_content


def demo_interactive():
    """演示4：交互式流式对话"""
    print("\n" + "=" * 60)
    print("演示4：交互式流式对话")
    print("=" * 60)
    print("输入 'quit' 退出\n")
    
    while True:
        try:
            user_input = input("\n用户：").strip()
        except (EOFError, KeyboardInterrupt):
            break
        
        if not user_input:
            continue
        if user_input.lower() == 'quit':
            break
        
        print("AI：", end="", flush=True)
        
        client = get_client()
        model = get_model()
        
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_input}],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print()  # 换行
    
    print("\n再见！")


if __name__ == "__main__":
    demo_non_streaming()
    demo_streaming()
    demo_streaming_with_callback()
    
    # 交互式演示（可选）
    # demo_interactive()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n流式响应核心知识：")
    print("  1. stream=True 开启流式")
    print("  2. 返回的是迭代器，逐个chunk处理")
    print("  3. chunk.choices[0].delta.content 获取内容")
    print("  4. 优势：首token延迟低，用户体验好")
    print("  5. 适用场景：长文本生成、聊天机器人")

