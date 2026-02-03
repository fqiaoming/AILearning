![RAG评估体系](./images/evaluation.svg)
*图：RAG评估体系*

# 第66课：RAG评估指标体系

> **本课目标**：掌握RAG系统评估的完整指标体系
> 
> **核心技能**：检索评估、生成评估、端到端评估
> 
> **实战案例**：构建RAG评估系统
> 
> **学习时长**：75分钟

---

## 📖 口播文案（5分钟）
![Generation Eval](./images/generation_eval.svg)
*图：Generation Eval*


### 🎯 前言

"做了这么多RAG系统优化，你有没有想过一个问题：

**怎么知道系统到底好不好？**

我在做企业级RAG项目时，最常被问到的问题就是：

老板：'你这个系统效果怎么样？'

我：'效果很好啊！'

老板：'有多好？能不能量化？'

我：'呃...用户反馈不错...'

老板：'不够，我要看数据！'

**这就是问题所在：没有评估体系！**

很多同学做RAG项目时也是这样：
- ❌ 凭感觉判断效果
- ❌ 看几个case就觉得好了
- ❌ 没有系统的评估方法
- ❌ 无法量化优化效果

**为什么评估这么重要？**

举个真实例子：

我优化了一个RAG系统的检索算法，自我感觉良好。

但是！当我用评估系统测试后发现：

```
优化前：
  • 检索准确率：75%
  • 答案准确率：68%
  • 平均响应时间：3.2秒
  • 用户满意度：72%

优化后：
  • 检索准确率：85% ↑ 13%  ✅
  • 答案准确率：65% ↓ 4%   ❌
  • 平均响应时间：4.5秒 ↑ 40%  ❌
  • 用户满意度：68% ↓ 5%   ❌
```

**我的优化反而让整体效果变差了！**

如果没有评估系统，我还以为自己做得很好呢！

**没有评估就没有优化！**

**RAG评估的三个维度：**

```
1. 检索质量 (Retrieval Quality)
   → 检索到的文档相关吗？

2. 生成质量 (Generation Quality)
   → 生成的答案准确吗？

3. 端到端质量 (End-to-End Quality)
   → 整体用户体验好吗？
```

**每个维度都有不同的指标：**

**检索质量指标：**
- Precision@K: 检索到的K个文档中有多少是相关的
- Recall@K: 所有相关文档中检索到了多少
- MRR: 第一个相关文档的排名
- NDCG: 考虑排名的综合指标

**生成质量指标：**
- Faithfulness: 答案是否忠于上下文
- Answer Relevancy: 答案是否回答了问题
- Correctness: 答案是否正确
- Completeness: 答案是否完整

**端到端指标：**
- Response Time: 响应时间
- Cost per Query: 每次查询成本
- User Satisfaction: 用户满意度
- Success Rate: 成功率

**但是！评估也有挑战：**

**挑战1：如何获取Ground Truth？**
- 需要人工标注
- 成本高、耗时长
- 标注质量参差不齐

**挑战2：如何自动化评估？**
- 人工评估不可扩展
- LLM评估可能有偏差
- 需要平衡准确性和效率

**挑战3：如何综合多个指标？**
- 不同指标可能冲突
- 需要权衡取舍
- 难以用单一数字衡量

**今天这一课，我要教你：**

**第一部分：评估指标详解**
- 检索指标
- 生成指标
- 端到端指标

**第二部分：评估数据准备**
- Ground Truth构建
- 测试集设计
- 标注规范

**第三部分：自动化评估**
- 基于规则的评估
- 基于模型的评估
- LLM作为评估器

**第四部分：评估系统实现**
- 评估框架
- 指标计算
- 结果分析

**第五部分：最佳实践**
- 评估策略
- 持续监控
- 优化闭环

学完这一课，你将建立完整的RAG评估体系！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【评估的重要性】

没有评估：
  • 不知道系统好坏
  • 无法量化优化效果
  • 难以做技术决策

有评估：
  • 清楚知道哪里好哪里差
  • 优化有的放矢
  • 数据驱动决策

【评估的三个层次】

Level 1: 组件评估
  单独评估检索、生成等组件

Level 2: 集成评估
  评估组件之间的配合

Level 3: 系统评估
  评估整体用户体验
```

---

## 📚 第一部分：评估指标详解

### 一、检索质量指标

```python
from typing import List, Set, Dict
import numpy as np

