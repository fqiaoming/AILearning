![RAG系统架构](./images/rag_flow.svg)
*图：RAG系统架构*

# 第56课：检索优化：相似度 vs MMR vs 语义检索

> **本课目标**：深入理解不同检索算法，掌握如何选择和优化检索策略
> 
> **核心技能**：相似度检索、MMR算法、语义检索、检索评估
> 
> **实战案例**：对比不同检索策略的效果，选择最优方案
> 
> **学习时长**：75分钟

---

## 📖 口播文案（3分钟）

### 🎯 前言

"上节课我们实现了一个基础的RAG系统，用的是最简单的向量相似度检索。

但很多同学反馈：'检索效果不理想，经常返回重复的内容，或者检索不到真正相关的文档'

**为什么？因为检索算法没选对！**

我见过太多RAG系统，明明知识库里有答案，但就是检索不出来！或者检索出来的都是重复信息，没有多样性！

今天这一课，我会用75分钟，深入讲解三种核心检索算法：

**1. 相似度检索（Similarity Search）**
- 最常用，但容易返回重复内容
- 适合精确匹配场景

**2. MMR检索（Maximum Marginal Relevance）**
- 平衡相关性和多样性
- 避免重复，返回更丰富的信息

**3. 语义检索（Semantic Search）**
- 理解语义而不是字面意思
- 能找到相关但不完全相同的内容

学完这一课，你会知道：
- ✅ 每种算法的原理和适用场景
- ✅ 如何实现和优化每种算法
- ✅ 如何评估检索效果
- ✅ 如何根据场景选择最优策略

这不是理论课，每个算法我都会带你从零实现！

让我们开始！"

---

### 💡 核心知识点

#### 检索的核心目标

```
1. 相关性（Relevance）
   - 返回的文档与查询相关

2. 多样性（Diversity）
   - 返回的文档之间不重复，信息互补

3. 完整性（Coverage）
   - 覆盖查询的不同方面
```

#### 三种检索算法对比

```
┌────────────────────────────────────────────────┐
│  算法对比                                      │
├────────────────────────────────────────────────┤
│  相似度检索（Similarity）                      │
│  • 原理：余弦相似度                            │
│  • 优点：简单快速                              │
│  • 缺点：容易返回重复内容                      │
│  • 适用：精确匹配查询                          │
├────────────────────────────────────────────────┤
│  MMR检索（Maximum Marginal Relevance）         │
│  • 原理：平衡相关性和多样性                    │
│  • 优点：结果多样，信息丰富                    │
│  • 缺点：计算稍慢                              │
│  • 适用：需要全面信息的查询                    │
├────────────────────────────────────────────────┤
│  语义检索（Semantic Search）                   │
│  • 原理：理解语义而非字面                      │
│  • 优点：能找到语义相关内容                    │
│  • 缺点：可能偏离原意                          │
│  • 适用：需要扩展理解的查询                    │
└────────────────────────────────────────────────┘
```

---

## 📚 知识讲解

### 一、相似度检索（Similarity Search）

#
![检索优化](./images/retrieval.svg)
*图：检索优化*

### 1.1 原理详解

```
相似度检索的核心：余弦相似度

向量A: [0.2, 0.5, 0.8]
向量B: [0.3, 0.4, 0.7]

余弦相似度 = (A·B) / (||A|| × ||B||)

其中：
- A·B：向量点积
- ||A||：向量A的模长
- ||B||：向量B的模长

相似度范围：-1 到 1
- 1：完全相同
- 0：正交（无关）
- -1：完全相反
```

#### 1.2 实现相似度检索

