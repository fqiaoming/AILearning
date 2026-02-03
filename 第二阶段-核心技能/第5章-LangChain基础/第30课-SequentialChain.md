![Chain链式调用流程](./images/chain_flow.svg)
*图：Chain链式调用流程*

# 第30课：SequentialChain - 串联多个处理步骤

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第6章 - Chain高级应用（第1/7课）
> - 学习目标：掌握SequentialChain，实现复杂的多步骤AI工作流
> - 预计时间：70-80分钟
> - 前置知识：第23-29课

---

## 📢 课程导入

### 前言

想象一个场景：你要让AI帮你写一篇文章，流程是：**构思大纲 → 扩展每个章节 → 润色语言 → 添加示例 → 生成总结**。每一步都依赖上一步的输出！

用普通方法，你要手动执行5次，每次都要复制粘贴上一步的结果...太麻烦了！但如果有个工具能自动串联这些步骤，像流水线一样自动执行，那就太爽了！

**SequentialChain就是干这个的！**它让你能优雅地串联多个步骤，构建复杂的AI工作流！今天这课，我要教你如何用SequentialChain打造强大的AI流水线！

---

### 核心价值点

**第一，SequentialChain解决了多步骤工作流的痛点。**

真实AI应用很少是一步到位的，通常需要多个步骤：
- **内容创作**：构思 → 撰写 → 优化 → 审核
- **数据分析**：收集 → 清洗 → 分析 → 可视化
- **客服系统**：理解意图 → 查询信息 → 生成回复 → 质量检查

每个步骤都是独立的Chain，但需要串联起来。SequentialChain让这一切变得简单！

**第二，SequentialChain不是简单的for循环。**

很多人以为SequentialChain就是：
```python
for step in steps:
    result = step(result)
```

错！SequentialChain提供的是：
- **数据流管理**：自动传递中间结果
- **错误处理**：某步失败能优雅处理
- **变量管理**：灵活的输入输出映射
- **调试支持**：清晰看到每步的执行
- **性能优化**：自动缓存和批处理

这才是专业的工作流引擎！

**第三，SequentialChain是构建复杂AI应用的基础。**

看看哪些场景需要SequentialChain：
- **AI写作助手**：多轮优化文本
- **智能代码生成**：分析需求 → 生成代码 → 测试 → 优化
- **数据处理管道**：ETL流程
- **多语言翻译**：中文 → 英文 → 法文 → 西班牙文

这些都需要多步骤串联！掌握SequentialChain，你就能开发这些复杂应用！

**第四，这是从中级到高级的关键技能。**

初级开发者：只会用单个Chain
中级开发者：能用LCEL组合Chain
高级开发者：能设计复杂的Sequential工作流

学会SequentialChain，你就具备了高级开发者的能力！

---

### 行动号召

今天这一课会教你：
- SequentialChain的原理和用法
- SimpleSequentialChain vs SequentialChain
- 变量传递和映射
- 错误处理和调试
- 实战：构建完整的AI工作流

**学完这课，你就能构建任意复杂的多步骤AI流程了！**

---

## 📖 知识讲解

### 1. SequentialChain概述

#
![Model Io](./images/model_io.svg)
*图：Model Io*

### 1.1 什么是SequentialChain

```
SequentialChain：
- 将多个Chain按顺序串联
- 自动传递中间结果
- 每个Chain的输出是下一个Chain的输入

工作流程：
Input → Chain1 → Output1
      → Chain2(Output1) → Output2
      → Chain3(Output2) → Output3
      → Final Output
```

#### 1.2 两种类型

```
1. SimpleSequentialChain
   - 简单版本
   - 每个Chain只有一个输入和一个输出
   - 自动传递
   - 适合简单流程

2. SequentialChain
   - 完整版本
   - 支持多个输入输出
   - 灵活的变量映射
   - 适合复杂流程
```

---

### 2. SimpleSequentialChain

#### 2.1 基础用法

```python
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

# Chain 1: 生成文章标题
chain1 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "为这个主题生成一个吸引人的标题：{topic}"
    )
)

# Chain 2: 基于标题写大纲
chain2 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "为这个标题写一个详细的大纲：{title}"
    )
)

# Chain 3: 基于大纲写文章
chain3 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "根据这个大纲写一篇文章：{outline}"
    )
)

# 组合成Sequential Chain
sequential_chain = SimpleSequentialChain(
    chains=[chain1, chain2, chain3],
    verbose=True  # 显示中间步骤
)

# 执行
final_output = sequential_chain.invoke("人工智能的未来")
print(final_output)
```

