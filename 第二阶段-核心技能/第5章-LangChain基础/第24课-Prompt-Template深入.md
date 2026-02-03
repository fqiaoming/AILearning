![Prompt模板工作流程](./images/prompt_template.svg)
*图：Prompt模板工作流程*

# 第24课：Prompt Template深入 - 打造灵活的提示词系统

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第5章 - LangChain核心概念（第2/7课）
> - 学习目标：深入掌握Prompt Template，构建专业的提示词管理系统
> - 预计时间：70-80分钟
> - 前置知识：第23课

---

## 📢 课程导入

### 前言

上节课我们学了LangChain的基础，知道了Prompt Template能让提示词模板化。但你可能会想：**就是个字符串替换而已，有必要专门学一课吗？**

大错特错！LangChain的Prompt Template远比你想象的强大！它不仅仅是字符串替换，而是一个完整的提示词工程解决方案！支持Few-shot、条件逻辑、多语言、版本管理...今天这课会让你大开眼界！

---

### 核心价值点

**第一，Prompt Template是LangChain的基石。**

为什么Prompt Template这么重要？因为：
- **可维护性**：提示词和代码分离，易于修改
- **可复用性**：一个模板多处使用
- **可测试性**：模板可以单独测试
- **团队协作**：非技术人员也能修改提示词

在大型AI项目中，可能有几百个提示词，如果没有Template管理，会一团糟！

**第二，LangChain的Template功能非常丰富。**

LangChain的Prompt Template不是简单的`f-string`，它支持：
- **变量验证**：自动检查必需变量
- **Few-shot**：动态添加示例
- **条件逻辑**：根据条件选择不同模板
- **部分填充**：先填一部分，后面再填其余
- **输出指令**：自动添加格式说明
- **多语言**：一键切换语言

这些功能让提示词管理变得专业和高效！

**第三，掌握Template是提示词工程的核心技能。**

真实项目中，提示词会不断迭代：
- A/B测试不同版本
- 针对不同用户定制
- 根据场景动态调整
- 多语言支持

如果用硬编码，每次改动都要改代码、测试、部署，效率极低！但用Template，只需修改配置，立即生效！

**第四，这是从初级到中级的关键跃升。**

初级开发：提示词写在代码里
中级开发：用Template管理提示词
高级开发：建立完整的Prompt Hub

学会Template，你就具备了中级LangChain开发能力！

---

### 行动号召

今天这一课会教你：
- PromptTemplate的所有用法
- ChatPromptTemplate深度解析
- Few-shot Template实战
- 自定义Template
- Prompt工程最佳实践

**学完这课，你就能专业地管理提示词了！**

---

## 📖 知识讲解

### 1. PromptTemplate基础

#
![Model Io](./images/model_io.svg)
*图：Model Io*

### 1.1 基础用法

```python
from langchain.prompts import PromptTemplate

# 方式1：使用from_template
template = PromptTemplate.from_template(
    "请用{language}回答：{question}"
)

# 方式2：完整定义
template = PromptTemplate(
    input_variables=["language", "question"],
    template="请用{language}回答：{question}"
)

# 使用
prompt = template.format(language="中文", question="什么是AI？")
print(prompt)
# 输出：请用中文回答：什么是AI？
```

#### 1.2 变量验证

```python
# 定义必需变量
template = PromptTemplate(
    input_variables=["name", "age"],  # 必需变量
    template="你好，我是{name}，今年{age}岁"
)

# 正确使用
prompt = template.format(name="Alice", age=25)

# 错误使用（会报错）
prompt = template.format(name="Alice")  # 缺少age
# KeyError: 'age'
```

#### 1.3 部分变量（Partial）

```python
# 先填充部分变量
template = PromptTemplate.from_template(
    "你是{role}，请用{style}的方式回答：{question}"
)

# 固定role和style
partial_template = template.partial(
    role="Python专家",
    style="通俗易懂"
)

# 后续只需填question
prompt1 = partial_template.format(question="什么是装饰器？")
prompt2 = partial_template.format(question="什么是生成器？")
```

**使用场景：**
```
✅ 固定的system message
✅ 统一的角色设定
✅ 默认配置
✅ 减少重复参数
```

---

### 2. ChatPromptTemplate

#### 2.1 基础用法

