![LangChain核心架构](./images/langchain_arch.svg)
*图：LangChain核心架构*

# 第23课：LangChain入门与核心概念

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第5章 - LangChain核心概念（第1/7课）
> - 学习目标：理解LangChain的设计哲学，掌握核心概念和基本用法
> - 预计时间：70-80分钟
> - 前置知识：第16-22课（API调用基础）

---

## 📢 课程导入

### 前言

前面7课我们学会了直接调用OpenAI API，写了很多代码：错误处理、重试、缓存、成本优化...每次都要重复写这些代码，太累了！

有没有一个框架能把这些常用功能封装好，让我们专注于业务逻辑？**有！它就是LangChain——最流行的LLM应用开发框架！**

**2025年，LangChain已经发布了1.0正式版本！** 这标志着框架已经非常成熟和稳定。LangChain不是简单的API封装，而是一套完整的开发范式！它让AI应用开发变得像搭积木一样简单！今天这课，我们正式进入LangChain 1.0的世界！

---

### 核心价值点

**第一，LangChain是LLM应用开发的事实标准。**

为什么要学LangChain？看看这些数据：
- GitHub star数：90k+
- 每月下载量：500万+
- 大厂都在用：微软、谷歌、亚马逊
- 招聘需求：几乎所有AI岗位都要求会LangChain

不会LangChain，就像前端不会React，后端不会Spring！这是AI开发的必备技能！

**第二，LangChain不是简单的API封装，而是开发范式。**

很多人以为LangChain只是封装了OpenAI API，错！LangChain提供的是：
- **组件化**：把复杂功能拆成可复用组件
- **链式调用**：组件之间灵活组合
- **抽象统一**：不同模型用统一接口
- **最佳实践**：内置了很多优化和模式

学会LangChain，你的开发效率能提升5-10倍！

**第三，LangChain的核心概念非常优雅。**

LangChain的设计理念是：
- **Components**：可复用的组件（Prompt、Model、Parser）
- **Chains**：组件的组合（Input → Process → Output）
- **Agents**：自主决策的智能体
- **Memory**：记住对话历史

这套理念清晰、优雅，一旦理解，开发AI应用就像搭乐高一样简单！

**第四，现在学LangChain是最好的时机。**

LangChain在2023年爆火，现在已经很成熟了：
- 文档完善
- 社区活跃
- 生态丰富
- 版本稳定

而且越来越多的公司在用，现在学会，找工作大大加分！

---

### 行动号召

今天这一课会教你：
- LangChain的设计哲学和架构
- 核心概念：Components、Chains、Agents
- 安装和基础配置
- 第一个LangChain程序
- 与原生API的对比

**学完这课，你就正式进入LangChain的世界了！**

---

## 📖 知识讲解

### 1. LangChain是什么

#
![Model Io](./images/model_io.svg)
*图：Model Io*

### 1.1 官方定义（LangChain 1.0）

```
LangChain 1.0 是用于构建由LLM驱动的Agents和应用的最简单方式。

核心特性：
1. 标准化模型接口：轻松连接OpenAI、Anthropic、Google等
2. 预构建Agent架构：不到10行代码即可创建Agent
3. 基于LangGraph：提供持久化、流式输出、人机交互支持
4. 与LangSmith集成：强大的调试和可视化工具
5. 生产就绪：稳定的1.0版本API

推荐场景：
- 快速构建Agents和自治应用
- 需要快速原型开发
- 基础到中等复杂度的Agent需求
```

#### 1.2 为什么需要LangChain

**没有LangChain的开发方式：**
```python
# 原生API调用
from openai import OpenAI

client = OpenAI()

# 每次都要写大量重复代码
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是Python专家"},
        {"role": "user", "content": "解释装饰器"}
    ],
    temperature=0.7
)

# 手动处理输出
result = response.choices[0].message.content

# 手动解析JSON
# 手动错误处理
# 手动缓存
# ...
```

**使用LangChain 1.0：**
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 1. 定义模型
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 2. 定义提示词模板
prompt = ChatPromptTemplate.from_template(
    "作为{role}，请{task}"
)

# 3. 组成链
chain = prompt | llm

