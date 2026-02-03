![RAG系统架构](./images/rag_flow.svg)
*图：RAG系统架构*

# 第54课：RAG系统架构设计

> **本课目标**：深入理解RAG系统的架构设计原理，掌握从简单到复杂的架构演进
> 
> **核心技能**：架构设计、组件解耦、扩展性设计、性能优化
> 
> **实战案例**：设计可扩展的企业级RAG架构
> 
> **学习时长**：75分钟

---

## 📖 口播文案（3分钟）

### 🎯 前言

"很多人学RAG，上来就是一顿操作：加载文档、分块、向量化、检索、生成……代码写了一大堆，结果系统跑不起来，或者跑起来了效果很差！

为什么？**因为没有架构设计！**

我见过太多人，把所有代码写在一个main.py文件里，几千行代码，想改个参数要翻半天，想加个功能不知道从哪下手，出了问题不知道哪里错了！

**这就是没有架构的代价！**

好的架构设计，能让你的RAG系统：
- ✅ 容易理解和维护
- ✅ 组件可以独立测试
- ✅ 轻松扩展新功能
- ✅ 性能问题容易定位
- ✅ 可以应对不同场景

今天这一课，我会用75分钟，带你深入理解RAG系统的架构设计！

从最简单的Naive RAG，到生产级的Advanced RAG，从单体架构到微服务架构，从原理到实践，一课讲透！

这不是理论课，这是实战架构课！学完你就知道如何设计一个真正可用的RAG系统！

让我们开始！"

---

### 💡 核心知识点

大家好！今天我们进入RAG系统的核心：**架构设计**。

#### 什么是RAG？

RAG = Retrieval Augmented Generation（检索增强生成）

```
传统LLM：
用户问题 → LLM → 答案
问题：知识有限，容易幻觉

RAG：
用户问题 → 检索相关知识 → 将知识+问题给LLM → 答案
优势：知识实时更新，答案有依据
```

#### RAG的核心流程

```
1. 离线索引阶段（Indexing）
   文档加载 → 分块 → 向量化 → 存储到向量库

2. 在线检索阶段（Retrieval）
   用户问题 → 向量化 → 向量检索 → 返回相关文档

3. 生成阶段（Generation）
   问题 + 检索到的文档 → LLM → 答案
```

#### RAG架构的演进

```
Level 1: Naive RAG（朴素RAG）
- 简单直接
- 效果一般
- 适合学习

Level 2: Advanced RAG（高级RAG）
- 引入各种优化技术
- 效果提升
- 生产可用

Level 3: Modular RAG（模块化RAG）
- 组件化设计
- 灵活可扩展
- 企业级
```

#### 今天的学习路线

1. **Naive RAG架构**：最简单的实现
2. **Advanced RAG架构**：各种优化技术
3. **Modular RAG架构**：模块化设计
4. **架构设计原则**：如何设计好架构
5. **实战：可扩展的RAG架构**

---

## 📚 知识讲解

### 一、Naive RAG架构

#
![RAG架构设计](./images/retrieval.svg)
*图：RAG架构设计*

### 1.1 基础架构图

```
┌─────────────┐
│  文档集合   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  1. Indexing (离线) │
│  • 文档加载         │
│  • 文本分块         │
│  • Embedding        │
│  • 存储向量库       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  向量数据库         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  2. Retrieval (在线)│
│  • 用户问题         │
│  • Query Embedding  │
│  • 向量检索         │
│  • 返回Top-K        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  3. Generation      │
│  • 构建Prompt       │
│  • LLM生成          │
│  • 返回答案         │
└─────────────────────┘
```

#### 1.2 Naive RAG实现

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

class NaiveRAG:
    """最简单的RAG实现"""
    
    def __init__(self, documents_path):
        # 1. 加载文档
        loader = TextLoader(documents_path)
        documents = loader.load()
        
        # 2. 分块
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)
        
        # 3. 创建向量库
        embeddings = HuggingFaceEmbeddings()
        self.vectorstore = Chroma.from_documents(chunks, embeddings)
        
        # 4. 创建LLM
        self.llm = OpenAI(temperature=0)
        
        # 5. 创建检索链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
        )
    
    def query(self, question):
        """查询"""
        return self.qa_chain.run(question)

