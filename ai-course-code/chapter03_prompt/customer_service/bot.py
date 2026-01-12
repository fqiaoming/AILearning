"""
第3章-Prompt工程实战：智能客服机器人
对应课程：第15课-提示词工程实战

功能：完整的智能客服系统，整合意图识别和回复生成
"""

from intent_classifier import IntentClassifier
from response_generator import ResponseGenerator


class CustomerServiceBot:
    """智能客服机器人"""
    
    def __init__(self):
        """初始化"""
        self.intent_classifier = IntentClassifier()
        self.response_generator = ResponseGenerator()
        self.conversation_history = []
    
    def chat(self, user_input: str) -> dict:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入
            
        Returns:
            {
                'intent': 意图,
                'response': 回复,
                'should_handoff': 是否转人工,
                'confidence': 置信度
            }
        """
        # 1. 意图识别
        intent, confidence = self.intent_classifier.classify(user_input)
        
        # 2. 判断是否转人工
        should_handoff = self._should_handoff(intent, confidence, user_input)
        
        # 3. 生成回复
        if should_handoff:
            response = self._handoff_message(intent)
        else:
            response = self.response_generator.generate(user_input, intent)
        
        # 4. 记录历史
        self.conversation_history.append({
            'user': user_input,
            'intent': intent,
            'bot': response
        })
        
        return {
            'intent': intent,
            'response': response,
            'should_handoff': should_handoff,
            'confidence': confidence
        }
    
    def _should_handoff(self, intent: str, confidence: float, 
                       user_input: str) -> bool:
        """判断是否需要转人工"""
        # 规则1：投诉直接转人工
        if intent == "complaint":
            return True
        
        # 规则2：置信度太低
        if confidence < 0.6:
            return True
        
        # 规则3：包含特定关键词
        handoff_keywords = ["投诉", "经理", "人工", "转人工"]
        if any(kw in user_input for kw in handoff_keywords):
            return True
        
        # 规则4：对话轮数过多
        if len(self.conversation_history) > 5:
            return True
        
        return False
    
    def _handoff_message(self, intent: str) -> str:
        """转人工的提示消息"""
        messages = {
            "complaint": "非常抱歉给您带来不好的体验。我已经为您转接人工客服，稍后会有专人为您处理。",
            "default": "您的问题比较复杂，我已为您转接人工客服，请稍等。"
        }
        return messages.get(intent, messages["default"])
    
    def reset(self):
        """重置对话历史"""
        self.conversation_history = []


def main():
    """主函数：交互式测试"""
    print("=" * 60)
    print("🤖 智能客服系统")
    print("=" * 60)
    print("输入 'quit' 退出，输入 'reset' 重置对话\n")
    
    bot = CustomerServiceBot()
    
    while True:
        try:
            user_input = input("用户：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n感谢使用！再见！")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("感谢使用！再见！")
            break
        
        if user_input.lower() == 'reset':
            bot.reset()
            print("对话已重置\n")
            continue
        
        # 处理输入
        result = bot.chat(user_input)
        
        # 显示结果
        print(f"[意图：{result['intent']}，置信度：{result['confidence']:.2f}]")
        print(f"客服：{result['response']}")
        
        if result['should_handoff']:
            print("[系统]：已转人工客服")
        
        print()


if __name__ == "__main__":
    main()

