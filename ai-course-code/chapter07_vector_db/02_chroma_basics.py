"""
第7章-向量数据库：Chroma入门
对应课程：第42课-Chroma入门

功能：使用Chroma向量数据库存储和检索文档
"""

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv()


def demo_chroma_basics():
    """演示1：Chroma基础操作"""
    print("=" * 60)
    print("演示1：Chroma向量数据库基础")
    print("=" * 60)
    
    # 创建客户端（内存模式）
    client = chromadb.Client()
    
    # 使用sentence-transformers作为embedding
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # 创建集合
    collection = client.create_collection(
        name="my_documents",
        embedding_function=embedding_fn
    )
    
    print("✅ 创建Chroma集合成功")
    print(f"   集合名称：my_documents")
    
    # 添加文档
    documents = [
        "Python是一种流行的编程语言，适合初学者学习",
        "机器学习是人工智能的核心技术之一",
        "深度学习使用多层神经网络处理数据",
        "自然语言处理让计算机理解人类语言",
        "计算机视觉让机器能够识别图像内容"
    ]
    
    # 添加到集合
    collection.add(
        documents=documents,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )
    
    print(f"✅ 添加了{len(documents)}个文档")
    
    # 查询
    results = collection.query(
        query_texts=["AI如何理解文字"],
        n_results=3
    )
    
    print(f"\n查询：AI如何理解文字")
    print("搜索结果：")
    for i, (doc, distance) in enumerate(zip(
        results['documents'][0], 
        results['distances'][0]
    ), 1):
        print(f"  {i}. [距离:{distance:.3f}] {doc}")


def demo_persistent_storage():
    """演示2：持久化存储"""
    print("\n" + "=" * 60)
    print("演示2：持久化存储")
    print("=" * 60)
    
    # 持久化客户端（数据保存到磁盘）
    persist_directory = "./chroma_data"
    
    client = chromadb.PersistentClient(path=persist_directory)
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # 获取或创建集合
    collection = client.get_or_create_collection(
        name="persistent_docs",
        embedding_function=embedding_fn
    )
    
    # 检查是否已有数据
    count = collection.count()
    
    if count == 0:
        # 添加数据
        collection.add(
            documents=["测试文档1", "测试文档2"],
            ids=["test_1", "test_2"]
        )
        print(f"✅ 添加了2个文档")
    else:
        print(f"✅ 集合已存在，包含{count}个文档")
    
    print(f"   数据保存在：{persist_directory}")


def demo_metadata():
    """演示3：使用元数据"""
    print("\n" + "=" * 60)
    print("演示3：元数据（Metadata）")
    print("=" * 60)
    
    client = chromadb.Client()
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    collection = client.create_collection(
        name="docs_with_metadata",
        embedding_function=embedding_fn
    )
    
    # 添加带元数据的文档
    collection.add(
        documents=[
            "Python入门教程",
            "Python高级编程",
            "Java入门指南",
            "机器学习基础"
        ],
        metadatas=[
            {"language": "python", "level": "beginner", "year": 2024},
            {"language": "python", "level": "advanced", "year": 2024},
            {"language": "java", "level": "beginner", "year": 2023},
            {"language": "python", "level": "intermediate", "year": 2024}
        ],
        ids=["doc_1", "doc_2", "doc_3", "doc_4"]
    )
    
    print("✅ 添加了4个带元数据的文档")
    
    # 带过滤条件的查询
    print("\n查询：编程教程（只要Python的）")
    results = collection.query(
        query_texts=["编程教程"],
        n_results=3,
        where={"language": "python"}  # 元数据过滤
    )
    
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        print(f"  - {doc} | {meta}")
    
    # 复合过滤
    print("\n查询：编程教程（Python + 入门级）")
    results = collection.query(
        query_texts=["编程教程"],
        n_results=3,
        where={"$and": [
            {"language": "python"},
            {"level": "beginner"}
        ]}
    )
    
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        print(f"  - {doc} | {meta}")


def demo_update_delete():
    """演示4：更新和删除"""
    print("\n" + "=" * 60)
    print("演示4：更新和删除文档")
    print("=" * 60)
    
    client = chromadb.Client()
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    collection = client.create_collection(
        name="crud_demo",
        embedding_function=embedding_fn
    )
    
    # 添加
    collection.add(
        documents=["原始文档内容"],
        ids=["doc_1"]
    )
    print("✅ 添加文档：原始文档内容")
    
    # 更新
    collection.update(
        ids=["doc_1"],
        documents=["更新后的文档内容"]
    )
    print("✅ 更新文档：更新后的文档内容")
    
    # 查看
    result = collection.get(ids=["doc_1"])
    print(f"   当前内容：{result['documents'][0]}")
    
    # 删除
    collection.delete(ids=["doc_1"])
    print("✅ 删除文档")
    print(f"   当前文档数：{collection.count()}")


if __name__ == "__main__":
    demo_chroma_basics()
    demo_persistent_storage()
    demo_metadata()
    demo_update_delete()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nChroma核心操作：")
    print("  1. 创建集合：client.create_collection()")
    print("  2. 添加文档：collection.add()")
    print("  3. 查询：collection.query()")
    print("  4. 元数据过滤：where参数")
    print("  5. 持久化：PersistentClient")

