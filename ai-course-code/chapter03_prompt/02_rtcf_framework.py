"""
第3章-Prompt工程：RTCF框架
对应课程：第09课-提示词四大要素

RTCF = Role + Task + Context + Format
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_client():
    """获取AI客户端"""
    return OpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
    )


def chat(client, prompt, temperature=0.7):
    """发送对话请求"""
    response = client.chat.completions.create(
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=800
    )
    return response.choices[0].message.content


def demo_rtcf_elements():
    """演示RTCF四大要素"""
    print("=" * 60)
    print("RTCF框架演示")
    print("=" * 60)
    print("""
RTCF = 提示词四大要素：
  R - Role（角色）：告诉AI它是谁
  T - Task（任务）：告诉AI要做什么
  C - Context（背景）：提供上下文信息
  F - Format（格式）：指定输出格式
""")
    
    client = get_client()
    
    # RTCF完整示例
    rtcf_prompt = """【R - Role】
你是一位有10年经验的Python后端工程师。

【T - Task】
任务：实现用户注册API接口
功能要求：
1. 接收用户名、密码、邮箱
2. 验证输入合法性
3. 返回注册结果

【C - Context】
背景：SaaS平台用户系统，日活1万
技术栈：Python 3.10 + FastAPI

【F - Format】
输出：完整代码 + 简短注释"""
    
    print("【RTCF完整提示词】")
    print(rtcf_prompt)
    print("\n" + "-" * 60)
    print("AI输出：\n")
    
    response = chat(client, rtcf_prompt, temperature=0.3)
    print(response)


def demo_each_element():
    """分别演示每个要素的作用"""
    print("\n" + "=" * 60)
    print("各要素单独演示")
    print("=" * 60)
    
    client = get_client()
    
    # Role的作用
    print("\n【Role - 角色的作用】")
    prompts = [
        ("无角色", "解释什么是微服务"),
        ("初学者导师", "你是一位耐心的技术导师，向编程新手解释什么是微服务"),
        ("架构师", "你是一位有10年经验的系统架构师，解释什么是微服务"),
    ]
    
    for name, prompt in prompts:
        print(f"\n{name}：")
        response = chat(client, prompt, temperature=0.5)
        print(response[:150] + "..." if len(response) > 150 else response)
    
    # Format的作用
    print("\n" + "-" * 60)
    print("\n【Format - 格式的作用】")
    
    base_task = "列出Python的5个优点"
    formats = [
        ("无格式", base_task),
        ("列表格式", f"{base_task}\n\n输出格式：用数字列表，每条不超过20字"),
        ("JSON格式", f"{base_task}\n\n输出格式：JSON数组，每项包含title和description字段"),
    ]
    
    for name, prompt in formats:
        print(f"\n{name}：")
        response = chat(client, prompt, temperature=0.3)
        print(response[:200] + "..." if len(response) > 200 else response)


if __name__ == "__main__":
    demo_rtcf_elements()
    demo_each_element()
    
    print("\n" + "=" * 60)
    print("✅ RTCF框架演示完成！")
    print("\n口诀：角色定身份，任务说清楚，背景给上下文，格式要明确")