```python
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Document:
    """文档对象"""
    content: str
    embedding: np.ndarray
    metadata: dict = None

class SimilarityRetriever:
    """相似度检索器"""
    
    def __init__(self):
        self.documents: List[Document] = []
    
    def add_documents(self, documents: List[Document]):
        """添加文档"""
        self.documents.extend(documents)
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        # 点积
        dot_product = np.dot(vec1, vec2)
        
        # 模长
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        # 余弦相似度
        similarity = dot_product / (norm1 * norm2)
        
        return similarity
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Document, float]]:
        """相似度检索"""
        # 计算查询与所有文档的相似度
        similarities = []
        
        for doc in self.documents:
            sim = self.cosine_similarity(query_embedding, doc.embedding)
            similarities.append((doc, sim))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 返回top-k
        return similarities[:k]

# 使用示例
def demo_similarity_search():
    """演示相似度检索"""
    
    # 1. 准备文档（简化示例，实际应该用embedding模型）
    documents = [
        Document(
            content="人工智能是计算机科学的一个分支",
            embedding=np.array([0.8, 0.6, 0.2, 0.1]),
            metadata={"source": "doc1.txt"}
        ),
        Document(
            content="机器学习是人工智能的核心技术",
            embedding=np.array([0.7, 0.7, 0.3, 0.1]),
            metadata={"source": "doc2.txt"}
        ),
        Document(
            content="深度学习是机器学习的一个分支",
            embedding=np.array([0.75, 0.65, 0.25, 0.15]),
            metadata={"source": "doc3.txt"}
        ),
        Document(
            content="今天天气真好",
            embedding=np.array([0.1, 0.2, 0.8, 0.9]),
            metadata={"source": "doc4.txt"}
        ),
    ]
    
    # 2. 创建检索器
    retriever = SimilarityRetriever()
    retriever.add_documents(documents)
    
    # 3. 查询
    query_embedding = np.array([0.8, 0.6, 0.2, 0.1])  # 与doc1相似
    
    results = retriever.search(query_embedding, k=3)
    
    # 4. 显示结果
    print("相似度检索结果：")
    for i, (doc, score) in enumerate(results):
        print(f"\n{i+1}. 相似度: {score:.4f}")
        print(f"   内容: {doc.content}")
        print(f"   来源: {doc.metadata['source']}")

demo_similarity_search()
```

#### 1.3 相似度检索的问题

```python
# 问题演示
documents = [
    "人工智能是计算机科学的一个分支",
    "人工智能是计算机技术的一个分支",  # 几乎相同
    "AI是计算机科学的一个重要领域",     # 几乎相同
    "机器学习是AI的核心技术",            # 相关但不同
]

query = "什么是人工智能？"

# 相似度检索返回：
# 1. "人工智能是计算机科学的一个分支"      - 相关 ✅
# 2. "人工智能是计算机技术的一个分支"      - 重复 ❌
# 3. "AI是计算机科学的一个重要领域"        - 重复 ❌

# 问题：前三个结果几乎相同，缺乏多样性！
# 第4个结果"机器学习是AI的核心技术"更有价值，但被排除了
```

---

### 二、MMR检索（Maximum Marginal Relevance）

#### 2.1 MMR原理

```
MMR的目标：平衡相关性和多样性

公式：
MMR = argmax[λ × Sim(Di, Q) - (1-λ) × max Sim(Di, Dj)]
           Di∈R\S              Dj∈S

其中：
- Di：候选文档
- Q：查询
- S：已选择的文档集合
- R：所有文档
- λ：平衡参数（0-1）
  - λ=1：只考虑相关性（退化为相似度检索）
  - λ=0：只考虑多样性
  - λ=0.5：平衡相关性和多样性（常用）

直观理解：
- 第一项 Sim(Di, Q)：与查询的相关性（越大越好）
- 第二项 max Sim(Di, Dj)：与已选文档的相似性（越小越好）
- 通过平衡两项，选择"相关但不重复"的文档
```

#### 2.2 MMR实现

