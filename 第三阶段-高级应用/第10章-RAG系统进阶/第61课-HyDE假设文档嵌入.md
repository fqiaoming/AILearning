![RAG高级检索流程](./images/rag_flow.svg)
*图：RAG高级检索流程*

# 第61课：HyDE假设文档嵌入

> **本课目标**：掌握HyDE技术，通过假设文档提升检索效果
> 
> **核心技能**：HyDE原理、假设文档生成、检索优化
> 
> **实战案例**：实现HyDE增强的RAG系统
> 
> **学习时长**：75分钟

---

## 📖 口播文案（5分钟）
![Hyde](./images/hyde.svg)
*图：Hyde*


### 🎯 前言

"我在做RAG项目时遇到过一个很头疼的问题：

**用户的问题和知识库的表述方式差距太大！**

举个例子：

用户问：'我的电脑开不了机怎么办？'

知识库里的文档是：
- '计算机启动故障排查流程'
- '主板电源模块故障诊断'
- '系统引导失败解决方案'

你看，用户说的是大白话'开不了机'，知识库用的是专业术语'启动故障'、'引导失败'。

结果？**向量检索效果很差！**

因为：
- '开不了机' 和 '启动故障' 的向量距离比较远
- 即使用了Query改写，效果也不够好

我试过很多方法：
- ❌ 同义词扩展：覆盖不全
- ❌ Query改写：不够准确
- ❌ 多Query检索：计算成本高

直到我发现了**HyDE（Hypothetical Document Embeddings）**！

**HyDE的核心思想超级巧妙：**

不是直接用问题去检索，而是：

1. **先让LLM生成一个假设的答案**
   - 问题：'我的电脑开不了机怎么办？'
   - 假设答案：'电脑无法启动可能是电源故障、主板问题或系统引导错误...'

2. **用假设答案的向量去检索**
   - 假设答案用的是专业术语
   - 和知识库的表述更接近
   - 向量相似度更高！

3. **检索效果大幅提升**
   - 召回率提升20-30%
   - 准确率也显著提高

**为什么HyDE这么有效？**

传统检索：
```
用户问题(口语) → 向量化 → 检索知识库(书面语)
           ↑
      表述差异大，效果差
```

HyDE检索：
```
用户问题 → LLM生成假设答案(书面语) → 向量化 → 检索知识库(书面语)
                    ↑
              表述方式一致，效果好！
```

**但是，HyDE也有坑！**

我在实际使用中发现：

**坑1：假设答案可能错误**
- LLM生成的答案不一定对
- 但没关系！我们只用它来检索，不直接给用户

**坑2：增加了延迟**
- 多了一次LLM调用
- 需要优化性能

**坑3：不是所有场景都适用**
- 简单的事实性问题：效果提升不大
- 复杂的推理问题：效果提升明显

**今天这一课，我要教你：**

**第一部分：HyDE原理深度剖析**
- 为什么HyDE有效？
- HyDE vs 传统检索
- 适用场景分析

**第二部分：HyDE实现**
- 假设文档生成策略
- 多假设文档技术
- 向量融合方法

**第三部分：性能优化**
- 缓存假设文档
- 异步生成
- 批量处理

**第四部分：效果评估**
- 对比实验
- 指标分析
- 场景选择

**第五部分：生产级实现**
- 完整的HyDE系统
- 自适应策略
- 降级方案

学完这一课，你的RAG系统检索效果将提升一个档次！

准备好了吗？让我们开始！"

---

### 💡 核心概念

```
【传统检索 vs HyDE检索】

传统检索：
Query → Embedding → 检索
问题：Query和Document表述方式不一致

HyDE检索：
Query → LLM生成假设文档 → Embedding → 检索
优势：假设文档和真实文档表述方式一致

【HyDE的核心洞察】

"答案和答案之间的相似度，
 远高于问题和答案之间的相似度"

例子：
- "如何学习Python" vs "Python学习指南" (问答)
  → 相似度：0.75

- "Python学习指南" vs "Python入门教程" (答答)
  → 相似度：0.90 ✨
```

---

## 📚 第一部分：HyDE原理

### 一、为什么HyDE有效？