class RetrievalMetrics:
    """检索质量指标"""
    
    @staticmethod
    def precision_at_k(
        retrieved: List[str],
        relevant: Set[str],
        k: int
    ) -> float:
        """
        Precision@K
        
        定义：检索到的前K个文档中，相关文档的比例
        
        公式：P@K = (检索到的相关文档数) / K
        
        例子：
        检索到: [doc1, doc2, doc3, doc4, doc5]
        相关的: {doc1, doc3, doc5, doc7}
        P@3 = 2/3 = 0.67 (doc1, doc3是相关的)
        """
        retrieved_k = retrieved[:k]
        relevant_retrieved = sum(1 for doc in retrieved_k if doc in relevant)
        return relevant_retrieved / k if k > 0 else 0
    
    @staticmethod
    def recall_at_k(
        retrieved: List[str],
        relevant: Set[str],
        k: int
    ) -> float:
        """
        Recall@K
        
        定义：所有相关文档中，检索到前K个的比例
        
        公式：R@K = (检索到的相关文档数) / (总相关文档数)
        
        例子：
        检索到: [doc1, doc2, doc3]
        相关的: {doc1, doc3, doc5, doc7}
        R@3 = 2/4 = 0.5 (找到了4个相关文档中的2个)
        """
        retrieved_k = set(retrieved[:k])
        relevant_retrieved = retrieved_k & relevant
        return len(relevant_retrieved) / len(relevant) if relevant else 0
    
    @staticmethod
    def f1_at_k(
        retrieved: List[str],
        relevant: Set[str],
        k: int
    ) -> float:
        """
        F1@K
        
        定义：Precision和Recall的调和平均
        
        公式：F1 = 2 * (P * R) / (P + R)
        """
        p = RetrievalMetrics.precision_at_k(retrieved, relevant, k)
        r = RetrievalMetrics.recall_at_k(retrieved, relevant, k)
        
        if p + r == 0:
            return 0
        
        return 2 * (p * r) / (p + r)
    
    @staticmethod
    def mrr(retrieved: List[str], relevant: Set[str]) -> float:
        """
        MRR (Mean Reciprocal Rank)
        
        定义：第一个相关文档的排名倒数
        
        公式：MRR = 1 / (第一个相关文档的排名)
        
        例子：
        检索到: [doc1, doc2, doc3, doc4]
        相关的: {doc3, doc5}
        第一个相关文档doc3在第3位
        MRR = 1/3 = 0.333
        
        直观理解：MRR越高，说明相关文档排名越靠前
        """
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1.0 / (i + 1)
        return 0.0
    
    @staticmethod
    def ndcg_at_k(
        retrieved: List[str],
        relevance_scores: Dict[str, float],
        k: int
    ) -> float:
        """
        NDCG@K (Normalized Discounted Cumulative Gain)
        
        定义：考虑排名位置和相关性程度的综合指标
        
        优点：
        1. 考虑了文档的相关性程度（不只是0/1）
        2. 考虑了排名位置（越靠前权重越大）
        
        公式：
        DCG@K = Σ (rel_i / log2(i+1))
        NDCG@K = DCG@K / IDCG@K
        
        其中IDCG是理想情况下的DCG（按相关性排序）
        """
        # DCG (Discounted Cumulative Gain)
        dcg = 0
        for i, doc in enumerate(retrieved[:k]):
            rel = relevance_scores.get(doc, 0)
            dcg += rel / np.log2(i + 2)  # i+2 because log2(1)=0
        
        # IDCG (Ideal DCG)
        sorted_scores = sorted(relevance_scores.values(), reverse=True)
        idcg = 0
        for i, rel in enumerate(sorted_scores[:k]):
            idcg += rel / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0

# 演示
def demo_retrieval_metrics():
    """演示检索指标"""
    
    # 检索结果
    retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    
    # 相关文档（Ground Truth）
    relevant = {"doc1", "doc3", "doc5", "doc7", "doc9"}
    
    # 相关性分数（用于NDCG）
    relevance_scores = {
        "doc1": 3,  # 高度相关
        "doc2": 0,  # 不相关
        "doc3": 2,  # 中度相关
        "doc4": 0,
        "doc5": 3,
        "doc7": 2,
        "doc9": 1
    }
    
    print("="*60)
    print("检索质量指标演示")
    print("="*60)
    
    print(f"\n检索结果: {retrieved}")
    print(f"相关文档(真实): {relevant}")
    
    k = 5
    
    print(f"\n【Precision@{k}】")
    p = RetrievalMetrics.precision_at_k(retrieved, relevant, k)
    print(f"  值: {p:.3f}")
    print(f"  含义: 检索到的{k}个文档中，{p*100:.0f}%是相关的")
    
    print(f"\n【Recall@{k}】")
    r = RetrievalMetrics.recall_at_k(retrieved, relevant, k)
    print(f"  值: {r:.3f}")
    print(f"  含义: {len(relevant)}个相关文档中，找到了{r*100:.0f}%")
    
    print(f"\n【F1@{k}】")
    f1 = RetrievalMetrics.f1_at_k(retrieved, relevant, k)
    print(f"  值: {f1:.3f}")
    print(f"  含义: Precision和Recall的平衡指标")
    
    print(f"\n【MRR】")
    mrr = RetrievalMetrics.mrr(retrieved, relevant)
    print(f"  值: {mrr:.3f}")
    print(f"  含义: 第一个相关文档doc1在第{int(1/mrr)}位")
    
    print(f"\n【NDCG@{k}】")
    ndcg = RetrievalMetrics.ndcg_at_k(retrieved, relevance_scores, k)
    print(f"  值: {ndcg:.3f}")
    print(f"  含义: 考虑排名和相关性程度的综合得分")
    
    print("\n【指标对比】")
    print(f"  Precision@{k}: {p:.3f} - 准确性")
    print(f"  Recall@{k}: {r:.3f} - 召回率")
    print(f"  F1@{k}: {f1:.3f} - 综合")
    print(f"  MRR: {mrr:.3f} - 排序质量")
    print(f"  NDCG@{k}: {ndcg:.3f} - 最全面")

