![LangChain核心架构](./images/langchain_arch.svg)
*图：LangChain核心架构*

# LangChain 1.0 快速上手实战

> **配套课程**：第23课 - LangChain入门与核心概念
> 
> **目标**：通过实战快速掌握LangChain 1.0的核心用法
>
> **时长**：30分钟

---

## 🚀 环境准备

### 1. 安装LangChain 1.0

```bash
# 确保Python 3.10+
python --version

# 安装LangChain（选择你需要的模型）
pip install -U "langchain[anthropic]"
# 或
pip install -U "langchain[openai]"

# 使用uv更快（推荐）
uv add langchain
```

### 2. 配置API Key

```python
# .env文件
OPENAI_API_KEY=your-key-here
# 或
ANTHROPIC_API_KEY=your-key-here
```

---

## 📝 示例1：基础对话（最简单）

```python
from langchain_openai import ChatOpenAI

# 创建模型
model = ChatOpenAI(model="gpt-4")

# 直接调用
response = model.invoke("用一句话解释LangChain 1.0的主要优势")

print(response.content)
```

**输出示例：**
```
LangChain 1.0提供了简化的Agent创建API，基于LangGraph构建，
不到10行代码即可创建生产级Agent，并内置流式输出、持久化等高级特性。
```

---

## 📝 示例2：使用Prompt Template

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

# 创建模型
model = ChatOpenAI(model="gpt-3.5-turbo")

# 创建Prompt模板
prompt = ChatPromptTemplate.from_template(
    "你是一位{role}专家。用{words}字以内解释：{concept}"
)

# 创建链
chain = prompt | model | StrOutputParser()

# 执行
result = chain.invoke({
    "role": "Python",
    "words": "50",
    "concept": "装饰器"
})

print(result)
```

**核心要点：**
- 使用 `|` 操作符组合组件（LCEL语法）
- `StrOutputParser()` 自动提取字符串内容
- 清晰的数据流：输入 → Prompt → Model → Parser → 输出

---

## 📝 示例3：创建简单Agent（重点！）

```python
from langchain.agents import create_agent

# 定义工具函数
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    
    Args:
        city: The name of the city
    
    Returns:
        Weather information as a string
    """
    # 实际应用中这里调用天气API
    return f"北京今天晴，20-28℃"

def calculate(expression: str) -> float:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: Math expression like "2+3*4"
    
    Returns:
        The calculation result
    """
    return eval(expression)

# 创建Agent（只需5行代码！）
agent = create_agent(
    model="gpt-4",
    tools=[get_weather, calculate],
    system_prompt="You are a helpful assistant"
)

# 使用Agent
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "北京今天天气怎么样？"}
    ]
})

print(result)
```

**核心改进（对比旧版本）：**
- ❌ 旧版本需要20+行代码创建Agent
- ✅ 新版本只需5行代码
- ❌ 旧版本需要手动定义Tool类
- ✅ 新版本直接使用Python函数
- ❌ 旧版本需要手动创建AgentExecutor
- ✅ 新版本自动处理

---

## 📝 示例4：流式输出

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("写一首关于{topic}的诗")

chain = prompt | model

# 流式输出（逐字显示）
for chunk in chain.stream({"topic": "人工智能"}):
    print(chunk.content, end="", flush=True)
```

---

## 📝 示例5：批量处理

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("翻译成英文：{text}")
chain = prompt | model | StrOutputParser()

# 批量翻译
texts = ["你好", "再见", "谢谢"]
inputs = [{"text": t} for t in texts]

results = chain.batch(inputs)

for text, result in zip(texts, results):
    print(f"{text} → {result}")
```

**输出：**
```
你好 → Hello
再见 → Goodbye
谢谢 → Thank you
```

---

## 📝 示例6：多步骤Chain

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

model = ChatOpenAI()

# 步骤1：生成创意
creative_chain = (
    ChatPromptTemplate.from_template("为{category}产品想3个名字")
    | model
    | StrOutputParser()
)

# 步骤2：评估创意
evaluate_chain = (
    ChatPromptTemplate.from_template("评估这些名字：{names}\n选出最好的一个并说明理由")
    | model
    | StrOutputParser()
)

# 组合Chain
full_chain = {"names": creative_chain} | evaluate_chain

# 执行
result = full_chain.invoke({"category": "AI助手"})
print(result)
```

