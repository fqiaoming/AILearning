"""
第8章-文档处理：文本分割器
对应课程：第47课-文本分割

功能：将长文档切分成合适大小的块
"""

from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter
)
from langchain_core.documents import Document


def demo_why_split():
    """演示1：为什么需要分割"""
    print("=" * 60)
    print("演示1：为什么需要分割文档")
    print("=" * 60)
    
    print("""
为什么要分割文档？

1. LLM有token限制
   - GPT-3.5: 4K tokens
   - GPT-4: 8K-128K tokens
   - 超长文档无法一次处理

2. 向量化效果
   - 太长的文本，向量太"平均"
   - 短文本向量更能捕捉具体信息

3. 检索精度
   - 大块：召回可能包含无关内容
   - 小块：召回更精准

推荐分块大小：
- 一般场景：500-1000字符
- 需要精确检索：200-500字符
- 需要完整上下文：1000-2000字符
""")


def demo_character_splitter():
    """演示2：字符分割器"""
    print("\n" + "=" * 60)
    print("演示2：CharacterTextSplitter")
    print("=" * 60)
    
    long_text = """
Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。
Python的设计理念强调代码的可读性和简洁性。
它支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。
Python拥有丰富的标准库和第三方库生态系统。
它广泛应用于Web开发、数据分析、人工智能、科学计算等领域。
Python的语法简洁明了，非常适合初学者学习。
"""
    
    # 基础分割器
    splitter = CharacterTextSplitter(
        separator="\n",      # 分隔符
        chunk_size=100,      # 每块最大字符数
        chunk_overlap=20,    # 块之间重叠字符数
        length_function=len
    )
    
    chunks = splitter.split_text(long_text)
    
    print(f"\n原文长度：{len(long_text)}字符")
    print(f"分割成{len(chunks)}块")
    print("\n各块内容：")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n[块{i}] ({len(chunk)}字符)")
        print(f"  {chunk[:50]}...")


def demo_recursive_splitter():
    """演示3：递归分割器（推荐）"""
    print("\n" + "=" * 60)
    print("演示3：RecursiveCharacterTextSplitter（推荐）")
    print("=" * 60)
    
    long_text = """
# Python简介

Python是一种高级编程语言。它的特点包括：
- 语法简洁
- 易于学习
- 功能强大

## 应用领域

Python广泛应用于：

1. Web开发
   使用Django、Flask等框架

2. 数据分析
   使用Pandas、NumPy等库

3. 人工智能
   使用TensorFlow、PyTorch等框架
"""
    
    # 递归分割器：按优先级尝试不同分隔符
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "，", " ", ""],  # 分隔符优先级
        chunk_size=100,
        chunk_overlap=20
    )
    
    chunks = splitter.split_text(long_text)
    
    print(f"\n原文长度：{len(long_text)}字符")
    print(f"分割成{len(chunks)}块")
    print("\n各块内容：")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n[块{i}] ({len(chunk)}字符)")
        print(f"  {chunk.strip()[:60]}...")
    
    print("\n💡 递归分割器的优势：")
    print("  - 尽量保持段落完整")
    print("  - 不会在句子中间断开")
    print("  - 自动选择最合适的分隔点")


def demo_split_documents():
    """演示4：分割Document对象"""
    print("\n" + "=" * 60)
    print("演示4：分割Document对象（保留元数据）")
    print("=" * 60)
    
    # 创建Document
    doc = Document(
        page_content="Python是编程语言。它很流行。Python用于AI开发。",
        metadata={"source": "python.txt", "chapter": 1}
    )
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=20,
        chunk_overlap=5
    )
    
    # 分割Document
    chunks = splitter.split_documents([doc])
    
    print(f"\n原始文档：1个")
    print(f"分割后：{len(chunks)}个")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n[块{i}]")
        print(f"  内容：{chunk.page_content}")
        print(f"  元数据：{chunk.metadata}")
    
    print("\n💡 注意：分割后每个块都保留了原始元数据")


def demo_overlap_importance():
    """演示5：重叠的重要性"""
    print("\n" + "=" * 60)
    print("演示5：chunk_overlap的作用")
    print("=" * 60)
    
    text = "A和B相关。B和C相关。C和D相关。D和E相关。"
    
    # 无重叠
    splitter_no_overlap = CharacterTextSplitter(
        separator="。",
        chunk_size=15,
        chunk_overlap=0
    )
    
    # 有重叠
    splitter_with_overlap = CharacterTextSplitter(
        separator="。",
        chunk_size=15,
        chunk_overlap=8
    )
    
    print(f"\n原文：{text}")
    
    print("\n无重叠分割：")
    for i, chunk in enumerate(splitter_no_overlap.split_text(text), 1):
        print(f"  块{i}: {chunk}")
    
    print("\n有重叠分割（overlap=8）：")
    for i, chunk in enumerate(splitter_with_overlap.split_text(text), 1):
        print(f"  块{i}: {chunk}")
    
    print("\n💡 重叠的作用：")
    print("  - 防止信息在边界处丢失")
    print("  - 保持上下文连贯性")
    print("  - 通常设置为chunk_size的10-20%")


if __name__ == "__main__":
    demo_why_split()
    demo_character_splitter()
    demo_recursive_splitter()
    demo_split_documents()
    demo_overlap_importance()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n文本分割核心知识：")
    print("  1. 推荐使用RecursiveCharacterTextSplitter")
    print("  2. chunk_size通常500-1000")
    print("  3. chunk_overlap通常10-20%")
    print("  4. 分割后保留原始metadata")

