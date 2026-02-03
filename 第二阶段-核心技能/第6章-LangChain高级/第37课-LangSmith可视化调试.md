![调试与问题排查](./images/debugging.svg)
*图：调试与问题排查*

# 第37课：LangSmith可视化调试 - 强大的调试神器

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第7章 - LangChain调试与监控（第1/4课）
> - 学习目标：掌握LangSmith可视化调试工具，提升10倍调试效率
> - 预计时间：80-90分钟
> - 前置知识：第23-36课

---

## 📢 课程导入

### 前言

你的LangChain应用运行出问题了！你加了一堆print语句，刷新了无数次终端，盯着日志看了半天，还是找不到问题在哪...这种调试体验简直是噩梦！

但如果有个工具能：**可视化显示每一步的执行、输入输出一目了然、性能瓶颈直接标红、错误信息精准定位**，调试会不会变得超级简单？

**LangSmith就是这样的神器！**官方开发的可视化调试平台，让LangChain调试从"黑盒摸索"变成"一览无余"！今天我要教你如何用LangSmith让调试效率提升10倍！

---

### 核心价值点

**第一，LangSmith是LangChain官方的调试平台。**

不是第三方工具，是LangChain团队专门为开发者打造的：
- ✅ 与LangChain深度集成
- ✅ 零侵入，只需配置环境变量
- ✅ 免费使用（有限额）
- ✅ 功能强大且持续更新

这是官方推荐的最佳调试工具！

**第二，可视化调试比打印日志高效100倍。**

对比两种调试方式：

**传统方式**：
```python
print("Chain开始...")
print(f"输入：{input}")
result = chain.invoke(input)
print(f"输出：{result}")
print(f"耗时：{elapsed}")
```
- 代码侵入性强
- 日志混乱难看
- 无法回溯历史
- 性能分析困难

**LangSmith方式**：
- 自动记录所有执行
- 可视化流程图
- 交互式查看数据
- 性能时间线
- 历史记录永久保存

差距太大了！

**第三，LangSmith不只是调试工具，还是监控平台。**

很多人以为LangSmith只能调试，其实它能做：
- **调试**：可视化执行流程
- **监控**：实时性能指标
- **测试**：自动化测试套件
- **优化**：性能瓶颈分析
- **协作**：团队共享调试信息

一个工具，搞定开发、测试、运维全流程！

**第四，这是从业余到专业的分水岭。**

- **业余开发者**：出问题就慌，到处打log，盲目试错
- **专业开发者**：用LangSmith秒定位，看流程图就知道问题

掌握LangSmith，你的调试能力立即提升一个档次！面试时说"我用LangSmith调试"，立即显得专业！

---

### 行动号召

今天这一课会教你：
- LangSmith的核心功能
- 如何配置和使用
- 可视化调试技巧
- 性能分析方法
- 团队协作最佳实践

**学完这课，调试变得轻松愉快！**

---

## 📖 知识讲解

### 1. LangSmith简介

#
![Monitoring](./images/monitoring.svg)
*图：Monitoring*

### 1.1 什么是LangSmith

```
LangSmith是LangChain官方开发的：
- 可视化调试平台
- 性能监控系统
- 测试评估工具
- 团队协作平台

官网：https://smith.langchain.com
```

#### 1.2 核心功能

```
1. 追踪（Tracing）：
   - 记录每次Chain执行
   - 可视化执行流程
   - 查看输入输出
   - 分析性能耗时

2. 评估（Evaluation）：
   - 自动化测试
   - 回归测试
   - A/B测试
   - 质量评分

3. 监控（Monitoring）：
   - 实时性能指标
   - 错误率统计
   - 成本追踪
   - 告警通知

4. 数据集（Datasets）：
   - 测试用例管理
   - Few-shot示例库
   - 评估基准
```

---

### 2. 快速开始

#### 2.1 注册和配置

```bash
# 1. 访问 https://smith.langchain.com 注册账号

# 2. 获取API Key（在Settings -> API Keys）

# 3. 配置环境变量
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="你的API密钥"
export LANGCHAIN_PROJECT="my-project"  # 项目名称
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```

