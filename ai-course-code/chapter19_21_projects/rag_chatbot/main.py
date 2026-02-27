"""
企业RAG知识库系统 - 主程序
对应课程：第89-93课

完整的RAG系统实现
"""

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()


class RAGChatbot:
    """企业RAG知识库聊天机器人"""
    
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = None
        self.chain = None
        
        # 初始化LLM
        self.llm = ChatOpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
            model=os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
        )
    
    def load_documents(self, file_paths):
        """加载文档"""
        documents = []
        for file_path in file_paths:
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
        
        # 分割文档
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        print(f"加载了 {len(documents)} 个文档，分割成 {len(chunks)} 个块")
        return chunks
    
    def build_vectorstore(self, chunks):
        """构建向量库"""
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        print(f"向量库构建完成，保存在 {self.persist_directory}")
    
    def load_vectorstore(self):
        """加载已有向量库"""
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        print("向量库加载完成")
    
    def build_chain(self):
        """构建RAG链"""
        # 检索器
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # 提示词模板
        template = """基于以下上下文回答问题。如果无法从上下文中找到答案，请说"抱歉，我在知识库中没有找到相关信息"。

上下文：
{context}

问题：{question}

回答："""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # 格式化检索结果
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        # 构建链
        self.chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        print("RAG链构建完成")
    
    def chat(self, question):
        """对话"""
        if not self.chain:
            raise ValueError("请先构建RAG链")
        return self.chain.invoke(question)


def main():
    """主函数演示"""
    print("=" * 60)
    print("企业RAG知识库系统")
    print("=" * 60)
    
    # 创建示例文档
    sample_content = """
    公司员工手册
    
    第一章 入职须知
    1. 新员工入职需要提供身份证、学历证明、离职证明
    2. 入职第一天需要完成IT系统账号申请
    3. 试用期为3个月
    
    第二章 考勤制度
    1. 工作时间：周一至周五 9:00-18:00
    2. 午休时间：12:00-13:00
    3. 迟到30分钟以内扣款50元，30分钟以上按旷工半天处理
    
    第三章 请假制度
    1. 年假：入职满一年享有5天年假
    2. 病假：需提供医院证明，每月最多3天带薪病假
    3. 事假：需提前一天申请，无薪
    """
    
    # 保存示例文档
    os.makedirs("./docs", exist_ok=True)
    with open("./docs/handbook.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    # 创建RAG系统
    bot = RAGChatbot()
    
    # 加载文档并构建向量库
    chunks = bot.load_documents(["./docs/handbook.txt"])
    bot.build_vectorstore(chunks)
    bot.build_chain()
    
    # 测试问答
    questions = [
        "新员工入职需要准备什么材料？",
        "迟到怎么处理？",
        "年假有几天？"
    ]
    
    print("\n" + "=" * 60)
    print("测试问答")
    print("=" * 60)
    
    for q in questions:
        print(f"\n问：{q}")
        answer = bot.chat(q)
        print(f"答：{answer}")


if __name__ == "__main__":
    main()

