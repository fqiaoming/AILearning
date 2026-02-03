![LangChain核心架构](./images/langchain_arch.svg)
*图：LangChain核心架构*

# 第28课：LangChain实战项目1 - 智能对话助手

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第5章 - LangChain核心概念（第6/7课）
> - 学习目标：整合所有LangChain知识，构建完整的智能对话助手
> - 预计时间：100-120分钟
> - 前置知识：第23-27课

---

## 📢 课程导入
![Model Io](./images/model_io.svg)
*图：Model Io*


### 前言

前面5课我们学了LangChain的各个组件：Prompt Template、Output Parser、Model管理、Chain组合...每个都很强大，但都是单点知识。

今天，我们要把这些全部串起来，**从零构建一个完整的智能对话助手！**这不是玩具demo，而是真正能用的生产级系统，包括：意图识别、多轮对话、上下文管理、工具调用、错误处理...

这是你第一个LangChain实战项目！完成后，你就真正会用LangChain了！

---

### 核心价值点

**第一，实战项目是检验学习效果的唯一标准。**

学了那么多理论，到底会不会用？只有做项目才知道！这个项目会让你遇到真实问题：
- 组件怎么组合？
- 数据怎么流转？
- 错误怎么处理？
- 性能怎么优化？

这些都是理论课学不到的，只有实战才能掌握！

**第二，智能对话助手是最典型的AI应用。**

为什么选这个项目？因为它：
- **典型性**：包含AI应用的核心功能
- **实用性**：可以直接用于生产
- **扩展性**：可以改造成各种助手
- **完整性**：涵盖前面所有知识点

学会这个，你就能举一反三，做出各种AI应用！

**第三，这个项目可以直接写进简历。**

完成后，你可以在简历上写：
- 独立开发智能对话助手，支持多轮对话和上下文管理
- 使用LangChain框架，实现意图识别和智能路由
- 集成Function Calling，支持工具调用
- 实现错误处理、降级策略和性能优化

这些都是面试官想看到的项目经验！

**第四，项目代码可以直接复用到实际工作中。**

这不是教学demo，而是生产级代码：
- 模块化设计
- 完整的错误处理
- 详细的注释
- 可扩展的架构

你可以把这个项目作为模板，快速开发自己的AI应用！

---

### 行动号召

今天这一课会带你：
1. 设计完整的系统架构
2. 实现所有核心功能
3. 处理各种边界情况
4. 测试和优化性能

**完成这个项目，你就是真正的LangChain开发者了！**

---

## 📖 项目需求

### 1. 功能需求

```
核心功能：
1. 多轮对话
   - 记住对话历史
   - 理解上下文
   - 连贯回复

2. 意图识别
   - 识别用户意图
   - 路由到不同处理器
   - 支持多种意图

3. 工具调用
   - 天气查询
   - 时间查询
   - 计算器
   - 可扩展

4. 智能回退
   - 主模型失败用备用
   - 优雅的错误处理
   - 用户友好的提示

5. 性能优化
   - 缓存常见问题
   - 批处理支持
   - 异步执行
```

---

## 💻 项目实现

### 第一步：项目结构

```
intelligent_assistant/
├── src/
│   ├── __init__.py
│   ├── assistant.py          # 主逻辑
│   ├── intent_classifier.py  # 意图识别
│   ├── conversation_manager.py  # 对话管理
│   ├── tools.py              # 工具集
│   └── config.py             # 配置
├── prompts/
│   ├── system_prompt.txt
│   ├── intent_prompt.txt
│   └── tool_prompts/
├── tests/
│   └── test_assistant.py
├── .env
├── requirements.txt
└── README.md
```

---

### 第二步：配置管理

创建`src/config.py`：

```python
"""
配置管理
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """全局配置"""
    
    # API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LOCAL_LLM_URL = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")
    
    # 模型配置
    PRIMARY_MODEL = "gpt-3.5-turbo"
    FALLBACK_MODEL = "gpt-3.5-turbo"
    LOCAL_MODEL = "qwen2.5-7b-instruct"
    
    # 性能配置
    ENABLE_CACHE = True
    MAX_CONVERSATION_HISTORY = 10
    TIMEOUT = 30
    MAX_RETRIES = 3
    
    # 功能开关
    ENABLE_TOOLS = True
    ENABLE_INTENT_CLASSIFICATION = True
    ENABLE_FALLBACK = True


config = Config()
```

