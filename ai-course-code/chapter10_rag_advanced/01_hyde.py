"""
第10章-RAG进阶：HyDE假设文档嵌入
对应课程：第61课-HyDE假设文档嵌入

HyDE = Hypothetical Document Embeddings
核心思想：先让LLM生成一个假设的答案，用这个假设答案去检索
"""

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    return ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
    )


def demo_hyde_concept():
    """演示HyDE概念"""
    print("=" * 60)
    print("HyDE（假设文档嵌入）概念")
    print("=" * 60)
    
    print("""
传统检索的问题：
- 用户问题和文档内容的表述方式不同
- "什么是Python？" vs "Python是一种编程语言..."
- 问题是疑问句，文档是陈述句，向量可能不够相似

HyDE的解决方案：
1. 先让LLM生成一个"假设的答案"
2. 用这个假设答案去检索（陈述句 vs 陈述句）
3. 检索结果更准确

示例：
问题："Python有什么优点？"
     ↓ LLM生成假设答案
假设答案："Python的优点包括语法简洁、易于学习、
          拥有丰富的库生态系统..."
     ↓ 用假设答案去检索
检索结果更精准！
""")


def demo_hyde_implementation():
    """演示HyDE实现"""
    print("\n" + "=" * 60)
    print("HyDE实现演示")
    print("=" * 60)
    
    # 准备知识库
    documents = [
        Document(page_content="Python具有简洁的语法，代码可读性强，适合初学者学习。"),
        Document(page_content="Python拥有丰富的第三方库，如NumPy、Pandas、TensorFlow等。"),
        Document(page_content="Python支持多种编程范式，包括面向对象和函数式编程。"),
        Document(page_content="Java是一种强类型的面向对象编程语言。"),
    ]
    
    # 创建向量库
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    # HyDE提示词
    hyde_prompt = ChatPromptTemplate.from_template("""
请直接回答以下问题（不要说"我不知道"，尽量给出答案）：

问题：{question}

回答：""")
    
    llm = get_llm()
    
    # 测试问题
    question = "Python有什么优点？"
    
    # 方法1：直接用问题检索
    print(f"\n问题：{question}")
    print("\n【方法1：直接用问题检索】")
    results1 = vectorstore.similarity_search(question, k=2)
    for i, doc in enumerate(results1, 1):
        print(f"  {i}. {doc.page_content[:50]}...")
    
    # 方法2：HyDE - 先生成假设答案
    print("\n【方法2：HyDE - 用假设答案检索】")
    
    # 生成假设答案
    hyde_chain = hyde_prompt | llm | StrOutputParser()
    hypothetical_answer = hyde_chain.invoke({"question": question})
    print(f"  假设答案：{hypothetical_answer[:100]}...")
    
    # 用假设答案检索
    results2 = vectorstore.similarity_search(hypothetical_answer, k=2)
    print("\n  检索结果：")
    for i, doc in enumerate(results2, 1):
        print(f"  {i}. {doc.page_content[:50]}...")
    
    print("\n💡 对比：HyDE的检索结果通常更相关")


if __name__ == "__main__":
    demo_hyde_concept()
    demo_hyde_implementation()
    
    print("\n" + "=" * 60)
    print("✅ HyDE演示完成！")
    print("\nHyDE核心要点：")
    print("  1. 先生成假设答案")
    print("  2. 用假设答案检索")
    print("  3. 适合问题和文档表述差异大的场景")