```python
from langchain.prompts import ChatPromptTemplate

# 方式1：简单模板
template = ChatPromptTemplate.from_template(
    "你是{role}，请回答：{question}"
)

# 方式2：多消息模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是一位{role}"),
    ("human", "{question}"),
    ("ai", "{example_answer}"),  # 可选的Few-shot
    ("human", "{new_question}")
])

# 使用
messages = template.format_messages(
    role="Python专家",
    question="什么是装饰器？",
    example_answer="装饰器是...",
    new_question="能举个例子吗？"
)
```

#### 2.2 消息类型

```python
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

# 系统消息
system_template = SystemMessagePromptTemplate.from_template(
    "你是{role}，擅长{skill}"
)

# 人类消息
human_template = HumanMessagePromptTemplate.from_template(
    "{question}"
)

# 组合
chat_template = ChatPromptTemplate.from_messages([
    system_template,
    human_template
])

# 使用
messages = chat_template.format_messages(
    role="Python导师",
    skill="用简单比喻解释复杂概念",
    question="什么是闭包？"
)
```

---

### 3. Few-shot Prompt Template

#### 3.1 基础Few-shot

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# 定义示例
examples = [
    {
        "input": "今天天气真好",
        "output": "正面"
    },
    {
        "input": "这个产品太差了",
        "output": "负面"
    },
    {
        "input": "还可以吧",
        "output": "中性"
    }
]

# 定义示例模板
example_template = PromptTemplate(
    input_variables=["input", "output"],
    template="输入：{input}\n输出：{output}"
)

# 定义Few-shot模板
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="以下是情感分类的示例：",
    suffix="输入：{input}\n输出：",
    input_variables=["input"]
)

# 使用
prompt = few_shot_template.format(input="这个挺好的")
print(prompt)
```

**输出：**
```
以下是情感分类的示例：
输入：今天天气真好
输出：正面
输入：这个产品太差了
输出：负面
输入：还可以吧
输出：中性
输入：这个挺好的
输出：
```

---

#### 3.2 动态Few-shot（根据输入选择示例）

```python
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 定义示例库
examples = [
    {"input": "Python是什么？", "output": "Python是一种编程语言"},
    {"input": "如何安装Python？", "output": "可以从官网下载..."},
    {"input": "什么是列表？", "output": "列表是..."},
    {"input": "如何定义函数？", "output": "使用def关键字..."},
    # ... 更多示例
]

# 创建示例选择器（基于语义相似度）
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    Chroma,
    k=2  # 选择最相似的2个示例
)

# 创建Few-shot模板
few_shot_template = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate(
        input_variables=["input", "output"],
        template="Q: {input}\nA: {output}"
    ),
    prefix="以下是一些Python问答：",
    suffix="Q: {input}\nA:",
    input_variables=["input"]
)

# 使用（自动选择相似示例）
prompt = few_shot_template.format(input="怎么定义类？")
# 会选择最相关的2个示例
```

---

### 4. 高级Template技巧

#### 4.1 条件模板

```python
from langchain.prompts import PromptTemplate

def create_prompt(difficulty: str):
    """根据难度创建不同模板"""
    if difficulty == "easy":
        template = PromptTemplate.from_template(
            "用小学生能懂的话解释：{topic}"
        )
    elif difficulty == "medium":
        template = PromptTemplate.from_template(
            "用通俗的话解释：{topic}"
        )
    else:  # hard
        template = PromptTemplate.from_template(
            "用专业术语详细解释：{topic}"
        )
    
    return template

# 使用
easy_prompt = create_prompt("easy")
hard_prompt = create_prompt("hard")

print(easy_prompt.format(topic="递归"))
print(hard_prompt.format(topic="递归"))
```

#### 4.2 组合模板

```python
from langchain.prompts import PromptTemplate

# 定义可复用的部分
system_template = PromptTemplate.from_template(
    "你是{role}，擅长{skill}"
)

task_template = PromptTemplate.from_template(
    "请{action}：{content}"
)

# 组合
full_template = PromptTemplate.from_template(
    f"{system_template.template}\n{task_template.template}"
)

# 使用
prompt = full_template.format(
    role="Python专家",
    skill="代码优化",
    action="重构以下代码",
    content="def add(a, b): return a + b"
)
```

#### 4.3 Template中的函数

```python
from datetime import datetime

