# 🤖 智能对话助手 - LangChain实战项目

第5章第28课的完整实战项目，使用LangChain框架构建智能对话助手。

## 项目结构

```
intelligent_assistant/
├── src/
│   ├── __init__.py              # 包初始化
│   ├── assistant.py             # 主逻辑（意图路由、Chain编排）
│   ├── intent_classifier.py     # 意图识别（Pydantic + LCEL）
│   ├── conversation_manager.py  # 对话管理（多会话、历史裁剪）
│   ├── tools.py                 # 工具集（时间、天气、计算器）
│   └── config.py                # 配置管理
├── prompts/
│   ├── system_prompt.txt        # 系统提示词
│   ├── intent_prompt.txt        # 意图识别提示词
│   └── tool_prompts/            # 工具相关提示词
│       ├── weather_prompt.txt
│       ├── calculator_prompt.txt
│       └── time_prompt.txt
├── tests/
│   └── test_assistant.py        # 测试套件
├── .env                         # 环境变量
├── requirements.txt             # 依赖
└── README.md                    # 本文件
```

## 核心功能

1. **多轮对话**：基于ConversationManager管理对话历史，支持上下文理解
2. **意图识别**：使用LangChain LCEL + Pydantic OutputParser，识别4类意图
3. **工具调用**：时间查询、天气查询、计算器、知识搜索
4. **智能路由**：根据意图自动路由到不同的Chain处理
5. **Fallback降级**：主模型失败时自动切换备用模型

## 涉及的LangChain知识点

- ChatPromptTemplate（提示词模板）
- PydanticOutputParser（结构化输出解析）
- LCEL链式调用（Prompt | LLM | Parser）
- with_fallbacks（降级策略）
- StrOutputParser（字符串输出解析）

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动LM Studio并加载模型

# 3. 交互式测试
python -m src.assistant

# 4. 运行测试
python tests/test_assistant.py
```

## 示例对话

```
你：你好
助手：你好！我是你的智能助手，有什么可以帮你的吗？
[意图：chat，置信度：0.95]

你：现在几点了？
助手：现在是2024年1月1日 14:30:25，周一。
[意图：tool_call，置信度：0.90，工具：get_current_time]

你：北京天气怎么样？
助手：北京今天晴天，气温15°C，北风3级，适合外出~
[意图：tool_call，置信度：0.92，工具：get_weather]

你：帮我算一下 123 + 456
助手：123 + 456 = 579
[意图：tool_call，置信度：0.88，工具：calculator]
```

## 简历亮点

```
• 独立开发智能对话助手，支持多轮对话和上下文管理
• 使用LangChain LCEL框架，实现意图识别和智能路由
• 集成工具调用（天气、时间、计算器），支持自然语言交互
• 实现Fallback降级策略和完整的错误处理机制
```