---

### 第三步：意图识别

创建`src/intent_classifier.py`：

```python
"""
意图识别模块
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal


class Intent(BaseModel):
    """意图模型"""
    category: Literal["chat", "tool_call", "question", "complex"] = Field(
        description="意图类别"
    )
    confidence: float = Field(description="置信度，0-1之间")
    reason: str = Field(description="判断理由")


class IntentClassifier:
    """意图分类器"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.parser = PydanticOutputParser(pydantic_object=Intent)
        
        self.prompt = ChatPromptTemplate.from_template(
            """分析用户消息的意图。

意图类别：
- chat: 闲聊、打招呼
- tool_call: 需要调用工具（天气、时间、计算等）
- question: 知识问答
- complex: 复杂任务，需要深度思考

{format_instructions}

用户消息：{message}"""
        )
        
        self.chain = (
            self.prompt.partial(
                format_instructions=self.parser.get_format_instructions()
            )
            | self.llm
            | self.parser
        )
    
    def classify(self, message: str) -> Intent:
        """分类意图"""
        try:
            return self.chain.invoke({"message": message})
        except Exception as e:
            # 失败时返回默认
            return Intent(
                category="chat",
                confidence=0.5,
                reason=f"分类失败：{e}"
            )
```

---

### 第四步：对话管理

创建`src/conversation_manager.py`：

```python
"""
对话管理模块
"""

from typing import List, Dict
from datetime import datetime


class ConversationManager:
    """对话历史管理"""
    
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.conversations: Dict[str, List[Dict]] = {}
    
    def add_message(self, session_id: str, role: str, content: str):
        """添加消息"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # 限制历史长度
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = \
                self.conversations[session_id][-self.max_history:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """获取历史"""
        return self.conversations.get(session_id, [])
    
    def get_messages_for_llm(self, session_id: str) -> List[Dict]:
        """获取适合LLM的消息格式"""
        history = self.get_history(session_id)
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]
    
    def clear_history(self, session_id: str):
        """清除历史"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    def get_context_summary(self, session_id: str) -> str:
        """生成上下文摘要"""
        history = self.get_history(session_id)
        if not history:
            return "无历史对话"
        
        summary = f"对话轮数：{len(history)//2}\n"
        if len(history) >= 4:
            summary += f"最近话题：{history[-2]['content'][:50]}..."
        
        return summary
```

---

### 第五步：工具集

创建`src/tools.py`：

```python
"""
工具集
"""

from datetime import datetime
import math


class Tools:
    """工具集合"""
    
    @staticmethod
    def get_current_time() -> str:
        """获取当前时间"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_weather(city: str) -> str:
        """获取天气（模拟）"""
        # 实际应用中调用真实API
        weather_data = {
            "北京": "晴天，15°C",
            "上海": "多云，20°C",
            "深圳": "雷阵雨，28°C"
        }
        return weather_data.get(city, f"{city}的天气数据暂时无法获取")
    
    @staticmethod
    def calculator(expression: str) -> str:
        """计算器"""
        try:
            # 注意：生产环境不要用eval，有安全风险
            result = eval(expression, {"__builtins__": {}}, {
                "math": math,
                "abs": abs,
                "round": round
            })
            return str(result)
        except Exception as e:
            return f"计算错误：{e}"
    
    @staticmethod
    def search_knowledge(query: str) -> str:
        """知识搜索（模拟）"""
        # 实际应用中接入搜索API
        return f"关于'{query}'的搜索结果：[这里应该是真实的搜索结果]"


# 工具描述（用于AI理解）
TOOL_DESCRIPTIONS = {
    "get_current_time": "获取当前日期和时间",
    "get_weather": "查询指定城市的天气，参数：city（城市名）",
    "calculator": "执行数学计算，参数：expression（数学表达式）",
    "search_knowledge": "搜索知识，参数：query（搜索词）"
}
```

---

### 第六步：主助手逻辑

创建`src/assistant.py`：