**执行流程：**
```
输入：人工智能的未来
↓
Chain1：生成标题
输出：《AI：重塑人类未来的力量》
↓
Chain2：写大纲
输出：1. AI发展历程
      2. 当前应用
      3. 未来趋势
↓
Chain3：写文章
输出：完整的文章
```

#### 2.2 SimpleSequentialChain的局限

```python
# ❌ 不支持：
# 1. 无法保留中间结果
# 2. 无法多输入多输出
# 3. 无法跳过某些步骤
# 4. 变量名固定

# 这些场景需要用完整的SequentialChain
```

---

### 3. SequentialChain（完整版）

#### 3.1 基础用法

```python
from langchain.chains import LLMChain, SequentialChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

# Chain 1: 分析主题
chain1 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "分析这个主题的关键点：{topic}"
    ),
    output_key="analysis"  # 指定输出变量名
)

# Chain 2: 生成标题（需要topic和analysis）
chain2 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "主题：{topic}\n分析：{analysis}\n\n生成一个标题"
    ),
    output_key="title"
)

# Chain 3: 写文章
chain3 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "标题：{title}\n分析：{analysis}\n\n写文章"
    ),
    output_key="article"
)

# 组合
sequential_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=["topic"],  # 初始输入
    output_variables=["analysis", "title", "article"],  # 保留的输出
    verbose=True
)

# 执行
result = sequential_chain.invoke({"topic": "量子计算"})

# 可以访问所有中间结果
print("分析：", result["analysis"])
print("标题：", result["title"])
print("文章：", result["article"])
```

#### 3.2 变量传递机制

```python
# 详细的变量传递示例
from langchain.chains import LLMChain, SequentialChain

# Chain 1: 输入topic，输出keywords
chain1 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "提取关键词：{topic}"
    ),
    output_key="keywords"
)

# Chain 2: 输入topic和keywords，输出summary
chain2 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "主题：{topic}\n关键词：{keywords}\n\n写摘要"
    ),
    output_key="summary"
)

# Chain 3: 输入所有前面的结果，输出final
chain3 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        """主题：{topic}
关键词：{keywords}
摘要：{summary}

生成最终报告"""
    ),
    output_key="final_report"
)

sequential = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=["topic"],
    output_variables=["keywords", "summary", "final_report"],
    verbose=True
)

result = sequential.invoke({"topic": "区块链技术"})
```

**变量传递规则：**
```
1. 每个Chain可以访问：
   - 初始输入变量
   - 前面所有Chain的输出

2. output_variables指定：
   - 哪些变量要保留到最终结果
   - 未指定的中间变量会被丢弃

3. 变量名必须匹配：
   - Chain的output_key
   - 后续Chain的prompt中的变量名
```

---

### 4. 高级特性

#### 4.1 条件执行

```python
from langchain.chains import LLMChain, SequentialChain

# 使用LCEL实现条件逻辑
def should_skip_step(inputs):
    """判断是否跳过某步"""
    return len(inputs.get("text", "")) < 100

# Chain with conditional
chain1 = LLMChain(...)
chain2 = LLMChain(...)

# 条件组合
from langchain.schema.runnable import RunnableBranch

conditional_chain = RunnableBranch(
    (should_skip_step, chain1),
    SequentialChain(chains=[chain1, chain2])
)
```

#### 4.2 错误处理

```python
class RobustSequentialChain:
    """带错误处理的Sequential Chain"""
    
    def __init__(self, chains):
        self.chains = chains
    
    def invoke(self, inputs):
        """执行所有链，带错误处理"""
        results = inputs.copy()
        
        for i, chain in enumerate(self.chains):
            try:
                output = chain.invoke(results)
                results.update(output)
                print(f"✓ Chain {i+1} 完成")
            except Exception as e:
                print(f"✗ Chain {i+1} 失败: {e}")
                # 决定是继续还是中断
                if self._is_critical_step(i):
                    raise
                else:
                    results[f"chain_{i}_error"] = str(e)
                    continue
        
        return results
    
    def _is_critical_step(self, step_index):
        """判断是否关键步骤"""
        return step_index == 0  # 第一步是关键步骤
```

#### 4.3 并行+顺序组合

```python
from langchain.schema.runnable import RunnableParallel

# 第一步：并行处理
parallel_step = RunnableParallel(
    translation=translation_chain,
    summary=summary_chain,
    keywords=keyword_chain
)

# 第二步：汇总
final_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        """翻译：{translation}
摘要：{summary}
关键词：{keywords}

生成最终报告"""
    )
)

# 组合：先并行，后顺序
full_pipeline = parallel_step | final_chain
```

