![RAG系统架构](./images/rag_flow.svg)
*图：RAG系统架构*

# 第59课：Rerank重排序技术

> **本课目标**：掌握Rerank重排序技术，大幅提升检索结果的准确性
> 
> **核心技能**：Cross-Encoder、重排序策略、性能优化
> 
> **实战案例**：构建高精度重排序系统
> 
> **学习时长**：75分钟

---

## 📖 口播文案（3分钟）

### 🎯 前言

"你有没有发现一个问题：

向量检索返回的Top-10结果中，最相关的内容经常不在第一位！

比如：
用户问：'Python和Java哪个更适合AI开发？'

检索结果：
1. Python语法基础 ❌（不相关）
2. Java面向对象编程 ❌（不相关）
3. Python在AI领域的应用 ✅（相关！）
4. AI开发语言对比 ✅✅（最相关！）

**问题是：第4个才是最佳答案，但它排在后面！**

为什么会这样？

因为向量检索只看'语义相似度'，不看'真正的相关性'！

**今天这一课，我要教你Rerank（重排序）技术！**

它的作用是：
- 对初筛结果进行精细化排序
- 用更强大的模型重新评分
- 把最相关的结果放在最前面

学完这一课，你会掌握：

✅ **Bi-Encoder vs Cross-Encoder**：两种编码器的区别
✅ **重排序原理**：如何重新评分
✅ **性能优化**：平衡精度和速度
✅ **完整实现**：可用于生产的重排序系统

这是RAG系统从'80分'到'95分'的关键技术！

很多企业级RAG系统的秘密武器就是Rerank！

准备好了吗？让我们开始！"

---

### 💡 核心知识点

#### 为什么需要重排序？

```
【检索的两阶段策略】

第一阶段：快速召回（Retrieval）
• 目标：从海量文档中快速找出候选集
• 方法：向量检索（Bi-Encoder）
• 特点：速度快，但不够精准
• 结果：Top-100 ~ Top-1000候选

第二阶段：精准排序（Rerank）
• 目标：从候选集中找出最相关的
• 方法：Cross-Encoder重排序
• 特点：精准，但较慢
• 结果：Top-5 ~ Top-10最终结果

类比：
就像招聘：
1. 简历筛选（快速） → Retrieval
2. 面试评估（精准） → Rerank
```

#### Bi-Encoder vs Cross-Encoder

```
【Bi-Encoder（双塔模型）】
┌─────────┐         ┌─────────┐
│  Query  │         │Document │
└────┬────┘         └────┬────┘
     │                   │
     ↓                   ↓
┌─────────┐         ┌─────────┐
│ Encoder │         │ Encoder │
└────┬────┘         └────┬────┘
     │                   │
     ↓                   ↓
  Vector₁             Vector₂
     │                   │
     └────────┬──────────┘
              ↓
       Cosine Similarity

优点：
• 可以预先计算文档向量
• 检索速度快（向量相似度计算）
• 适合大规模检索

缺点：
• Query和Document分开编码
• 无法捕捉细粒度交互
• 准确性有限

【Cross-Encoder（交叉编码器）】
┌─────────────────────────┐
│  Query + Document       │
│  (拼接在一起)            │
└───────────┬─────────────┘
            ↓
      ┌─────────┐
      │ Encoder │
      └────┬────┘
           ↓
     ┌──────────┐
     │Classifier│
     └────┬─────┘
          ↓
    Relevance Score
    (0-1之间的相关性分数)

优点：
• Query和Document联合编码
• 捕捉细粒度交互
• 准确性高

缺点：
• 无法预先计算
• 每个Query-Document对都要重新计算
• 速度慢，不适合大规模检索

【最佳实践】
Bi-Encoder召回 → Cross-Encoder重排序
  (快速筛选)      (精准排序)
```

---

## 📚 知识讲解

### 一、Cross-Encoder原理

#
![Generation](./images/generation.svg)
*图：Generation*

### 1.1 Cross-Encoder架构