# 4. 执行
result = chain.invoke({"role": "Python专家", "task": "解释装饰器"})
```

**对比优势：**
```
✅ 代码简洁（少70%）
✅ 可读性强（意图清晰）
✅ 可复用性高（组件化）
✅ 内置最佳实践（错误处理、重试等）
✅ 易于扩展（添加功能只需组合组件）
```

---

### 2. LangChain架构

#### 2.1 核心层次

```
┌─────────────────────────────────────┐
│         Applications                 │
│  (你的AI应用)                         │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│            Chains                    │
│  (组件的组合和编排)                    │
│  • LLMChain                         │
│  • SequentialChain                  │
│  • RouterChain                      │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│          Components                  │
│  (可复用的基础组件)                    │
├─────────────────────────────────────┤
│ • Models (LLMs, Chat Models)        │
│ • Prompts (Templates)               │
│ • Output Parsers                    │
│ • Memory (ConversationBuffer...)    │
│ • Tools (APIs, Databases...)        │
│ • Embeddings                        │
│ • Vector Stores                     │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│         Integrations                 │
│  (第三方服务集成)                      │
│  • OpenAI, Anthropic, Hugging Face  │
│  • Pinecone, Chroma, Weaviate      │
│  • MongoDB, PostgreSQL              │
└─────────────────────────────────────┘
```

---

#### 2.2 核心概念

**1. Models（模型）- LangChain 1.0统一接口**
```python
# LangChain 1.0 推荐使用标准化的导入方式
from langchain_openai import ChatOpenAI

# 创建模型实例
chat_model = ChatOpenAI(model="gpt-4")

# 统一的invoke接口
result = chat_model.invoke("Hello")

# 也支持其他提供商
from langchain_anthropic import ChatAnthropic
claude = ChatAnthropic(model="claude-sonnet-4")
```

**2. Prompts（提示词）**
```python
# 模板化提示词
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["topic"],
    template="写一首关于{topic}的诗"
)

# 填充变量
formatted = prompt.format(topic="AI")
```

**3. Output Parsers（输出解析器）**
```python
# 解析结构化输出
from langchain.output_parsers import JSONOutputParser

parser = JSONOutputParser()

# 自动解析JSON
result = parser.parse('{"name": "Alice", "age": 25}')
```

**4. Chains（链）**
```python
# 组合组件
chain = prompt | llm | parser

# 执行
result = chain.invoke({"topic": "AI"})
```

**5. Memory（记忆）**
```python
# 记住对话历史
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context({"input": "你好"}, {"output": "你好！"})
```

**6. Agents（智能体）**
```python
# 自主决策和使用工具
from langchain.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)
```

---

### 3. 安装和配置

#### 3.1 安装（LangChain 1.0）

```bash
# 基础安装（Python 3.10+）
pip install -U langchain

# 安装OpenAI集成（推荐）
pip install -U "langchain[anthropic]"
# 或者根据需要选择其他模型
pip install -U "langchain[openai]"

# 完整安装（包含所有功能）
pip install -U langchain[all]

# 推荐安装方式（使用uv更快）
uv add langchain
```

#### 3.2 环境配置

```python
# .env文件
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 或者直接设置
import os
os.environ["OPENAI_API_KEY"] = "sk-xxxxx"
```

---

### 4. 第一个LangChain程序

#### 4.1 Hello World

```python
from langchain_openai import ChatOpenAI

# 创建模型
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 调用
response = llm.invoke("你好，介绍一下自己")

print(response.content)
```

#### 4.2 使用Prompt Template

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 1. 创建模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. 创建提示词模板
prompt = ChatPromptTemplate.from_template(
    "你是一位{role}。请{task}，用{style}的风格。"
)

# 3. 创建链
chain = prompt | llm

# 4. 执行
result = chain.invoke({
    "role": "Python老师",
    "task": "解释装饰器",
    "style": "通俗易懂"
})

print(result.content)
```

#### 4.3 添加Output Parser

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

# 链式组合
chain = (
    ChatPromptTemplate.from_template("写一首关于{topic}的诗")
    | ChatOpenAI(model="gpt-3.5-turbo")
    | StrOutputParser()  # 提取content字段
)

# 执行
poem = chain.invoke({"topic": "人工智能"})
print(poem)  # 直接是字符串，不是对象
```

---

### 5. LCEL（LangChain Expression Language）

#### 5.1 什么是LCEL

```
LCEL是LangChain的核心语法，使用管道操作符 | 连接组件