```python
class MMRRetriever:
    """MMR检索器"""
    
    def __init__(self, lambda_param: float = 0.5):
        """
        Args:
            lambda_param: 平衡参数
                - 1.0: 只考虑相关性
                - 0.0: 只考虑多样性
                - 0.5: 平衡（推荐）
        """
        self.documents: List[Document] = []
        self.lambda_param = lambda_param
    
    def add_documents(self, documents: List[Document]):
        """添加文档"""
        self.documents.extend(documents)
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Document, float]]:
        """MMR检索"""
        # 1. 计算所有文档与查询的相似度
        query_similarities = []
        for doc in self.documents:
            sim = self.cosine_similarity(query_embedding, doc.embedding)
            query_similarities.append((doc, sim))
        
        # 2. 按相似度排序
        query_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 3. MMR选择
        selected = []  # 已选择的文档
        candidates = query_similarities.copy()  # 候选文档
        
        # 选择第一个（与查询最相似的）
        if candidates:
            first_doc, first_sim = candidates.pop(0)
            selected.append((first_doc, first_sim))
        
        # 迭代选择剩余文档
        while len(selected) < k and candidates:
            best_score = -float('inf')
            best_idx = -1
            
            # 遍历候选文档
            for idx, (candidate_doc, query_sim) in enumerate(candidates):
                # 计算与已选文档的最大相似度
                max_sim_to_selected = 0
                for selected_doc, _ in selected:
                    sim = self.cosine_similarity(
                        candidate_doc.embedding,
                        selected_doc.embedding
                    )
                    max_sim_to_selected = max(max_sim_to_selected, sim)
                
                # 计算MMR分数
                mmr_score = (
                    self.lambda_param * query_sim - 
                    (1 - self.lambda_param) * max_sim_to_selected
                )
                
                # 选择MMR分数最高的
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx
            
            # 添加到已选择列表
            if best_idx >= 0:
                selected.append(candidates.pop(best_idx))
        
        return selected

# 使用示例
def demo_mmr_search():
    """演示MMR检索"""
    
    # 1. 准备文档
    documents = [
        Document(
            content="人工智能是计算机科学的一个分支",
            embedding=np.array([0.8, 0.6, 0.2, 0.1]),
            metadata={"id": 1}
        ),
        Document(
            content="人工智能是计算机技术的一个分支",  # 与上面几乎相同
            embedding=np.array([0.81, 0.59, 0.21, 0.11]),
            metadata={"id": 2}
        ),
        Document(
            content="机器学习是人工智能的核心技术",
            embedding=np.array([0.7, 0.7, 0.3, 0.1]),
            metadata={"id": 3}
        ),
        Document(
            content="深度学习使用神经网络进行学习",
            embedding=np.array([0.6, 0.5, 0.4, 0.2]),
            metadata={"id": 4}
        ),
    ]
    
    # 2. 对比相似度检索和MMR检索
    query_embedding = np.array([0.8, 0.6, 0.2, 0.1])
    
    # 相似度检索
    print("【相似度检索】")
    sim_retriever = SimilarityRetriever()
    sim_retriever.add_documents(documents)
    sim_results = sim_retriever.search(query_embedding, k=3)
    
    for i, (doc, score) in enumerate(sim_results):
        print(f"{i+1}. ID={doc.metadata['id']}, 相似度={score:.4f}")
        print(f"   {doc.content}")
    
    # MMR检索
    print("\n【MMR检索】(λ=0.5)")
    mmr_retriever = MMRRetriever(lambda_param=0.5)
    mmr_retriever.add_documents(documents)
    mmr_results = mmr_retriever.search(query_embedding, k=3)
    
    for i, (doc, score) in enumerate(mmr_results):
        print(f"{i+1}. ID={doc.metadata['id']}, 分数={score:.4f}")
        print(f"   {doc.content}")
    
    print("\n观察：")
    print("- 相似度检索：ID=1和ID=2几乎相同（重复）")
    print("- MMR检索：选择了ID=1、ID=3、ID=4（多样性更好）")

demo_mmr_search()
```

#### 2.3 调整Lambda参数

```python
def demo_lambda_effect():
    """演示lambda参数的影响"""
    
    # 准备文档（同上）
    documents = [...]
    query_embedding = np.array([0.8, 0.6, 0.2, 0.1])
    
    # 测试不同的lambda值
    lambdas = [0.0, 0.3, 0.5, 0.7, 1.0]
    
    for lambda_val in lambdas:
        print(f"\n【Lambda = {lambda_val}】")
        
        retriever = MMRRetriever(lambda_param=lambda_val)
        retriever.add_documents(documents)
        results = retriever.search(query_embedding, k=3)
        
        for i, (doc, score) in enumerate(results):
            print(f"{i+1}. ID={doc.metadata['id']}")
    
    print("\n分析：")
    print("- λ=0.0: 最大多样性，可能不相关")
    print("- λ=0.5: 平衡，推荐")
    print("- λ=1.0: 最大相关性，等同于相似度检索")
```

---

### 三、语义检索（Semantic Search）

#### 3.1 语义检索原理

```
语义检索 vs 字面检索

字面检索：
查询："苹果手机怎么样？"
匹配："苹果手机"、"iPhone"
不匹配："水果"（虽然也叫苹果）

语义检索：
查询："苹果手机怎么样？"
理解：用户想了解iPhone的评价
匹配：
  - "iPhone性能不错"  ✅
  - "iOS系统很流畅"   ✅
  - "苹果的产品质量好" ✅
  - "苹果很甜"        ❌ (不同语义)

核心：理解语义，而不是匹配关键词
```