```python
from sentence_transformers import CrossEncoder
from typing import List, Tuple
import numpy as np

class CrossEncoderReranker:
    """Cross-Encoder重排序器"""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        初始化Cross-Encoder
        
        常用模型：
        • cross-encoder/ms-marco-MiniLM-L-6-v2 (英文)
        • BAAI/bge-reranker-base (中文)
        • maidalun1020/bce-reranker-base_v1 (中文)
        """
        print(f"🤖 加载Cross-Encoder模型: {model_name}")
        self.model = CrossEncoder(model_name)
        print("✅ 模型加载完成")
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Tuple[str, float, int]]:
        """
        重排序文档
        
        Args:
            query: 查询
            documents: 文档列表
            top_k: 返回top-k个结果
        
        Returns:
            List of (document, score, original_index)
        """
        print(f"\n🔄 重排序 {len(documents)} 个文档...")
        
        # 1. 构建Query-Document对
        pairs = [[query, doc] for doc in documents]
        
        # 2. 计算相关性分数
        scores = self.model.predict(pairs)
        
        # 3. 排序
        doc_score_indices = [
            (documents[i], scores[i], i)
            for i in range(len(documents))
        ]
        doc_score_indices.sort(key=lambda x: x[1], reverse=True)
        
        print(f"✅ 重排序完成")
        
        # 4. 返回top-k
        return doc_score_indices[:top_k]
    
    def rerank_with_threshold(
        self,
        query: str,
        documents: List[str],
        threshold: float = 0.5,
        top_k: int = 10
    ) -> List[Tuple[str, float, int]]:
        """
        重排序并过滤低分文档
        
        Args:
            threshold: 分数阈值，低于此值的文档被过滤
        """
        # 重排序
        results = self.rerank(query, documents, top_k=len(documents))
        
        # 过滤
        filtered = [
            (doc, score, idx)
            for doc, score, idx in results
            if score >= threshold
        ]
        
        return filtered[:top_k]

# 使用示例
def demo_cross_encoder():
    """演示Cross-Encoder"""
    
    # 准备数据
    query = "Python和Java哪个更适合AI开发？"
    
    documents = [
        "Python是一种简单易学的编程语言，语法清晰",
        "Java是一种面向对象的编程语言，应用广泛",
        "Python在人工智能和机器学习领域应用最广泛",
        "Java在企业级应用开发中占据重要地位",
        "AI开发主要使用Python，因为有丰富的库如TensorFlow和PyTorch",
        "Python和Java都可以用于AI开发，但Python生态更成熟",
        "深度学习框架大多基于Python开发",
        "Java也有DeepLearning4j等AI框架",
    ]
    
    print("="*60)
    print("Cross-Encoder重排序演示")
    print("="*60)
    print(f"查询: {query}\n")
    
    # 显示原始顺序
    print("【原始文档顺序】")
    for i, doc in enumerate(documents):
        print(f"{i+1}. {doc}")
    
    # 创建重排序器
    reranker = CrossEncoderReranker()
    
    # 重排序
    results = reranker.rerank(query, documents, top_k=5)
    
    # 显示重排序结果
    print("\n【重排序后（Top-5）】")
    for i, (doc, score, idx) in enumerate(results):
        print(f"{i+1}. [原序号={idx+1}] 分数={score:.4f}")
        print(f"   {doc}")

demo_cross_encoder()
```

#### 1.2 对比Bi-Encoder和Cross-Encoder