优势：
✅ 代码简洁清晰
✅ 自动支持流式、批处理、异步
✅ 易于调试和监控
✅ 组件可复用

语法：
chain = component1 | component2 | component3
```

#### 5.2 LCEL示例

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

# 定义组件
prompt = ChatPromptTemplate.from_template("翻译成英文：{text}")
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

# 组合成链
chain = prompt | model | output_parser

# 执行
result = chain.invoke({"text": "你好，世界"})
print(result)  # "Hello, world"

# 流式执行
for chunk in chain.stream({"text": "你好，世界"}):
    print(chunk, end="", flush=True)

# 批处理
results = chain.batch([
    {"text": "你好"},
    {"text": "再见"},
    {"text": "谢谢"}
])
```

---

## 💻 Demo案例：LangChain基础实战

创建`langchain_basics_demo.py`：

```python
"""
LangChain基础功能演示
从Hello World到复杂链
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers import StrOutputParser, JSONOutputParser
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


def demo_1_basic_call():
    """示例1：最简单的调用"""
    print("\n" + "="*60)
    print("示例1：基础调用")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    response = llm.invoke("用一句话解释什么是LangChain")
    
    print(f"回复：{response.content}")
    print(f"类型：{type(response)}")


def demo_2_with_template():
    """示例2：使用提示词模板"""
    print("\n" + "="*60)
    print("示例2：提示词模板")
    print("="*60)
    
    # 创建模板
    prompt = ChatPromptTemplate.from_template(
        "你是一位{role}。请用{words}字以内回答：{question}"
    )
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 创建链
    chain = prompt | llm | StrOutputParser()
    
    # 执行
    result = chain.invoke({
        "role": "Python专家",
        "words": 50,
        "question": "什么是列表推导式？"
    })
    
    print(f"回复：{result}")


def demo_3_multiple_templates():
    """示例3：多消息模板"""
    print("\n" + "="*60)
    print("示例3：多消息模板")
    print("="*60)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位{role}，擅长{skill}"),
        ("human", "{question}")
    ])
    
    chain = prompt | ChatOpenAI() | StrOutputParser()
    
    result = chain.invoke({
        "role": "技术导师",
        "skill": "用简单的比喻解释复杂概念",
        "question": "什么是装饰器？"
    })
    
    print(f"回复：{result}")


def demo_4_json_output():
    """示例4：结构化输出"""
    print("\n" + "="*60)
    print("示例4：JSON输出解析")
    print("="*60)
    
    # 要求输出JSON格式
    prompt = ChatPromptTemplate.from_template(
        "请用JSON格式回答以下问题，包含name、age、hobby字段：\n"
        "介绍一个虚构的程序员角色。\n"
        "只返回JSON，不要其他文字。"
    )
    
    chain = prompt | ChatOpenAI() | JSONOutputParser()
    
    try:
        result = chain.invoke({})
        print(f"解析结果：{result}")
        print(f"类型：{type(result)}")
        print(f"姓名：{result.get('name')}")
    except Exception as e:
        print(f"解析失败：{e}")


def demo_5_streaming():
    """示例5：流式输出"""
    print("\n" + "="*60)
    print("示例5：流式输出")
    print("="*60)
    
    prompt = ChatPromptTemplate.from_template(
        "写一首关于{topic}的四行诗"
    )
    
    chain = prompt | ChatOpenAI() | StrOutputParser()
    
    print("诗歌（流式输出）：\n")
    for chunk in chain.stream({"topic": "人工智能"}):
        print(chunk, end="", flush=True)
    print("\n")


def demo_6_batch():
    """示例6：批处理"""
    print("\n" + "="*60)
    print("示例6：批量处理")
    print("="*60)
    
    prompt = ChatPromptTemplate.from_template(
        "用一句话描述{language}的特点"
    )
    
    chain = prompt | ChatOpenAI() | StrOutputParser()
    
    # 批量执行
    languages = ["Python", "JavaScript", "Go", "Rust"]
    inputs = [{"language": lang} for lang in languages]
    
    results = chain.batch(inputs)
    
    for lang, result in zip(languages, results):
        print(f"{lang}: {result}")


def demo_7_complex_chain():
    """示例7：复杂链"""
    print("\n" + "="*60)
    print("示例7：多步骤链")
    print("="*60)
    
    from langchain.schema.runnable import RunnablePassthrough
    
    # 步骤1：生成主题
    topic_chain = (
        ChatPromptTemplate.from_template("给我一个{category}相关的话题")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    # 步骤2：基于主题写内容
    content_chain = (
        ChatPromptTemplate.from_template("写一段关于{topic}的介绍（50字）")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    # 组合链
    full_chain = {
        "topic": topic_chain
    } | content_chain
    
    result = full_chain.invoke({"category": "人工智能"})
    print(f"生成内容：\n{result}")


def demo_8_langchain_vs_native():
    """示例8：LangChain vs 原生API对比"""
    print("\n" + "="*60)
    print("示例8：LangChain vs 原生API")
    print("="*60)
    
    from openai import OpenAI
    import time
    
    # 原生API
    print("【原生API方式】")
    start = time.time()
    
    native_client = OpenAI()
    response = native_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是Python专家"},
            {"role": "user", "content": "什么是装饰器？"}
        ]
    )
    native_result = response.choices[0].message.content
    native_time = time.time() - start
    
    print(f"结果：{native_result[:100]}...")
    print(f"耗时：{native_time:.2f}s")
    
    # LangChain
    print("\n【LangChain方式】")
    start = time.time()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是Python专家"),
        ("human", "什么是装饰器？")
    ])
    chain = prompt | ChatOpenAI() | StrOutputParser()
    lc_result = chain.invoke({})
    lc_time = time.time() - start
    
    print(f"结果：{lc_result[:100]}...")
    print(f"耗时：{lc_time:.2f}s")
    
    print(f"\n代码简洁度：LangChain更优")
    print(f"可读性：LangChain更优")
    print(f"可扩展性：LangChain更优")


def main():
    """主函数"""
    print("🎯 LangChain基础功能演示")
    print("="*60)
    
    demo_1_basic_call()
    demo_2_with_template()
    demo_3_multiple_templates()
    demo_4_json_output()
    demo_5_streaming()
    demo_6_batch()
    demo_7_complex_chain()
    demo_8_langchain_vs_native()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 核心要点：")
    print("1. LangChain使用组件化设计")
    print("2. LCEL（|操作符）让代码简洁清晰")
    print("3. 自动支持流式、批处理、异步")
    print("4. 提示词模板化，易于复用")
    print("5. Output Parser自动解析输出")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 LangChain vs 原生API

### 代码对比

```python
# ===== 任务：翻译+总结 =====