#### 2.2 Python代码配置

```python
import os

# 方式1：直接设置环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "你的API密钥"
os.environ["LANGCHAIN_PROJECT"] = "my-first-project"

# 方式2：使用.env文件
from dotenv import load_dotenv
load_dotenv()  # 自动加载.env文件中的配置

# 就这样！现在所有Chain执行都会自动追踪
```

#### 2.3 验证配置

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 配置LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "你的密钥"
os.environ["LANGCHAIN_PROJECT"] = "test-project"

# 正常使用LangChain
llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("解释{topic}")
chain = prompt | llm

# 执行（自动追踪到LangSmith）
result = chain.invoke({"topic": "AI"})

print("✓ 执行完成！")
print("✓ 访问 https://smith.langchain.com 查看追踪记录")
```

---

### 3. 可视化调试

#### 3.1 查看执行流程

```
执行完Chain后，在LangSmith界面你会看到：

┌─────────────────────────────────────┐
│  RunnableSequence (2.34s)           │  ← 总耗时
├─────────────────────────────────────┤
│  ├─ ChatPromptTemplate (0.01s)      │
│  │   Input: {topic: "AI"}           │
│  │   Output: ChatPromptValue(...)   │
│  │                                   │
│  └─ ChatOpenAI (2.33s)              │  ← 性能瓶颈
│      Input: messages=[...]          │
│      Output: AIMessage(...)         │
│      Tokens: 150                    │
└─────────────────────────────────────┘

点击每个节点可以查看：
- 完整的输入数据
- 完整的输出数据
- 执行耗时
- Token使用
- 错误信息（如果有）
```

#### 3.2 交互式探索

```
在LangSmith Web界面：

1. Timeline视图：
   ├─ 时间线展示执行顺序
   └─ 一眼看出哪个步骤慢

2. Tree视图：
   ├─ 树形结构展示调用关系
   └─ 清晰看到嵌套关系

3. Input/Output标签：
   ├─ 查看原始数据
   └─ 支持JSON格式化

4. Metadata标签：
   ├─ 模型参数
   ├─ Token统计
   └─ 自定义元数据

5. Feedback标签：
   └─ 标记执行质量（好/坏）
```

---

### 4. 性能分析

#### 4.1 找出性能瓶颈

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# 复杂的Chain
prompt1 = ChatPromptTemplate.from_template("总结：{text}")
llm1 = ChatOpenAI()

prompt2 = ChatPromptTemplate.from_template("翻译成英文：{summary}")
llm2 = ChatOpenAI()

prompt3 = ChatPromptTemplate.from_template("提取关键词：{translation}")
llm3 = ChatOpenAI()

# 组合Chain
chain = (
    {"text": lambda x: x}
    | prompt1 | llm1 | StrOutputParser()
    | {"summary": lambda x: x}
    | prompt2 | llm2 | StrOutputParser()
    | {"translation": lambda x: x}
    | prompt3 | llm3 | StrOutputParser()
)

# 执行
result = chain.invoke("这是一篇很长的文章...")

# 在LangSmith中查看：
# - 哪个LLM调用最慢？
# - 哪个步骤占用时间最多？
# - 是否有优化空间？
```

**LangSmith会显示**：
```
Step 1: Prompt1 + LLM1 → 2.3秒  ⚠️
Step 2: Prompt2 + LLM2 → 2.1秒  ⚠️
Step 3: Prompt3 + LLM3 → 2.5秒  ⚠️
总计：6.9秒

优化建议：
✓ 三个LLM调用可以优化为一个
✓ 或者使用更快的模型
✓ 或者添加缓存
```

---

#### 4.2 对比不同版本

```python
# 版本1：未优化
os.environ["LANGCHAIN_PROJECT"] = "test-v1-original"

result1 = slow_chain.invoke(input)

# 版本2：优化后
os.environ["LANGCHAIN_PROJECT"] = "test-v2-optimized"

result2 = fast_chain.invoke(input)

# 在LangSmith中对比：
# - 响应时间：6.9s → 2.3s（提升3倍）
# - Token使用：500 → 200（节省60%）
# - LLM调用：3次 → 1次
```