**工作流程：**
```
输入: {"category": "AI助手"}
    ↓
creative_chain: 生成3个名字
    ↓
evaluate_chain: 评估并选择最佳
    ↓
输出: 最佳名字及理由
```

---

## 📝 示例7：完整的Agent应用

```python
"""
完整的个人助手Agent
支持天气查询、计算、搜索
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from datetime import datetime

# 定义工具集
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 实际应用中调用天气API
    return f"{city}今天晴，温度20-28℃"

def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"

def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_info(query: str) -> str:
    """搜索信息（模拟）"""
    # 实际应用中调用搜索API
    return f"关于'{query}'的搜索结果：[模拟数据]"

# 创建Agent
agent = create_agent(
    model="gpt-4",
    tools=[get_weather, calculate, get_current_time, search_info],
    system_prompt="""你是一个智能助手，可以：
    1. 查询天气
    2. 进行数学计算
    3. 获取当前时间
    4. 搜索信息
    
    请根据用户需求选择合适的工具。"""
)

# 测试场景
test_queries = [
    "北京今天天气怎么样？",
    "帮我算一下 123 * 456",
    "现在几点了？",
    "搜索Python装饰器的用法"
]

print("="*60)
print("智能助手Agent演示")
print("="*60)

for query in test_queries:
    print(f"\n用户: {query}")
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    print(f"助手: {result['messages'][-1]['content']}")
    print("-"*60)
```

---

## 📝 示例8：调试和监控（LangSmith）

```python
import os
from langchain.agents import create_agent

# 启用LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"

def get_weather(city: str) -> str:
    """获取天气"""
    return f"{city}天气：晴"

agent = create_agent(
    model="gpt-4",
    tools=[get_weather],
    system_prompt="You are helpful"
)

# 所有执行会自动记录到LangSmith
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气"}]
})

print("✅ 执行已记录到LangSmith，可以在线查看详细trace")
```

---


![Model Io](./images/model_io.svg)
*图：Model Io*

## 🎯 核心要点总结

### 1. LangChain 1.0的核心优势

```
✅ 不到10行代码创建Agent
✅ 直接使用Python函数作为工具
✅ 自动推断工具schema
✅ 基于LangGraph，支持高级特性
✅ 统一的模型接口
✅ 内置LangSmith集成
```

### 2. 从旧版本迁移的关键变化

```python
# ❌ 旧版本 (0.x)
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
# ... 20+行代码 ...

# ✅ 新版本 (1.0)
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
agent = create_agent(model, tools, system_prompt)  # 5行搞定
```

### 3. 最佳实践

```python
# 1. 使用类型提示
def my_tool(param: str) -> str:  # 清晰的类型
    """详细的docstring"""  # Agent会读取这个
    return result

# 2. 使用LCEL组合组件
chain = prompt | model | parser  # 清晰的数据流

# 3. 启用LangSmith调试
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# 4. 合理选择模型
gpt-3.5-turbo  # 快速、便宜
gpt-4         # 复杂任务
claude-sonnet # 平衡性能和成本
```

---

## 💡 下一步学习

1. **第24-27课**：深入学习Prompt、Parser、Chain
2. **第12章**：深入Agent开发
3. **第13章**：高级工具开发
4. **LangGraph**：复杂工作流（按需）

---

## 🔗 参考资源

- [LangChain 1.0 官方文档](https://docs.langchain.com/oss/python/langchain/overview)
- [Agent文档](https://docs.langchain.com/oss/python/langchain/agents)
- [LangSmith](https://docs.langchain.com/langsmith)

---

**🎉 恭喜！你已经掌握了LangChain 1.0的核心用法！**

继续下一课深入学习吧！