#### 3.2 语义检索实现

```python
from sentence_transformers import SentenceTransformer

class SemanticRetriever:
    """语义检索器"""
    
    def __init__(self, model_name: str = "moka-ai/m3e-base"):
        """
        初始化语义检索器
        
        使用预训练的Sentence-BERT模型
        这种模型专门为语义相似度优化
        """
        print(f"加载语义模型: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None
    
    def add_documents(self, documents: List[str]):
        """添加文档并编码"""
        self.documents = documents
        
        # 批量编码（更高效）
        print(f"编码 {len(documents)} 个文档...")
        self.embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            show_progress_bar=True
        )
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """语义检索"""
        # 1. 编码查询
        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]
        
        # 2. 计算相似度
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            sim = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((self.documents[i], sim))
        
        # 3. 排序返回
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]
    
    def _cosine_similarity(self, vec1, vec2):
        """计算余弦相似度"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 使用示例
def demo_semantic_search():
    """演示语义检索"""
    
    # 1. 准备文档
    documents = [
        "iPhone 15性能非常出色，处理速度快",
        "苹果手机的iOS系统非常流畅",
        "苹果公司的产品质量一直很好",
        "这个苹果很甜，很好吃",
        "水果店的苹果新鲜又便宜",
        "机器学习是人工智能的核心技术",
    ]
    
    # 2. 创建检索器
    retriever = SemanticRetriever()
    retriever.add_documents(documents)
    
    # 3. 语义查询
    queries = [
        "苹果手机怎么样？",
        "AI技术有哪些？",
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        print("="*60)
        
        results = retriever.search(query, k=3)
        
        for i, (doc, score) in enumerate(results):
            print(f"{i+1}. 相似度: {score:.4f}")
            print(f"   {doc}")
    
    print("\n观察：")
    print("- 查询'苹果手机'时，正确理解为iPhone，不是水果")
    print("- 返回的都是关于iPhone的内容，语义相关")

demo_semantic_search()
```

#### 3.3 语义检索的优势

```python
def compare_search_methods():
    """对比不同检索方法"""
    
    documents = [
        "北京是中国的首都，人口超过2000万",
        "上海是中国最大的城市，经济发达",
        "深圳是中国的科技中心，创新企业众多",
        "猫是一种可爱的宠物",
        "狗是人类最忠诚的朋友",
    ]
    
    # 测试查询
    query = "中国有哪些大城市？"
    
    print(f"查询: {query}\n")
    
    # 1. 关键词检索（简单实现）
    print("【关键词检索】")
    keyword_results = []
    for doc in documents:
        # 简单计算关键词匹配
        keywords = ["中国", "城市"]
        score = sum(1 for kw in keywords if kw in doc)
        if score > 0:
            keyword_results.append((doc, score))
    
    keyword_results.sort(key=lambda x: x[1], reverse=True)
    for i, (doc, score) in enumerate(keyword_results[:3]):
        print(f"{i+1}. 匹配度={score}: {doc}")
    
    # 2. 语义检索
    print("\n【语义检索】")
    retriever = SemanticRetriever()
    retriever.add_documents(documents)
    semantic_results = retriever.search(query, k=3)
    
    for i, (doc, score) in enumerate(semantic_results):
        print(f"{i+1}. 相似度={score:.4f}: {doc}")
    
    print("\n对比：")
    print("- 关键词：只匹配包含'中国'和'城市'的文档")
    print("- 语义：理解查询意图，返回相关城市信息")
    print("- 语义检索能找到'上海'、'深圳'（虽然文档中没有'城市'二字）")
```

---

### 四、检索策略对比与选择

#### 4.1 三种策略全面对比