---

### 5. 错误调试

#### 5.1 错误追踪

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 故意制造错误
prompt = ChatPromptTemplate.from_template("分析{topic}和{style}")

chain = prompt | ChatOpenAI()

# 缺少style参数
try:
    result = chain.invoke({"topic": "AI"})  # 会报错
except Exception as e:
    print(f"错误：{e}")

# 在LangSmith中查看：
# ❌ 精确显示哪一步出错
# ❌ 完整的错误堆栈
# ❌ 输入数据是什么
# ❌ 期望什么，实际是什么
```

**LangSmith错误显示**：
```
┌─────────────────────────────────┐
│ ❌ ChatPromptTemplate           │
│    Error: KeyError: 'style'     │
│                                  │
│    Input: {topic: "AI"}         │
│    Missing: style               │
│                                  │
│    Stack Trace:                 │
│    File "prompt.py", line 42    │
│    ...                          │
└─────────────────────────────────┘

建议：
✓ 提供missing参数 'style'
✓ 或者使用 partial(style="default")
```

---

### 6. 数据集和测试

#### 6.1 创建测试数据集

```python
from langsmith import Client

client = Client()

# 创建数据集
dataset_name = "qa-test-dataset"

examples = [
    {
        "inputs": {"question": "什么是AI？"},
        "outputs": {"answer": "人工智能..."}
    },
    {
        "inputs": {"question": "什么是ML？"},
        "outputs": {"answer": "机器学习..."}
    },
    {
        "inputs": {"question": "什么是DL？"},
        "outputs": {"answer": "深度学习..."}
    }
]

# 上传数据集
dataset = client.create_dataset(dataset_name)

for example in examples:
    client.create_example(
        inputs=example["inputs"],
        outputs=example["outputs"],
        dataset_id=dataset.id
    )

print(f"✓ 数据集创建成功：{dataset_name}")
```

---

#### 6.2 运行测试

```python
from langchain.smith import RunEvalConfig, run_on_dataset

# 定义评估Chain
qa_chain = prompt | llm | StrOutputParser()

# 配置评估
eval_config = RunEvalConfig(
    evaluators=[
        "qa",  # QA评估器
        "criteria",  # 标准评估器
    ]
)

# 在数据集上运行
results = run_on_dataset(
    client=client,
    dataset_name="qa-test-dataset",
    llm_or_chain_factory=lambda: qa_chain,
    evaluation=eval_config,
    project_name="qa-eval-run-1"
)

print(f"✓ 测试完成")
print(f"  通过：{results['passed']}")
print(f"  失败：{results['failed']}")

