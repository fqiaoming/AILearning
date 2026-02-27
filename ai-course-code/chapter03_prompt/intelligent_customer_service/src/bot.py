"""
智能客服机器人主逻辑
对应课程：第15课-提示词工程实战

功能：整合意图识别、回复生成、转人工判断的完整客服系统
"""

from .intent_classifier import IntentClassifier
from .response_generator import ResponseGenerator
from .utils import log_conversation


class CustomerServiceBot:
    """智能客服机器人 - 完整的对话处理流程"""
    
    # 转人工的提示消息
    HANDOFF_MESSAGES = {
        "complaint": "非常抱歉给您带来不好的体验。我已经为您转接人工客服，稍后会有专人为您处理，请您稍等。",
        "account": "您的账户问题需要人工客服协助处理，为了保障您的账户安全，我已为您转接专属客服。",
        "default": "您的问题比较复杂，我已为您转接人工客服，请稍等片刻。",
    }
    
    # 触发转人工的关键词
    HANDOFF_KEYWORDS = ["投诉", "经理", "人工", "转人工", "找人工", "真人"]
    
    def __init__(self):
        """初始化客服机器人"""
        self.intent_classifier = IntentClassifier()
        self.response_generator = ResponseGenerator()
        self.conversation_history = []
    
    def chat(self, user_input: str) -> dict:
        """
        处理用户输入，返回完整的响应结果
        
        流程：意图识别 → 转人工判断 → 生成回复 → 记录历史
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            {
                'intent': 意图标识,
                'response': 回复内容,
                'should_handoff': 是否转人工,
                'confidence': 置信度
            }
        """
        # 1. 意图识别
        intent, confidence = self.intent_classifier.classify(user_input)
        
        # 2. 判断是否需要转人工
        should_handoff = self._should_handoff(intent, confidence, user_input)
        
        # 3. 生成回复
        if should_handoff:
            response = self._get_handoff_message(intent)
        else:
            response = self.response_generator.generate(
                user_input, intent, self.conversation_history
            )
        
        # 4. 记录对话历史
        self.conversation_history.append({
            "user": user_input,
            "intent": intent,
            "bot": response,
        })
        
        # 5. 记录日志
        log_conversation(user_input, intent, response, confidence)
        
        return {
            "intent": intent,
            "response": response,
            "should_handoff": should_handoff,
            "confidence": confidence,
        }
    
    def _should_handoff(self, intent: str, confidence: float,
                        user_input: str) -> bool:
        """
        判断是否需要转人工客服
        
        转人工规则（任一满足即转）：
        1. 投诉类意图 → 直接转人工
        2. 置信度低于0.6 → AI不确定，转人工
        3. 包含转人工关键词 → 用户主动要求
        4. 对话超过5轮未解决 → 避免用户等待过久
        """
        # 规则1：投诉直接转人工
        if intent == "complaint":
            return True
        
        # 规则2：置信度太低，AI不确定
        if confidence < 0.6:
            return True
        
        # 规则3：用户主动要求转人工
        if any(kw in user_input for kw in self.HANDOFF_KEYWORDS):
            return True
        
        # 规则4：对话轮数过多，可能问题复杂
        if len(self.conversation_history) > 5:
            return True
        
        return False
    
    def _get_handoff_message(self, intent: str) -> str:
        """获取转人工的提示消息"""
        return self.HANDOFF_MESSAGES.get(intent, self.HANDOFF_MESSAGES["default"])
    
    def reset(self):
        """重置对话历史，开始新的会话"""
        self.conversation_history = []
    
    def get_history(self) -> list:
        """获取当前对话历史"""
        return self.conversation_history.copy()


def main():
    """交互式命令行测试入口"""
    print("=" * 60)
    print("🤖 智能客服系统 v1.0")
    print("=" * 60)
    print("输入 'quit' 退出，输入 'reset' 重置对话\n")
    
    bot = CustomerServiceBot()
    
    while True:
        try:
            user_input = input("用户：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n感谢使用，再见！")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == "quit":
            print("感谢使用，再见！")
            break
        
        if user_input.lower() == "reset":
            bot.reset()
            print("对话已重置\n")
            continue
        
        # 处理用户输入
        result = bot.chat(user_input)
        
        # 显示结果
        print(f"[意图：{result['intent']}，置信度：{result['confidence']:.2f}]")
        print(f"客服：{result['response']}")
        
        if result["should_handoff"]:
            print("[系统]：已转人工客服")
        
        print()


if __name__ == "__main__":
    main()
