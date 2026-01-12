"""
第4章-OpenAI API：API基础调用
对应课程：第16课-OpenAI API入门

功能：演示Chat Completions API的基本用法
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_client():
    """
    获取AI客户端
    优先使用本地LM Studio（免费），如果配置了OpenAI则使用OpenAI
    """
    if os.getenv("OPENAI_API_KEY"):
        print("使用：OpenAI API")
        return OpenAI()
    else:
        print("使用：本地LM Studio")
        return OpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        )


def get_model():
    """获取模型名称"""
    if os.getenv("OPENAI_API_KEY"):
        return "gpt-3.5-turbo"
    else:
        return os.getenv("LM_STUDIO_MODEL", "qwen/qwen3-30b-a3b-2507")


def demo_basic_chat():
    """演示1：基础对话"""
    print("=" * 60)
    print("演示1：基础Chat Completions调用")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    # 最简单的调用方式
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "你好！请用一句话介绍你自己"}
        ]
    )
    
    print(f"\n模型：{model}")
    print(f"问题：你好！请用一句话介绍你自己")
    print(f"回答：{response.choices[0].message.content}")
    print(f"\nToken使用：")
    print(f"  - 输入：{response.usage.prompt_tokens}")
    print(f"  - 输出：{response.usage.completion_tokens}")
    print(f"  - 总计：{response.usage.total_tokens}")


def demo_system_message():
    """演示2：使用system消息"""
    print("\n" + "=" * 60)
    print("演示2：使用System消息定义角色")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    # 使用system消息定义AI的角色
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": "你是一位专业的Python程序员，回答简洁专业，代码要有注释"
            },
            {
                "role": "user", 
                "content": "写一个快速排序函数"
            }
        ],
        temperature=0.3  # 代码生成用较低温度
    )
    
    print(f"\nSystem: 你是一位专业的Python程序员...")
    print(f"User: 写一个快速排序函数")
    print(f"\n回答：\n{response.choices[0].message.content}")


def demo_multi_turn():
    """演示3：多轮对话"""
    print("\n" + "=" * 60)
    print("演示3：多轮对话")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    # 模拟多轮对话
    messages = [
        {"role": "system", "content": "你是一位友好的AI助手"},
        {"role": "user", "content": "我叫小明"},
        {"role": "assistant", "content": "你好小明！很高兴认识你！有什么我可以帮助你的吗？"},
        {"role": "user", "content": "你还记得我叫什么名字吗？"}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    
    print("\n对话历史：")
    for msg in messages:
        role = msg["role"].upper()
        print(f"  [{role}] {msg['content']}")
    
    print(f"\n  [ASSISTANT] {response.choices[0].message.content}")
    print("\n💡 注意：多轮对话需要把历史消息一起发送")


def demo_parameters():
    """演示4：各种参数的作用"""
    print("\n" + "=" * 60)
    print("演示4：重要参数说明")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    # 不同temperature的效果
    prompt = "给我的AI项目起一个名字"
    temperatures = [0.1, 0.7, 1.2]
    
    print(f"\n问题：{prompt}")
    print("\n【temperature参数对比】")
    print("（控制输出的随机性/创造性）")
    
    for temp in temperatures:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp
            # ,
            # max_tokens=50
        )
        print(f"\n  temperature={temp}: {response.choices[0].message.content}")
    
    print("\n💡 总结：")
    print("  - temperature=0.1：输出确定性强，适合代码/翻译")
    print("  - temperature=0.7：平衡，适合大多数场景")
    print("  - temperature=1.2：输出随机，适合创意写作")


def demo_response_format():
    """演示5：指定返回格式"""
    print("\n" + "=" * 60)
    print("演示5：JSON格式输出")
    print("=" * 60)
    
    client = get_client()
    model = get_model()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是一个API，只返回JSON格式的数据，不要有其他文字"
            },
            {
                "role": "user",
                "content": "分析这句话的情感：'这个产品太棒了，强烈推荐！'。返回JSON格式，包含sentiment和confidence字段"
            }
        ],
        temperature=0.3
    )
    
    print(f"\n任务：情感分析，返回JSON格式")
    print(f"输入：'这个产品太棒了，强烈推荐！'")
    print(f"\n输出：\n{response.choices[0].message.content}")


if __name__ == "__main__":
    # demo_basic_chat()
    # demo_system_message()
    # demo_multi_turn()
    demo_parameters()
    # demo_response_format()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n核心知识点：")
    print("  1. messages格式：[{role, content}, ...]")
    print("  2. role类型：system（角色设定）、user（用户）、assistant（AI回复）")
    print("  3. temperature：控制输出随机性（0-2）")
    print("  4. max_tokens：限制输出长度")
    print("  5. 多轮对话：需要包含历史消息")