# 使用
rag = NaiveRAG("documents.txt")
answer = rag.query("什么是RAG？")
print(answer)
```

#### 1.3 Naive RAG的问题

```python
问题1：检索质量不稳定
- 简单的向量相似度检索
- 没有考虑上下文
- 容易检索到不相关内容

问题2：固定的分块策略
- 统一的chunk_size
- 可能破坏语义完整性
- 没有考虑文档结构

问题3：没有质量保障
- 不知道检索结果是否相关
- 不知道生成答案是否准确
- 没有评估机制

问题4：性能问题
- 没有缓存
- 没有批处理
- 响应速度慢

问题5：不可扩展
- 代码耦合
- 难以添加新功能
- 难以维护
```

---

### 二、Advanced RAG架构

#### 2.1 架构优化

```
┌─────────────────────────────────────┐
│  Advanced RAG Architecture          │
└─────────────────────────────────────┘

【离线索引阶段】
┌─────────────┐
│  文档集合   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  预处理优化         │
│  • 文档清洗         │
│  • 格式统一         │
│  • OCR识别          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  智能分块           │
│  • 语义分块         │
│  • 保留结构         │
│  • 元数据增强       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  多路索引           │
│  • 密集向量         │
│  • 稀疏向量（BM25） │
│  • 元数据索引       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  混合存储           │
│  • 向量数据库       │
│  • 关系数据库       │
│  • 缓存层           │
└─────────────────────┘

【在线检索阶段】
┌─────────────────────┐
│  查询优化           │
│  • Query重写        │
│  • Query扩展        │
│  • 意图识别         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  混合检索           │
│  • 向量检索         │
│  • 关键词检索       │
│  • 元数据过滤       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  重排序（Re-rank）  │
│  • 相关性重排       │
│  • 多样性优化       │
│  • 质量筛选         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  上下文压缩         │
│  • 删除冗余         │
│  • 提取关键信息     │
│  • 控制长度         │
└──────┬──────────────┘

【生成阶段】
       │
       ▼
