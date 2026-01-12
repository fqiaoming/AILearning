"""
第3章-Prompt工程：提示词基础
对应课程：第08课-提示词是什么

功能：展示好提示词vs差提示词的效果对比
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
        max_tokens=500
    )
    return response.choices[0].message.content


def demo_bad_vs_good_prompt():
    """演示差的提示词 vs 好的提示词"""
    print("=" * 60)
    print("提示词基础：好提示词 vs 差提示词")
    print("=" * 60)
    
    client = get_client()
    
    # 差的提示词
    bad_prompt = "写一篇关于AI的文章"
    
    # 好的提示词（RTCF框架）
    good_prompt = """你是一位资深科技作家。

任务：写一篇面向普通大众的AI科普文章

要求：
1. 主题：AI大模型如何改变工作方式
2. 字数：200-300字
3. 结构：开头用故事引入 + 2个应用场景 + 简短展望
4. 风格：通俗易懂，多用比喻"""
    
    print("\n【差的提示词】")
    print(f"提示词：{bad_prompt}")
    print("-" * 40)
    print("AI输出：")
    bad_response = chat(client, bad_prompt)
    print(bad_response[:300] + "..." if len(bad_response) > 300 else bad_response)
    
    print("\n" + "=" * 60)
    
    print("\n【好的提示词】")
    print(f"提示词：\n{good_prompt}")
    print("-" * 40)
    print("AI输出：")
    good_response = chat(client, good_prompt)
    print(good_response)
    
    print("\n" + "=" * 60)
    print("💡 对比总结：")
    print("  差的提示词：AI不知道你要什么，输出泛泛而谈")
    print("  好的提示词：要求明确，AI输出结构清晰、可直接使用")
    print("  记住：AI不是不聪明，是你没说清楚！")


def demo_role_impact():
    """演示角色对输出的影响"""
    print("\n" + "=" * 60)
    print("角色（Role）对输出的影响")
    print("=" * 60)
    
    client = get_client()
    question = "介绍一下Python"
    
    roles = [
        ("无角色", question),
        ("初学者导师", f"你是一位耐心的Python初学者导师。{question}"),
        ("技术专家", f"你是一位有15年经验的Python架构师。{question}"),
    ]
    
    for role_name, prompt in roles:
        print(f"\n【{role_name}】")
        response = chat(client, prompt, temperature=0.5)
        print(response[:200] + "..." if len(response) > 200 else response)
        print("-" * 40)
    
    print("\n💡 结论：同一个问题，角色不同，答案天差地别！")


if __name__ == "__main__":
    demo_bad_vs_good_prompt()
    demo_role_impact()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n核心记忆：")
    print("  1. 提示词的本质 = 用人话给AI编程")
    print("  2. 好提示词 = 角色 + 任务 + 背景 + 格式")
    print("  3. AI不是不聪明，是你没说清楚")