```python
# 演示HyDE的核心优势
from sentence_transformers import SentenceTransformer
import numpy as np

def demonstrate_hyde_advantage():
    """演示HyDE的优势"""
    
    model = SentenceTransformer('moka-ai/m3e-base')
    
    # 场景：用户问题 vs 知识库文档
    query = "电脑开不了机怎么办"
    
    documents = [
        "计算机启动故障排查流程：首先检查电源连接...",
        "主板电源模块故障诊断方法详解...",
        "系统引导失败的常见原因及解决方案..."
    ]
    
    # LLM生成的假设答案
    hypothetical_answer = """
    计算机无法启动的问题可能由多种原因导致：
    1. 电源故障：检查电源连接和电源适配器
    2. 主板问题：可能是主板电源模块损坏
    3. 系统引导失败：检查硬盘和系统文件
    解决方案包括排查电源、检测主板、修复系统引导等。
    """
    
    print("="*60)
    print("HyDE优势演示")
    print("="*60)
    
    # 1. 传统检索：直接用Query
    print("\n【传统检索】Query → Documents")
    query_emb = model.encode([query])[0]
    doc_embs = model.encode(documents)
    
    traditional_scores = []
    for i, doc_emb in enumerate(doc_embs):
        score = np.dot(query_emb, doc_emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
        )
        traditional_scores.append(score)
        print(f"文档{i+1}: {score:.4f}")
    
    # 2. HyDE检索：用假设答案
    print("\n【HyDE检索】Hypothetical Answer → Documents")
    hyp_emb = model.encode([hypothetical_answer])[0]
    
    hyde_scores = []
    for i, doc_emb in enumerate(doc_embs):
        score = np.dot(hyp_emb, doc_emb) / (
            np.linalg.norm(hyp_emb) * np.linalg.norm(doc_emb)
        )
        hyde_scores.append(score)
        print(f"文档{i+1}: {score:.4f}")
    
    # 3. 对比
    print("\n【对比分析】")
    for i in range(len(documents)):
        improvement = (hyde_scores[i] - traditional_scores[i]) / traditional_scores[i] * 100
        print(f"文档{i+1}: 提升 {improvement:+.1f}%")
    
    avg_improvement = (np.mean(hyde_scores) - np.mean(traditional_scores)) / np.mean(traditional_scores) * 100
    print(f"\n平均提升: {avg_improvement:+.1f}%")

demonstrate_hyde_advantage()
```

### 二、HyDE的工作流程