```python
class ComprehensiveRetriever:
    """综合检索器（支持三种策略）"""
    
    def __init__(self, model_name: str = "moka-ai/m3e-base"):
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None
    
    def add_documents(self, documents: List[str]):
        """添加文档"""
        self.documents = documents
        self.embeddings = self.model.encode(documents, convert_to_numpy=True)
    
    def search_similarity(self, query: str, k: int = 5):
        """相似度检索"""
        query_emb = self.model.encode([query])[0]
        
        similarities = []
        for i, doc_emb in enumerate(self.embeddings):
            sim = np.dot(query_emb, doc_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
            )
            similarities.append((self.documents[i], sim, i))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]
    
    def search_mmr(self, query: str, k: int = 5, lambda_param: float = 0.5):
        """MMR检索"""
        query_emb = self.model.encode([query])[0]
        
        # 计算所有相似度
        query_sims = []
        for i, doc_emb in enumerate(self.embeddings):
            sim = np.dot(query_emb, doc_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
            )
            query_sims.append((i, sim))
        
        query_sims.sort(key=lambda x: x[1], reverse=True)
        
        # MMR选择
        selected_indices = []
        candidates = [idx for idx, _ in query_sims]
        
        # 选择第一个
        if candidates:
            selected_indices.append(candidates.pop(0))
        
        # 迭代选择
        while len(selected_indices) < k and candidates:
            best_score = -float('inf')
            best_idx = -1
            best_cand_idx = -1
            
            for cand_idx, doc_idx in enumerate(candidates):
                # 查询相似度
                query_sim = query_sims[doc_idx][1]
                
                # 与已选文档的最大相似度
                max_sim = 0
                for sel_idx in selected_indices:
                    sim = np.dot(
                        self.embeddings[doc_idx],
                        self.embeddings[sel_idx]
                    ) / (
                        np.linalg.norm(self.embeddings[doc_idx]) *
                        np.linalg.norm(self.embeddings[sel_idx])
                    )
                    max_sim = max(max_sim, sim)
                
                # MMR分数
                score = lambda_param * query_sim - (1 - lambda_param) * max_sim
                
                if score > best_score:
                    best_score = score
                    best_idx = doc_idx
                    best_cand_idx = cand_idx
            
            if best_idx >= 0:
                selected_indices.append(candidates.pop(best_cand_idx))
        
        # 构建结果
        results = []
        for idx in selected_indices:
            results.append((self.documents[idx], query_sims[idx][1], idx))
        
        return results
    
    def compare_all(self, query: str, k: int = 3):
        """对比所有检索策略"""
        print(f"查询: {query}")
        print("="*80)
        
        # 1. 相似度检索
        print("\n【1. 相似度检索】")
        sim_results = self.search_similarity(query, k)
        for i, (doc, score, idx) in enumerate(sim_results):
            print(f"{i+1}. [ID={idx}] 相似度={score:.4f}")
            print(f"   {doc[:80]}...")
        
        # 2. MMR检索 (λ=0.5)
        print("\n【2. MMR检索 (λ=0.5)】")
        mmr_results = self.search_mmr(query, k, lambda_param=0.5)
        for i, (doc, score, idx) in enumerate(mmr_results):
            print(f"{i+1}. [ID={idx}] 分数={score:.4f}")
            print(f"   {doc[:80]}...")
        
        # 3. MMR检索 (λ=0.7 - 更重视相关性)
        print("\n【3. MMR检索 (λ=0.7 - 偏重相关性)】")
        mmr_results_07 = self.search_mmr(query, k, lambda_param=0.7)
        for i, (doc, score, idx) in enumerate(mmr_results_07):
            print(f"{i+1}. [ID={idx}] 分数={score:.4f}")
            print(f"   {doc[:80]}...")
        
        # 4. 分析
        print("\n【分析】")
        sim_ids = [idx for _, _, idx in sim_results]
        mmr_ids = [idx for _, _, idx in mmr_results]
        
        print(f"- 相似度检索返回的文档ID: {sim_ids}")
        print(f"- MMR检索返回的文档ID: {mmr_ids}")
        
        if sim_ids == mmr_ids:
            print("- 两种方法返回相同结果（文档差异较大）")
        else:
            print("- MMR检索结果更多样化")

# 完整演示
def full_demo():
    """完整演示"""
    
    # 准备测试文档
    documents = [
        "人工智能是计算机科学的一个重要分支，研究如何让机器模拟人类智能",
        "人工智能技术在现代社会中扮演着越来越重要的角色",
        "AI是Artificial Intelligence的缩写，指的是人工智能技术",
        "机器学习是实现人工智能的一种重要方法，通过数据训练模型",
        "深度学习是机器学习的一个分支，使用多层神经网络",
        "神经网络是深度学习的基础，模拟人脑神经元的工作方式",
        "自然语言处理是AI的一个重要应用领域",
        "计算机视觉让机器能够理解和分析图像",
        "今天天气很好，适合出去散步",
        "我喜欢吃苹果，它很甜很有营养",
    ]
    
    # 创建检索器
    retriever = ComprehensiveRetriever()
    retriever.add_documents(documents)
    
    # 测试查询
    queries = [
        "什么是人工智能？",
        "机器学习的方法有哪些？",
    ]
    
    for query in queries:
        retriever.compare_all(query, k=3)
        print("\n" + "="*80 + "\n")

full_demo()
```

