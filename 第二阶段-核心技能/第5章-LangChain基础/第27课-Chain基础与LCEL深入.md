![Chain链式调用流程](./images/chain_flow.svg)
*图：Chain链式调用流程*

# 第27课：Chain基础与LCEL深入 - 组合的艺术

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第5章 - LangChain核心概念（第5/7课）
> - 学习目标：深入掌握Chain和LCEL，构建复杂的AI工作流
> - 预计时间：80-90分钟
> - 前置知识：第23-26课

---

## 📢 课程导入

### 前言

前面几课我们学了组件：Prompt、Model、Parser，每个都很强大。但真实AI应用需要把它们组合起来：**先分析用户意图 → 根据意图选择不同策略 → 调用模型 → 解析输出 → 后处理结果**

这种多步骤的流程怎么优雅地实现？一个个手动调用？太原始了！**LangChain的Chain就是解决这个问题的！**

Chain让你能像搭积木一样组合组件，用管道操作符`|`串联起来，代码清晰、可维护、易扩展！今天这课，我要教你Chain的全部精髓！

---

### 核心价值点

**第一，Chain是LangChain的核心，也是灵魂。**

为什么这么说？因为：
- Prompt、Model、Parser是**组件**（零件）
- Chain是**组合**（成品）
- 组件再强大，不组合起来也没用

Chain就是把零散的组件串成完整的AI工作流！没有Chain，LangChain只是一堆工具函数；有了Chain，才是完整的框架！

**第二，LCEL不是简单的语法糖，而是设计哲学。**

LCEL（LangChain Expression Language）是LangChain 0.2的核心创新：
- **声明式编程**：说"做什么"而不是"怎么做"
- **自动优化**：流式、批处理、异步自动支持
- **可组合性**：小Chain组成大Chain
- **调试友好**：清晰的执行流程

LCEL让AI工作流的开发效率提升10倍！

**第三，掌握Chain是从初级到中级的关键跨越。**

看看不同水平的代码：

**初级（手动调用）：**
```python
prompt = template.format(question=q)
response = llm.invoke(prompt)
result = parser.parse(response)
```

**中级（使用Chain）：**
```python
chain = prompt | llm | parser
result = chain.invoke({"question": q})
```

**高级（复杂Chain组合）：**
```python
chain = (
    {"query": RunnablePassthrough()}
    | intent_classifier
    | RunnableBranch(...)
    | fallback_chain
)
```

学会Chain，你就是中级开发者了！

**第四，Chain是构建复杂AI应用的唯一方式。**

真实项目中，AI工作流可能有：
- 10+个步骤
- 条件分支
- 并行执行
- 错误重试
- 结果缓存

没有Chain，代码会乱成一团！有了Chain，一切井然有序！

---

### 行动号召

今天这一课会教你：
- Chain的基本类型和用法
- LCEL的高级特性
- 条件Chain和并行Chain
- Chain的调试和监控
- 实战：构建复杂工作流

**学完这课，你就能构建任意复杂的AI工作流了！**

---

## 📖 知识讲解

### 1. Chain基础

#
![Model Io](./images/model_io.svg)
*图：Model Io*

### 1.1 最简单的Chain

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

# 三个组件
prompt = ChatPromptTemplate.from_template("解释{topic}")
model = ChatOpenAI()
parser = StrOutputParser()

# 组成Chain（使用|操作符）
chain = prompt | model | parser

# 执行
result = chain.invoke({"topic": "量子计算"})
print(result)
```

**执行流程：**
```
{"topic": "量子计算"} 
→ prompt 生成消息
→ model 调用AI
→ parser 提取文本
→ 返回字符串
```

#### 1.2 Chain的自动特性

```python
# 流式输出（自动支持）
for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)

# 批处理（自动支持）
results = chain.batch([
    {"topic": "Python"},
    {"topic": "JavaScript"},
    {"topic": "Go"}
])

# 异步（自动支持）
import asyncio
result = await chain.ainvoke({"topic": "ML"})
```

---

### 2. LCEL核心概念

#### 2.1 Runnable接口

```
所有可以用于Chain的组件都实现了Runnable接口：

核心方法：
- invoke(input)：同步执行
- ainvoke(input)：异步执行
- stream(input)：流式输出
- astream(input)：异步流式
- batch(inputs)：批处理
- abatch(inputs)：异步批处理

这就是为什么所有组件都能无缝组合！
```

#### 2.2 RunnablePassthrough（透传）

```python
from langchain.schema.runnable import RunnablePassthrough

# 场景：需要在Chain中保留原始输入
chain = {
    "original": RunnablePassthrough(),  # 透传输入
    "processed": prompt | model
}