```python
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class HyDEConfig:
    """HyDE配置"""
    num_hypothetical_docs: int = 1  # 生成假设文档数量
    use_query_in_retrieval: bool = False  # 是否同时使用原始Query
    hypothetical_doc_weight: float = 1.0  # 假设文档权重
    query_weight: float = 0.3  # 原始Query权重

class HyDERetriever:
    """HyDE检索器"""
    
    def __init__(
        self,
        llm,
        embedding_model,
        vectorstore,
        config: HyDEConfig = None
    ):
        self.llm = llm
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
        self.config = config or HyDEConfig()
    
    def generate_hypothetical_document(self, query: str) -> str:
        """生成假设文档"""
        prompt = f"""请针对以下问题，生成一个假设的答案。

要求：
1. 答案要专业、详细
2. 使用准确的术语
3. 结构清晰
4. 不需要绝对正确，但要合理

问题：{query}

假设答案："""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def retrieve(
        self,
        query: str,
        k: int = 5,
        verbose: bool = False
    ) -> List[Tuple[str, float]]:
        """
        HyDE检索
        
        流程：
        1. 生成假设文档
        2. 向量化假设文档
        3. 用假设文档检索
        4. (可选) 融合原始Query检索结果
        """
        if verbose:
            print("="*60)
            print("🔍 HyDE检索")
            print("="*60)
            print(f"原始Query: {query}\n")
        
        # 1. 生成假设文档
        if verbose:
            print("【步骤1】生成假设文档")
        
        hypothetical_docs = []
        for i in range(self.config.num_hypothetical_docs):
            hyp_doc = self.generate_hypothetical_document(query)
            hypothetical_docs.append(hyp_doc)
            
            if verbose:
                print(f"\n假设文档{i+1}:")
                print(f"{hyp_doc[:200]}...")
        
        # 2. 向量化
        if verbose:
            print("\n【步骤2】向量化")
        
        # 假设文档的向量
        hyp_embeddings = self.embedding_model.encode(hypothetical_docs)
        
        # 如果需要，也计算Query的向量
        if self.config.use_query_in_retrieval:
            query_embedding = self.embedding_model.encode([query])[0]
        
        # 3. 检索
        if verbose:
            print("\n【步骤3】检索")
        
        # 用假设文档检索
        results_from_hyp = []
        for i, hyp_emb in enumerate(hyp_embeddings):
            results = self.vectorstore.similarity_search_by_vector(
                hyp_emb,
                k=k
            )
            results_from_hyp.append(results)
        
        # 4. 融合结果
        if self.config.use_query_in_retrieval:
            # 也用原始Query检索
            results_from_query = self.vectorstore.similarity_search_by_vector(
                query_embedding,
                k=k
            )
            
            # 融合
            final_results = self._merge_results(
                results_from_hyp,
                results_from_query
            )
        else:
            # 只用假设文档的结果
            final_results = self._merge_hypothetical_results(results_from_hyp)
        
        if verbose:
            print(f"\n【步骤4】返回Top-{len(final_results)}结果")
            for i, (doc, score) in enumerate(final_results[:3]):
                print(f"\n{i+1}. 分数={score:.4f}")
                print(f"   {doc[:100]}...")
        
        return final_results
    
    def _merge_hypothetical_results(
        self,
        results_list: List[List[Tuple]]
    ) -> List[Tuple[str, float]]:
        """融合多个假设文档的检索结果"""
        from collections import defaultdict
        
        # 聚合分数
        doc_scores = defaultdict(list)
        doc_content = {}
        
        for results in results_list:
            for doc, score in results:
                doc_content[doc] = doc
                doc_scores[doc].append(score)
        
        # 计算平均分数
        merged = []
        for doc, scores in doc_scores.items():
            avg_score = np.mean(scores)
            merged.append((doc, avg_score))
        
        # 排序
        merged.sort(key=lambda x: x[1], reverse=True)
        
        return merged
    
    def _merge_results(
        self,
        hyp_results: List[List[Tuple]],
        query_results: List[Tuple]
    ) -> List[Tuple[str, float]]:
        """融合假设文档和原始Query的结果"""
        from collections import defaultdict
        
        doc_scores = defaultdict(float)
        
        # 假设文档的结果
        for results in hyp_results:
            for doc, score in results:
                doc_scores[doc] += score * self.config.hypothetical_doc_weight
        
        # 原始Query的结果
        for doc, score in query_results:
            doc_scores[doc] += score * self.config.query_weight
        
        # 排序
        merged = [(doc, score) for doc, score in doc_scores.items()]
        merged.sort(key=lambda x: x[1], reverse=True)
        
        return merged
```

---

## 💻 第二部分：HyDE实现技巧

### 一、多假设文档生成

```python
class MultiHyDEGenerator:
    """多假设文档生成器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def generate_diverse_hypotheticals(
        self,
        query: str,
        num_docs: int = 3,
        strategies: List[str] = None
    ) -> List[str]:
        """
        生成多个假设文档
        
        策略：
        1. 不同角度
        2. 不同深度
        3. 不同风格
        """
        if strategies is None:
            strategies = ['detailed', 'concise', 'technical']
        
        hypotheticals = []
        
        for strategy in strategies[:num_docs]:
            hyp = self._generate_with_strategy(query, strategy)
            hypotheticals.append(hyp)
        
        return hypotheticals
    
    def _generate_with_strategy(
        self,
        query: str,
        strategy: str
    ) -> str:
        """根据策略生成假设文档"""
        
        strategy_prompts = {
            'detailed': """请生成一个详细的、专业的假设答案。
            
问题：{query}

要求：
- 详细阐述
- 包含具体步骤
- 使用专业术语

假设答案：""",
            
            'concise': """请生成一个简洁的、要点式的假设答案。

问题：{query}

要求：
- 简洁明了
- 突出关键点
- 使用准确术语

假设答案：""",
            
            'technical': """请从技术角度生成一个假设答案。

问题：{query}

要求：
- 技术性强
- 包含专业概念
- 结构化表述

假设答案："""
        }
        
        prompt = strategy_prompts[strategy].format(query=query)
        response = self.llm.invoke(prompt)
        
        return response.content

# 使用示例
def demo_multi_hypotheticals():
    """演示多假设文档"""
    from langchain.chat_models import ChatOpenAI
    
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0.7  # 增加多样性
    )
    
    generator = MultiHyDEGenerator(llm)
    
    query = "如何优化Python程序的性能？"
    
    print("="*60)
    print("多假设文档生成")
    print("="*60)
    print(f"问题: {query}\n")
    
    hypotheticals = generator.generate_diverse_hypotheticals(
        query,
        num_docs=3
    )
    
    for i, hyp in enumerate(hypotheticals):
        print(f"\n【假设文档{i+1}】")
        print(hyp)
        print("-"*60)

demo_multi_hypotheticals()
```

