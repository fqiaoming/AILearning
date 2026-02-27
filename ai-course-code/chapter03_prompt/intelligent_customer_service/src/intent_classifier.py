"""
意图分类器
对应课程：第15课-提示词工程实战

功能：识别用户咨询的意图类别
技巧：Few-shot + 明确输出格式
"""

from openai import OpenAI
from .utils import load_prompt, get_llm_config


class IntentClassifier:
    """意图分类器 - 识别用户咨询属于哪个类别"""
    
    # 意图映射：中文 → 英文标识
    INTENTS = {
        "订单查询": "order_query",
        "退换货": "refund",
        "商品咨询": "product_inquiry",
        "投诉建议": "complaint",
        "账户问题": "account",
        "其他": "other",
    }
    
    def __init__(self):
        """初始化分类器，加载提示词和LLM客户端"""
        config = get_llm_config()
        self.client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
        )
        self.model = config["model"]
        
        # 从文件加载提示词模板
        self.prompt_template = load_prompt("prompts/intent_recognition.md")
    
    def classify(self, user_input: str) -> tuple:
        """
        分类用户输入的意图
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            (意图英文标识, 置信度) 例如 ("order_query", 0.9)
        """
        prompt = self.prompt_template.replace("{user_input}", user_input)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # 低温度，确保分类稳定
                max_tokens=50,
            )
            
            result = response.choices[0].message.content.strip()
            
            # 将中文意图映射为英文标识
            for intent_cn, intent_en in self.INTENTS.items():
                if intent_cn in result:
                    return intent_en, 0.9
            
            return "other", 0.5
            
        except Exception as e:
            print(f"意图识别错误：{e}")
            return "other", 0.0
    
    def classify_batch(self, inputs: list) -> list:
        """
        批量分类
        
        Args:
            inputs: 用户输入列表
            
        Returns:
            [(意图, 置信度), ...] 列表
        """
        return [self.classify(text) for text in inputs]


# 独立运行测试
if __name__ == "__main__":
    import sys
    import os
    # 添加项目根目录到路径，方便独立运行
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    classifier = IntentClassifier()
    
    test_cases = [
        "我的订单什么时候到？",
        "我要退货",
        "这个手机支持5G吗？",
        "你们服务太差了！",
        "忘记密码了",
        "今天天气不错",
    ]
    
    print("=" * 50)
    print("意图分类器测试")
    print("=" * 50)
    
    for text in test_cases:
        intent, conf = classifier.classify(text)
        print(f"\n输入：{text}")
        print(f"意图：{intent}，置信度：{conf}")