demo_retrieval_metrics()
```

### 二、生成质量指标

```python
class GenerationMetrics:
    """生成质量指标"""
    
    @staticmethod
    def faithfulness(
        answer: str,
        context: str,
        llm
    ) -> float:
        """
        Faithfulness (忠实度)
        
        定义：答案是否忠于上下文，没有幻觉
        
        评估方法：
        1. 提取答案中的陈述(statements)
        2. 检查每个陈述是否能从上下文推导
        3. 计算被支持的陈述比例
        """
        prompt = f"""请判断以下答案是否忠实于上下文。

上下文：
{context}

答案：
{answer}

任务：
1. 提取答案中的关键陈述
2. 对每个陈述，判断是否能从上下文推导出
3. 计算忠实度分数(0-1)

以JSON格式返回：
{{
    "statements": ["陈述1", "陈述2", ...],
    "supported": [true, false, ...],
    "score": 0.8
}}

JSON结果："""
        
        response = llm.invoke(prompt)
        
        try:
            import json
            result = json.loads(response.content)
            return result.get('score', 0.5)
        except:
            return 0.5
    
    @staticmethod
    def answer_relevancy(
        question: str,
        answer: str,
        llm
    ) -> float:
        """
        Answer Relevancy (答案相关性)
        
        定义：答案是否直接回答了问题
        
        评估方法：使用LLM判断答案对问题的相关程度
        """
        prompt = f"""请评估答案对问题的相关性。

问题：{question}

答案：{answer}

请给出0-1之间的相关性分数：
- 1.0: 完美回答了问题
- 0.7-0.9: 大部分回答了问题
- 0.4-0.6: 部分回答了问题
- 0.1-0.3: 几乎没回答问题
- 0.0: 完全不相关

只返回一个数字："""
        
        response = llm.invoke(prompt)
        
        try:
            score = float(response.content.strip())
            return max(0, min(1, score))
        except:
            return 0.5
    
    @staticmethod
    def correctness(
        answer: str,
        ground_truth: str,
        llm
    ) -> float:
        """
        Correctness (正确性)
        
        定义：答案与标准答案的匹配程度
        
        评估方法：对比生成答案和标准答案
        """
        prompt = f"""请评估生成答案的正确性。

标准答案：
{ground_truth}

生成答案：
{answer}

请给出0-1之间的正确性分数：
- 1.0: 完全正确
- 0.7-0.9: 大部分正确
- 0.4-0.6: 部分正确
- 0.1-0.3: 大部分错误
- 0.0: 完全错误

只返回一个数字："""
        
        response = llm.invoke(prompt)
        
        try:
            score = float(response.content.strip())
            return max(0, min(1, score))
        except:
            return 0.5

# 演示
def demo_generation_metrics():
    """演示生成质量指标"""
    
    from langchain.chat_models import ChatOpenAI
    
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    # 测试数据
    context = """
    Python是一种高级编程语言。它由Guido van Rossum于1991年首次发布。
    Python语法简洁清晰，非常适合初学者。
    Python在数据科学、机器学习、Web开发等领域应用广泛。
    """
    
    question = "Python是什么时候发布的？"
    
    answer_good = "Python由Guido van Rossum于1991年首次发布。"
    answer_bad = "Python是一种很流行的编程语言，现在很多公司都在使用。"
    
    ground_truth = "Python于1991年首次发布。"
    
    print("="*60)
    print("生成质量指标演示")
    print("="*60)
    
    print(f"\n问题: {question}")
    print(f"上下文: {context[:50]}...")
    print(f"标准答案: {ground_truth}")
    
    print("\n【好答案评估】")
    print(f"答案: {answer_good}")
    
    faith_good = GenerationMetrics.faithfulness(answer_good, context, llm)
    rel_good = GenerationMetrics.answer_relevancy(question, answer_good, llm)
    corr_good = GenerationMetrics.correctness(answer_good, ground_truth, llm)
    
    print(f"  Faithfulness: {faith_good:.2f}")
    print(f"  Relevancy: {rel_good:.2f}")
    print(f"  Correctness: {corr_good:.2f}")
    
    print("\n【差答案评估】")
    print(f"答案: {answer_bad}")
    
    faith_bad = GenerationMetrics.faithfulness(answer_bad, context, llm)
    rel_bad = GenerationMetrics.answer_relevancy(question, answer_bad, llm)
    corr_bad = GenerationMetrics.correctness(answer_bad, ground_truth, llm)
    
    print(f"  Faithfulness: {faith_bad:.2f}")
    print(f"  Relevancy: {rel_bad:.2f}")
    print(f"  Correctness: {corr_bad:.2f}")

