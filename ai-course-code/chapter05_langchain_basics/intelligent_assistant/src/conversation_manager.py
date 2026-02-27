"""
对话管理模块
对应课程：第28课-LangChain实战项目1

管理多轮对话历史，支持多会话、历史裁剪、上下文摘要
"""

from typing import List, Dict, Optional
from datetime import datetime


class ConversationManager:
    """
    对话历史管理器
    
    功能：
    - 多会话支持（通过session_id区分）
    - 自动裁剪历史（防止token超限）
    - 生成上下文摘要
    - 导出LLM兼容的消息格式
    """

    def __init__(self, max_history: int = 10):
        """
        Args:
            max_history: 每个会话最多保留的消息数
        """
        self.max_history = max_history
        self.conversations: Dict[str, List[Dict]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        """
        添加一条消息到对话历史
        
        Args:
            session_id: 会话ID
            role: 角色（user / assistant / system）
            content: 消息内容
        """
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        self.conversations[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })

        # 超出限制时裁剪旧消息
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = \
                self.conversations[session_id][-self.max_history:]

    def get_history(self, session_id: str) -> List[Dict]:
        """获取完整对话历史"""
        return self.conversations.get(session_id, [])

    def get_messages_for_llm(self, session_id: str) -> List[Dict]:
        """
        获取适合LLM输入的消息格式
        
        Returns:
            [{"role": "user", "content": "..."}, ...]
        """
        history = self.get_history(session_id)
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]

    def clear_history(self, session_id: str):
        """清除指定会话的历史"""
        if session_id in self.conversations:
            del self.conversations[session_id]

    def get_context_summary(self, session_id: str) -> str:
        """
        生成当前对话的上下文摘要
        
        用于在提示词中注入简短的上下文信息
        """
        history = self.get_history(session_id)
        if not history:
            return "无历史对话"

        turns = len([m for m in history if m["role"] == "user"])
        summary = f"对话轮数：{turns}\n"

        # 提取最近的用户消息作为话题参考
        recent_user_msgs = [
            m["content"] for m in history if m["role"] == "user"
        ]
        if recent_user_msgs:
            last_topic = recent_user_msgs[-1][:50]
            summary += f"最近话题：{last_topic}..."

        return summary

    def get_session_ids(self) -> List[str]:
        """获取所有活跃的会话ID"""
        return list(self.conversations.keys())

    def get_turn_count(self, session_id: str) -> int:
        """获取指定会话的对话轮数"""
        history = self.get_history(session_id)
        return len([m for m in history if m["role"] == "user"])
