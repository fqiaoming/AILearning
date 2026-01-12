"""
第3章-Prompt工程：Few-shot与Chain-of-Thought
对应课程：第12课-Few-shot与CoT

Few-shot：给AI看例子
Chain-of-Thought：让AI一步步思考
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


def demo_fewshot():
    """演示Few-shot学习"""
    print("=" * 60)
    print("Few-shot学习演示")
    print("=" * 60)
    print("""
Few-shot = 给AI看例子
- Zero-shot：不给例子
- One-shot：给1个例子
- Few-shot：给2-5个例子
""")
    
    client = get_client()
    
    # Zero-shot
    zero_shot = """判断以下评论的情感：
评论：这个产品太棒了，强烈推荐！
情感："""
    
    # Few-shot
    few_shot = """判断以下评论的情感（正面/负面/中性）：

示例1：
评论：这个产品太棒了，强烈推荐！
情感：正面

示例2：
评论：质量太差了，买了就后悔
情感：负面

示例3：
评论：还行吧，一般般
情感：中性

现在判断：
评论：包装很精美，但是用了两天就坏了
情感："""
    
    print("\n【Zero-shot（无示例）】")
    print(f"提示词：{zero_shot}")
    print(f"AI输出：{chat(client, zero_shot, 0.3)}")
    
    print("\n【Few-shot（有示例）】")
    print("提示词：（包含3个示例）")
    print(f"AI输出：{chat(client, few_shot, 0.3)}")
    
    print("\n💡 结论：给了示例，AI更能理解你要什么格式和标准")


def demo_chain_of_thought():
    """演示Chain-of-Thought思维链"""
    print("\n" + "=" * 60)
    print("Chain-of-Thought（思维链）演示")
    print("=" * 60)
    print("""
CoT的核心：让AI把思考过程展示出来
魔法咒语：Let's think step by step
""")
    
    client = get_client()
    
    # 数学应用题
    math_problem = """Roger有5个网球。他又买了2罐网球，每罐3个球。他现在有多少个球？"""
    
    # 不用CoT
    direct_prompt = f"{math_problem}\n答案："
    
    # 用CoT
    cot_prompt = f"""{math_problem}

让我们一步步思考："""
    
    print("\n【不用CoT - 直接回答】")
    print(f"问题：{math_problem}")
    print(f"AI输出：{chat(client, direct_prompt, 0.3)}")
    
    print("\n【用CoT - 一步步思考】")
    print(f"问题：{math_problem}")
    print("提示词加了：让我们一步步思考")
    print(f"AI输出：\n{chat(client, cot_prompt, 0.3)}")
    
    print("\n💡 结论：CoT让AI'慢下来思考'，推理准确率大幅提升")


def demo_fewshot_cot_combined():
    """演示Few-shot + CoT组合"""
    print("\n" + "=" * 60)
    print("Few-shot + CoT 组合使用")
    print("=" * 60)
    
    client = get_client()
    
    combined_prompt = """示例1：
问题：小明有15元，买了3支铅笔，每支2元，还剩多少钱？
思考过程：
1. 计算铅笔总价：3×2=6元
2. 计算剩余：15-6=9元
答案：9元

示例2：
问题：一个班30人，女生比男生多6人，男生有多少人？
思考过程：
1. 设男生x人，女生(x+6)人
2. 方程：x+(x+6)=30
3. 求解：2x=24，x=12
答案：12人

现在请解决：
问题：一辆汽车每小时行驶60公里，从A城到B城用了3小时，B城到C城用了2小时，A城到C城的距离是多少公里？
思考过程："""
    
    print("【组合提示词】")
    print("（2个带思考过程的示例 + 新问题）")
    print(f"\nAI输出：\n{chat(client, combined_prompt, 0.3)}")
    
    print("\n💡 结论：Few-shot + CoT 组合 = 效果最强！")


if __name__ == "__main__":
    demo_fewshot()
    demo_chain_of_thought()
    demo_fewshot_cot_combined()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n核心记忆：")
    print("  1. Few-shot：示例消除歧义，2-3个最佳")
    print("  2. CoT：'让我们一步步思考'，推理能力翻倍")
    print("  3. 组合使用效果最强")

