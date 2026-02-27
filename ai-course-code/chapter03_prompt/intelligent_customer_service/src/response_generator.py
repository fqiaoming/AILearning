"""
回复生成器
对应课程：第15课-提示词工程实战

功能：根据用户意图生成合适的客服回复
技巧：角色设定 + 回复要点约束 + 上下文感知
"""

from openai import OpenAI
from .utils import get_llm_config, format_conversation_history


class ResponseGenerator:
    """回复生成器 - 根据意图生成个性化客服回复"""
    
    # 各意图对应的提示词模板
    TEMPLATES = {
        "order_query": """你是一位专业的电商客服，正在帮助用户处理订单相关问题。

回复要求：
- 语气友好、耐心
- 提供具体的操作指导（如何查看订单、物流等）
- 告知查询方式或预计时间
- 如果用户提供了订单号，表示会帮忙查询
- 长度：50-100字
- 不要编造具体的物流信息

对话历史：
{context}

用户：{user_input}
客服：""",

        "refund": """你是一位专业的电商客服，正在帮助用户处理退换货问题。

回复要求：
- 首先表示理解和抱歉
- 说明退换货流程：进入"我的订单"→选择对应订单→点击"申请退货/换货"→填写原因→提交
- 告知退款时间：审核通过后3-5个工作日
- 引导用户操作
- 语气诚恳、有耐心
- 长度：60-120字

对话历史：
{context}

用户：{user_input}
客服：""",

        "product_inquiry": """你是一位专业的电商客服，正在帮助用户了解商品信息。

回复要求：
- 针对用户的问题给出回答
- 如果不确定具体参数，引导用户查看商品详情页
- 可以推荐用户查看评价区了解其他买家的使用体验
- 语气专业但不生硬，像朋友一样推荐
- 长度：50-100字

对话历史：
{context}

用户：{user_input}
客服：""",

        "complaint": """你是一位专业的电商客服，用户正在表达不满或投诉。

回复要求：
- 首先真诚地表达歉意
- 表示理解用户的感受（共情）
- 表示会重视并记录问题
- 说明会转接人工客服跟进处理
- 语气真诚、有同理心，不要敷衍
- 长度：60-100字

对话历史：
{context}

用户：{user_input}
客服：""",

        "account": """你是一位专业的电商客服，正在帮助用户处理账户相关问题。

回复要求：
- 给出清晰的解决步骤
- 强调账户安全的重要性
- 如涉及敏感操作（修改密码、绑定手机等），建议通过官方渠道操作
- 复杂问题建议联系人工客服
- 长度：50-100字

对话历史：
{context}

用户：{user_input}
客服：""",

        "other": """你是一位友好的电商客服，用户的咨询不在常见问题范围内。

回复要求：
- 友好回应用户
- 询问是否有具体需要帮助的问题
- 引导用户描述具体需求
- 如果是闲聊，简短友好回应后引导回正题
- 长度：30-60字

对话历史：
{context}

用户：{user_input}
客服：""",
    }
    
    def __init__(self):
        """初始化回复生成器"""
        config = get_llm_config()
        self.client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
        )
        self.model = config["model"]
    
    def generate(self, user_input: str, intent: str,
                 context: list = None) -> str:
        """
        根据意图生成客服回复
        
        Args:
            user_input: 用户输入
            intent: 意图类别（英文标识）
            context: 对话历史列表
            
        Returns:
            生成的回复文本
        """
        template = self.TEMPLATES.get(intent, self.TEMPLATES["other"])
        
        # 格式化对话历史
        context_str = format_conversation_history(context) if context else "无"
        
        prompt = template.replace("{user_input}", user_input)
        prompt = prompt.replace("{context}", context_str)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,  # 适中温度，保证回复多样性
                max_tokens=200,
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"回复生成错误：{e}")
            return "抱歉，我暂时无法回答您的问题。请联系人工客服，谢谢！"


# 独立运行测试
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    generator = ResponseGenerator()
    
    test_cases = [
        ("我的订单什么时候到？", "order_query"),
        ("我要退货", "refund"),
        ("这个手机支持5G吗？", "product_inquiry"),
        ("你们服务太差了！", "complaint"),
        ("忘记密码了怎么办", "account"),
        ("你好呀", "other"),
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
