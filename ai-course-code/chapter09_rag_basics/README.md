# 第9章：RAG系统基础

本章代码展示如何搭建完整的RAG（检索增强生成）系统。

## 文件说明

| 文件 | 说明 | 对应课程 |
|------|------|----------|
| 01_rag_concept.py | RAG概念演示 | 第51课-RAG原理 |
| 02_basic_rag.py | 基础RAG实现 | 第52课-构建基础RAG |
| 03_retrieval_chain.py | 检索Chain | 第53课-检索Chain |
| 04_conversational_rag.py | 对话式RAG | 第54课-对话式RAG |
| project_qa_system/ | 实战项目：文档问答 | 第55课-RAG实战项目 |

## 使用方法

```bash
# 安装依赖
pip install langchain langchain-openai langchain-chroma chromadb

# 运行示例
python 01_rag_concept.py
python 02_basic_rag.py
```

## RAG核心流程

```
文档 → 分块 → 向量化 → 存储到向量库
                          ↓
用户提问 → 向量化 → 检索相关文档 → LLM生成答案
```

