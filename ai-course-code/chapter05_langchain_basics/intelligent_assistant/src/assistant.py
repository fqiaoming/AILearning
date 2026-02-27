"""
智能助手主逻辑
对应课程：第28课-LangChain实战项目1

整合意图识别、对话管理、工具调用、Chain路由的完整对话助手
核心技术：LCEL链式调用、Fallback降级、多Chain路由
"""

import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

from .intent_classifier import IntentClassifier
from .conversation_manager import ConversationManager
from .tools import Tools, TOOL_DESCRIPTIONS
from .config import config


class IntelligentAssistant:
    """
    智能对话助手
    
    处理流程：
    1. 保存用户消息
    2. 意图识别（chat / tool_call / question / complex）
    3. 工具调用检测（关键词匹配）
    4. 根据意图路由到对应Chain处理
    5. 保存助手回复
    """

    def __init__(self, session_id: str = "default"):
        """
        Args:
            session_id: 会话ID，用于区分不同用户/会话
        """
        self.session_id = session_id

        # 初始化组件
        self.intent_classifier = IntentClassifier()
        self.conversation_manager = ConversationManager(
            max_history=config.MAX_CONVERSATION_HISTORY
        )
        self.tools = Tools()

        # 初始化LLM模型
        if config.USE_LOCAL_MODEL:
            self.primary_model = ChatOpenAI(
                base_url=config.LOCAL_LLM_URL,
                api_key=config.LOCAL_LLM_API_KEY,
                model=config.LOCAL_MODEL,
                temperature=0.7,
                timeout=config.TIMEOUT,
            )
            self.fallback_model = ChatOpenAI(
                base_url=config.LOCAL_LLM_URL,
                api_key=config.LOCAL_LLM_API_KEY,
                model=config.LOCAL_MODEL,
                temperature=0.7,
            )
        else:
            self.primary_model = ChatOpenAI(
                model=config.PRIMARY_MODEL,
                temperature=0.7,
                timeout=config.TIMEOUT,
            )
            self.fallback_model = ChatOpenAI(
                model=config.FALLBACK_MODEL,
                temperature=0.7,
            )

        # 构建各类处理Chain
        self._build_chains()

    def _build_chains(self):
        """构建不同意图对应的处理链"""

        # 闲聊Chain（带Fallback降级）
        primary_chat = (
            ChatPromptTemplate.from_messages([
                ("system", "你是一个友好的AI助手，用简洁有趣的方式回答。保持轻松的语气。"),
                ("human", "{message}"),
            ])
            | self.primary_model
            | StrOutputParser()
        )
        fallback_chat = (
            ChatPromptTemplate.from_messages([
                ("system", "你是助手，请简短回答。"),
                ("human", "{message}"),
            ])
            | self.fallback_model
            | StrOutputParser()
        )
        self.chat_chain = primary_chat.with_fallbacks([fallback_chat])

        # 知识问答Chain
        self.qa_chain = (
            ChatPromptTemplate.from_messages([
                ("system",
                 "你是知识专家，提供准确、详细、有条理的回答。"
                 "如果不确定，请诚实说明。"),
                ("human", "{message}"),
            ])
            | self.primary_model
            | StrOutputParser()
        )

        # 复杂任务Chain（引导分步思考）
        self.complex_chain = (
            ChatPromptTemplate.from_messages([
                ("system",
                 "你是高级AI助手，擅长处理复杂任务。\n"
                 "请分步骤思考，给出详细的分析和建议。\n"
                 "使用清晰的结构组织回答。"),
                ("human", "{message}"),
            ])
            | self.primary_model
            | StrOutputParser()
        )

        # 工具结果整合Chain（将工具返回值转为自然语言）
        self.tool_response_chain = (
            ChatPromptTemplate.from_template(
                "用户问：{message}\n"
                "工具调用：{tool_name}\n"
                "工具结果：{result}\n\n"
                "请用自然、友好的语言回答用户的问题。"
            )
            | self.primary_model
            | StrOutputParser()
        )

    def _detect_tool_call(self, message: str) -> tuple:
        """
        检测是否需要调用工具（基于关键词匹配）
        
        Returns:
            (tool_name, params) 或 (None, {})
        """
        # 时间查询
        if any(word in message for word in ["时间", "几点", "日期", "今天"]):
            return ("get_current_time", {})

        # 天气查询
        if any(word in message for word in ["天气", "气温", "下雨"]):
            cities = ["北京", "上海", "深圳", "广州", "杭州", "成都"]
            for city in cities:
                if city in message:
                    return ("get_weather", {"city": city})
            return ("get_weather", {"city": "北京"})

        # 计算器
        if any(word in message for word in ["计算", "等于", "算一下"]):
            expr = re.findall(r'[\d+\-*/().%\s]+', message)
            if expr:
                return ("calculator", {"expression": expr[0].strip()})

        # 知识搜索
        if any(word in message for word in ["什么是", "解释一下", "介绍"]):
            # 提取搜索关键词
            for prefix in ["什么是", "解释一下", "介绍"]:
                if prefix in message:
                    query = message.split(prefix)[-1].strip().rstrip("？?。")
                    if query:
                        return ("search_knowledge", {"query": query})

        return (None, {})

    def chat(self, message: str) -> dict:
        """
        处理用户消息，返回完整响应
        
        Args:
            message: 用户输入文本
            
        Returns:
            {
                'success': bool,
                'response': str,
                'intent': str,
                'confidence': float,
                'tool_used': str or None
            }
        """
        # 1. 保存用户消息
        self.conversation_manager.add_message(
            self.session_id, "user", message
        )

        try:
            # 2. 意图识别
            if config.ENABLE_INTENT_CLASSIFICATION:
                intent = self.intent_classifier.classify(message)
            else:
                from .intent_classifier import Intent
                intent = Intent(category="chat", confidence=1.0, reason="分类已禁用")

            # 3. 检测工具调用
            tool_name, tool_params = self._detect_tool_call(message)
            tool_used = None

            # 4. 根据意图路由处理
            if tool_name and config.ENABLE_TOOLS:
                response = self._handle_tool_call(tool_name, tool_params, message)
                tool_used = tool_name

            elif intent.category == "chat":
                response = self.chat_chain.invoke({"message": message})

            elif intent.category == "question":
                response = self.qa_chain.invoke({"message": message})

            elif intent.category == "complex":
                response = self.complex_chain.invoke({"message": message})

            else:
                response = self.chat_chain.invoke({"message": message})

            # 5. 保存助手回复
            self.conversation_manager.add_message(
                self.session_id, "assistant", response
            )

            return {
                "success": True,
                "response": response,
                "intent": intent.category,
                "confidence": intent.confidence,
                "tool_used": tool_used,
            }

        except Exception as e:
            error_msg = f"抱歉，我遇到了一些问题，请稍后再试。（错误：{e}）"
            self.conversation_manager.add_message(
                self.session_id, "assistant", error_msg
            )
            return {
                "success": False,
                "response": error_msg,
                "intent": "error",
                "confidence": 0.0,
                "tool_used": None,
                "error": str(e),
            }

    def _handle_tool_call(self, tool_name: str, params: dict,
                          original_message: str) -> str:
        """
        处理工具调用：执行工具 → 用AI整合结果为自然语言
        """
        # 调用工具函数
        tool_function = getattr(self.tools, tool_name)
        tool_result = tool_function(**params)

        # 用Chain将工具结果转为自然语言回复
        response = self.tool_response_chain.invoke({
            "message": original_message,
            "tool_name": TOOL_DESCRIPTIONS.get(tool_name, {}).get("name", tool_name),
            "result": tool_result,
        })

        return response

    def get_history(self) -> list:
        """获取当前会话的对话历史"""
        return self.conversation_manager.get_history(self.session_id)

    def clear_history(self):
        """清除当前会话的对话历史"""
        self.conversation_manager.clear_history(self.session_id)

    def get_context_summary(self) -> str:
        """获取当前会话的上下文摘要"""
        return self.conversation_manager.get_context_summary(self.session_id)