#### 4.2 选择检索策略的原则

```python
def choose_strategy_guide():
    """检索策略选择指南"""
    
    guide = """
    ┌─────────────────────────────────────────────────┐
    │  检索策略选择指南                               │
    └─────────────────────────────────────────────────┘
    
    【场景1：FAQ问答】
    • 特点：问题明确，答案唯一
    • 推荐：相似度检索
    • 原因：需要精确匹配，不需要多样性
    • 示例："密码忘记了怎么办？"
    
    【场景2：研究调研】
    • 特点：需要全面了解某个主题
    • 推荐：MMR检索 (λ=0.5)
    • 原因：需要多角度信息，避免重复
    • 示例："人工智能的发展历史"
    
    【场景3：创意写作】
    • 特点：需要不同视角的素材
    • 推荐：MMR检索 (λ=0.3, 偏重多样性)
    • 原因：激发创意，提供多样化内容
    • 示例："写一篇关于未来科技的文章"
    
    【场景4：语义理解】
    • 特点：查询表达模糊，需要理解意图
    • 推荐：语义检索
    • 原因：能理解同义词、相关概念
    • 示例："怎么让电脑变聪明？"（意图：AI）
    
    【场景5：技术文档查询】
    • 特点：需要准确的技术信息
    • 推荐：相似度检索 + 元数据过滤
    • 原因：精确度优先
    • 示例："如何配置nginx反向代理？"
    
    【场景6：新闻检索】
    • 特点：需要多个来源的报道
    • 推荐：MMR检索 (λ=0.6)
    • 原因：相关但不重复的新闻
    • 示例："最新的AI技术突破"
    
    ┌─────────────────────────────────────────────────┐
    │  快速决策树                                     │
    └─────────────────────────────────────────────────┘
    
    问题1：是否需要多样性？
    ├─ 否 → 使用相似度检索
    └─ 是 → 问题2
    
    问题2：查询表达是否明确？
    ├─ 是 → 使用MMR检索
    └─ 否 → 使用语义检索
    
    问题3：相关性 vs 多样性？
    ├─ 偏重相关性 → MMR (λ=0.7)
    ├─ 平衡 → MMR (λ=0.5)
    └─ 偏重多样性 → MMR (λ=0.3)
    """
    
    print(guide)

choose_strategy_guide()
```

---

### 五、检索效果评估

#### 5.1 评估指标

