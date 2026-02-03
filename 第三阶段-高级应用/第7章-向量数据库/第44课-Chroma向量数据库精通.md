![向量数据库架构](./images/vector_db.svg)
*图：向量数据库架构*

# 第44课：Chroma向量数据库精通 - 最易用的向量数据库

> 📚 **课程信息**
> - 所属模块：第三模块 - 向量数据库与RAG系统  
> - 章节：第8章 - 向量数据库基础（第4/6课）
> - 学习目标：精通Chroma向量数据库的使用和优化
> - 预计时间：110-120分钟
> - 前置知识：第41-43课

---

## 📢 课程导入

### 前言

前面我们学了Embedding和本地部署，现在有个问题：**生成的向量存哪里？怎么快速检索？**

如果你想：
- 存储百万级文档向量
- 毫秒级相似度搜索
- 与Lang Chain无缝集成
- 简单易用，3行代码搞定

**Chroma就是你的最佳选择！**它是目前**最易用**的开源向量数据库，没有之一！

今天这课，我要带你彻底掌握Chroma，从基础到高级，从开发到生产！

---

### 核心价值点

**第一，Chroma是最适合入门的向量数据库。**

对比其他向量数据库：
```
Milvus：
  安装：复杂（Docker Compose）
  配置：繁琐（多个配置文件）
  学习曲线：陡峭

Chroma：
  安装：pip install chromadb（1行）
  配置：无需配置（开箱即用）
  学习曲线：平缓（3行代码就能用）
```

**这就是为什么90%的入门项目都用Chroma！**

**第二，易用不意味着功能弱。**

Chroma虽然简单，但功能完整：
- ✅ 支持多种距离度量（余弦、欧式、点积）
- ✅ 元数据过滤（where条件）
- ✅ 持久化存储
- ✅ 集合管理
- ✅ LangChain完美集成
- ✅ 分布式部署（Client/Server模式）

**能满足90%的应用场景！**

**第三，Chroma是RAG系统的最佳伴侣。**

LangChain + Chroma是最经典的组合：
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

# 3行代码搭建向量检索系统
embeddings = SentenceTransformerEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)
results = vectorstore.similarity_search("查询")
```

**简洁、优雅、高效！**

**第四，学会Chroma，其他向量数据库也能快速上手。**

向量数据库的核心概念都相似：
- 集合（Collection）
- 向量（Embeddings）
- 元数据（Metadata）
- 相似度搜索（Similarity Search）

**掌握Chroma，触类旁通！**

---

### 行动号召

今天这一课会教你：
- Chroma完整安装和配置
- 集合管理和数据操作
- 多种检索方式
- 元数据过滤技巧
- 持久化和备份
- 生产环境最佳实践

**学完这课，你就能构建完整的向量检索系统！**

---

## 📖 知识讲解

![Chroma向量检索](./images/similarity.svg)
*图：Chroma向量检索*


### 1. Chroma快速入门

#### 1.1 安装

```bash
# 安装Chroma
pip install chromadb

# 可选：安装额外依赖
pip install chromadb[server]  # 服务器模式
```

#### 1.2 3分钟上手

```python
import chromadb

# 1. 创建客户端（内存模式）
client = chromadb.Client()

# 2. 创建集合
collection = client.create_collection(name="my_collection")

# 3. 添加数据
collection.add(
    documents=["这是文档1", "这是文档2", "这是文档3"],
    ids=["id1", "id2", "id3"]
)

# 4. 搜索
results = collection.query(
    query_texts=["文档"],
    n_results=2
)

print(results)
```

---

### 2. 核心概念

#### 2.1 客户端模式

```python
# 模式1：内存模式（临时）
client = chromadb.Client()

# 模式2：持久化模式（推荐）
client = chromadb.PersistentClient(path="./chroma_db")

# 模式3：HTTP客户端（Client/Server）
client = chromadb.HttpClient(host="localhost", port=8000)
```

#### 2.2 集合（Collection）

```python
# 创建集合
collection = client.create_collection(
    name="documents",
    metadata={"description": "文档集合"}
)

# 获取集合
collection = client.get_collection(name="documents")

# 获取或创建
collection = client.get_or_create_collection(name="documents")

# 列出所有集合
collections = client.list_collections()
print([c.name for c in collections])