┌─────────────────────┐
│  Prompt工程         │
│  • 动态模板         │
│  • Few-shot示例     │
│  • 角色设定         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  LLM生成            │
│  • 流式输出         │
│  • 错误处理         │
│  • 幻觉检测         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  后处理             │
│  • 答案验证         │
│  • 格式化           │
│  • 溯源标注         │
└─────────────────────┘
```

#### 2.2 关键优化技术

**1. 查询优化（Query Enhancement）**

```python
class QueryOptimizer:
    """查询优化器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def optimize(self, query):
        """优化查询"""
        # 1. Query重写（让查询更清晰）
        rewritten = self._rewrite_query(query)
        
        # 2. Query扩展（增加同义词）
        expanded = self._expand_query(rewritten)
        
        return expanded
    
    def _rewrite_query(self, query):
        """重写查询"""
        prompt = f"""
        将以下用户查询重写为更适合检索的形式：
        
        原查询：{query}
        
        重写后的查询：
        """
        return self.llm.predict(prompt)
    
    def _expand_query(self, query):
        """扩展查询（增加同义词）"""
        prompt = f"""
        为以下查询生成3个相似的表达方式：
        
        原查询：{query}
        
        变体：
        1.
        2.
        3.
        """
        return self.llm.predict(prompt)

# 使用
optimizer = QueryOptimizer(llm)
optimized_query = optimizer.optimize("RAG是啥？")
# 优化后："什么是检索增强生成（RAG）技术？"
```

**2. 混合检索（Hybrid Retrieval）**

```python
from rank_bm25 import BM25Okapi

class HybridRetriever:
    """混合检索器"""
    
    def __init__(self, vectorstore, documents):
        self.vectorstore = vectorstore
        
        # 构建BM25索引
        tokenized_docs = [doc.page_content.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        self.documents = documents
    
    def retrieve(self, query, k=10, alpha=0.5):
        """混合检索
        
        Args:
            alpha: 向量检索权重（0-1），1-alpha为BM25权重
        """
        # 1. 向量检索
        vector_results = self.vectorstore.similarity_search_with_score(query, k=k*2)
        
        # 2. BM25检索
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_results = sorted(
            zip(self.documents, bm25_scores),
            key=lambda x: x[1],
            reverse=True
        )[:k*2]
        
        # 3. 融合结果
        scores = {}
        
        # 向量得分（归一化）
        max_vector_score = max([score for _, score in vector_results])
        for doc, score in vector_results:
            doc_id = id(doc)
            scores[doc_id] = {
                "doc": doc,
                "score": alpha * (score / max_vector_score)
            }
        
        # BM25得分（归一化）
        max_bm25_score = max([score for _, score in bm25_results])
        for doc, score in bm25_results:
            doc_id = id(doc)
            if doc_id in scores:
                scores[doc_id]["score"] += (1 - alpha) * (score / max_bm25_score)
            else:
                scores[doc_id] = {
                    "doc": doc,
                    "score": (1 - alpha) * (score / max_bm25_score)
                }
        
        # 4. 排序返回
        sorted_results = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )[:k]
        
        return [item["doc"] for item in sorted_results]
```

**3. 重排序（Re-ranking）**

```python
from sentence_transformers import CrossEncoder

class Reranker:
    """重排序器"""
    
    def __init__(self):
        # 使用交叉编码器模型
        self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    def rerank(self, query, documents, top_k=5):
        """重排序"""
        # 1. 构建query-document对
        pairs = [[query, doc.page_content] for doc in documents]
        
        # 2. 计算相关性分数
        scores = self.model.predict(pairs)
        
        # 3. 排序
        sorted_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )
        
        # 4. 返回top-k
        return [documents[i] for i in sorted_indices[:top_k]]

# 使用
reranker = Reranker()
reranked_docs = reranker.rerank(query, retrieved_docs, top_k=5)
```

**4. 上下文压缩（Context Compression）**

```python
class ContextCompressor:
    """上下文压缩器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def compress(self, query, documents, max_length=2000):
        """压缩上下文"""
        # 1. 提取每个文档的关键句子
        relevant_sentences = []
        
        for doc in documents:
            # 使用LLM提取与query相关的句子
            prompt = f"""
            从以下文档中，提取与问题相关的关键句子（不超过3句）：
            
            问题：{query}
            
            文档：
            {doc.page_content}
            
            关键句子：
            """
            
            key_sentences = self.llm.predict(prompt)
            relevant_sentences.append(key_sentences)
        
        # 2. 合并并控制长度
        compressed_context = "\n\n".join(relevant_sentences)
        
        # 3. 如果还是太长，进一步压缩
        if len(compressed_context) > max_length:
            compressed_context = compressed_context[:max_length]
        
        return compressed_context