### 二、向量融合策略

```python
class VectorFusion:
    """向量融合策略"""
    
    @staticmethod
    def average_fusion(vectors: List[np.ndarray]) -> np.ndarray:
        """平均融合"""
        return np.mean(vectors, axis=0)
    
    @staticmethod
    def weighted_fusion(
        vectors: List[np.ndarray],
        weights: List[float]
    ) -> np.ndarray:
        """加权融合"""
        weighted = [v * w for v, w in zip(vectors, weights)]
        return np.sum(weighted, axis=0)
    
    @staticmethod
    def max_fusion(vectors: List[np.ndarray]) -> np.ndarray:
        """最大值融合（每个维度取最大）"""
        return np.max(vectors, axis=0)

class ImprovedHyDERetriever:
    """改进的HyDE检索器（支持向量融合）"""
    
    def __init__(
        self,
        llm,
        embedding_model,
        vectorstore,
        fusion_strategy: str = 'average'
    ):
        self.llm = llm
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
        self.fusion_strategy = fusion_strategy
    
    def retrieve_with_fusion(
        self,
        query: str,
        num_hypotheticals: int = 3,
        k: int = 5
    ) -> List[Tuple[str, float]]:
        """使用向量融合的HyDE检索"""
        
        # 1. 生成多个假设文档
        generator = MultiHyDEGenerator(self.llm)
        hypotheticals = generator.generate_diverse_hypotheticals(
            query,
            num_docs=num_hypotheticals
        )
        
        # 2. 向量化
        hyp_vectors = self.embedding_model.encode(hypotheticals)
        
        # 3. 融合向量
        if self.fusion_strategy == 'average':
            fused_vector = VectorFusion.average_fusion(hyp_vectors)
        elif self.fusion_strategy == 'max':
            fused_vector = VectorFusion.max_fusion(hyp_vectors)
        else:
            fused_vector = hyp_vectors[0]
        
        # 4. 用融合后的向量检索
        results = self.vectorstore.similarity_search_by_vector(
            fused_vector,
            k=k
        )
        
        return results
```

---

## ⚡ 第三部分：性能优化

### 一、假设文档缓存

```python
import hashlib
from typing import Optional

class HyDECache:
    """HyDE缓存系统"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def _get_key(self, query: str) -> str:
        """生成缓存key"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def get(self, query: str) -> Optional[str]:
        """获取缓存的假设文档"""
        key = self._get_key(query)
        return self.cache.get(key)
    
    def set(self, query: str, hypothetical: str):
        """缓存假设文档"""
        key = self._get_key(query)
        
        # LRU淘汰
        if len(self.cache) >= self.max_size:
            # 删除最老的
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        
        self.cache[key] = hypothetical

class CachedHyDERetriever(HyDERetriever):
    """带缓存的HyDE检索器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = HyDECache()
    
    def generate_hypothetical_document(self, query: str) -> str:
        """生成假设文档（带缓存）"""
        # 检查缓存
        cached = self.cache.get(query)
        if cached:
            print("  📦 使用缓存的假设文档")
            return cached
        
        # 生成新的
        hypothetical = super().generate_hypothetical_document(query)
        
        # 保存到缓存
        self.cache.set(query, hypothetical)
        
        return hypothetical
```

### 二、异步HyDE