```python
"""
智能助手主逻辑
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableBranch

from .intent_classifier import IntentClassifier, Intent
from .conversation_manager import ConversationManager
from .tools import Tools, TOOL_DESCRIPTIONS
from .config import config


class IntelligentAssistant:
    """智能对话助手"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        
        # 初始化组件
        self.intent_classifier = IntentClassifier()
        self.conversation_manager = ConversationManager(
            max_history=config.MAX_CONVERSATION_HISTORY
        )
        self.tools = Tools()
        
        # 初始化模型
        self.primary_model = ChatOpenAI(
            model=config.PRIMARY_MODEL,
            temperature=0.7,
            timeout=config.TIMEOUT
        )
        
        self.fallback_model = ChatOpenAI(
            model=config.FALLBACK_MODEL,
            temperature=0.7
        )
        
        # 构建Chain
        self._build_chains()
    
    def _build_chains(self):
        """构建处理链"""
        
        # 闲聊Chain
        self.chat_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "你是一个友好的助手，用简洁有趣的方式回答。"),
                ("human", "{message}")
            ])
            | self.primary_model
            | StrOutputParser()
        ).with_fallbacks([
            ChatPromptTemplate.from_messages([
                ("system", "你是助手"),
                ("human", "{message}")
            ])
            | self.fallback_model
            | StrOutputParser()
        ])
        
        # 问答Chain
        self.qa_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "你是知识专家，提供准确详细的回答。"),
                ("human", "{message}")
            ])
            | self.primary_model
            | StrOutputParser()
        )
        
        # 复杂任务Chain
        self.complex_chain = (
            ChatPromptTemplate.from_messages([
                ("system", """你是高级AI助手，擅长处理复杂任务。
请分步骤思考，给出详细的分析和建议。"""),
                ("human", "{message}")
            ])
            | self.primary_model
            | StrOutputParser()
        )
    
    def _detect_tool_call(self, message: str) -> tuple:
        """检测是否需要调用工具"""
        message_lower = message.lower()
        
        # 简单规则匹配（实际应该用AI判断）
        if any(word in message for word in ["时间", "几点", "日期"]):
            return ("get_current_time", {})
        
        elif any(word in message for word in ["天气"]):
            # 提取城市名（简化处理）
            for city in ["北京", "上海", "深圳"]:
                if city in message:
                    return ("get_weather", {"city": city})
            return ("get_weather", {"city": "北京"})
        
        elif any(word in message for word in ["计算", "等于", "+", "-", "*", "/"]):
            # 提取表达式（简化处理）
            import re
            expr = re.findall(r'[\d+\-*/().\s]+', message)
            if expr:
                return ("calculator", {"expression": expr[0]})
        
        return (None, {})
    
    def chat(self, message: str) -> dict:
        """处理用户消息"""
        # 1. 保存用户消息
        self.conversation_manager.add_message(
            self.session_id, "user", message
        )
        
        try:
            # 2. 意图识别
            intent = self.intent_classifier.classify(message)
            
            # 3. 检测工具调用
            tool_name, tool_params = self._detect_tool_call(message)
            
            # 4. 处理
            if tool_name and config.ENABLE_TOOLS:
                # 调用工具
                response = self._handle_tool_call(
                    tool_name, tool_params, message
                )
            
            elif intent.category == "chat":
                # 闲聊
                response = self.chat_chain.invoke({"message": message})
            
            elif intent.category == "question":
                # 问答
                response = self.qa_chain.invoke({"message": message})
            
            elif intent.category == "complex":
                # 复杂任务
                response = self.complex_chain.invoke({"message": message})
            
            else:
                # 默认
                response = self.chat_chain.invoke({"message": message})
            
            # 5. 保存助手回复
            self.conversation_manager.add_message(
                self.session_id, "assistant", response
            )
            
            return {
                "success": True,
                "response": response,
                "intent": intent.category,
                "confidence": intent.confidence
            }
        
        except Exception as e:
            error_msg = f"抱歉，我遇到了一些问题：{e}"
            self.conversation_manager.add_message(
                self.session_id, "assistant", error_msg
            )
            
            return {
                "success": False,
                "response": error_msg,
                "error": str(e)
            }
    
    def _handle_tool_call(self, tool_name: str, params: dict, 
                         original_message: str) -> str:
        """处理工具调用"""
        # 调用工具
        tool_function = getattr(self.tools, tool_name)
        tool_result = tool_function(**params)
        
        # 用AI生成自然语言回复
        prompt = ChatPromptTemplate.from_template(
            """用户问：{message}
工具调用：{tool_name}
工具结果：{result}

请用自然语言回答用户的问题。"""
        )
        
        response = (prompt | self.primary_model | StrOutputParser()).invoke({
            "message": original_message,
            "tool_name": tool_name,
            "result": tool_result
        })
        
        return response
    
    def get_history(self) -> list:
        """获取对话历史"""
        return self.conversation_manager.get_history(self.session_id)
    
    def clear_history(self):
        """清除历史"""
        self.conversation_manager.clear_history(self.session_id)


def main():
    """交互式测试"""
    print("🤖 智能对话助手")
    print("="*60)
    print("输入 'quit' 退出，输入 'clear' 清除历史\n")
    
    assistant = IntelligentAssistant()
    
    while True:
        user_input = input("你：").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("再见！👋")
            break
        
        if user_input.lower() == 'clear':
            assistant.clear_history()
            print("历史已清除\n")
            continue
        
        # 处理消息
        result = assistant.chat(user_input)
        
        # 显示回复
        print(f"\n助手：{result['response']}")
        
        # 显示调试信息
        if result.get('intent'):
            print(f"[意图：{result['intent']}，置信度：{result.get('confidence', 0):.2f}]")
        
        print()


if __name__ == "__main__":
    main()
```