result = chain.invoke("你好")
# {
#   "original": "你好",
#   "processed": AIMessage(...)
# }
```

#### 2.3 RunnableLambda（自定义函数）

```python
from langchain.schema.runnable import RunnableLambda

# 将普通函数变成Runnable
def uppercase(text: str) -> str:
    return text.upper()

uppercase_runnable = RunnableLambda(uppercase)

# 用于Chain
chain = (
    ChatPromptTemplate.from_template("说一个词")
    | ChatOpenAI()
    | StrOutputParser()
    | uppercase_runnable  # 自定义处理
)

result = chain.invoke({})
# "HELLO" (转大写)
```

---

### 3. 复杂Chain模式

#### 3.1 顺序Chain（Sequential）

```python
# Chain 1：翻译
translate_chain = (
    ChatPromptTemplate.from_template("翻译成英文：{text}")
    | ChatOpenAI()
    | StrOutputParser()
)

# Chain 2：总结
summarize_chain = (
    ChatPromptTemplate.from_template("用10字总结：{text}")
    | ChatOpenAI()
    | StrOutputParser()
)

# 组合：先翻译，再总结
full_chain = {"text": translate_chain} | summarize_chain

result = full_chain.invoke({"text": "人工智能正在改变世界"})
# "AI transforms world"
```

#### 3.2 并行Chain

```python
from langchain.schema.runnable import RunnableParallel

# 定义多个并行任务
parallel_chain = RunnableParallel(
    translation=(
        ChatPromptTemplate.from_template("翻译：{text}")
        | ChatOpenAI()
        | StrOutputParser()
    ),
    summary=(
        ChatPromptTemplate.from_template("总结：{text}")
        | ChatOpenAI()
        | StrOutputParser()
    ),
    sentiment=(
        ChatPromptTemplate.from_template("情感：{text}")
        | ChatOpenAI()
        | StrOutputParser()
    )
)

# 并行执行
result = parallel_chain.invoke({"text": "今天天气真好"})
# {
#   "translation": "The weather is nice today",
#   "summary": "天气好",
#   "sentiment": "正面"
# }
```

#### 3.3 条件Chain（分支）

```python
from langchain.schema.runnable import RunnableBranch

# 意图分类器
def classify_intent(inputs):
    text = inputs["text"]
    if "翻译" in text:
        return "translate"
    elif "总结" in text:
        return "summarize"
    else:
        return "chat"

# 不同意图的Chain
translate_chain = (
    ChatPromptTemplate.from_template("翻译：{text}")
    | ChatOpenAI()
    | StrOutputParser()
)

summarize_chain = (
    ChatPromptTemplate.from_template("总结：{text}")
    | ChatOpenAI()
    | StrOutputParser()
)

chat_chain = (
    ChatPromptTemplate.from_template("回答：{text}")
    | ChatOpenAI()
    | StrOutputParser()
)

# 条件路由
conditional_chain = RunnableBranch(
    (lambda x: classify_intent(x) == "translate", translate_chain),
    (lambda x: classify_intent(x) == "summarize", summarize_chain),
    chat_chain  # 默认
)

# 根据输入自动选择Chain
result1 = conditional_chain.invoke({"text": "请翻译：你好"})
result2 = conditional_chain.invoke({"text": "请总结这篇文章"})
```

---

### 4. Chain的高级特性

#### 4.1 Fallback（备用Chain）

```python
# 主Chain
primary_chain = (
    ChatPromptTemplate.from_template("详细解释{topic}")
    | ChatOpenAI(model="gpt-4-turbo", timeout=3)
    | StrOutputParser()
)

# 备用Chain
fallback_chain = (
    ChatPromptTemplate.from_template("简单解释{topic}")
    | ChatOpenAI(model="gpt-3.5-turbo")
    | StrOutputParser()
)

# 主Chain失败时使用备用
chain_with_fallback = primary_chain.with_fallbacks([fallback_chain])

# 使用（如果GPT-4超时，自动切换到GPT-3.5）
result = chain_with_fallback.invoke({"topic": "量子纠缠"})
```

#### 4.2 Retry（重试）

```python
from langchain.schema.runnable import RunnableRetry

# 带重试的Chain
chain_with_retry = (
    ChatPromptTemplate.from_template("回答{question}")
    | ChatOpenAI()
    | StrOutputParser()
).with_retry(max_attempts=3, wait_exponential_jitter=True)

# 失败会自动重试最多3次
result = chain_with_retry.invoke({"question": "什么是AI？"})
```

#### 4.3 Timeout（超时）

```python
# 设置超时
chain_with_timeout = (
    ChatPromptTemplate.from_template("详细分析{topic}")
    | ChatOpenAI()
    | StrOutputParser()
).with_config(timeout=10)  # 10秒超时

