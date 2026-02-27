# 企业RAG知识库系统

> 对应课程：第89-93课

## 功能

- 文档上传与解析
- 向量化存储
- 智能问答
- 对话历史管理

## 文件结构

```
rag_chatbot/
├── main.py           # 主程序入口
├── document_loader.py # 文档加载器
├── vectorstore.py    # 向量存储
├── chain.py          # RAG链
└── config.py         # 配置文件
```

## 运行方式

```bash
# 安装依赖
pip install langchain chromadb openai

# 运行
python main.py
```