def main():
    """交互式命令行测试入口"""
    print("🤖 智能对话助手 v1.0")
    print("=" * 60)
    print("输入 'quit' 退出，输入 'clear' 清除历史")
    print("输入 'history' 查看对话历史\n")

    assistant = IntelligentAssistant()

    while True:
        try:
            user_input = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！👋")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("再见！👋")
            break

        if user_input.lower() == "clear":
            assistant.clear_history()
            print("历史已清除\n")
            continue

        if user_input.lower() == "history":
            history = assistant.get_history()
            if not history:
                print("暂无对话历史\n")
            else:
                for msg in history:
                    role = "你" if msg["role"] == "user" else "助手"
                    print(f"  {role}：{msg['content']}")
                print()
            continue

        # 处理消息
        result = assistant.chat(user_input)

        # 显示回复
        print(f"\n助手：{result['response']}")

        # 显示调试信息
        debug_parts = []
        if result.get("intent"):
            debug_parts.append(f"意图：{result['intent']}")
        if result.get("confidence"):
            debug_parts.append(f"置信度：{result['confidence']:.2f}")
        if result.get("tool_used"):
            debug_parts.append(f"工具：{result['tool_used']}")
        if debug_parts:
            print(f"[{', '.join(debug_parts)}]")

        print()


if __name__ == "__main__":
    main()
