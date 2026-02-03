![RAG高级检索流程](./images/rag_flow.svg)
*图：RAG高级检索流程*

# 第64课：Parent Document Retriever

> **本课目标**：掌握Parent Document Retriever技术，平衡检索精度和上下文完整性
> 
> **核心技能**：小块检索、大块返回、层级文档管理
> 
> **实战案例**：智能文档检索系统
> 
> **学习时长**：75分钟

---

## 📖 口播文案（5分钟）
![Hyde](./images/hyde.svg)
*图：Hyde*


### 🎯 前言

"做RAG系统时，我遇到过一个很纠结的问题：

**文档分块的粒度怎么选？**

**选小块（200字）：**
- ✅ 优点：检索精准，能精确定位相关段落
- ❌ 缺点：上下文不完整，LLM看不懂

例子：
```
用户问："深度学习的反向传播算法原理是什么？"

检索到：
"反向传播算法计算梯度，更新权重..."
```

LLM说："上下文不够，无法完整回答"

**选大块（1000字）：**
- ✅ 优点：上下文完整，LLM能理解
- ❌ 缺点：检索不精准，很多无关内容

例子：
```
检索到一大段：
"深度学习是机器学习的分支...（500字无关内容）...
反向传播算法计算梯度...（终于到重点了）...
还有其他很多内容...（又是无关的）"
```

LLM被大量无关内容干扰，答案质量下降。

**这就是经典的两难问题：**

```
小块检索 → 精准但上下文不足 ❌
大块检索 → 上下文足但不精准 ❌
```

**有没有办法两全其美？**

**有！这就是Parent Document Retriever！**

**核心思想超级巧妙：**

```
1. 索引时：用小块（200字）建索引
   → 保证检索精度

2. 检索时：用小块找到相关内容
   → 精准定位

3. 返回时：返回小块所属的大块（完整段落/章节）
   → 上下文完整
```

**举个真实例子：**

文档结构：
```
【章节】深度学习基础（大块，2000字）
  ├─ 【段落1】什么是深度学习（小块，200字）
  ├─ 【段落2】神经网络结构（小块，300字）
  ├─ 【段落3】反向传播算法（小块，400字）  ← 检索命中这里
  └─ 【段落4】优化算法（小块，200字）
```

传统检索：
- 只返回段落3（400字）
- 上下文不足

Parent Document Retriever：
- 检索命中段落3
- 返回整个章节（2000字）
- 上下文完整！

**效果对比：**

| 方法 | 检索精度 | 上下文完整性 | 答案质量 |
|------|---------|-------------|---------|
| 小块检索 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 大块检索 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Parent Document** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**但是，实现起来有挑战！**

**挑战1：如何建立parent-child关系？**
- 需要记录每个小块的父文档
- 数据结构设计要合理

**挑战2：返回多个parent会重复？**
- 多个小块可能属于同一个parent
- 需要去重

**挑战3：parent太大怎么办？**
- 完整章节可能有5000字
- 超过LLM上下文长度
- 需要智能截取

**今天这一课，我要教你：**

**第一部分：Parent Document原理**
- 层级文档结构
- Parent-Child关系
- 检索流程

**第二部分：核心实现**
- 文档分层
- 索引构建
- 检索逻辑

**第三部分：高级策略**
- 多级层级
- 智能截取
- 动态选择

**第四部分：性能优化**
- 去重策略
- 缓存优化
- 并发处理

**第五部分：生产实战**
- 完整系统
- 效果评估
- 最佳实践

学完这一课，你的RAG系统将同时拥有精准性和完整性！

准备好了吗？让我们开始！"

---

### 💡 核心概念

```
【Parent-Child文档层级】

Level 0: 完整文档
  └─ Level 1: 章节（Parent）
      ├─ Level 2: 段落（Child，用于检索）
      └─ Level 2: 段落（Child，用于检索）

【检索流程】

1. 用Child（小块）建索引
   → 检索精度高

2. 用Child检索
   → 精准定位

3. 返回Parent（大块）
   → 上下文完整

【关键设计】

Child Document:
- 用于检索（小，精准）
- 包含parent_id引用

Parent Document:
- 用于返回（大，完整）
- 包含完整上下文
```

---

## 📚 第一部分：Parent Document原理

### 一、文档层级结构

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class DocumentLevel(Enum):
    """文档层级"""
    DOCUMENT = "文档"     # 完整文档
    CHAPTER = "章节"      # 章节
    SECTION = "段落"      # 段落
    CHUNK = "块"          # 最小块