# 在LangSmith中查看：
# - 每个测试用例的执行结果
# - 通过率统计
# - 失败原因分析
```

---

## 💻 Demo案例：LangSmith实战

创建`langsmith_demo.py`：

```python
"""
LangSmith完整演示
从配置到调试、测试、优化
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import LLMChain


# ============= 配置LangSmith =============

def setup_langsmith(project_name: str):
    """配置LangSmith追踪"""
    
    # 注意：这里使用示例密钥，请替换为你的真实密钥
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # os.environ["LANGCHAIN_API_KEY"] = "你的LangSmith API Key"
    os.environ["LANGCHAIN_PROJECT"] = project_name
    
    print(f"✓ LangSmith已配置")
    print(f"  项目：{project_name}")
    print(f"  追踪：已启用")
    print(f"  查看：https://smith.langchain.com\n")


# ============= Demo 1：基础追踪 =============

def demo_1_basic_tracing():
    """演示1：基础追踪"""
    
    print("="*60)
    print("演示1：基础追踪")
    print("="*60 + "\n")
    
    setup_langsmith("demo-1-basic")
    
    # 简单的Chain
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_template("用一句话解释{topic}")
    chain = prompt | llm | StrOutputParser()
    
    # 执行
    print("执行Chain...")
    result = chain.invoke({"topic": "量子计算"})
    
    print(f"结果：{result}\n")
    print("✓ 追踪已发送到LangSmith")
    print("✓ 访问 https://smith.langchain.com 查看可视化流程\n")


# ============= Demo 2：复杂Chain追踪 =============

def demo_2_complex_chain():
    """演示2：复杂Chain的追踪"""
    
    print("="*60)
    print("演示2：复杂Chain追踪")
    print("="*60 + "\n")
    
    setup_langsmith("demo-2-complex")
    
    llm = ChatOpenAI()
    
    # 多步骤Chain
    step1 = (
        ChatPromptTemplate.from_template("总结（50字）：{text}")
        | llm
        | StrOutputParser()
    )
    
    step2 = (
        ChatPromptTemplate.from_template("翻译成英文：{summary}")
        | llm
        | StrOutputParser()
    )
    
    step3 = (
        ChatPromptTemplate.from_template("提取3个关键词：{translation}")
        | llm
        | StrOutputParser()
    )
    
    # 组合Chain（简化版，实际需要更复杂的组合）
    print("执行3步骤Chain...")
    
    text = "人工智能正在改变世界，从医疗到金融，AI应用无处不在。"
    
    summary = step1.invoke({"text": text})
    print(f"步骤1完成：总结")
    
    translation = step2.invoke({"summary": summary})
    print(f"步骤2完成：翻译")
    
    keywords = step3.invoke({"translation": translation})
    print(f"步骤3完成：关键词")
    
    print(f"\n最终结果：{keywords}")
    print("\n✓ 在LangSmith中可以看到：")
    print("  - 3个独立的Chain执行")
    print("  - 每步的输入输出")
    print("  - 各步骤的耗时对比\n")


# ============= Demo 3：错误调试 =============

def demo_3_error_debugging():
    """演示3：错误调试"""
    
    print("="*60)
    print("演示3：错误调试")
    print("="*60 + "\n")
    
    setup_langsmith("demo-3-error")
    
    # 故意制造错误
    prompt = ChatPromptTemplate.from_template(
        "分析{topic}，风格：{style}"
    )
    
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    
    print("尝试执行（缺少参数）...")
    
    try:
        # 缺少style参数
        result = chain.invoke({"topic": "AI"})
    except Exception as e:
        print(f"❌ 错误：{type(e).__name__}")
        print(f"   消息：{str(e)[:100]}")
    
    print("\n✓ 在LangSmith中可以看到：")
    print("  - 错误发生在哪个组件")
    print("  - 完整的错误堆栈")
    print("  - 输入数据是什么")
    print("  - 缺少哪个参数\n")


# ============= Demo 4：性能对比 =============

def demo_4_performance_comparison():
    """演示4：性能对比"""
    
    print("="*60)
    print("演示4：性能对比")
    print("="*60 + "\n")
    
    # 版本1：详细Prompt
    setup_langsmith("demo-4-v1-verbose")
    
    verbose_prompt = ChatPromptTemplate.from_template("""