try:
    result = chain_with_timeout.invoke({"topic": "宇宙起源"})
except TimeoutError:
    print("执行超时")
```

---

### 5. Chain的调试

#### 5.1 verbose模式

```python
# 打印详细日志
chain = (
    ChatPromptTemplate.from_template("解释{topic}")
    | ChatOpenAI()
    | StrOutputParser()
)

# 启用详细日志
result = chain.invoke({"topic": "AI"}, config={"verbose": True})
```

#### 5.2 自定义Callback

```python
from langchain.callbacks.base import BaseCallbackHandler

class MyCallback(BaseCallbackHandler):
    """自定义回调"""
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"[Chain开始] 输入: {inputs}")
    
    def on_chain_end(self, outputs, **kwargs):
        print(f"[Chain结束] 输出: {outputs}")
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"[LLM调用] Prompts: {prompts}")
    
    def on_llm_end(self, response, **kwargs):
        print(f"[LLM完成] Response: {response}")

# 使用callback
chain = prompt | model | parser
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [MyCallback()]}
)
```

---

## 💻 Demo案例：Chain实战

创建`chain_advanced_demo.py`：

```python
"""
Chain高级用法完整演示
从基础到复杂工作流
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser
from langchain.schema.runnable import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
    RunnableBranch
)


def demo_1_basic_chain():
    """示例1：基础Chain"""
    print("\n" + "="*60)
    print("示例1：基础Chain组合")
    print("="*60)
    
    chain = (
        ChatPromptTemplate.from_template("用一句话解释{concept}")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    result = chain.invoke({"concept": "区块链"})
    print(f"结果：{result}")


def demo_2_multi_step():
    """示例2：多步骤Chain"""
    print("\n" + "="*60)
    print("示例2：多步骤处理")
    print("="*60)
    
    # 步骤1：生成
    generate_chain = (
        ChatPromptTemplate.from_template("给{category}起3个名字")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    # 步骤2：评价
    evaluate_chain = (
        ChatPromptTemplate.from_template(
            "评价这些名字：{names}\n给出最好的一个"
        )
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    # 组合
    full_chain = {"names": generate_chain} | evaluate_chain
    
    result = full_chain.invoke({"category": "AI产品"})
    print(f"最佳名字：{result}")


def demo_3_parallel():
    """示例3：并行执行"""
    print("\n" + "="*60)
    print("示例3：并行Chain")
    print("="*60)
    
    text = "Python是一种高级编程语言，简单易学，功能强大"
    
    # 三个并行任务
    parallel = RunnableParallel(
        translate=(
            ChatPromptTemplate.from_template("翻译成英文：{text}")
            | ChatOpenAI()
            | StrOutputParser()
        ),
        summarize=(
            ChatPromptTemplate.from_template("用5个字总结：{text}")
            | ChatOpenAI()
            | StrOutputParser()
        ),
        keywords=(
            ChatPromptTemplate.from_template("提取3个关键词：{text}")
            | ChatOpenAI()
            | StrOutputParser()
        )
    )
    
    results = parallel.invoke({"text": text})
    
    print(f"翻译：{results['translate']}")
    print(f"总结：{results['summarize']}")
    print(f"关键词：{results['keywords']}")


def demo_4_conditional():
    """示例4：条件Chain"""
    print("\n" + "="*60)
    print("示例4：条件分支")
    print("="*60)
    
    # 意图检测
    def detect_intent(inputs):
        text = inputs["text"]
        if "翻译" in text:
            return "translate"
        elif "代码" in text:
            return "code"
        else:
            return "chat"
    
    # 不同的处理链
    translate_chain = (
        ChatPromptTemplate.from_template("翻译：{text}")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    code_chain = (
        ChatPromptTemplate.from_template("生成代码：{text}")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    chat_chain = (
        ChatPromptTemplate.from_template("回答：{text}")
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    # 条件路由
    router = RunnableBranch(
        (lambda x: detect_intent(x) == "translate", translate_chain),
        (lambda x: detect_intent(x) == "code", code_chain),
        chat_chain
    )
    
    # 测试不同输入
    inputs = [
        "请翻译：Hello World",
        "写一个Python函数计算斐波那契数列",
        "什么是人工智能？"
    ]
    
    for inp in inputs:
        result = router.invoke({"text": inp})
        print(f"\n输入：{inp}")
        print(f"输出：{result[:100]}...")


def demo_5_passthrough():
    """示例5：透传和转换"""
    print("\n" + "="*60)
    print("示例5：RunnablePassthrough")
    print("="*60)
    
    # 保留原始输入并添加处理结果
    chain = {
        "original": RunnablePassthrough(),
        "uppercase": RunnableLambda(lambda x: x.upper()),
        "length": RunnableLambda(lambda x: len(x)),
        "analysis": (
            ChatPromptTemplate.from_template("分析这句话：{text}")
            | ChatOpenAI()
            | StrOutputParser()
        ).with_config(input_key="text")
    }
    
    result = chain.invoke("hello world")
    
    print(f"原始：{result.get('original')}")
    print(f"大写：{result.get('uppercase')}")
    print(f"长度：{result.get('length')}")


def demo_6_fallback():
    """示例6：备用Chain"""
    print("\n" + "="*60)
    print("示例6：Fallback（主Chain失败用备用）")
    print("="*60)
    
    # 主Chain（可能失败）
    primary = (
        ChatPromptTemplate.from_template("详细解释{topic}（2000字）")
        | ChatOpenAI(model="gpt-4-turbo", timeout=2)  # 短超时，容易失败
        | StrOutputParser()
    )
    
    # 备用Chain
    fallback = (
        ChatPromptTemplate.from_template("简单解释{topic}")
        | ChatOpenAI(model="gpt-3.5-turbo")
        | StrOutputParser()
    )
    
    # 组合
    chain_with_fallback = primary.with_fallbacks([fallback])
    
    try:
        result = chain_with_fallback.invoke({"topic": "量子计算"})
        print(f"结果：{result[:200]}...")
    except Exception as e:
        print(f"失败：{e}")


def demo_7_complex_workflow():
    """示例7：复杂工作流"""
    print("\n" + "="*60)
    print("示例7：完整的复杂工作流")
    print("="*60)
    
    # 步骤1：分析输入
    analyze_chain = (
        ChatPromptTemplate.from_template(
            "分析这个需求的复杂度（简单/中等/复杂）：{request}"
        )
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    # 步骤2：根据复杂度选择处理方式
    simple_chain = (
        ChatPromptTemplate.from_template("快速回答：{request}")
        | ChatOpenAI(model="gpt-3.5-turbo")
        | StrOutputParser()
    )
    
    complex_chain = (
        ChatPromptTemplate.from_template("详细分析：{request}")
        | ChatOpenAI(model="gpt-4-turbo")
        | StrOutputParser()
    )
    
    # 步骤3：后处理
    def post_process(result):
        return f"[AI回复] {result}\n[字数统计] {len(result)}"
    
    # 完整工作流
    full_workflow = (
        {
            "request": RunnablePassthrough(),
            "complexity": analyze_chain
        }
        | RunnableBranch(
            (lambda x: "简单" in x["complexity"], simple_chain.with_config(input_key="request")),
            complex_chain.with_config(input_key="request")
        )
        | RunnableLambda(post_process)
    )
    
    request = "如何学习机器学习？"
    result = full_workflow.invoke({"request": request})
    
    print(result)


def main():
    """主函数"""
    print("🎯 Chain高级用法演示")
    print("="*60)
    
    demo_1_basic_chain()
    demo_2_multi_step()
    demo_3_parallel()
    demo_4_conditional()
    demo_5_passthrough()
    demo_6_fallback()
    demo_7_complex_workflow()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 核心要点：")
    print("1. Chain用|组合组件，清晰直观")
    print("2. 支持顺序、并行、条件执行")
    print("3. RunnablePassthrough保留原始数据")
    print("4. Fallback提供备用方案")
    print("5. 可以构建任意复杂的工作流")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 Chain设计模式

### 常见模式

```
1. Pipeline模式（顺序）
   A → B → C → D

2. Fan-out模式（并行）
   A → B1
     → B2
     → B3

3. Router模式（条件）
   A → 判断 → B1或B2或B3

4. Map-Reduce模式
   输入 → 分割 → 并行处理 → 合并 → 输出

5. Retry-Fallback模式
   尝试A → 失败 → 重试 → 失败 → 备用B
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 使用LCEL组合Chain
- [ ] 实现顺序、并行、条件Chain
- [ ] 使用Fallback和Retry
- [ ] 调试Chain执行流程
- [ ] 构建复杂的AI工作流

---

## 📝 下一课预告

**第28课：LangChain实战项目1 - 智能文档问答**

下一课我们将整合所有知识，构建第一个完整项目：
- 文档加载和处理
- 向量化和检索
- 基于Chain的问答系统
- 完整的实战代码

**理论学完了，实战开始！**

---

**🎉 恭喜你完成第27课！**

你现在能构建任意复杂的AI工作流了！

**进度：27/165课（16.4%完成）** 🚀