template = PromptTemplate(
    input_variables=["topic"],
    template="当前时间：{time}\n话题：{topic}",
    partial_variables={
        "time": lambda: datetime.now().strftime("%Y-%m-%d %H:%M")
    }
)

# 每次调用时time都是当前时间
prompt = template.format(topic="AI")
```

---

## 💻 Demo案例：Prompt Template实战

创建`prompt_template_demo.py`：

```python
"""
Prompt Template完整演示
从基础到高级的所有用法
"""

from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder
)
from langchain_openai import ChatOpenAI
from datetime import datetime


def demo_1_basic():
    """示例1：基础模板"""
    print("\n" + "="*60)
    print("示例1：基础Prompt Template")
    print("="*60)
    
    template = PromptTemplate.from_template(
        "将以下{source_lang}翻译成{target_lang}：\n{text}"
    )
    
    prompt = template.format(
        source_lang="中文",
        target_lang="英文",
        text="你好，世界"
    )
    
    print(f"生成的提示词：\n{prompt}")


def demo_2_chat_template():
    """示例2：Chat模板"""
    print("\n" + "="*60)
    print("示例2：ChatPrompt Template")
    print("="*60)
    
    template = ChatPromptTemplate.from_messages([
        ("system", "你是{role}，擅长{skill}"),
        ("human", "{question}"),
        ("ai", "让我帮你解答..."),
        ("human", "请详细说明")
    ])
    
    messages = template.format_messages(
        role="Python导师",
        skill="通俗讲解",
        question="什么是生成器？"
    )
    
    print("生成的消息：")
    for msg in messages:
        print(f"{msg.type}: {msg.content}")


def demo_3_few_shot():
    """示例3：Few-shot模板"""
    print("\n" + "="*60)
    print("示例3：Few-shot Template")
    print("="*60)
    
    # 定义示例
    examples = [
        {"word": "happy", "antonym": "sad"},
        {"word": "tall", "antonym": "short"},
        {"word": "hot", "antonym": "cold"}
    ]
    
    # 示例格式
    example_template = PromptTemplate(
        input_variables=["word", "antonym"],
        template="Word: {word}\nAntonym: {antonym}"
    )
    
    # Few-shot模板
    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_template,
        prefix="Give the antonym of every word:",
        suffix="Word: {input}\nAntonym:",
        input_variables=["input"]
    )
    
    prompt = few_shot_template.format(input="big")
    print(f"生成的提示词：\n{prompt}")


def demo_4_partial():
    """示例4：部分填充"""
    print("\n" + "="*60)
    print("示例4：Partial Variables")
    print("="*60)
    
    # 创建模板
    template = PromptTemplate(
        input_variables=["task", "content"],
        template="作为{role}，{task}：\n{content}"
    )
    
    # 固定role
    python_expert_template = template.partial(role="Python专家")
    js_expert_template = template.partial(role="JavaScript专家")
    
    # 使用
    prompt1 = python_expert_template.format(
        task="解释以下代码",
        content="lambda x: x * 2"
    )
    
    prompt2 = js_expert_template.format(
        task="解释以下代码",
        content="const add = (a, b) => a + b"
    )
    
    print(f"Python专家提示词：\n{prompt1}\n")
    print(f"JS专家提示词：\n{prompt2}")


def demo_5_with_function():
    """示例5：函数变量"""
    print("\n" + "="*60)
    print("示例5：动态变量（函数）")
    print("="*60)
    
    template = PromptTemplate(
        input_variables=["topic"],
        template="时间：{time}\n日期：{date}\n话题：{topic}",
        partial_variables={
            "time": lambda: datetime.now().strftime("%H:%M:%S"),
            "date": lambda: datetime.now().strftime("%Y-%m-%d")
        }
    )
    
    # 每次调用时间都不同
    import time
    
    prompt1 = template.format(topic="AI")
    print(f"第一次：\n{prompt1}\n")
    
    time.sleep(2)
    
    prompt2 = template.format(topic="ML")
    print(f"第二次（2秒后）：\n{prompt2}")


