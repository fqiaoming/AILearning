![LangChain核心架构](./images/langchain_arch.svg)
*图：LangChain核心架构*

# LangChain 1.0 迁移指南与重要变化

> **重要提示**：本课程已全面更新为LangChain 1.0版本
> 
> LangChain 1.0于2024-2025年正式发布，带来了革命性的改进
>
> 官方文档：https://docs.langchain.com/oss/python/langchain/overview

---

## 🎯 LangChain 1.0 核心变化

### 一、Agent创建大幅简化

#### ❌ 旧版本(0.x)方式
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 需要手动创建提示词模板
prompt = ChatPromptTemplate.from_messages([...])

# 需要手动创建agent
agent = create_react_agent(llm, tools, prompt)

# 需要手动创建executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# 执行
agent_executor.invoke({"input": "query"})
```

#### ✅ LangChain 1.0 新方式
```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# 一步创建Agent，不到10行代码！
agent = create_agent(
    model="claude-sonnet-4-5-20250929",  # 支持多种模型
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# 直接invoke
result = agent.invoke({
    "messages": [{"role": "user", "content": "what is the weather in sf"}]
})
```

**核心改进：**
- ✅ 代码量减少70%
- ✅ 不需要手动创建AgentExecutor
- ✅ 不需要手动编写ReAct提示词模板
- ✅ 内置最佳实践

---

### 二、Agent基于LangGraph构建

#### LangGraph的优势

LangChain 1.0的Agents底层基于LangGraph构建，提供：

```python
# 自动获得这些高级特性：
- 持久化执行（Durable Execution）
- 流式输出（Streaming）
- 人机交互（Human-in-the-Loop）
- 状态持久化（Persistence）
- 执行历史追踪
```

#### 何时使用LangChain vs LangGraph

```
使用LangChain 1.0:
✅ 快速构建基础到中等复杂度的Agent
✅ 需要快速原型开发
✅ 标准的Agent工作流

使用LangGraph:
✅ 需要复杂的自定义工作流
✅ 需要精细控制执行流程
✅ 需要确定性和智能工作流的混合
✅ 对延迟有严格要求
```

---

### 三、标准化的模型接口

#### ❌ 旧版本(0.x)
```python
# 多种导入方式，容易混淆
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI  # 还有这种方式
```

#### ✅ LangChain 1.0
```python
# 统一的标准化导入
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# 所有模型使用相同的接口
model = ChatOpenAI(model="gpt-4")
result = model.invoke("Hello")
```

**支持的模型提供商：**
- OpenAI
- Anthropic (Claude)
- Google (Gemini)
- 以及更多...

---

### 四、安装方式更新

#### ❌ 旧版本(0.x)
```bash
pip install langchain
pip install langchain-openai
pip install langchain-community
```

#### ✅ LangChain 1.0 （Python 3.10+）
```bash
# 基础安装
pip install -U langchain

# 安装特定模型支持（推荐）
pip install -U "langchain[anthropic]"
pip install -U "langchain[openai]"

# 或使用uv（更快）
uv add langchain
```

---

### 五、Agent工具定义更简单

#### ❌ 旧版本(0.x)
```python
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel

# 需要定义复杂的工具类
class WeatherInput(BaseModel):
    city: str
    
tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description="Get weather",
    args_schema=WeatherInput
)
```

#### ✅ LangChain 1.0
```python
# 直接使用Python函数，自动推断schema
def get_weather(city: str) -> str:
    """Get weather for a given city."""  # Docstring作为描述
    return f"Weather in {city}"

# 直接传入函数列表即可
agent = create_agent(
    model="claude-sonnet-4",
    tools=[get_weather],  # 就这么简单！
    system_prompt="You are helpful"
)
```

---

## 📚 迁移步骤

### Step 1: 更新安装

```bash
# 卸载旧版本
pip uninstall langchain langchain-openai langchain-community

# 安装LangChain 1.0
pip install -U "langchain[anthropic]"
# 或根据需要选择其他模型
```

### Step 2: 更新导入语句

```python
# ❌ 旧的导入
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor

# ✅ 新的导入
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
```

### Step 3: 简化Agent创建

```python
# ❌ 旧的方式（20+行代码）
prompt = ChatPromptTemplate.from_messages([...])
llm = ChatOpenAI()
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "query"})

# ✅ 新的方式（5行代码）
agent = create_agent(
    model="gpt-4",
    tools=tools,
    system_prompt="You are helpful"
)
result = agent.invoke({"messages": [{"role": "user", "content": "query"}]})
```

### Step 4: 更新工具定义

```python
# ❌ 旧的方式
from langchain.tools import Tool
tool = Tool(
    name="calculator",
    func=calculate,
    description="Calculate math"
)

# ✅ 新的方式
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)

# 直接使用函数，自动推断参数和描述
```

---

## 🎓 学习路径

### 1. 基础概念（本章第5章）
- LangChain 1.0核心概念
- 模型接口使用
- Prompt Templates
- Output Parsers
- LCEL语法

### 2. Agent开发（第12章）
- 使用`create_agent()`快速创建Agent
- 工具函数定义
- Agent执行和调试
- 与LangSmith集成


![Model Io](./images/model_io.svg)
*图：Model Io*

### 3. 高级特性（第13章）
- Tool Calling详解
- 自定义工具开发
- 多工具Agent
- LangGraph深入（按需）

---

## 💡 最佳实践

### 1. 优先使用LangChain 1.0的简化API

```python
# ✅ 推荐：使用新的create_agent
agent = create_agent(model, tools, system_prompt)

# ❌ 不推荐：使用旧的复杂方式
# agent = create_react_agent(...)
# executor = AgentExecutor(...)
```

### 2. 利用类型提示和Docstring

```python
def search_database(query: str, limit: int = 10) -> list[dict]:
    """
    Search the database for relevant documents.
    
    Args:
        query: The search query string
        limit: Maximum number of results (default: 10)
    
    Returns:
        List of matching documents
    """
    # LangChain会自动解析这些信息！
    return results
```

### 3. 使用LangSmith调试

```python
# LangChain 1.0原生支持LangSmith
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"

# 自动追踪所有Agent执行
agent = create_agent(model, tools, system_prompt)
result = agent.invoke({...})  # 自动记录到LangSmith
```

---

## 🔗 相关资源

- [LangChain 1.0 发布说明](https://docs.langchain.com/oss/python/releases/langchain-v1)
- [迁移指南](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- [Agent文档](https://docs.langchain.com/oss/python/langchain/agents)
- [LangGraph文档](https://docs.langchain.com/oss/python/langgraph/overview)

---

## ✅ 检查清单

完成迁移后，确认以下事项：

- [ ] 已安装LangChain 1.0 (Python 3.10+)
- [ ] 更新了所有导入语句
- [ ] 使用`create_agent()`替代旧的Agent创建方式
- [ ] 工具定义使用简单的Python函数
- [ ] 测试所有Agent功能正常
- [ ] （可选）配置LangSmith追踪

---

**🎉 欢迎来到LangChain 1.0时代！**

更简单、更强大、更易用的Agent开发体验！