@dataclass
class Document:
    """文档基类"""
    content: str
    doc_id: str
    level: DocumentLevel
    metadata: dict

@dataclass
class ChildDocument(Document):
    """子文档（用于检索）"""
    parent_id: str                    # 父文档ID
    position: int                     # 在父文档中的位置
    
@dataclass
class ParentDocument(Document):
    """父文档（用于返回）"""
    children_ids: List[str]           # 子文档ID列表

class DocumentHierarchy:
    """文档层级管理器"""
    
    def __init__(self):
        self.parents = {}  # parent_id -> ParentDocument
        self.children = {}  # child_id -> ChildDocument
    
    def add_parent(self, parent: ParentDocument):
        """添加父文档"""
        self.parents[parent.doc_id] = parent
    
    def add_child(self, child: ChildDocument):
        """添加子文档"""
        self.children[child.doc_id] = child
    
    def get_parent(self, child_id: str) -> Optional[ParentDocument]:
        """通过子文档ID获取父文档"""
        child = self.children.get(child_id)
        if child:
            return self.parents.get(child.parent_id)
        return None
    
    def get_children(self, parent_id: str) -> List[ChildDocument]:
        """获取父文档的所有子文档"""
        return [
            child for child in self.children.values()
            if child.parent_id == parent_id
        ]

# 示例
def demo_document_hierarchy():
    """演示文档层级"""
    
    hierarchy = DocumentHierarchy()
    
    # 父文档（章节）
    parent = ParentDocument(
        content="深度学习是机器学习的一个分支...(完整章节2000字)",
        doc_id="chapter_1",
        level=DocumentLevel.CHAPTER,
        metadata={"title": "深度学习基础"},
        children_ids=["chunk_1_1", "chunk_1_2", "chunk_1_3"]
    )
    hierarchy.add_parent(parent)
    
    # 子文档（段落）
    children = [
        ChildDocument(
            content="深度学习是机器学习的一个分支，使用多层神经网络...",
            doc_id="chunk_1_1",
            level=DocumentLevel.CHUNK,
            metadata={},
            parent_id="chapter_1",
            position=0
        ),
        ChildDocument(
            content="神经网络由多个层组成，包括输入层、隐藏层和输出层...",
            doc_id="chunk_1_2",
            level=DocumentLevel.CHUNK,
            metadata={},
            parent_id="chapter_1",
            position=1
        ),
        ChildDocument(
            content="反向传播算法用于计算梯度，更新网络权重...",
            doc_id="chunk_1_3",
            level=DocumentLevel.CHUNK,
            metadata={},
            parent_id="chapter_1",
            position=2
        )
    ]
    
    for child in children:
        hierarchy.add_child(child)
    
    print("="*60)
    print("文档层级结构")
    print("="*60)
    
    print(f"\n父文档: {parent.doc_id}")
    print(f"  内容: {parent.content[:50]}...")
    print(f"  子文档数: {len(parent.children_ids)}")
    
    print(f"\n子文档:")
    for child in children:
        print(f"  - {child.doc_id}")
        print(f"    位置: {child.position}")
        print(f"    内容: {child.content[:40]}...")
    
    # 通过子文档获取父文档
    print(f"\n通过子文档获取父文档:")
    retrieved_parent = hierarchy.get_parent("chunk_1_2")
    print(f"  子文档: chunk_1_2")
    print(f"  父文档: {retrieved_parent.doc_id}")
    print(f"  父文档内容: {retrieved_parent.content[:50]}...")

