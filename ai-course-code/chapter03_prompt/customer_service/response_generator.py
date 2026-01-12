"""
第3章-Prompt工程实战：回复生成器
对应课程：第15课-提示词工程实战

功能：根据用户意图生成合适的回复
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class ResponseGenerator:
    """回复生成器"""
    
    # 各类意图的提示词模板
    TEMPLATES = {
        "order_query": """你是一位专业的电商客服。

用户咨询订单相关问题。请给出友好、专业的回复。

回复要点：
- 语气友好、耐心
- 提供具体的操作指导
- 告知查询方式或预计时间
- 长度：50-80字

用户：{user_input}
客服：""",
        
        "refund": """你是一位专业的电商客服。

用户想申请退换货。请给出友好、专业的回复。

回复要点：
- 表示理解和抱歉
- 说明退换货流程
- 引导用户操作（进入订单详情→申请退货）
- 语气诚恳

用户：{user_input}
客服：""",
        
        "product_inquiry": """你是一位专业的电商客服。

用户咨询商品相关信息。请给出友好、专业的回复。

回复要点：
- 针对问题给出答案
- 如果不确定，引导用户查看商品详情页
- 语气专业但不生硬

用户：{user_input}
客服：""",
        
        "complaint": """你是一位专业的电商客服。

用户表达不满或投诉。请给出真诚、安抚性的回复。

回复要点：
- 首先表达歉意和理解
- 表示会重视问题
- 说明会转人工客服跟进
- 语气真诚、有同理心

用户：{user_input}
客服：""",
        
        "account": """你是一位专业的电商客服。

用户遇到账户相关问题。请给出专业的回复。

回复要点：
- 给出解决方案的步骤
- 强调账户安全
- 如涉及敏感操作，建议联系人工

用户：{user_input}
客服：""",
        
        "other": """你是一位友好的电商客服。

用户的咨询不在常见问题范围内。请友好回应并引导。

回复要点：
- 友好回应
- 询问具体需求
- 引导到常见问题或转人工

用户：{user_input}
客服："""
    }
    
    def __init__(self):
        """初始化"""
        self.client = OpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        )
        self.model = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
    
    def generate(self, user_input: str, intent: str) -> str:
        """
        生成回复
        
        Args:
            user_input: 用户输入
            intent: 意图类别
            
        Returns:
            回复内容
        """
        template = self.TEMPLATES.get(intent, self.TEMPLATES["other"])
        prompt = template.replace('{user_input}', user_input)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"回复生成错误：{e}")
            return "抱歉，我暂时无法回答您的问题。请联系人工客服，谢谢！"


if __name__ == "__main__":
    # 测试
    generator = ResponseGenerator()
    
    test_cases = [
        ("我的订单什么时候到？", "order_query"),
        ("我要退货", "refund"),
        ("这个手机支持5G吗？", "product_inquiry"),
        ("你们服务太差了！", "complaint")
    ]
    
    print("=" * 50)
    print("回复生成器测试")
    print("=" * 50)
    
    for text, intent in test_cases:
        response = generator.generate(text, intent)
        print(f"\n用户：{text}")
        print(f"意图：{intent}")
        print(f"回复：{response}")
        print("-" * 40)