# demo_generation_metrics()
```

---

## 💻 第二部分：评估数据准备

### Ground Truth构建

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class RAGTestCase:
    """RAG测试用例"""
    query: str                          # 查询
    relevant_docs: Set[str]             # 相关文档ID
    ground_truth_answer: str            # 标准答案
    context: str                        # 应该检索到的上下文
    metadata: Dict = None               # 其他元数据

class GroundTruthBuilder:
    """Ground Truth构建器"""
    
    def __init__(self):
        self.test_cases: List[RAGTestCase] = []
    
    def add_test_case(
        self,
        query: str,
        relevant_docs: Set[str],
        ground_truth_answer: str,
        context: str,
        metadata: Dict = None
    ):
        """添加测试用例"""
        case = RAGTestCase(
            query=query,
            relevant_docs=relevant_docs,
            ground_truth_answer=ground_truth_answer,
            context=context,
            metadata=metadata or {}
        )
        self.test_cases.append(case)
    
    def save(self, filepath: str):
        """保存到文件"""
        import json
        
        data = [
            {
                'query': case.query,
                'relevant_docs': list(case.relevant_docs),
                'ground_truth_answer': case.ground_truth_answer,
                'context': case.context,
                'metadata': case.metadata
            }
            for case in self.test_cases
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self, filepath: str):
        """从文件加载"""
        import json
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.test_cases = [
            RAGTestCase(
                query=item['query'],
                relevant_docs=set(item['relevant_docs']),
                ground_truth_answer=item['ground_truth_answer'],
                context=item['context'],
                metadata=item.get('metadata', {})
            )
            for item in data
        ]

# 示例
def demo_ground_truth():
    """演示Ground Truth构建"""
    
    builder = GroundTruthBuilder()
    
    # 添加测试用例
    builder.add_test_case(
        query="Python是什么时候发布的？",
        relevant_docs={"doc1", "doc3"},
        ground_truth_answer="Python由Guido van Rossum于1991年首次发布。",
        context="Python是一种高级编程语言。它由Guido van Rossum于1991年首次发布。",
        metadata={"difficulty": "easy", "category": "fact"}
    )
    
    builder.add_test_case(
        query="如何在Python中处理异常？",
        relevant_docs={"doc5", "doc7", "doc9"},
        ground_truth_answer="使用try-except语句处理异常...",
        context="Python使用try-except语句处理异常...",
        metadata={"difficulty": "medium", "category": "how-to"}
    )
    
    print("="*60)
    print("Ground Truth构建")
    print("="*60)
    print(f"\n测试用例数: {len(builder.test_cases)}")
    
    for i, case in enumerate(builder.test_cases):
        print(f"\n用例{i+1}:")
        print(f"  查询: {case.query}")
        print(f"  相关文档: {case.relevant_docs}")
        print(f"  标准答案: {case.ground_truth_answer[:50]}...")
        print(f"  元数据: {case.metadata}")
    
    # 保存
    # builder.save("test_cases.json")

demo_ground_truth()
```

---

## 📝 课后练习

### 练习1：实现MAP指标
实现Mean Average Precision指标

### 练习2：自动化标注
使用LLM辅助生成Ground Truth

### 练习3：评估报告
生成可视化的评估报告

---

## 🎓 知识总结

### 核心要点

1. **评估的重要性**
   - 没有评估就没有优化
   - 数据驱动决策
   - 持续改进

2. **三大评估维度**
   - 检索质量
   - 生成质量
   - 端到端质量

3. **关键指标**
   - Precision/Recall/F1
   - MRR/NDCG
   - Faithfulness/Relevancy

4. **Ground Truth**
   - 高质量标注
   - 覆盖多种场景
   - 持续更新

---

## 🚀 下节预告

下一课：**第67课：检索质量评估**

- 离线评估方法
- 在线评估方法
- 检索质量优化

**深入检索评估！** 📊

---

**💪 记住：评估是优化的前提！**

**下一课见！** 🎉