# 【原生API】
from openai import OpenAI
client = OpenAI()

# 步骤1：翻译
response1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"翻译成英文：{chinese_text}"}]
)
english_text = response1.choices[0].message.content

# 步骤2：总结
response2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"总结：{english_text}"}]
)
summary = response2.choices[0].message.content

# 【LangChain】
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

# 翻译链
translate_chain = (
    ChatPromptTemplate.from_template("翻译成英文：{text}")
    | llm
    | StrOutputParser()
)

# 总结链
summarize_chain = (
    ChatPromptTemplate.from_template("总结：{text}")
    | llm
    | StrOutputParser()
)

# 组合
full_chain = {"text": translate_chain} | summarize_chain
summary = full_chain.invoke({"text": chinese_text})
```

**对比：**
```
代码行数：原生25行 vs LangChain 15行
可读性：LangChain更清晰
可复用性：LangChain组件可单独使用
错误处理：LangChain内置
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解LangChain的核心概念
- [ ] 安装和配置LangChain
- [ ] 使用基础组件（Model、Prompt、Parser）
- [ ] 理解LCEL语法
- [ ] 创建简单的链
- [ ] 对比LangChain和原生API的优劣

---

## 📝 下一课预告

**第24课：Prompt Template深入 - 打造灵活的提示词系统**

下一课我们将深入学习：
- Prompt Template的高级用法
- Few-shot Template
- Chat Prompt Template
- 自定义Template
- 提示词工程最佳实践

**让提示词管理更加专业！**

---

**🎉 恭喜你完成第23课！**

你已经正式进入LangChain的世界！

**进度：23/165课（13.9%完成）** 🚀