```python
from sentence_transformers import SentenceTransformer
import time

def compare_encoders():
    """对比两种编码器"""
    
    query = "Python在AI开发中的优势"
    
    documents = [
        "Python语法简单易学，适合初学者",
        "Python有丰富的AI库，如TensorFlow、PyTorch",
        "Python在数据科学领域应用广泛",
        "Java性能优秀，适合大型系统",
        "AI开发首选Python，社区支持好",
    ]
    
    print("="*60)
    print("Bi-Encoder vs Cross-Encoder 对比")
    print("="*60)
    
    # 1. Bi-Encoder
    print("\n【Bi-Encoder】")
    bi_model = SentenceTransformer('moka-ai/m3e-base')
    
    start = time.time()
    
    # 编码query和documents
    query_emb = bi_model.encode([query])[0]
    doc_embs = bi_model.encode(documents)
    
    # 计算相似度
    similarities = []
    for i, doc_emb in enumerate(doc_embs):
        sim = np.dot(query_emb, doc_emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
        )
        similarities.append((documents[i], sim, i))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    bi_time = time.time() - start
    
    print(f"耗时: {bi_time:.4f}秒")
    print("Top-3结果:")
    for i, (doc, score, idx) in enumerate(similarities[:3]):
        print(f"  {i+1}. [#{idx+1}] {score:.4f} - {doc[:40]}...")
    
    # 2. Cross-Encoder
    print("\n【Cross-Encoder】")
    cross_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    start = time.time()
    
    pairs = [[query, doc] for doc in documents]
    scores = cross_model.predict(pairs)
    
    results = [(documents[i], scores[i], i) for i in range(len(documents))]
    results.sort(key=lambda x: x[1], reverse=True)
    
    cross_time = time.time() - start
    
    print(f"耗时: {cross_time:.4f}秒")
    print("Top-3结果:")
    for i, (doc, score, idx) in enumerate(results[:3]):
        print(f"  {i+1}. [#{idx+1}] {score:.4f} - {doc[:40]}...")
    
    # 3. 对比分析
    print("\n【对比分析】")
    print(f"速度对比: Bi-Encoder {bi_time:.4f}s vs Cross-Encoder {cross_time:.4f}s")
    print(f"速度比: Cross-Encoder是Bi-Encoder的 {cross_time/bi_time:.2f}倍")
    print("\n排序差异:")
    bi_top3 = [idx for _, _, idx in similarities[:3]]
    cross_top3 = [idx for _, _, idx in results[:3]]
    print(f"  Bi-Encoder Top-3: {[i+1 for i in bi_top3]}")
    print(f"  Cross-Encoder Top-3: {[i+1 for i in cross_top3]}")

compare_encoders()
```

---

### 二、两阶段检索+重排序

#### 2.1 完整流程实现