```python
from typing import Set

class RetrievalEvaluator:
    """检索效果评估器"""
    
    def precision_at_k(
        self,
        retrieved: List[int],
        relevant: Set[int],
        k: int
    ) -> float:
        """
        Precision@K：前K个结果中相关的比例
        
        P@K = (检索到的相关文档数) / K
        """
        retrieved_k = set(retrieved[:k])
        relevant_retrieved = retrieved_k & relevant
        return len(relevant_retrieved) / k if k > 0 else 0
    
    def recall_at_k(
        self,
        retrieved: List[int],
        relevant: Set[int],
        k: int
    ) -> float:
        """
        Recall@K：相关文档被检索到的比例
        
        R@K = (检索到的相关文档数) / (总相关文档数)
        """
        retrieved_k = set(retrieved[:k])
        relevant_retrieved = retrieved_k & relevant
        return len(relevant_retrieved) / len(relevant) if relevant else 0
    
    def f1_at_k(
        self,
        retrieved: List[int],
        relevant: Set[int],
        k: int
    ) -> float:
        """
        F1@K：精确率和召回率的调和平均
        
        F1 = 2 * (P * R) / (P + R)
        """
        p = self.precision_at_k(retrieved, relevant, k)
        r = self.recall_at_k(retrieved, relevant, k)
        
        if p + r == 0:
            return 0
        
        return 2 * (p * r) / (p + r)
    
    def mrr(self, retrieved: List[int], relevant: Set[int]) -> float:
        """
        MRR (Mean Reciprocal Rank)：第一个相关结果的倒数排名
        
        MRR = 1 / (第一个相关文档的排名)
        """
        for i, doc_id in enumerate(retrieved):
            if doc_id in relevant:
                return 1.0 / (i + 1)
        return 0.0
    
    def ndcg_at_k(
        self,
        retrieved: List[int],
        relevance_scores: dict,
        k: int
    ) -> float:
        """
        NDCG@K (Normalized Discounted Cumulative Gain)
        考虑排名位置的评估指标
        """
        # DCG (Discounted Cumulative Gain)
        dcg = 0
        for i, doc_id in enumerate(retrieved[:k]):
            rel = relevance_scores.get(doc_id, 0)
            dcg += rel / np.log2(i + 2)  # i+2因为log2(1)=0
        
        # IDCG (Ideal DCG)
        sorted_rels = sorted(relevance_scores.values(), reverse=True)
        idcg = 0
        for i, rel in enumerate(sorted_rels[:k]):
            idcg += rel / np.log2(i + 2)
        
        # NDCG
        return dcg / idcg if idcg > 0 else 0

# 使用示例
def demo_evaluation():
    """演示评估"""
    
    evaluator = RetrievalEvaluator()
    
    # 假设检索结果（文档ID）
    retrieved = [1, 3, 5, 2, 8, 10, 4]
    
    # 真实相关的文档ID
    relevant = {1, 2, 4, 6, 7}
    
    # 计算各项指标
    k = 5
    
    print(f"检索结果: {retrieved[:k]}")
    print(f"相关文档: {relevant}")
    print("\n评估指标:")
    
    precision = evaluator.precision_at_k(retrieved, relevant, k)
    print(f"- Precision@{k}: {precision:.4f}")
    print(f"  含义: 前{k}个结果中，{precision*100:.1f}%是相关的")
    
    recall = evaluator.recall_at_k(retrieved, relevant, k)
    print(f"\n- Recall@{k}: {recall:.4f}")
    print(f"  含义: {len(relevant)}个相关文档中，检索到了{recall*100:.1f}%")
    
    f1 = evaluator.f1_at_k(retrieved, relevant, k)
    print(f"\n- F1@{k}: {f1:.4f}")
    print(f"  含义: 精确率和召回率的平衡")
    
    mrr = evaluator.mrr(retrieved, relevant)
    print(f"\n- MRR: {mrr:.4f}")
    print(f"  含义: 第一个相关结果在第{int(1/mrr)}位")
    
    # 带相关性分数的评估
    relevance_scores = {1: 3, 2: 2, 4: 2, 6: 1, 7: 1, 3: 0, 5: 0, 8: 0, 10: 0}
    ndcg = evaluator.ndcg_at_k(retrieved, relevance_scores, k)
    print(f"\n- NDCG@{k}: {ndcg:.4f}")
    print(f"  含义: 考虑排名位置的综合指标")

demo_evaluation()
```

---

## 📝 课后练习

### 练习1：实现混合检索

结合相似度和MMR，设计一个自适应检索策略

### 练习2：优化MMR性能

MMR计算复杂度高，优化算法提升速度

### 练习3：A/B测试

在实际场景中对比不同策略的效果

---

## 🎓 知识总结

### 核心要点

1. **三种检索算法**
   - 相似度：简单快速，但易重复
   - MMR：平衡相关性和多样性
   - 语义：理解意图，不拘泥字面

2. **选择原则**
   - FAQ：相似度检索
   - 研究：MMR检索
   - 模糊查询：语义检索

3. **评估指标**
   - Precision@K：精确率
   - Recall@K：召回率
   - F1@K：综合指标
   - NDCG：考虑排名

### 最佳实践

✅ 根据场景选择策略
✅ 调整MMR的λ参数
✅ 使用评估指标验证
✅ A/B测试对比效果
✅ 持续优化迭代

---

## 🚀 下节预告

下一课：**第57课：混合检索：向量+关键词+元数据**

- 如何结合多种检索方式
- BM25关键词检索
- 元数据过滤
- 完整的混合检索系统

**让检索更精准、更全面！** 🎯

---

**💪 记住：选对检索策略，RAG效果提升一半！**

**下一课见！** 🎉