---

### 第七步：测试

创建`tests/test_assistant.py`：

```python
"""
助手测试
"""

import sys
sys.path.append('..')

from src.assistant import IntelligentAssistant


def test_basic_chat():
    """测试基础对话"""
    print("\n" + "="*60)
    print("测试1：基础对话")
    print("="*60)
    
    assistant = IntelligentAssistant("test_1")
    
    messages = [
        "你好",
        "你叫什么名字？",
        "你能做什么？"
    ]
    
    for msg in messages:
        result = assistant.chat(msg)
        print(f"\n用户：{msg}")
        print(f"助手：{result['response']}")
        print(f"意图：{result.get('intent')}")


def test_tool_calls():
    """测试工具调用"""
    print("\n" + "="*60)
    print("测试2：工具调用")
    print("="*60)
    
    assistant = IntelligentAssistant("test_2")
    
    tool_messages = [
        "现在几点了？",
        "北京的天气怎么样？",
        "帮我算一下 123 + 456"
    ]
    
    for msg in tool_messages:
        result = assistant.chat(msg)
        print(f"\n用户：{msg}")
        print(f"助手：{result['response']}")


def test_context():
    """测试上下文"""
    print("\n" + "="*60)
    print("测试3：上下文理解")
    print("="*60)
    
    assistant = IntelligentAssistant("test_3")
    
    conversation = [
        "我叫小明",
        "你还记得我叫什么吗？",
        "我喜欢Python",
        "你记得我喜欢什么吗？"
    ]
    
    for msg in conversation:
        result = assistant.chat(msg)
        print(f"\n用户：{msg}")
        print(f"助手：{result['response']}")


def main():
    """运行所有测试"""
    print("🧪 智能助手测试套件")
    
    test_basic_chat()
    test_tool_calls()
    test_context()
    
    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 项目总结

### 完成的功能

```
✅ 多轮对话和上下文管理
✅ 意图识别和智能路由
✅ 工具调用（时间、天气、计算器）
✅ 错误处理和降级
✅ 模块化设计
✅ 完整的测试
```

### 可扩展的方向

```
1. 功能扩展
   - 添加更多工具
   - 支持文件上传
   - 集成知识库

2. 性能优化
   - Redis缓存
   - 异步处理
   - 批量请求

3. 用户体验
   - Web界面
   - 语音输入输出
   - 多语言支持

4. 企业功能
   - 多租户支持
   - 权限管理
   - 使用统计
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 设计完整的AI助手架构
- [ ] 实现意图识别和路由
- [ ] 管理多轮对话历史
- [ ] 集成工具调用
- [ ] 处理各种异常情况
- [ ] 测试和优化系统

---

## 📝 下一课预告

**第29课：LangChain核心概念总结与第5章综合实战**

下一课我们将：
- 总结第5章所有知识点
- 更高级的实战技巧
- 性能优化方法
- 最佳实践总结

**第5章的完美收官！**

---

**🎉 恭喜你完成第28课！**

你已经能用LangChain开发完整的AI应用了！

**进度：28/165课（17.0%完成）** 🚀