# 删除集合
client.delete_collection(name="documents")
```

#### 2.3 距离度量

```python
# 创建集合时指定距离度量
collection = client.create_collection(
    name="my_collection",
    metadata={
        "hnsw:space": "cosine"  # 余弦距离（默认）
        # 可选：l2（欧式距离）、ip（内积）
    }
)
```

---

### 3. 数据操作

#### 3.1 添加数据

```python
# 方式1：自动生成Embedding
collection.add(
    documents=["文档1", "文档2", "文档3"],
    ids=["id1", "id2", "id3"],
    metadatas=[
        {"source": "web", "date": "2024-01-01"},
        {"source": "pdf", "date": "2024-01-02"},
        {"source": "api", "date": "2024-01-03"}
    ]
)

# 方式2：提供自己的Embedding
import numpy as np

embeddings = [
    np.random.rand(384).tolist(),
    np.random.rand(384).tolist()
]

collection.add(
    embeddings=embeddings,
    documents=["文档1", "文档2"],
    ids=["id1", "id2"]
)

# 方式3：批量添加
documents = ["文档" + str(i) for i in range(1000)]
ids = ["id_" + str(i) for i in range(1000)]

collection.add(
    documents=documents,
    ids=ids
)
```

#### 3.2 查询数据

```python
# 获取所有数据
all_data = collection.get()
print(f"总数：{len(all_data['ids'])}")

# 按ID获取
specific_data = collection.get(
    ids=["id1", "id2"],
    include=["documents", "metadatas", "embeddings"]
)

# 按条件获取
filtered_data = collection.get(
    where={"source": "web"},
    limit=10
)
```

#### 3.3 更新和删除

```python
# 更新
collection.update(
    ids=["id1"],
    documents=["更新后的文档"],
    metadatas=[{"source": "updated"}]
)

# 删除（按ID）
collection.delete(ids=["id1", "id2"])

# 删除（按条件）
collection.delete(where={"source": "web"})

# 删除全部
collection.delete(where={})  # 小心使用！
```

---

### 4. 检索操作

#### 4.1 相似度搜索

```python
# 基础搜索
results = collection.query(
    query_texts=["人工智能"],
    n_results=5
)

print("结果：")
for i, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0])):
    print(f"{i+1}. [{dist:.4f}] {doc}")

# 使用自定义Embedding搜索
query_embedding = model.encode(["人工智能"])[0].tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)
```

#### 4.2 元数据过滤

```python
# where条件（精确匹配）
results = collection.query(
    query_texts=["人工智能"],
    n_results=5,
    where={"source": "web"}
)

# where_document（文档内容过滤）
results = collection.query(
    query_texts=["AI"],
    n_results=5,
    where_document={"$contains": "机器学习"}
)

# 组合条件
results = collection.query(
    query_texts=["AI"],
    n_results=5,
    where={
        "$and": [
            {"source": "web"},
            {"date": {"$gte": "2024-01-01"}}
        ]
    }
)

# 复杂查询操作符
operators = {
    "$eq": "等于",
    "$ne": "不等于",
    "$gt": "大于",
    "$gte": "大于等于",
    "$lt": "小于",
    "$lte": "小于等于",
    "$in": "在列表中",
    "$nin": "不在列表中",
    "$and": "与",
    "$or": "或"
}
```

#### 4.3 高级检索

```python
# 返回特定字段
results = collection.query(
    query_texts=["AI"],
    n_results=5,
    include=["documents", "metadatas", "distances"]  # 不返回embeddings
)

# MMR（最大边际相关性）检索
# 注意：Chroma目前不直接支持MMR，需要自己实现或使用LangChain

from langchain.vectorstores import Chroma as LangChainChroma

vectorstore = LangChainChroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# MMR检索
docs = vectorstore.max_marginal_relevance_search(
    "查询",
    k=5,
    fetch_k=20,
    lambda_mult=0.5  # 多样性参数（0-1）
)
```

---

### 5. 持久化和备份

#### 5.1 持久化配置

```python
# 创建持久化客户端
client = chromadb.PersistentClient(
    path="./my_chroma_db",  # 存储路径
    settings=chromadb.Settings(
        anonymized_telemetry=False,  # 关闭遥测
        allow_reset=True  # 允许重置
    )
)

# 所有操作会自动持久化
collection = client.get_or_create_collection("my_docs")
collection.add(
    documents=["文档1"],
    ids=["id1"]
)

# 重启后数据仍然存在
client2 = chromadb.PersistentClient(path="./my_chroma_db")
collection2 = client2.get_collection("my_docs")
print(collection2.count())  # 1
```

#### 5.2 备份和迁移

```python
# 方式1：直接复制目录
import shutil

# 备份
shutil.copytree("./my_chroma_db", "./my_chroma_db_backup")

# 恢复
shutil.copytree("./my_chroma_db_backup", "./my_chroma_db_restored")