```

#### 2.3 Advanced RAG完整实现

```python
class AdvancedRAG:
    """高级RAG系统"""
    
    def __init__(self):
        # 初始化组件
        self.vectorstore = None
        self.llm = None
        self.query_optimizer = QueryOptimizer(self.llm)
        self.hybrid_retriever = None
        self.reranker = Reranker()
        self.compressor = ContextCompressor(self.llm)
    
    def index(self, documents):
        """索引文档"""
        # 1. 智能分块
        chunks = self._smart_chunking(documents)
        
        # 2. 构建向量库
        self.vectorstore = Chroma.from_documents(chunks, embeddings)
        
        # 3. 构建混合检索器
        self.hybrid_retriever = HybridRetriever(self.vectorstore, chunks)
    
    def query(self, question, k=5):
        """查询"""
        # 1. 查询优化
        optimized_query = self.query_optimizer.optimize(question)
        
        # 2. 混合检索
        retrieved_docs = self.hybrid_retriever.retrieve(optimized_query, k=k*2)
        
        # 3. 重排序
        reranked_docs = self.reranker.rerank(optimized_query, retrieved_docs, top_k=k)
        
        # 4. 上下文压缩
        compressed_context = self.compressor.compress(optimized_query, reranked_docs)
        
        # 5. 构建Prompt
        prompt = self._build_prompt(question, compressed_context)
        
        # 6. LLM生成
        answer = self.llm.predict(prompt)
        
        # 7. 后处理
        final_answer = self._post_process(answer, reranked_docs)
        
        return final_answer
    
    def _build_prompt(self, question, context):
        """构建Prompt"""
        return f"""
基于以下上下文回答问题：

上下文：
{context}

问题：{question}

请基于上下文给出准确的答案。如果上下文中没有相关信息，请说"我不知道"。

答案：
"""
```

---

### 三、Modular RAG架构

#### 3.1 模块化设计原则

```
核心原则：
1. 单一职责：每个模块只负责一件事
2. 接口清晰：模块间通过接口通信
3. 松耦合：模块可以独立修改和测试
4. 可扩展：容易添加新模块
5. 可配置：行为可以通过配置改变
```

#### 3.2 Modular RAG架构图

```
┌─────────────────────────────────────────────┐
│          Modular RAG System                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  【Document Processing Pipeline】           │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Loader  │→ │  Parser  │→ │ Chunker  │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│       ↓             ↓             ↓         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Metadata │→ │ Enricher │→ │ Indexer  │ │
│  │Extractor │  │          │  │          │ │
│  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  【Query Processing Pipeline】              │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Query   │→ │  Query   │→ │  Query   │ │
│  │Validator │  │Optimizer │  │Expander  │ │
│  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  【Retrieval Pipeline】                     │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Vector   │→ │  Hybrid  │→ │ Reranker │ │
│  │Retriever │  │Retriever │  │          │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│       ↓             ↓             ↓         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Filter  │→ │Compressor│→ │Selector  │ │
│  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  【Generation Pipeline】                    │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Prompt   │→ │   LLM    │→ │  Post    │ │
│  │ Builder  │  │Generator │  │Processor │ │
│  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  【Support Modules】                        │
│                                             │
│  • Storage (Vector DB, Cache, Index)       │
│  • Monitor (Logging, Metrics, Tracing)     │
│  • Config (Settings, Profiles)             │
└─────────────────────────────────────────────┘
```

#### 3.3 模块化实现

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# ============= 基础接口 =============

class Pipeline(ABC):
    """Pipeline基类"""
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """处理数据"""
        pass

class Component(ABC):
    """组件基类"""
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """执行组件逻辑"""
        pass

# ============= 文档处理Pipeline =============

class DocumentProcessor(Pipeline):
    """文档处理Pipeline"""
    
    def __init__(self):
        self.components = []
    
    def add_component(self, component: Component):
        """添加组件"""
        self.components.append(component)
        return self
    
    def process(self, documents: List) -> List:
        """处理文档"""
        result = documents
        for component in self.components:
            result = component.execute(result)
        return result

# 具体组件
class LoaderComponent(Component):
    """文档加载组件"""
    
    def execute(self, file_paths: List[str]) -> List:
        """加载文档"""
        # 实现加载逻辑
        pass

class ChunkerComponent(Component):
    """分块组件"""
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def execute(self, documents: List) -> List:
        """分块"""
        # 实现分块逻辑
        pass

class MetadataExtractorComponent(Component):
    """元数据提取组件"""
    
    def execute(self, documents: List) -> List:
        """提取元数据"""
        # 实现元数据提取逻辑
        pass

# ============= 检索Pipeline =============

class RetrievalPipeline(Pipeline):
    """检索Pipeline"""
    
    def __init__(self):
        self.components = []
    
    def add_component(self, component: Component):
        self.components.append(component)
        return self
    
    def process(self, query: str) -> List:
        """执行检索"""
        result = query
        for component in self.components:
            result = component.execute(result)
        return result

class VectorRetrieverComponent(Component):
    """向量检索组件"""
    
    def __init__(self, vectorstore, k=10):
        self.vectorstore = vectorstore
        self.k = k
    
    def execute(self, query: str) -> List:
        """向量检索"""
        return self.vectorstore.similarity_search(query, k=self.k)

class RerankerComponent(Component):
    """重排序组件"""
    
    def __init__(self, reranker):
        self.reranker = reranker
    
    def execute(self, data: Dict) -> Dict:
        """重排序"""
        query = data["query"]
        documents = data["documents"]
        
        reranked = self.reranker.rerank(query, documents)
        return {
            "query": query,
            "documents": reranked
        }

# ============= 模块化RAG系统 =============

class ModularRAGSystem:
    """模块化RAG系统"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # 构建各个Pipeline
        self.doc_pipeline = self._build_doc_pipeline()
        self.query_pipeline = self._build_query_pipeline()
        self.retrieval_pipeline = self._build_retrieval_pipeline()
        self.generation_pipeline = self._build_generation_pipeline()
    
    def _build_doc_pipeline(self):
        """构建文档处理Pipeline"""
        pipeline = DocumentProcessor()
        
        # 根据配置添加组件
        if self.config.get("enable_ocr"):
            pipeline.add_component(OCRComponent())
        
        pipeline.add_component(ChunkerComponent(
            chunk_size=self.config.get("chunk_size", 1000)
        ))
        
        pipeline.add_component(MetadataExtractorComponent())
        
        return pipeline
    
    def _build_retrieval_pipeline(self):
        """构建检索Pipeline"""
        pipeline = RetrievalPipeline()
        
        # 添加检索组件
        pipeline.add_component(VectorRetrieverComponent(
            vectorstore=self.vectorstore,
            k=self.config.get("retrieval_k", 10)
        ))
        
        # 如果启用重排序
        if self.config.get("enable_rerank"):
            pipeline.add_component(RerankerComponent(self.reranker))
        
        return pipeline
    
    def index(self, documents):
        """索引文档"""
        processed_docs = self.doc_pipeline.process(documents)
        # 构建向量库
        # ...
    
    def query(self, question):
        """查询"""
        # 1. 查询处理
        processed_query = self.query_pipeline.process(question)
        
        # 2. 检索
        retrieved_docs = self.retrieval_pipeline.process(processed_query)
        
        # 3. 生成
        answer = self.generation_pipeline.process({
            "query": processed_query,
            "documents": retrieved_docs
        })
        
        return answer
```

