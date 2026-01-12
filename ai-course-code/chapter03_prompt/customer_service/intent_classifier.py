"""
第3章-Prompt工程实战：意图分类器
对应课程：第15课-提示词工程实战

功能：识别用户咨询的意图类别
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class IntentClassifier:
    """意图分类器"""
    
    # 意图类别
    INTENTS = {
        "订单查询": "order_query",
        "退换货": "refund",
        "商品咨询": "product_inquiry",
        "投诉建议": "complaint",
        "账户问题": "account",
        "其他": "other"
    }
    
    # 意图识别提示词
    PROMPT_TEMPLATE = """你是一位专业的客服助手，擅长快速准确地识别用户意图。

任务：判断用户咨询属于以下哪个类别

类别：
1. 订单查询 - 询问订单状态、物流信息
2. 退换货 - 申请退货、换货、退款
3. 商品咨询 - 询问商品信息、使用方法
4. 投诉建议 - 表达不满、投诉、建议
5. 账户问题 - 登录、密码、账户安全
6. 其他 - 闲聊或不明确的咨询

示例：
用户：我的订单什么时候能到啊？
意图：订单查询

用户：这个东西质量太差了，我要退货！
意图：退换货

用户：这个手机有什么颜色？
意图：商品咨询

用户：你们客服态度太差了！
意图：投诉建议

用户：我忘记密码了
意图：账户问题

用户：今天天气真好
意图：其他

---
用户：{user_input}
意图："""
    
    def __init__(self):
        """初始化分类器"""
        self.client = OpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        )
        self.model = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
    
    def classify(self, user_input: str) -> tuple:
        """
        分类用户输入
        
        Args:
            user_input: 用户输入
            
        Returns:
            (意图类别, 置信度)
        """
        prompt = self.PROMPT_TEMPLATE.replace('{user_input}', user_input)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=50
            )
            
            result = response.choices[0].message.content.strip()
            
            # 映射到标准意图
            for intent_cn, intent_en in self.INTENTS.items():
                if intent_cn in result:
                    return intent_en, 0.9
            
            return "other", 0.5
            
        except Exception as e:
            print(f"意图识别错误：{e}")
            return "other", 0.0


if __name__ == "__main__":
    # 测试
    classifier = IntentClassifier()
    
    test_cases = [
        "我的订单什么时候到？",
        "我要退货",
        "这个手机支持5G吗？",
        "你们服务太差了！",
        "忘记密码了",
        "今天天气不错"
    ]
    
    print("=" * 50)
    print("意图分类器测试")
    print("=" * 50)
    
    for text in test_cases:
        intent, conf = classifier.classify(text)
        print(f"\n输入：{text}")
        print(f"意图：{intent}，置信度：{conf}")