```python
class TwoStageRetriever:
    """两阶段检索器（检索+重排序）"""
    
    def __init__(
        self,
        embedding_model: str = "moka-ai/m3e-base",
        rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        print("🚀 初始化两阶段检索系统")
        print("="*60)
        
        # 第一阶段：Bi-Encoder（快速召回）
        print("加载Bi-Encoder...")
        self.bi_encoder = SentenceTransformer(embedding_model)
        
        # 第二阶段：Cross-Encoder（精准重排）
        print("加载Cross-Encoder...")
        self.cross_encoder = CrossEncoder(rerank_model)
        
        self.documents = []
        self.embeddings = None
        
        print("✅ 初始化完成\n")
    
    def index_documents(self, documents: List[str]):
        """索引文档"""
        print(f"📚 索引 {len(documents)} 个文档...")
        
        self.documents = documents
        self.embeddings = self.bi_encoder.encode(
            documents,
            show_progress_bar=True
        )
        
        print("✅ 索引完成\n")
    
    def search(
        self,
        query: str,
        retrieval_k: int = 20,
        rerank_k: int = 5,
        enable_rerank: bool = True,
        verbose: bool = True
    ) -> List[Tuple[str, float, int]]:
        """
        两阶段检索
        
        Args:
            query: 查询
            retrieval_k: 第一阶段召回数量
            rerank_k: 第二阶段返回数量
            enable_rerank: 是否启用重排序
            verbose: 是否显示详细信息
        """
        if verbose:
            print("="*60)
            print("🔍 两阶段检索")
            print("="*60)
            print(f"查询: {query}\n")
        
        # 第一阶段：向量检索（快速召回）
        if verbose:
            print(f"【阶段1】向量检索 (召回Top-{retrieval_k})")
        
        start = time.time()
        
        query_emb = self.bi_encoder.encode([query])[0]
        
        # 计算相似度
        similarities = []
        for i, doc_emb in enumerate(self.embeddings):
            sim = np.dot(query_emb, doc_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
            )
            similarities.append((self.documents[i], sim, i))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        retrieved = similarities[:retrieval_k]
        
        retrieval_time = time.time() - start
        
        if verbose:
            print(f"  ✅ 召回完成，耗时 {retrieval_time:.3f}秒")
            print(f"  Top-3预览:")
            for i, (doc, score, idx) in enumerate(retrieved[:3]):
                print(f"    {i+1}. [ID={idx}] {score:.4f} - {doc[:50]}...")
        
        # 第二阶段：Cross-Encoder重排序
        if enable_rerank:
            if verbose:
                print(f"\n【阶段2】Cross-Encoder重排序 (精选Top-{rerank_k})")
            
            start = time.time()
            
            # 提取文档
            candidate_docs = [doc for doc, _, _ in retrieved]
            candidate_indices = [idx for _, _, idx in retrieved]
            
            # 重排序
            pairs = [[query, doc] for doc in candidate_docs]
            scores = self.cross_encoder.predict(pairs)
            
            # 重新排序
            reranked = [
                (candidate_docs[i], scores[i], candidate_indices[i])
                for i in range(len(candidate_docs))
            ]
            reranked.sort(key=lambda x: x[1], reverse=True)
            
            final_results = reranked[:rerank_k]
            
            rerank_time = time.time() - start
            
            if verbose:
                print(f"  ✅ 重排序完成，耗时 {rerank_time:.3f}秒")
                print(f"  总耗时: {retrieval_time + rerank_time:.3f}秒")
        else:
            final_results = retrieved[:rerank_k]
            rerank_time = 0
        
        # 显示最终结果
        if verbose:
            print(f"\n【最终结果】Top-{len(final_results)}")
            for i, (doc, score, idx) in enumerate(final_results):
                print(f"  {i+1}. [ID={idx}] 分数={score:.4f}")
                print(f"     {doc}")
        
        return final_results
    
    def compare_with_without_rerank(self, query: str, k: int = 5):
        """对比有无重排序的效果"""
        print("\n" + "🔬"*30)
        print("对比实验：有无重排序")
        print("🔬"*30)
        
        # 无重排序
        print("\n【方案A：仅向量检索】")
        results_without = self.search(
            query,
            retrieval_k=20,
            rerank_k=k,
            enable_rerank=False,
            verbose=False
        )
        
        print(f"Top-{k}结果:")
        for i, (doc, score, idx) in enumerate(results_without):
            print(f"  {i+1}. [ID={idx}] {score:.4f}")
            print(f"     {doc[:60]}...")
        
        # 有重排序
        print("\n【方案B：向量检索 + 重排序】")
        results_with = self.search(
            query,
            retrieval_k=20,
            rerank_k=k,
            enable_rerank=True,
            verbose=False
        )
        
        print(f"Top-{k}结果:")
        for i, (doc, score, idx) in enumerate(results_with):
            print(f"  {i+1}. [ID={idx}] {score:.4f}")
            print(f"     {doc[:60]}...")
        
        # 对比
        print("\n【对比分析】")
        without_ids = [idx for _, _, idx in results_without]
        with_ids = [idx for _, _, idx in results_with]
        
        print(f"  无重排序的文档ID: {without_ids}")
        print(f"  有重排序的文档ID: {with_ids}")
        
        # 计算排序变化
        changes = sum(1 for i in range(min(len(without_ids), len(with_ids)))
                     if without_ids[i] != with_ids[i])
        print(f"  排序变化: Top-{k}中有 {changes} 个位置发生变化")

# 完整示例
def full_demo():
    """完整演示"""
    
    # 1. 准备文档
    documents = [
        "Python是一种高级编程语言，语法简洁易读",
        "Java是面向对象的编程语言，广泛用于企业开发",
        "Python在人工智能和机器学习领域占据主导地位",
        "TensorFlow和PyTorch是Python的主流深度学习框架",
        "Java有DeepLearning4j等AI框架，但不如Python生态丰富",
        "Python的NumPy、Pandas等库使数据处理非常便捷",
        "AI研究人员和工程师首选Python作为开发语言",
        "Python社区活跃，AI相关的开源项目众多",
        "Java在大数据领域有Hadoop、Spark等成熟框架",
        "机器学习算法实现时，Python代码更简洁直观",
    ]
    
    # 2. 创建两阶段检索器
    retriever = TwoStageRetriever()
    retriever.index_documents(documents)
    
    # 3. 查询
    query = "为什么Python是AI开发的首选语言？"
    
    # 4. 对比有无重排序
    retriever.compare_with_without_rerank(query, k=5)

full_demo()
```