---

### 四、架构设计原则

#### 4.1 设计原则

```python
1. 单一职责原则（SRP）
   - 每个类/模块只负责一件事
   - 易于理解和维护

2. 开闭原则（OCP）
   - 对扩展开放，对修改关闭
   - 新功能通过添加代码实现，而不是修改现有代码

3. 依赖倒置原则（DIP）
   - 依赖抽象，不依赖具体实现
   - 使用接口/抽象类

4. 接口隔离原则（ISP）
   - 接口要小而专注
   - 不要强迫实现不需要的方法

5. 里氏替换原则（LSP）
   - 子类可以替换父类
   - 保证多态性
```

#### 4.2 架构模式

**1. Pipeline模式**

```python
# 数据流式处理
data → Component1 → Component2 → Component3 → result

优点：
- 清晰的数据流
- 组件可以独立测试
- 容易添加新组件
```

**2. Strategy模式**

```python
# 不同策略可以互换
class RetrieverStrategy(ABC):
    @abstractmethod
    def retrieve(self, query):
        pass

class VectorRetriever(RetrieverStrategy):
    def retrieve(self, query):
        # 向量检索
        pass

class HybridRetriever(RetrieverStrategy):
    def retrieve(self, query):
        # 混合检索
        pass

# 使用
retriever: RetrieverStrategy = VectorRetriever()  # 可以轻松切换
results = retriever.retrieve(query)
```

**3. Factory模式**