demo_document_hierarchy()
```

---

## 💻 第二部分：核心实现

### 一、文档分层处理器

```python
class HierarchicalDocumentProcessor:
    """层级文档处理器"""
    
    def __init__(
        self,
        child_chunk_size: int = 200,
        parent_chunk_size: int = 1000,
        overlap: int = 50
    ):
        self.child_chunk_size = child_chunk_size
        self.parent_chunk_size = parent_chunk_size
        self.overlap = overlap
    
    def process_document(
        self,
        content: str,
        doc_id: str
    ) -> tuple[List[ParentDocument], List[ChildDocument]]:
        """
        处理文档，生成层级结构
        
        策略：
        1. 先按parent_chunk_size分大块
        2. 每个大块再分成小块
        3. 建立parent-child关系
        """
        parents = []
        children = []
        
        # 1. 分大块（parent）
        parent_chunks = self._split_text(
            content,
            self.parent_chunk_size,
            self.overlap
        )
        
        for p_idx, parent_chunk in enumerate(parent_chunks):
            parent_id = f"{doc_id}_parent_{p_idx}"
            
            # 2. 分小块（children）
            child_chunks = self._split_text(
                parent_chunk,
                self.child_chunk_size,
                self.overlap // 2
            )
            
            children_ids = []
            
            for c_idx, child_chunk in enumerate(child_chunks):
                child_id = f"{parent_id}_child_{c_idx}"
                children_ids.append(child_id)
                
                # 创建子文档
                child = ChildDocument(
                    content=child_chunk,
                    doc_id=child_id,
                    level=DocumentLevel.CHUNK,
                    metadata={},
                    parent_id=parent_id,
                    position=c_idx
                )
                children.append(child)
            
            # 创建父文档
            parent = ParentDocument(
                content=parent_chunk,
                doc_id=parent_id,
                level=DocumentLevel.CHAPTER,
                metadata={},
                children_ids=children_ids
            )
            parents.append(parent)
        
        return parents, children
    
    def _split_text(
        self,
        text: str,
        chunk_size: int,
        overlap: int
    ) -> List[str]:
        """分割文本"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # 尝试在句子结束处切分
            if end < text_length:
                for sep in ['。', '！', '？', '\n\n']:
                    pos = text.rfind(sep, start, end)
                    if pos != -1:
                        end = pos + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap if end < text_length else text_length
        
        return chunks

# 使用示例
def demo_hierarchical_processor():
    """演示层级处理"""
    
    processor = HierarchicalDocumentProcessor(
        child_chunk_size=200,
        parent_chunk_size=600,
        overlap=50
    )
    
    # 示例文档
    content = """
    深度学习是机器学习的一个重要分支，它使用多层神经网络来学习数据的表示。
    深度学习在图像识别、语音识别、自然语言处理等领域取得了巨大成功。
    
    神经网络是深度学习的基础，它由多个层组成，包括输入层、隐藏层和输出层。
    每一层都包含多个神经元，神经元之间通过权重连接。
    前向传播过程将输入数据通过各层传递，最终产生输出。
    
    反向传播算法是训练神经网络的核心算法。
    它通过计算损失函数对权重的梯度，使用梯度下降法更新权重。
    反向传播算法使得深度神经网络的训练成为可能。
    
    优化算法如SGD、Adam等用于加速训练过程。
    这些算法通过自适应学习率等技术提高训练效率。
    """ * 2  # 重复以生成更长文本
    
    parents, children = processor.process_document(content, "doc_1")
    
    print("="*60)
    print("层级文档处理")
    print("="*60)
    
    print(f"\n原始文档: {len(content)}字")
    print(f"父文档数: {len(parents)}")
    print(f"子文档数: {len(children)}")
    
    print("\n父文档:")
    for i, parent in enumerate(parents):
        print(f"\n  {i+1}. {parent.doc_id}")
        print(f"     长度: {len(parent.content)}字")
        print(f"     子文档数: {len(parent.children_ids)}")
        print(f"     内容预览: {parent.content[:60]}...")
    
    print("\n子文档:")
    for i, child in enumerate(children[:5]):  # 只显示前5个
        print(f"\n  {i+1}. {child.doc_id}")
        print(f"     父文档: {child.parent_id}")
        print(f"     位置: {child.position}")
        print(f"     长度: {len(child.content)}字")
        print(f"     内容: {child.content[:50]}...")

demo_hierarchical_processor()
```

### 二、Parent Document Retriever实现

```python
from sentence_transformers import SentenceTransformer
from typing import Set

class ParentDocumentRetriever:
    """Parent Document检索器"""
    
    def __init__(
        self,
        embedding_model: str = "moka-ai/m3e-base"
    ):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.hierarchy = DocumentHierarchy()
        
        # 子文档的embedding（用于检索）
        self.child_embeddings = {}
        self.child_docs = []
    
    def index_documents(
        self,
        parents: List[ParentDocument],
        children: List[ChildDocument]
    ):
        """索引文档"""
        print("📚 索引层级文档...")
        
        # 1. 存储层级关系
        for parent in parents:
            self.hierarchy.add_parent(parent)
        
        for child in children:
            self.hierarchy.add_child(child)
        
        # 2. 只索引子文档
        self.child_docs = children
        child_contents = [child.content for child in children]
        
        print(f"  编码 {len(child_contents)} 个子文档...")
        child_embs = self.embedding_model.encode(child_contents)
        
        for child, emb in zip(children, child_embs):
            self.child_embeddings[child.doc_id] = emb
        
        print(f"  ✅ 索引完成")
        print(f"     父文档数: {len(parents)}")
        print(f"     子文档数: {len(children)}")
    
    def retrieve(
        self,
        query: str,
        k: int = 3,
        return_children: bool = False,
        verbose: bool = False
    ) -> List[ParentDocument]:
        """
        检索
        
        流程：
        1. 用子文档检索（精准）
        2. 获取对应的父文档（完整）
        3. 去重并返回
        """
        if verbose:
            print("\n" + "="*60)
            print("🔍 Parent Document检索")
            print("="*60)
            print(f"Query: {query}\n")
        
        # 1. 编码查询
        query_emb = self.embedding_model.encode([query])[0]
        
        # 2. 检索子文档
        if verbose:
            print("【步骤1】检索子文档")
        
        child_scores = []
        for child in self.child_docs:
            child_emb = self.child_embeddings[child.doc_id]
            score = np.dot(query_emb, child_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(child_emb)
            )
            child_scores.append((child, score))
        
        child_scores.sort(key=lambda x: x[1], reverse=True)
        top_children = child_scores[:k*2]  # 多检索一些，因为可能去重
        
        if verbose:
            print(f"  检索到 {len(top_children)} 个子文档")
            for i, (child, score) in enumerate(top_children[:3]):
                print(f"    {i+1}. [{score:.3f}] {child.doc_id}")
                print(f"       {child.content[:50]}...")
        
        # 3. 获取父文档（去重）
        if verbose:
            print(f"\n【步骤2】获取父文档并去重")
        
        seen_parent_ids: Set[str] = set()
        parent_results = []
        
        for child, score in top_children:
            parent = self.hierarchy.get_parent(child.doc_id)
            
            if parent and parent.doc_id not in seen_parent_ids:
                seen_parent_ids.add(parent.doc_id)
                parent_results.append((parent, score))
                
                if len(parent_results) >= k:
                    break
        
        if verbose:
            print(f"  去重后: {len(parent_results)} 个父文档")
        
        # 4. 显示结果
        if verbose:
            print(f"\n【步骤3】返回Top-{len(parent_results)}父文档")
            for i, (parent, score) in enumerate(parent_results):
                print(f"\n  {i+1}. {parent.doc_id} [分数={score:.3f}]")
                print(f"     长度: {len(parent.content)}字")
                print(f"     子文档数: {len(parent.children_ids)}")
                print(f"     内容: {parent.content[:80]}...")
        
        if return_children:
            return [(parent, score, [
                self.hierarchy.children[cid] 
                for cid in parent.children_ids
            ]) for parent, score in parent_results]
        
        return [parent for parent, _ in parent_results]

# 完整示例
def demo_parent_document_retriever():
    """演示Parent Document检索"""
    
    # 1. 准备文档
    content = """
    深度学习基础
    
    深度学习是机器学习的一个重要分支。它使用多层神经网络来学习数据的深层表示。
    与传统机器学习方法相比，深度学习能够自动学习特征，不需要人工设计特征。
    深度学习在图像识别、语音识别、自然语言处理等领域取得了革命性的突破。
    
    神经网络结构
    
    神经网络是深度学习的基础模型。一个典型的神经网络由输入层、多个隐藏层和输出层组成。
    每一层包含多个神经元，神经元之间通过权重连接。
    前向传播过程将输入数据逐层传递，每层对数据进行非线性变换。
    激活函数如ReLU、Sigmoid等引入非线性，使网络能够学习复杂的模式。
    
    反向传播算法
    
    反向传播是训练神经网络的核心算法。它基于链式法则计算损失函数对每个权重的梯度。
    算法从输出层开始，逆向计算每一层的梯度，然后使用梯度下降法更新权重。
    学习率是控制权重更新幅度的重要超参数。
    通过多次迭代，网络逐渐学习到数据的模式。
    
    优化技术
    
    现代深度学习使用各种优化技术来加速训练。
    批归一化可以稳定训练过程，加速收敛。
    Dropout通过随机丢弃神经元来防止过拟合。
    数据增强通过变换原始数据来扩充训练集。
    这些技术共同提升了深度学习模型的性能和泛化能力。
    """
    
    # 2. 处理文档
    processor = HierarchicalDocumentProcessor(
        child_chunk_size=150,
        parent_chunk_size=500
    )
    
    parents, children = processor.process_document(content, "doc_1")
    
    # 3. 创建检索器
    retriever = ParentDocumentRetriever()
    retriever.index_documents(parents, children)
    
    # 4. 测试检索
    queries = [
        "反向传播算法是什么？",
        "如何防止神经网络过拟合？"
    ]
    
    for query in queries:
        print("\n" + "🔍"*30)
        results = retriever.retrieve(query, k=2, verbose=True)
        print("🔍"*30)

demo_parent_document_retriever()
```

---

## 🎯 第三部分：高级策略

### 一、多级层级

```python
class MultiLevelHierarchy:
    """多级层级管理"""
    
    def __init__(self):
        self.documents = {}  # doc_id -> Document
        self.parent_map = {}  # child_id -> parent_id
        self.children_map = {}  # parent_id -> [child_ids]
    
    def add_document(
        self,
        doc: Document,
        parent_id: Optional[str] = None
    ):
        """添加文档"""
        self.documents[doc.doc_id] = doc
        
        if parent_id:
            self.parent_map[doc.doc_id] = parent_id
            
            if parent_id not in self.children_map:
                self.children_map[parent_id] = []
            self.children_map[parent_id].append(doc.doc_id)
    
    def get_ancestors(
        self,
        doc_id: str,
        max_level: int = None
    ) -> List[Document]:
        """获取所有祖先文档"""
        ancestors = []
        current_id = doc_id
        level = 0
        
        while current_id in self.parent_map:
            if max_level and level >= max_level:
                break
            
            parent_id = self.parent_map[current_id]
            ancestors.append(self.documents[parent_id])
            current_id = parent_id
            level += 1
        
        return ancestors
    
    def get_context_window(
        self,
        doc_id: str,
        window_size: int = 1
    ) -> List[Document]:
        """
        获取上下文窗口
        
        返回该文档及其前后window_size个兄弟文档
        """
        # 获取父文档
        if doc_id not in self.parent_map:
            return [self.documents[doc_id]]
        
        parent_id = self.parent_map[doc_id]
        siblings = self.children_map[parent_id]
        
        # 找到当前文档位置
        try:
            idx = siblings.index(doc_id)
        except ValueError:
            return [self.documents[doc_id]]
        
        # 获取窗口范围
        start = max(0, idx - window_size)
        end = min(len(siblings), idx + window_size + 1)
        
        return [
            self.documents[sib_id]
            for sib_id in siblings[start:end]
        ]
```

### 二、智能截取策略

```python
class SmartContextExtractor:
    """智能上下文提取器"""
    
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
    
    def extract_context(
        self,
        matched_child: ChildDocument,
        parent: ParentDocument,
        query: str,
        strategy: str = "expand"
    ) -> str:
        """
        智能提取上下文
        
        策略：
        - expand: 从匹配位置向两边扩展
        - focus: 只保留匹配位置附近
        - full: 返回完整parent（如果不超长）
        """
        parent_content = parent.content
        
        # 如果parent不超长，直接返回
        if len(parent_content) <= self.max_tokens:
            return parent_content
        
        if strategy == "expand":
            return self._expand_strategy(
                matched_child,
                parent,
                query
            )
        elif strategy == "focus":
            return self._focus_strategy(
                matched_child,
                parent
            )
        else:
            # 截取前max_tokens
            return parent_content[:self.max_tokens]
    
    def _expand_strategy(
        self,
        matched_child: ChildDocument,
        parent: ParentDocument,
        query: str
    ) -> str:
        """
        扩展策略：从匹配位置向两边扩展
        """
        # 找到child在parent中的位置
        child_pos = parent.content.find(matched_child.content)
        
        if child_pos == -1:
            return parent.content[:self.max_tokens]
        
        # 计算可用的左右空间
        left_space = self.max_tokens // 3
        right_space = self.max_tokens // 3
        center_space = self.max_tokens - left_space - right_space
        
        # 提取
        start = max(0, child_pos - left_space)
        end = min(len(parent.content), child_pos + len(matched_child.content) + right_space)
        
        extracted = parent.content[start:end]
        
        # 添加省略号
        if start > 0:
            extracted = "..." + extracted
        if end < len(parent.content):
            extracted = extracted + "..."
        
        return extracted
    
    def _focus_strategy(
        self,
        matched_child: ChildDocument,
        parent: ParentDocument
    ) -> str:
        """
        聚焦策略：只保留匹配位置附近
        """
        child_pos = parent.content.find(matched_child.content)
        
        if child_pos == -1:
            return parent.content[:self.max_tokens]
        
        # 以匹配位置为中心提取
        half_tokens = self.max_tokens // 2
        start = max(0, child_pos - half_tokens)
        end = min(len(parent.content), child_pos + half_tokens)
        
        return parent.content[start:end]
```

---

## ⚡ 第四部分：生产级实现

### 完整的Parent Document系统

```python
class ProductionParentDocumentRetriever:
    """生产级Parent Document检索器"""
    
    def __init__(
        self,
        embedding_model: str = "moka-ai/m3e-base",
        child_chunk_size: int = 200,
        parent_chunk_size: int = 1000,
        max_context_tokens: int = 2000
    ):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.processor = HierarchicalDocumentProcessor(
            child_chunk_size=child_chunk_size,
            parent_chunk_size=parent_chunk_size
        )
        self.context_extractor = SmartContextExtractor(
            max_tokens=max_context_tokens
        )
        
        self.hierarchy = DocumentHierarchy()
        self.child_embeddings = {}
        self.child_docs = []
        
        # 性能指标
        self.metrics = {
            'total_queries': 0,
            'avg_parent_length': 0,
            'dedup_rate': 0
        }
    
    def index_document(self, content: str, doc_id: str):
        """索引单个文档"""
        parents, children = self.processor.process_document(content, doc_id)
        
        for parent in parents:
            self.hierarchy.add_parent(parent)
        
        for child in children:
            self.hierarchy.add_child(child)
            self.child_docs.append(child)
        
        # 编码子文档
        child_contents = [c.content for c in children]
        child_embs = self.embedding_model.encode(child_contents)
        
        for child, emb in zip(children, child_embs):
            self.child_embeddings[child.doc_id] = emb
    
    def retrieve(
        self,
        query: str,
        k: int = 3,
        context_strategy: str = "expand",
        verbose: bool = False
    ) -> List[str]:
        """检索并返回智能截取的上下文"""
        
        self.metrics['total_queries'] += 1
        
        # 1. 检索子文档
        query_emb = self.embedding_model.encode([query])[0]
        
        child_scores = []
        for child in self.child_docs:
            child_emb = self.child_embeddings[child.doc_id]
            score = np.dot(query_emb, child_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(child_emb)
            )
            child_scores.append((child, score))
        
        child_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 2. 获取父文档并去重
        seen_parents = set()
        contexts = []
        matched_children = []
        
        for child, score in child_scores[:k*2]:
            parent = self.hierarchy.get_parent(child.doc_id)
            
            if parent and parent.doc_id not in seen_parents:
                seen_parents.add(parent.doc_id)
                matched_children.append(child)
                
                # 3. 智能提取上下文
                context = self.context_extractor.extract_context(
                    child,
                    parent,
                    query,
                    strategy=context_strategy
                )
                contexts.append(context)
                
                if len(contexts) >= k:
                    break
        
        # 更新指标
        if contexts:
            avg_len = sum(len(c) for c in contexts) / len(contexts)
            self.metrics['avg_parent_length'] = avg_len
        
        dedup_rate = 1 - len(contexts) / min(k*2, len(child_scores))
        self.metrics['dedup_rate'] = dedup_rate
        
        if verbose:
            print(f"\n检索指标:")
            print(f"  返回上下文数: {len(contexts)}")
            print(f"  平均长度: {self.metrics['avg_parent_length']:.0f}字")
            print(f"  去重率: {dedup_rate:.1%}")
        
        return contexts
    
    def get_metrics(self) -> dict:
        """获取性能指标"""
        return self.metrics
```

---

## 📝 课后练习

### 练习1：动态层级
根据文档特点自动决定层级深度

### 练习2：混合检索
结合Parent Document和其他检索方式

### 练习3：增量更新
支持动态添加和更新文档

---

## 🎓 知识总结

### 核心要点

1. **Parent Document优势**
   - 检索精度高（小块索引）
   - 上下文完整（大块返回）
   - 两全其美

2. **关键技术**
   - 层级文档结构
   - Parent-Child映射
   - 智能去重

3. **实现策略**
   - 小块建索引
   - 大块返回
   - 智能截取

4. **最佳实践**
   - Child: 200-300字
   - Parent: 800-1200字
   - 监控去重率

---

## 🚀 下节预告

下一课：**第65课：实战-多策略RAG系统**

- 整合所有高级技术
- 自适应策略选择
- 完整生产系统

**把所有技术融会贯通！** 🎯

---

**💪 记住：Parent Document让RAG既精准又完整！**

**下一课见！** 🎉