---

### 三、性能优化策略

#### 3.1 批量重排序优化

```python
class OptimizedReranker:
    """优化的重排序器"""
    
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)
    
    def rerank_batch(
        self,
        queries: List[str],
        documents_list: List[List[str]],
        batch_size: int = 32
    ) -> List[List[Tuple[str, float]]]:
        """
        批量重排序（性能优化）
        
        Args:
            queries: 查询列表
            documents_list: 每个查询对应的文档列表
            batch_size: 批处理大小
        """
        all_results = []
        
        for query, documents in zip(queries, documents_list):
            # 构建pairs
            pairs = [[query, doc] for doc in documents]
            
            # 批量预测（提高效率）
            scores = self.model.predict(
                pairs,
                batch_size=batch_size,
                show_progress_bar=False
            )
            
            # 排序
            results = [
                (documents[i], scores[i])
                for i in range(len(documents))
            ]
            results.sort(key=lambda x: x[1], reverse=True)
            
            all_results.append(results)
        
        return all_results
    
    def rerank_with_cache(
        self,
        query: str,
        documents: List[str],
        cache: dict
    ) -> List[Tuple[str, float]]:
        """
        带缓存的重排序
        """
        import hashlib
        
        # 生成缓存key
        cache_key = hashlib.md5(
            f"{query}{''.join(documents)}".encode()
        ).hexdigest()
        
        # 检查缓存
        if cache_key in cache:
            return cache[cache_key]
        
        # 计算
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        
        results = [
            (documents[i], scores[i])
            for i in range(len(documents))
        ]
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 保存到缓存
        cache[cache_key] = results
        
        return results
```

#### 3.2 自适应重排序

```python
class AdaptiveReranker:
    """自适应重排序器"""
    
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)
    
    def adaptive_rerank(
        self,
        query: str,
        documents: List[str],
        retrieval_scores: List[float],
        score_threshold: float = 0.7,
        max_rerank: int = 50
    ) -> List[Tuple[str, float, int]]:
        """
        自适应重排序
        
        策略：
        1. 如果召回分数都很高，只重排少量文档
        2. 如果召回分数不稳定，重排更多文档
        """
        # 分析召回分数
        avg_score = np.mean(retrieval_scores)
        std_score = np.std(retrieval_scores)
        
        # 决定重排序数量
        if avg_score > score_threshold and std_score < 0.1:
            # 分数高且稳定，只重排前面的
            rerank_count = min(10, len(documents))
        else:
            # 分数不稳定，重排更多
            rerank_count = min(max_rerank, len(documents))
        
        print(f"📊 召回分数分析:")
        print(f"  平均: {avg_score:.4f}, 标准差: {std_score:.4f}")
        print(f"  决定重排序前 {rerank_count} 个文档")
        
        # 重排序
        pairs = [[query, doc] for doc in documents[:rerank_count]]
        scores = self.model.predict(pairs)
        
        # 构建结果
        results = []
        for i in range(rerank_count):
            results.append((documents[i], scores[i], i))
        
        # 添加未重排的文档（保持原顺序）
        for i in range(rerank_count, len(documents)):
            results.append((documents[i], retrieval_scores[i], i))
        
        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
```

---

### 四、评估重排序效果

#### 4.1 评估指标