# 方式2：导出导入数据
def export_collection(collection, filename):
    """导出集合数据"""
    import json
    
    data = collection.get(include=["documents", "metadatas", "embeddings"])
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"导出完成：{filename}")


def import_collection(collection, filename):
    """导入集合数据"""
    import json
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    collection.add(
        ids=data['ids'],
        documents=data.get('documents'),
        metadatas=data.get('metadatas'),
        embeddings=data.get('embeddings')
    )
    
    print(f"导入完成：{len(data['ids'])}条")


# 使用
export_collection(collection, "backup.json")
import_collection(new_collection, "backup.json")
```

---

### 6. LangChain集成

#### 6.1 基础集成

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document

# 初始化Embeddings
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 创建文档
documents = [
    Document(
        page_content="人工智能是计算机科学的一个分支",
        metadata={"source": "wiki", "page": 1}
    ),
    Document(
        page_content="机器学习是AI的核心技术",
        metadata={"source": "book", "page": 10}
    )
]

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_langchain"
)

# 搜索
results = vectorstore.similarity_search("什么是AI", k=2)

for doc in results:
    print(f"内容：{doc.page_content}")
    print(f"元数据：{doc.metadata}\n")
```

#### 6.2 作为检索器

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings()

vectorstore = Chroma(
    collection_name="my_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# 转换为检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",  # 或 "mmr"
    search_kwargs={"k": 5}
)

# 使用检索器
docs = retriever.get_relevant_documents("人工智能")

for doc in docs:
    print(doc.page_content)
```

#### 6.3 与Chain集成

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# 创建QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 提问
result = qa_chain({"query": "什么是人工智能？"})

print("答案：", result['result'])
print("\n来源文档：")
for doc in result['source_documents']:
    print(f"- {doc.page_content[:100]}...")
```

---

## 💻 Demo案例：完整的Chroma应用

创建`chroma_complete_demo.py`：