```python
import asyncio
from typing import List

class AsyncHyDERetriever:
    """异步HyDE检索器"""
    
    def __init__(self, llm, embedding_model, vectorstore):
        self.llm = llm
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
    
    async def generate_hypothetical_async(self, query: str) -> str:
        """异步生成假设文档"""
        # 使用asyncio运行同步LLM调用
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._generate_sync,
            query
        )
    
    def _generate_sync(self, query: str) -> str:
        """同步生成（内部使用）"""
        prompt = f"请生成假设答案：{query}"
        response = self.llm.invoke(prompt)
        return response.content
    
    async def retrieve_async(
        self,
        query: str,
        num_hypotheticals: int = 3,
        k: int = 5
    ) -> List[Tuple[str, float]]:
        """异步HyDE检索"""
        
        # 并行生成多个假设文档
        tasks = [
            self.generate_hypothetical_async(query)
            for _ in range(num_hypotheticals)
        ]
        hypotheticals = await asyncio.gather(*tasks)
        
        # 向量化
        hyp_vectors = self.embedding_model.encode(hypotheticals)
        
        # 融合和检索
        fused_vector = np.mean(hyp_vectors, axis=0)
        results = self.vectorstore.similarity_search_by_vector(
            fused_vector,
            k=k
        )
        
        return results

# 使用示例
async def demo_async_hyde():
    """演示异步HyDE"""
    # ... 初始化 ...
    
    retriever = AsyncHyDERetriever(llm, embedding_model, vectorstore)
    
    # 异步检索
    results = await retriever.retrieve_async(
        "如何优化数据库查询？",
        num_hypotheticals=3,
        k=5
    )
    
    return results
```

---

## 📊 第四部分：效果评估

### 一、对比实验

```python
class HyDEEvaluator:
    """HyDE效果评估器"""
    
    def __init__(
        self,
        traditional_retriever,
        hyde_retriever,
        test_queries: List[str],
        relevance_labels: dict
    ):
        self.traditional = traditional_retriever
        self.hyde = hyde_retriever
        self.test_queries = test_queries
        self.relevance_labels = relevance_labels
    
    def evaluate(self, k: int = 5):
        """评估对比"""
        print("="*60)
        print("HyDE效果评估")
        print("="*60)
        
        traditional_scores = []
        hyde_scores = []
        
        for query in self.test_queries:
            # 传统检索
            trad_results = self.traditional.retrieve(query, k=k)
            trad_score = self._calculate_ndcg(
                query,
                trad_results,
                k
            )
            traditional_scores.append(trad_score)
            
            # HyDE检索
            hyde_results = self.hyde.retrieve(query, k=k)
            hyde_score = self._calculate_ndcg(
                query,
                hyde_results,
                k
            )
            hyde_scores.append(hyde_score)
            
            print(f"\nQuery: {query}")
            print(f"  传统: NDCG@{k}={trad_score:.4f}")
            print(f"  HyDE: NDCG@{k}={hyde_score:.4f}")
            print(f"  提升: {(hyde_score-trad_score)/trad_score*100:+.1f}%")
        
        # 总结
        print("\n" + "="*60)
        print("总体评估")
        print("="*60)
        avg_trad = np.mean(traditional_scores)
        avg_hyde = np.mean(hyde_scores)
        
        print(f"平均NDCG@{k}:")
        print(f"  传统: {avg_trad:.4f}")
        print(f"  HyDE: {avg_hyde:.4f}")
        print(f"  平均提升: {(avg_hyde-avg_trad)/avg_trad*100:+.1f}%")
    
    def _calculate_ndcg(
        self,
        query: str,
        results: List[Tuple],
        k: int
    ) -> float:
        """计算NDCG"""
        # 获取相关性标注
        relevance = self.relevance_labels.get(query, {})
        
        # DCG
        dcg = 0
        for i, (doc, _) in enumerate(results[:k]):
            rel = relevance.get(doc, 0)
            dcg += rel / np.log2(i + 2)
        
        # IDCG
        ideal_rels = sorted(relevance.values(), reverse=True)
        idcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(ideal_rels[:k]))
        
        return dcg / idcg if idcg > 0 else 0
```

---

## 🎯 第五部分：生产级实现

### 完整的HyDE系统