作为一位专业的技术专家，请详细、全面、深入地解释以下主题，
包括背景、原理、应用等多个方面：{topic}
""")
    
    llm = ChatOpenAI()
    verbose_chain = verbose_prompt | llm | StrOutputParser()
    
    print("执行版本1（详细Prompt）...")
    result1 = verbose_chain.invoke({"topic": "区块链"})
    print(f"结果长度：{len(result1)}字符\n")
    
    # 版本2：精简Prompt
    setup_langsmith("demo-4-v2-concise")
    
    concise_prompt = ChatPromptTemplate.from_template(
        "简要解释{topic}（50字内）"
    )
    
    concise_chain = concise_prompt | llm | StrOutputParser()
    
    print("执行版本2（精简Prompt）...")
    result2 = concise_chain.invoke({"topic": "区块链"})
    print(f"结果长度：{len(result2)}字符\n")
    
    print("✓ 在LangSmith中对比两个项目：")
    print("  - 响应时间差异")
    print("  - Token使用差异")
    print("  - 输出质量差异\n")


# ============= Demo 5：添加元数据 =============

def demo_5_with_metadata():
    """演示5：添加元数据"""
    
    print("="*60)
    print("演示5：添加元数据")
    print("="*60 + "\n")
    
    setup_langsmith("demo-5-metadata")
    
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_template("介绍{topic}")
    chain = prompt | llm | StrOutputParser()
    
    # 添加元数据
    print("执行并添加元数据...")
    result = chain.invoke(
        {"topic": "机器学习"},
        config={
            "metadata": {
                "user_id": "user_123",
                "session_id": "session_456",
                "version": "v1.0",
                "environment": "development"
            }
        }
    )
    
    print(f"结果：{result[:50]}...\n")
    print("✓ 在LangSmith中可以看到：")
    print("  - 自定义的元数据")
    print("  - 可以按元数据筛选")
    print("  - 便于分类和分析\n")


# ============= 主函数 =============

def main():
    """主函数"""
    
    print("\n" + "="*60)
    print("🎯 LangSmith完整演示")
    print("="*60 + "\n")
    
    print("⚠️  注意：需要配置LANGCHAIN_API_KEY才能使用")
    print("   获取方式：https://smith.langchain.com -> Settings -> API Keys\n")
    
    # 检查是否配置了API Key
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("❌ 未检测到LANGCHAIN_API_KEY")
        print("   请先配置：export LANGCHAIN_API_KEY='你的密钥'")
        print("\n演示代码仍会执行，但不会发送到LangSmith\n")
    
    demo_1_basic_tracing()
    demo_2_complex_chain()
    demo_3_error_debugging()
    demo_4_performance_comparison()
    demo_5_with_metadata()
    
    print("="*60)
    print("✅ 所有演示完成！")
    print("="*60)
    print("\n💡 LangSmith核心功能：")
    print("  1. 自动追踪所有Chain执行")
    print("  2. 可视化执行流程和数据")
    print("  3. 性能分析和对比")
    print("  4. 错误精准定位")
    print("  5. 测试数据集管理")
    print("\n🚀 访问 https://smith.langchain.com 查看追踪记录")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
```

---

## 🎯 LangSmith最佳实践

### 项目组织

```python
# ✅ 好的做法：按环境划分项目
os.environ["LANGCHAIN_PROJECT"] = "myapp-dev"      # 开发
os.environ["LANGCHAIN_PROJECT"] = "myapp-staging"  # 测试
os.environ["LANGCHAIN_PROJECT"] = "myapp-prod"     # 生产

# ✅ 按功能划分
os.environ["LANGCHAIN_PROJECT"] = "myapp-qa-bot"
os.environ["LANGCHAIN_PROJECT"] = "myapp-summarizer"
```

### 添加有意义的元数据

```python
chain.invoke(
    input,
    config={
        "metadata": {
            "user_id": user.id,
            "feature": "qa_system",
            "version": "v2.1",
            "ab_test_group": "A"
        }
    }
)

# 便于后续筛选和分析
```

### 控制追踪

```python
# 临时禁用追踪
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# 重新启用
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# 只追踪特定Chain
chain.invoke(
    input,
    config={
        "run_name": "重要的测试",  # 给trace命名
        "tags": ["production", "v2"]  # 添加标签
    }
)
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 配置和使用LangSmith
- [ ] 查看可视化执行流程
- [ ] 进行性能分析
- [ ] 调试错误问题
- [ ] 创建和运行测试数据集

---

## 📝 下一课预告

**第38课：生产级日志管理**

下一课我们将学习：
- 结构化日志设计
- 日志级别管理
- 日志轮转和归档
- 集成ELK/Loki
- 日志安全和合规

**构建企业级日志系统！**

---

**🎉 恭喜你完成第37课！**

你现在掌握了最强大的调试工具！

**进度：37/165课（22.4%完成）** 🚀