---

## 💻 Demo案例：SequentialChain实战

创建`sequential_chain_demo.py`：

```python
"""
SequentialChain完整演示
从简单到复杂的各种场景
"""

from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def demo_1_simple_sequential():
    """示例1：SimpleSequentialChain基础用法"""
    print("\n" + "="*60)
    print("示例1：SimpleSequentialChain - 文章生成流水线")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 步骤1：生成标题
    title_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "为'{topic}'生成一个吸引人的文章标题"
        )
    )
    
    # 步骤2：生成大纲
    outline_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "为这个标题'{title}'生成一个3点大纲"
        )
    )
    
    # 步骤3：扩展内容
    content_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "基于这个大纲'{outline}'，写一段100字的内容"
        )
    )
    
    # 组合
    sequential = SimpleSequentialChain(
        chains=[title_chain, outline_chain, content_chain],
        verbose=True
    )
    
    # 执行
    result = sequential.invoke("人工智能如何改变教育")
    print(f"\n最终结果：\n{result}")


def demo_2_full_sequential():
    """示例2：SequentialChain - 保留中间结果"""
    print("\n" + "="*60)
    print("示例2：SequentialChain - 产品分析流程")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 步骤1：提取关键特性
    features_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "列出这个产品的3个关键特性：{product}"
        ),
        output_key="features"
    )
    
    # 步骤2：分析优势
    advantages_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """产品：{product}
特性：{features}

分析这些特性的优势"""
        ),
        output_key="advantages"
    )
    
    # 步骤3：生成营销文案
    marketing_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """产品：{product}
特性：{features}
优势：{advantages}

生成一段吸引人的营销文案（50字）"""
        ),
        output_key="marketing_copy"
    )
    
    # 组合
    sequential = SequentialChain(
        chains=[features_chain, advantages_chain, marketing_chain],
        input_variables=["product"],
        output_variables=["features", "advantages", "marketing_copy"],
        verbose=True
    )
    
    # 执行
    result = sequential.invoke({"product": "智能手表"})
    
    print("\n结果：")
    print(f"特性：{result['features']}")
    print(f"优势：{result['advantages']}")
    print(f"文案：{result['marketing_copy']}")


def demo_3_multi_input():
    """示例3：多输入Sequential Chain"""
    print("\n" + "="*60)
    print("示例3：多输入场景 - 个性化推荐")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 步骤1：分析用户兴趣
    interest_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "根据用户年龄{age}和职业{occupation}，推测可能的兴趣"
        ),
        output_key="interests"
    )
    
    # 步骤2：推荐产品
    recommend_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """用户年龄：{age}
职业：{occupation}
兴趣：{interests}

推荐3个适合的产品"""
        ),
        output_key="recommendations"
    )
    
    # 步骤3：生成推荐理由
    reason_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """用户：{age}岁，{occupation}
兴趣：{interests}
推荐：{recommendations}

说明推荐理由"""
        ),
        output_key="reasons"
    )
    
    # 组合
    sequential = SequentialChain(
        chains=[interest_chain, recommend_chain, reason_chain],
        input_variables=["age", "occupation"],
        output_variables=["interests", "recommendations", "reasons"],
        verbose=True
    )
    
    # 执行
    result = sequential.invoke({
        "age": "28",
        "occupation": "软件工程师"
    })
    
    print("\n个性化推荐：")
    print(f"兴趣分析：{result['interests']}")
    print(f"推荐产品：{result['recommendations']}")
    print(f"推荐理由：{result['reasons']}")


def demo_4_content_creation_pipeline():
    """示例4：完整的内容创作流水线"""
    print("\n" + "="*60)
    print("示例4：内容创作完整流程")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 1. 主题分析
    analysis_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "分析这个主题'{topic}'的核心点（20字内）"
        ),
        output_key="analysis"
    )
    
    # 2. 标题生成
    title_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "主题：{topic}\n核心：{analysis}\n\n生成标题"
        ),
        output_key="title"
    )
    
    # 3. 大纲创建
    outline_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "标题：{title}\n核心：{analysis}\n\n生成3点大纲"
        ),
        output_key="outline"
    )
    
    # 4. 内容撰写
    content_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """标题：{title}
大纲：{outline}

写一段150字的内容"""
        ),
        output_key="content"
    )
    
    # 5. 质量检查
    review_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """标题：{title}
内容：{content}

评价这篇文章的质量（优秀/良好/一般）"""
        ),
        output_key="quality_review"
    )
    
    # 组合完整流程
    full_pipeline = SequentialChain(
        chains=[
            analysis_chain,
            title_chain,
            outline_chain,
            content_chain,
            review_chain
        ],
        input_variables=["topic"],
        output_variables=[
            "analysis", "title", "outline", 
            "content", "quality_review"
        ],
        verbose=True
    )
    
    # 执行
    result = full_pipeline.invoke({"topic": "远程工作的优势"})
    
    print("\n完整输出：")
    print(f"1. 分析：{result['analysis']}")
    print(f"2. 标题：{result['title']}")
    print(f"3. 大纲：{result['outline']}")
    print(f"4. 内容：{result['content'][:100]}...")
    print(f"5. 质量：{result['quality_review']}")


def demo_5_data_processing_pipeline():
    """示例5：数据处理流水线"""
    print("\n" + "="*60)
    print("示例5：数据处理ETL流程")
    print("="*60)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # 模拟数据处理链
    
    # 1. 数据清洗
    clean_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "清理这段文本，去除无关信息：{raw_data}"
        ),
        output_key="cleaned_data"
    )
    
    # 2. 信息提取
    extract_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "从这段文本中提取关键信息：{cleaned_data}"
        ),
        output_key="extracted_info"
    )
    
    # 3. 数据分析
    analyze_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "分析这些信息的趋势：{extracted_info}"
        ),
        output_key="analysis"
    )
    
    # 4. 生成报告
    report_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            """原始数据：{raw_data}
清洗后：{cleaned_data}
提取信息：{extracted_info}
分析结果：{analysis}

生成简洁的分析报告（50字）"""
        ),
        output_key="report"
    )
    
    # 组合ETL流程
    etl_pipeline = SequentialChain(
        chains=[clean_chain, extract_chain, analyze_chain, report_chain],
        input_variables=["raw_data"],
        output_variables=["cleaned_data", "extracted_info", "analysis", "report"],
        verbose=True
    )
    
    # 执行
    raw_text = """
    用户反馈：这个产品非常好用！推荐给朋友。
    另一条：界面有点复杂，希望简化。
    还有：性价比高，值得购买！
    """
    
    result = etl_pipeline.invoke({"raw_data": raw_text})
    
    print("\nETL结果：")
    print(f"清洗：{result['cleaned_data']}")
    print(f"提取：{result['extracted_info']}")
    print(f"分析：{result['analysis']}")
    print(f"报告：{result['report']}")


def main():
    """主函数"""
    print("🎯 SequentialChain完整演示")
    print("="*60)
    
    demo_1_simple_sequential()
    demo_2_full_sequential()
    demo_3_multi_input()
    demo_4_content_creation_pipeline()
    demo_5_data_processing_pipeline()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 核心要点：")
    print("1. SimpleSequentialChain适合简单流程")
    print("2. SequentialChain支持多输入输出")
    print("3. 可以保留所有中间结果")
    print("4. 变量名需要正确映射")
    print("5. verbose=True方便调试")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 最佳实践

### 设计Sequential Chain的原则

```
1. 单一职责
   每个Chain只做一件事