```python
"""
Chroma完整演示
从创建到检索，从基础到高级
"""

import chromadb
from chromadb.config import Settings
import numpy as np


# ============= 1. 初始化 =============

def demo_1_initialization():
    """演示1：初始化和基础操作"""
    
    print("\n" + "="*60)
    print("演示1：Chroma初始化")
    print("="*60 + "\n")
    
    # 持久化客户端
    client = chromadb.PersistentClient(path="./demo_chroma_db")
    
    # 创建集合
    collection = client.get_or_create_collection(
        name="tech_docs",
        metadata={"description": "技术文档集合"}
    )
    
    print(f"✓ 客户端创建成功")
    print(f"✓ 集合：{collection.name}")
    print(f"✓ 当前文档数：{collection.count()}\n")
    
    return client, collection


# ============= 2. 添加数据 =============

def demo_2_add_data(collection):
    """演示2：添加数据"""
    
    print("="*60)
    print("演示2：添加数据")
    print("="*60 + "\n")
    
    # 清空集合
    if collection.count() > 0:
        collection.delete(where={})
    
    # 添加技术文档
    documents = [
        "Python是一种高级编程语言，广泛用于数据科学和AI开发",
        "JavaScript是Web开发的核心语言，运行在浏览器中",
        "机器学习是人工智能的核心技术，使用数据来改进性能",
        "深度学习基于人工神经网络，在图像和语音识别中表现出色",
        "自然语言处理使计算机能够理解和生成人类语言",
        "向量数据库专门用于存储和检索向量，支持相似度搜索"
    ]
    
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    metadatas = [
        {"category": "编程语言", "difficulty": "beginner"},
        {"category": "编程语言", "difficulty": "beginner"},
        {"category": "AI", "difficulty": "intermediate"},
        {"category": "AI", "difficulty": "advanced"},
        {"category": "AI", "difficulty": "intermediate"},
        {"category": "数据库", "difficulty": "intermediate"}
    ]
    
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"✓ 添加了 {len(documents)} 个文档")
    print(f"✓ 当前总数：{collection.count()}\n")


# ============= 3. 基础搜索 =============

def demo_3_basic_search(collection):
    """演示3：基础搜索"""
    
    print("="*60)
    print("演示3：相似度搜索")
    print("="*60 + "\n")
    
    query = "如何学习人工智能"
    print(f"查询：{query}\n")
    
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    print("搜索结果：")
    for i, (doc, dist, meta) in enumerate(zip(
        results['documents'][0],
        results['distances'][0],
        results['metadatas'][0]
    ), 1):
        print(f"\n{i}. 相似度：{1-dist:.4f}")
        print(f"   类别：{meta['category']}")
        print(f"   难度：{meta['difficulty']}")
        print(f"   内容：{doc}")


# ============= 4. 过滤搜索 =============

def demo_4_filtered_search(collection):
    """演示4：带过滤的搜索"""
    
    print("\n" + "="*60)
    print("演示4：元数据过滤搜索")
    print("="*60 + "\n")
    
    query = "技术"
    
    # 只搜索AI类别
    print(f"查询：{query}（仅AI类别）\n")
    
    results = collection.query(
        query_texts=[query],
        n_results=3,
        where={"category": "AI"}
    )
    
    print("搜索结果：")
    for i, (doc, meta) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0]
    ), 1):
        print(f"\n{i}. 类别：{meta['category']}")
        print(f"   内容：{doc}")
    
    # 多条件过滤
    print("\n" + "-"*60)
    print("查询：技术（AI类别 + 中级难度）\n")
    
    results = collection.query(
        query_texts=[query],
        n_results=5,
        where={
            "$and": [
                {"category": "AI"},
                {"difficulty": "intermediate"}
            ]
        }
    )
    
    print("搜索结果：")
    for i, (doc, meta) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0]
    ), 1):
        print(f"\n{i}. {meta['category']} - {meta['difficulty']}")
        print(f"   {doc}")


# ============= 5. 数据管理 =============

def demo_5_data_management(collection):
    """演示5：数据管理"""
    
    print("\n" + "="*60)
    print("演示5：数据更新和删除")
    print("="*60 + "\n")
    
    print(f"初始文档数：{collection.count()}")
    
    # 更新
    print("\n更新 doc_0...")
    collection.update(
        ids=["doc_0"],
        documents=["Python是最流行的AI开发语言"],
        metadatas=[{"category": "编程语言", "difficulty": "beginner", "updated": True}]
    )
    
    updated = collection.get(ids=["doc_0"])
    print(f"✓ 更新后：{updated['documents'][0]}")
    
    # 删除
    print("\n删除难度为advanced的文档...")
    collection.delete(where={"difficulty": "advanced"})
    
    print(f"✓ 删除后文档数：{collection.count()}")


# ============= 6. 统计信息 =============

def demo_6_statistics(collection):
    """演示6：统计信息"""
    
    print("\n" + "="*60)
    print("演示6：集合统计")
    print("="*60 + "\n")
    
    # 总数
    total = collection.count()
    print(f"总文档数：{total}")
    
    # 按类别统计
    categories = ["AI", "编程语言", "数据库"]
    print("\n按类别统计：")
    for cat in categories:
        data = collection.get(where={"category": cat})
        count = len(data['ids'])
        print(f"  {cat}: {count}个")
    
    # 按难度统计
    difficulties = ["beginner", "intermediate", "advanced"]
    print("\n按难度统计：")
    for diff in difficulties:
        data = collection.get(where={"difficulty": diff})
        count = len(data['ids'])
        print(f"  {diff}: {count}个")


# ============= 主函数 =============

def main():
    """主函数"""
    
    print("\n" + "="*60)
    print("🎯 Chroma完整演示")
    print("="*60)
    
    # 运行演示
    client, collection = demo_1_initialization()
    demo_2_add_data(collection)
    demo_3_basic_search(collection)
    demo_4_filtered_search(collection)
    demo_5_data_management(collection)
    demo_6_statistics(collection)
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("="*60)
    print("\n💡 核心要点：")
    print("  1. Chroma安装和使用极其简单")
    print("  2. 支持持久化存储")
    print("  3. 元数据过滤功能强大")
    print("  4. 与LangChain完美集成")
    print("  5. 适合中小规模应用")
    print("\n🚀 下一课：向量数据库性能对比")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
```

---

## 🎯 最佳实践

### Chroma使用建议

```
开发环境：
✓ 使用内存模式快速测试
✓ 小数据集调试

生产环境：
✓ 使用持久化模式
✓ 定期备份数据
✓ 考虑Client/Server部署
✓ 监控集合大小

性能优化：
✓ 合理设置批量大小
✓ 使用元数据过滤减少搜索范围
✓ 避免存储过大的文档
✓ 定期清理无用数据
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 安装和配置Chroma
- [ ] 创建和管理集合
- [ ] 添加、查询、更新、删除数据
- [ ] 使用元数据过滤
- [ ] 持久化和备份数据
- [ ] 与LangChain集成

---

## 📝 下一课预告

**第45课：向量数据库性能对比**

下一课我们将：
- 对比Chroma、Milvus、Pinecone
- 性能测试和基准
- 功能特性对比
- 选择决策指南

**选择最适合你的向量数据库！**

---

**🎉 恭喜你完成第44课！**

**你已经精通Chroma向量数据库！**

**进度：44/165课（26.7%完成）** 🚀