```python
class ProductionHyDESystem:
    """生产级HyDE系统"""
    
    def __init__(
        self,
        llm,
        embedding_model,
        vectorstore,
        config: dict = None
    ):
        self.llm = llm
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
        
        # 配置
        self.config = config or {
            'enable_hyde': True,
            'num_hypotheticals': 1,
            'use_cache': True,
            'fallback_to_traditional': True,
            'hyde_timeout': 10
        }
        
        # 缓存
        if self.config['use_cache']:
            self.cache = HyDECache()
        
        # 指标
        self.metrics = {
            'total_queries': 0,
            'hyde_success': 0,
            'hyde_failure': 0,
            'cache_hits': 0
        }
    
    def retrieve(
        self,
        query: str,
        k: int = 5,
        force_hyde: bool = False
    ) -> List[Tuple[str, float]]:
        """
        智能检索（自适应HyDE）
        
        策略：
        1. 简单查询 → 传统检索
        2. 复杂查询 → HyDE检索
        3. HyDE失败 → 降级到传统检索
        """
        self.metrics['total_queries'] += 1
        
        # 判断是否使用HyDE
        use_hyde = force_hyde or self._should_use_hyde(query)
        
        if not use_hyde:
            # 传统检索
            return self._traditional_retrieve(query, k)
        
        # 尝试HyDE检索
        try:
            results = self._hyde_retrieve(query, k)
            self.metrics['hyde_success'] += 1
            return results
        except Exception as e:
            self.metrics['hyde_failure'] += 1
            
            if self.config['fallback_to_traditional']:
                # 降级到传统检索
                print(f"⚠️  HyDE失败，降级到传统检索: {e}")
                return self._traditional_retrieve(query, k)
            else:
                raise
    
    def _should_use_hyde(self, query: str) -> bool:
        """判断是否应该使用HyDE"""
        if not self.config['enable_hyde']:
            return False
        
        # 规则：
        # 1. 问句 → 使用HyDE
        # 2. 长查询 → 使用HyDE
        # 3. 关键词查询 → 不使用HyDE
        
        is_question = any(q in query for q in ['？', '?', '如何', '怎么', '什么'])
        is_long = len(query) > 20
        
        return is_question or is_long
    
    def _hyde_retrieve(
        self,
        query: str,
        k: int
    ) -> List[Tuple[str, float]]:
        """HyDE检索"""
        # 生成假设文档
        if self.config['use_cache']:
            cached = self.cache.get(query)
            if cached:
                self.metrics['cache_hits'] += 1
                hypothetical = cached
            else:
                hypothetical = self._generate_hypothetical(query)
                self.cache.set(query, hypothetical)
        else:
            hypothetical = self._generate_hypothetical(query)
        
        # 向量化并检索
        hyp_vector = self.embedding_model.encode([hypothetical])[0]
        results = self.vectorstore.similarity_search_by_vector(
            hyp_vector,
            k=k
        )
        
        return results
    
    def _traditional_retrieve(
        self,
        query: str,
        k: int
    ) -> List[Tuple[str, float]]:
        """传统检索"""
        query_vector = self.embedding_model.encode([query])[0]
        results = self.vectorstore.similarity_search_by_vector(
            query_vector,
            k=k
        )
        return results
    
    def _generate_hypothetical(self, query: str) -> str:
        """生成假设文档"""
        prompt = f"""请针对以下问题生成一个假设的答案。

问题：{query}

要求：使用专业、准确的表述，结构清晰。

假设答案："""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def get_metrics(self) -> dict:
        """获取指标"""
        total = self.metrics['total_queries']
        return {
            **self.metrics,
            'hyde_success_rate': (
                self.metrics['hyde_success'] / total if total > 0 else 0
            ),
            'cache_hit_rate': (
                self.metrics['cache_hits'] / total if total > 0 else 0
            )
        }
```

---

## 📝 课后练习

### 练习1：自适应HyDE
实现根据Query复杂度自动决定是否使用HyDE

### 练习2：混合检索
结合HyDE和传统检索，融合两者结果

### 练习3：多模态HyDE
扩展HyDE支持图像查询

---

## 🎓 知识总结

### 核心要点

1. **HyDE原理**
   - 用假设答案检索
   - 答案-答案相似度高
   - 解决表述差异问题

2. **适用场景**
   - ✅ 复杂问题
   - ✅ 专业领域
   - ✅ 表述差异大
   - ❌ 简单关键词查询

3. **性能优化**
   - 缓存假设文档
   - 异步生成
   - 向量融合

4. **生产实践**
   - 自适应策略
   - 降级方案
   - 效果监控

---

## 🚀 下节预告

下一课：**第62课：自查询检索器**

- 自动解析Query结构
- 元数据过滤优化
- 结构化查询生成

**让RAG更智能地理解复杂查询！** 🎯

---

**💪 记住：HyDE是提升RAG检索效果的利器！**

**下一课见！** 🎉