```python
class RerankEvaluator:
    """重排序效果评估器"""
    
    def mrr(
        self,
        rankings: List[List[int]],
        relevant: List[int]
    ) -> float:
        """
        MRR (Mean Reciprocal Rank)
        第一个相关结果的平均倒数排名
        """
        reciprocal_ranks = []
        
        for ranking in rankings:
            for i, doc_id in enumerate(ranking):
                if doc_id in relevant:
                    reciprocal_ranks.append(1.0 / (i + 1))
                    break
            else:
                reciprocal_ranks.append(0.0)
        
        return np.mean(reciprocal_ranks)
    
    def ndcg_at_k(
        self,
        ranking: List[int],
        relevance: dict,
        k: int
    ) -> float:
        """NDCG@K"""
        # DCG
        dcg = 0
        for i, doc_id in enumerate(ranking[:k]):
            rel = relevance.get(doc_id, 0)
            dcg += rel / np.log2(i + 2)
        
        # IDCG
        ideal_ranking = sorted(
            relevance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        idcg = 0
        for i, (_, rel) in enumerate(ideal_ranking[:k]):
            idcg += rel / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0
    
    def compare_rankings(
        self,
        before: List[int],
        after: List[int],
        relevance: dict,
        k: int = 5
    ):
        """对比重排序前后的效果"""
        print("\n" + "="*60)
        print("重排序效果对比")
        print("="*60)
        
        # 计算NDCG
        ndcg_before = self.ndcg_at_k(before, relevance, k)
        ndcg_after = self.ndcg_at_k(after, relevance, k)
        
        print(f"\nNDCG@{k}:")
        print(f"  重排序前: {ndcg_before:.4f}")
        print(f"  重排序后: {ndcg_after:.4f}")
        print(f"  提升: {(ndcg_after - ndcg_before):.4f} ({(ndcg_after/ndcg_before-1)*100:.1f}%)")
        
        # 查看排名变化
        print(f"\nTop-{k}排名对比:")
        print(f"  重排序前: {before[:k]}")
        print(f"  重排序后: {after[:k]}")
        
        # 相关文档的排名变化
        print(f"\n相关文档排名变化:")
        for doc_id, rel in sorted(relevance.items(), key=lambda x: x[1], reverse=True):
            if rel > 0:
                pos_before = before.index(doc_id) + 1 if doc_id in before else -1
                pos_after = after.index(doc_id) + 1 if doc_id in after else -1
                
                if pos_before > 0 and pos_after > 0:
                    change = pos_before - pos_after
                    arrow = "↑" if change > 0 else ("↓" if change < 0 else "→")
                    print(f"  文档{doc_id} (相关度={rel}): {pos_before} {arrow} {pos_after}")

# 使用示例
def demo_evaluation():
    """演示评估"""
    
    # 模拟重排序前后的排名
    before_ranking = [1, 3, 5, 2, 4, 7, 6, 8, 9, 0]
    after_ranking = [2, 4, 1, 7, 3, 5, 6, 8, 9, 0]
    
    # 相关性标注（0-3分）
    relevance = {
        0: 0,  # 不相关
        1: 1,  # 弱相关
        2: 3,  # 强相关
        3: 1,
        4: 3,  # 强相关
        5: 1,
        6: 0,
        7: 2,  # 中等相关
        8: 0,
        9: 0,
    }
    
    evaluator = RerankEvaluator()
    evaluator.compare_rankings(before_ranking, after_ranking, relevance, k=5)

demo_evaluation()
```

---

## 📝 课后练习

### 练习1：训练自己的Cross-Encoder

使用自己的数据fine-tune Cross-Encoder模型

### 练习2：多模型集成

结合多个重排序模型，投票决策

### 练习3：实时性优化

优化重排序性能，满足实时查询需求

---

## 🎓 知识总结

### 核心要点

1. **两阶段检索**
   - 召回：Bi-Encoder快速筛选
   - 重排：Cross-Encoder精准排序
   - 平衡速度和精度

2. **Cross-Encoder优势**
   - 联合编码Query和Document
   - 捕捉细粒度交互
   - 显著提升准确性

3. **性能优化**
   - 批量处理
   - 缓存结果
   - 自适应策略

4. **应用场景**
   - 企业搜索
   - 问答系统
   - 推荐系统

### 最佳实践

✅ 召回用Bi-Encoder（快）
✅ 重排用Cross-Encoder（准）
✅ 召回20-100，重排到5-10
✅ 监控重排序效果
✅ 根据场景调整策略

---

## 🚀 下节预告

下一课：**第60课：实战：构建生产级RAG系统**

- 完整系统架构
- 性能优化
- 错误处理
- 监控和日志
- 部署方案

**把所有技术整合到一起！** 🎯

---

**💪 记住：Rerank是提升RAG准确性的杀手锏！**

**下一课见！** 🎉