```python
class ComponentFactory:
    """组件工厂"""
    
    @staticmethod
    def create_retriever(type: str, **kwargs):
        """创建检索器"""
        if type == "vector":
            return VectorRetriever(**kwargs)
        elif type == "hybrid":
            return HybridRetriever(**kwargs)
        elif type == "bm25":
            return BM25Retriever(**kwargs)
        else:
            raise ValueError(f"Unknown retriever type: {type}")

# 使用
retriever = ComponentFactory.create_retriever("hybrid", alpha=0.5)
```

---

## 💻 实战案例

### 案例：可扩展的企业级RAG架构

**需求**：
- 支持多种文档格式
- 支持多种检索策略
- 易于扩展新功能
- 性能可监控
- 配置化管理

**完整架构实现**：

```python
# config.py
class RAGConfig:
    """RAG系统配置"""
    
    # 文档处理
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    ENABLE_OCR = True
    
    # 检索配置
    RETRIEVAL_TYPE = "hybrid"  # vector, bm25, hybrid
    RETRIEVAL_K = 10
    ENABLE_RERANK = True
    RERANK_TOP_K = 5
    
    # 生成配置
    LLM_MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0
    MAX_TOKENS = 500
    
    # 性能配置
    ENABLE_CACHE = True
    CACHE_TTL = 3600

# modular_rag.py
class EnterpriseRAGSystem:
    """企业级模块化RAG系统"""
    
    def __init__(self, config: RAGConfig):
        self.config = config
        
        # 初始化各个Pipeline
        self.doc_processor = self._create_doc_processor()
        self.retriever = self._create_retriever()
        self.generator = self._create_generator()
        
        # 监控
        self.metrics = MetricsCollector()
    
    def _create_doc_processor(self):
        """创建文档处理器"""
        processor = DocumentProcessor()
        
        # 动态添加组件
        processor.add_component(LoaderComponent())
        
        if self.config.ENABLE_OCR:
            processor.add_component(OCRComponent())
        
        processor.add_component(ChunkerComponent(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
        ))
        
        processor.add_component(MetadataExtractorComponent())
        
        return processor
    
    def _create_retriever(self):
        """创建检索器"""
        return ComponentFactory.create_retriever(
            type=self.config.RETRIEVAL_TYPE,
            k=self.config.RETRIEVAL_K
        )
    
    def index(self, documents):
        """索引文档"""
        with self.metrics.timer("indexing"):
            processed_docs = self.doc_processor.process(documents)
            # 构建向量库
            # ...
        
        self.metrics.increment("documents_indexed", len(processed_docs))
    
    def query(self, question):
        """查询"""
        with self.metrics.timer("query"):
            # 检索
            docs = self.retriever.retrieve(question)
            
            # 生成
            answer = self.generator.generate(question, docs)
            
            return answer
```

---

## 📝 课后练习

### 练习1：实现自己的Pipeline

设计一个可配置的文档处理Pipeline

### 练习2：添加新的检索策略

实现一个基于图的检索策略

### 练习3：性能优化

为RAG系统添加缓存层

---

## 🎓 知识总结

### 核心要点

1. **三种RAG架构**
   - Naive RAG：简单直接
   - Advanced RAG：各种优化
   - Modular RAG：模块化设计

2. **关键优化技术**
   - 查询优化
   - 混合检索
   - 重排序
   - 上下文压缩

3. **设计原则**
   - 单一职责
   - 开闭原则
   - 依赖倒置
   - 接口隔离

4. **架构模式**
   - Pipeline模式
   - Strategy模式
   - Factory模式

### 最佳实践

✅ 模块化设计
✅ 接口清晰
✅ 配置化管理
✅ 性能监控
✅ 易于扩展

---

## 🚀 下节预告

下一课：**第55课：基础RAG实现：从零开发**

- 完整实现一个基础RAG系统
- 每个步骤详细讲解
- 可运行的完整代码
- 性能测试和优化

**动手实现你的第一个RAG系统！** 🛠️

---

**💪 记住：好的架构是RAG系统成功的基础！**

**下一课见！** 🎉