2. 清晰的输入输出
   明确每个Chain需要什么，产生什么

3. 合理的粒度
   不要太细（太多步骤）
   不要太粗（步骤太复杂）

4. 错误处理
   关键步骤要有fallback

5. 可测试性
   每个Chain可以单独测试
```

### 调试技巧

```python
# 1. 启用verbose
sequential = SequentialChain(
    chains=[...],
    verbose=True  # 显示每步执行
)

# 2. 单独测试每个Chain
chain1.invoke(test_input)
chain2.invoke(chain1_output)

# 3. 检查中间结果
result = sequential.invoke(input_data)
print(result["intermediate_key"])

# 4. 使用logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解SequentialChain的工作原理
- [ ] 使用SimpleSequentialChain构建简单流程
- [ ] 使用SequentialChain处理复杂场景
- [ ] 正确配置变量映射
- [ ] 调试和优化Sequential工作流

---

## 📝 下一课预告

**第31课：RouterChain - 动态路由与智能分发**

下一课我们将学习：
- RouterChain的设计模式
- 基于内容的智能路由
- 多条件路由
- 路由策略优化

**让AI自动选择最佳处理路径！**

---

**🎉 恭喜你完成第30课！**

你现在能构建复杂的多步骤AI工作流了！

**进度：30/165课（18.2%完成）** 🚀
