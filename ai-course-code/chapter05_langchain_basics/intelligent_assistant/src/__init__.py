"""
智能对话助手 - Intelligent Assistant
第5章第28课：LangChain实战项目1

模块说明：
- assistant: 智能助手主逻辑
- intent_classifier: 意图识别
- conversation_manager: 对话管理
- tools: 工具集
- config: 配置管理
"""

from .assistant import IntelligentAssistant
from .intent_classifier import IntentClassifier
from .conversation_manager import ConversationManager
from .tools import Tools

__all__ = [
    "IntelligentAssistant",
    "IntentClassifier",
    "ConversationManager",
    "Tools",
]
