"""
第9章-RAG基础：构建基础RAG系统
对应课程：第52课-构建基础RAG

功能：实现完整的RAG流程
"""

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """获取LLM"""
    return ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
        temperature=0.3
    )


def get_embeddings():
    """获取Embedding模型"""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ==================== 准备知识库 ====================

def prepare_knowledge_base():
    """准备示例知识库"""
    # 模拟文档内容
    documents = [
        Document(
            page_content="Python是一种高级编程语言，由Guido van Rossum于1991年创建。Python的设计理念强调代码的可读性和简洁性。",
            metadata={"source": "python_intro.txt", "topic": "python"}
        ),
        Document(
            page_content="Python支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。它拥有丰富的标准库。",
            metadata={"source": "python_features.txt", "topic": "python"}
        ),
        Document(
            page_content="LangChain是一个用于开发LLM应用的框架。它提供了模块化的组件，包括模型、提示词模板、Chain和Agent。",
            metadata={"source": "langchain_intro.txt", "topic": "langchain"}
        ),
        Document(
            page_content="RAG（检索增强生成）是一种结合检索和生成的技术。它先从知识库检索相关文档，再用LLM生成答案。",
            metadata={"source": "rag_intro.txt", "topic": "rag"}
        ),
        Document(
            page_content="向量数据库用于存储和检索文本向量。常用的向量数据库包括Chroma、Pinecone、Milvus等。",
            metadata={"source": "vector_db.txt", "topic": "rag"}
        ),
    ]
    
    return documents


# ==================== 构建RAG系统 ====================

def build_rag_system():
    """构建完整的RAG系统"""
    print("=" * 60)
    print("构建RAG系统")
    print("=" * 60)
    
    # 1. 准备文档
    print("\n[步骤1] 准备文档...")
    documents = prepare_knowledge_base()
    print(f"  加载了{len(documents)}个文档")
    
    # 2. 文档分块
    print("\n[步骤2] 文档分块...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    chunks = splitter.split_documents(documents)
    print(f"  分割成{len(chunks)}个块")
    
    # 3. 创建向量库
    print("\n[步骤3] 创建向量库...")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="knowledge_base"
    )
    print(f"  向量库创建成功")
    
    # 4. 创建Retriever
    print("\n[步骤4] 创建Retriever...")
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # 返回top 3
    )
    print(f"  Retriever创建成功（返回top 3）")
    
    # 5. 创建RAG Chain
    print("\n[步骤5] 创建RAG Chain...")
    
    # RAG提示词模板
    rag_prompt = ChatPromptTemplate.from_template("""根据以下参考资料回答问题。如果资料中没有相关信息，请说"我不确定"。

参考资料：
{context}

问题：{question}

回答：""")
    
    llm = get_llm()
    
    # 格式化检索结果
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    # 构建Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    
    print("  RAG Chain创建成功")
    
    return rag_chain, vectorstore


def demo_rag_query(rag_chain):
    """演示RAG查询"""
    print("\n" + "=" * 60)
    print("RAG查询演示")
    print("=" * 60)
    
    # 测试问题
    questions = [
        "Python是什么？",
        "LangChain有什么功能？",
        "什么是RAG？",
        "如何做红烧肉？"  # 知识库中没有的问题
    ]
    
    for q in questions:
        print(f"\n问题：{q}")
        print("-" * 40)
        answer = rag_chain.invoke(q)
        print(f"回答：{answer}")


def demo_retrieval_details(vectorstore):
    """演示检索细节"""
    print("\n" + "=" * 60)
    print("检索细节演示")
    print("=" * 60)
    
    query = "什么是RAG？"
    print(f"\n查询：{query}")
    
    # 带分数的检索
    results = vectorstore.similarity_search_with_score(query, k=3)
    
    print("\n检索结果（按相似度排序）：")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n[结果{i}] 相似度分数：{score:.4f}")
        print(f"  来源：{doc.metadata.get('source', 'unknown')}")
        print(f"  内容：{doc.page_content[:100]}...")


if __name__ == "__main__":
    # 构建系统
    rag_chain, vectorstore = build_rag_system()
    
    # 演示查询
    demo_rag_query(rag_chain)
    
    # 演示检索细节
    demo_retrieval_details(vectorstore)
    
    print("\n" + "=" * 60)
    print("✅ RAG系统演示完成！")
    print("\nRAG核心流程：")
    print("  1. 文档 → 分块 → 向量化 → 存入向量库")
    print("  2. 问题 → 向量化 → 检索相关文档")
    print("  3. 问题 + 检索结果 → LLM → 生成答案")

