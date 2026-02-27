"""
第7章-向量数据库：Embedding基础
对应课程：第41课-Embedding原理

功能：理解文本向量化的原理和用法
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()


def get_embeddings():
    """获取Embedding模型"""
    # 使用HuggingFace的免费模型（推荐学习使用）
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def demo_what_is_embedding():
    """演示1：什么是Embedding"""
    print("=" * 60)
    print("演示1：什么是Embedding（文本向量化）")
    print("=" * 60)
    
    print("""
Embedding = 把文本转换成数字向量

例如：
"我喜欢Python" → [0.12, -0.34, 0.56, ..., 0.78]  # 384维向量

为什么要向量化？
1. 计算机不懂文字，但懂数字
2. 向量可以计算相似度
3. 语义相近的文本，向量也接近

核心应用：
- 语义搜索（根据意思搜索，而非关键词）
- 相似文档查找
- RAG系统的检索环节
""")


def demo_basic_embedding():
    """演示2：基础Embedding"""
    print("\n" + "=" * 60)
    print("演示2：基础Embedding操作")
    print("=" * 60)
    
    embeddings = get_embeddings()
    
    # 单个文本向量化
    text = "Python是一种编程语言"
    vector = embeddings.embed_query(text)
    
    print(f"\n原文：{text}")
    print(f"向量维度：{len(vector)}")
    print(f"向量前5个值：{vector[:5]}")
    
    # 批量向量化
    texts = [
        "Python是一种编程语言",
        "Java也是一种编程语言",
        "今天天气很好"
    ]
    
    vectors = embeddings.embed_documents(texts)
    
    print(f"\n批量向量化：{len(vectors)}个文本")
    for i, (t, v) in enumerate(zip(texts, vectors)):
        print(f"  文本{i+1}：{t[:20]}... → 向量[{v[0]:.4f}, {v[1]:.4f}, ...]")


def cosine_similarity(v1, v2):
    """计算余弦相似度"""
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def demo_similarity():
    """演示3：语义相似度计算"""
    print("\n" + "=" * 60)
    print("演示3：语义相似度计算")
    print("=" * 60)
    
    embeddings = get_embeddings()
    
    # 准备测试文本
    texts = [
        "Python是一种流行的编程语言",
        "Python是一门很棒的语言",
        "今天的天气非常晴朗",
        "Java是一种面向对象的语言"
    ]
    
    # 计算向量
    vectors = embeddings.embed_documents(texts)
    
    # 计算相似度
    print("\n相似度矩阵（余弦相似度）：")
    print(f"{'':40} ", end="")
    for i in range(len(texts)):
        print(f"文本{i+1:5}", end="")
    print()
    
    for i, t1 in enumerate(texts):
        print(f"文本{i+1}: {t1[:35]:35}", end=" ")
        for j, t2 in enumerate(texts):
            sim = cosine_similarity(vectors[i], vectors[j])
            print(f"{sim:.2f} ", end=" ")
        print()
    
    print("\n💡 观察：")
    print("  - 文本1和文本2都在说Python，相似度高")
    print("  - 文本1和文本3主题不同，相似度低")
    print("  - 文本1和文本4都是编程语言，有一定相似度")


def demo_semantic_search():
    """演示4：语义搜索示例"""
    print("\n" + "=" * 60)
    print("演示4：语义搜索（根据意思搜索）")
    print("=" * 60)
    
    embeddings = get_embeddings()
    
    # 文档库
    documents = [
        "Python是一种解释型的高级编程语言",
        "机器学习是人工智能的一个子领域",
        "深度学习使用神经网络进行学习",
        "数据分析帮助企业做出更好的决策",
        "自然语言处理研究计算机如何理解人类语言"
    ]
    
    # 计算文档向量
    doc_vectors = embeddings.embed_documents(documents)
    
    # 查询
    query = "AI如何理解文字"
    query_vector = embeddings.embed_query(query)
    
    # 计算相似度并排序
    similarities = [
        (doc, cosine_similarity(query_vector, vec))
        for doc, vec in zip(documents, doc_vectors)
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n查询：{query}")
    print("\n搜索结果（按相似度排序）：")
    for i, (doc, sim) in enumerate(similarities, 1):
        print(f"  {i}. [{sim:.3f}] {doc}")
    
    print("\n💡 注意：")
    print("  - 查询'AI如何理解文字'")
    print("  - 最相关的是'自然语言处理...'")
    print("  - 这就是语义搜索的威力：理解意思，而非匹配关键词")


if __name__ == "__main__":
    demo_what_is_embedding()
    demo_basic_embedding()
    demo_similarity()
    demo_semantic_search()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nEmbedding核心知识：")
    print("  1. Embedding = 文本 → 数字向量")
    print("  2. 语义相近的文本，向量也接近")
    print("  3. 用余弦相似度计算文本相似度")
    print("  4. 这是RAG检索的基础")