def demo_6_complex_chain():
    """示例6：复杂链式调用"""
    print("\n" + "="*60)
    print("示例6：Template链式调用")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 翻译模板
    translate_template = ChatPromptTemplate.from_template(
        "翻译成{language}：{text}"
    )
    
    # 总结模板
    summarize_template = ChatPromptTemplate.from_template(
        "用{words}字总结：{text}"
    )
    
    # 组合链
    from langchain.schema.output_parser import StrOutputParser
    
    translate_chain = translate_template | llm | StrOutputParser()
    
    # 先翻译
    translated = translate_chain.invoke({
        "language": "英文",
        "text": "人工智能正在改变世界"
    })
    
    print(f"翻译结果：{translated}")
    
    # 再总结
    summarize_chain = summarize_template | llm | StrOutputParser()
    summary = summarize_chain.invoke({
        "words": 10,
        "text": translated
    })
    
    print(f"总结结果：{summary}")


def demo_7_multi_language():
    """示例7：多语言模板"""
    print("\n" + "="*60)
    print("示例7：多语言支持")
    print("="*60)
    
    templates = {
        "zh": PromptTemplate.from_template(
            "你是{role}，请回答：{question}"
        ),
        "en": PromptTemplate.from_template(
            "You are a {role}, please answer: {question}"
        ),
        "ja": PromptTemplate.from_template(
            "あなたは{role}です。質問に答えてください：{question}"
        )
    }
    
    # 使用不同语言
    for lang, template in templates.items():
        prompt = template.format(
            role="AI expert",
            question="What is machine learning?"
        )
        print(f"{lang.upper()}: {prompt}\n")


def demo_8_production_example():
    """示例8：生产级示例"""
    print("\n" + "="*60)
    print("示例8：生产级Prompt管理")
    print("="*60)
    
    class PromptManager:
        """Prompt管理器"""
        
        def __init__(self):
            self.templates = {}
        
        def register(self, name: str, template: PromptTemplate):
            """注册模板"""
            self.templates[name] = template
        
        def get(self, name: str) -> PromptTemplate:
            """获取模板"""
            if name not in self.templates:
                raise ValueError(f"Template {name} not found")
            return self.templates[name]
        
        def list_templates(self):
            """列出所有模板"""
            return list(self.templates.keys())
    
    # 使用
    manager = PromptManager()
    
    # 注册多个模板
    manager.register("translate", PromptTemplate.from_template(
        "翻译成{lang}：{text}"
    ))
    
    manager.register("summarize", PromptTemplate.from_template(
        "用{words}字总结：{text}"
    ))
    
    manager.register("explain", PromptTemplate.from_template(
        "解释{topic}，面向{audience}"
    ))
    
    # 使用
    print("已注册模板：", manager.list_templates())
    
    translate_prompt = manager.get("translate").format(
        lang="英文",
        text="你好"
    )
    print(f"\n翻译提示词：{translate_prompt}")


def main():
    """主函数"""
    print("🎯 Prompt Template完整演示")
    print("="*60)
    
    demo_1_basic()
    demo_2_chat_template()
    demo_3_few_shot()
    demo_4_partial()
    demo_5_with_function()
    demo_6_complex_chain()
    demo_7_multi_language()
    demo_8_production_example()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 核心要点：")
    print("1. 使用Template让提示词可维护")
    print("2. Few-shot Template动态添加示例")
    print("3. Partial Variables减少重复")
    print("4. ChatPromptTemplate处理多轮对话")
    print("5. 建立Prompt管理系统统一管理")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 最佳实践

### Prompt管理策略

```
✅ 集中管理
  - 所有提示词统一存放
  - 使用配置文件或数据库
  - 建立版本控制

✅ 模板化
  - 提取公共部分
  - 使用变量替换
  - 支持多语言

✅ 测试验证
  - 单独测试提示词
  - A/B测试不同版本
  - 记录效果数据

✅ 文档化
  - 说明每个变量的作用
  - 记录使用示例
  - 标注适用场景
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 使用PromptTemplate和ChatPromptTemplate
- [ ] 实现Few-shot Template
- [ ] 使用Partial Variables
- [ ] 创建动态Template
- [ ] 建立Prompt管理系统

---

## 📝 下一课预告

**第25课：Output Parser详解 - 结构化AI输出**

下一课我们将学习如何解析AI的输出：
- JSON Parser
- List Parser
- Datetime Parser
- 自定义Parser
- Pydantic Parser

**让AI输出结构化、可靠！**

---

**🎉 恭喜你完成第24课！**

你现在能专业地管理提示词了！

**进度：24/165课（14.5%完成）** 🚀

