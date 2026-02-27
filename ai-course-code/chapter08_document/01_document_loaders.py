"""
第8章-文档处理：文档加载器
对应课程：第46课-文档加载

功能：加载各种格式的文档
"""

from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    UnstructuredMarkdownLoader
)
from langchain_core.documents import Document
import os


def demo_text_loader():
    """演示1：加载文本文件"""
    print("=" * 60)
    print("演示1：TextLoader - 加载文本文件")
    print("=" * 60)
    
    # 创建测试文件
    test_content = """Python是一种高级编程语言。
它的设计理念强调代码的可读性。
Python适合初学者学习，也能满足专业开发者的需求。"""
    
    with open("test_doc.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 加载文件
    loader = TextLoader("test_doc.txt", encoding="utf-8")
    documents = loader.load()
    
    print(f"\n加载了{len(documents)}个文档")
    print(f"内容：{documents[0].page_content[:100]}...")
    print(f"元数据：{documents[0].metadata}")
    
    # 清理
    os.remove("test_doc.txt")


def demo_directory_loader():
    """演示2：批量加载目录"""
    print("\n" + "=" * 60)
    print("演示2：DirectoryLoader - 批量加载目录")
    print("=" * 60)
    
    # 创建测试目录和文件
    os.makedirs("test_docs", exist_ok=True)
    
    for i in range(3):
        with open(f"test_docs/doc_{i}.txt", "w", encoding="utf-8") as f:
            f.write(f"这是测试文档{i}的内容。")
    
    # 加载整个目录
    loader = DirectoryLoader(
        "test_docs",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    
    documents = loader.load()
    
    print(f"\n加载了{len(documents)}个文档")
    for doc in documents:
        print(f"  - {doc.metadata['source']}: {doc.page_content[:30]}...")
    
    # 清理
    import shutil
    shutil.rmtree("test_docs")


def demo_document_structure():
    """演示3：Document结构"""
    print("\n" + "=" * 60)
    print("演示3：Document对象结构")
    print("=" * 60)
    
    # 手动创建Document
    doc = Document(
        page_content="这是文档的正文内容",
        metadata={
            "source": "manual_creation",
            "author": "示例作者",
            "date": "2024-01-01",
            "category": "教程"
        }
    )
    
    print(f"""
Document对象包含两个核心属性：

1. page_content（正文内容）：
   {doc.page_content}

2. metadata（元数据）：
   {doc.metadata}

元数据的用途：
- 记录文档来源（用于引用）
- 存储分类信息（用于过滤）
- 保存时间戳（用于更新）
""")


def demo_loader_types():
    """演示4：各种加载器类型"""
    print("\n" + "=" * 60)
    print("演示4：LangChain支持的文档加载器")
    print("=" * 60)
    
    print("""
LangChain支持多种文档格式：

1. 文本类
   - TextLoader：纯文本文件
   - UnstructuredMarkdownLoader：Markdown文件
   - JSONLoader：JSON文件
   - CSVLoader：CSV文件

2. 办公文档
   - PyPDFLoader：PDF文件
   - Docx2txtLoader：Word文档
   - UnstructuredExcelLoader：Excel文件
   - UnstructuredPowerPointLoader：PPT

3. 网页
   - WebBaseLoader：网页内容
   - UnstructuredURLLoader：URL列表
   - SeleniumURLLoader：动态网页

4. 代码
   - PythonLoader：Python文件
   - NotebookLoader：Jupyter Notebook

5. 特殊格式
   - WikipediaLoader：维基百科
   - ArxivLoader：学术论文
   - GitLoader：Git仓库
""")


if __name__ == "__main__":
    demo_text_loader()
    demo_directory_loader()
    demo_document_structure()
    demo_loader_types()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n文档加载核心知识：")
    print("  1. Document = page_content + metadata")
    print("  2. 不同格式用不同Loader")
    print("  3. DirectoryLoader批量加载")
    print("  4. metadata很重要，用于过滤和引用")

