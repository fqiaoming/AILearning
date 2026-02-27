# AI课程代码仓库

> 🎯 Java开发转AI应用开发 - 完整课程代码

## 📁 目录结构

```
ai-course-code/
├── chapter02_environment/      # 第2章：环境配置
├── chapter03_prompt/           # 第3章：Prompt工程
├── chapter04_openai_api/       # 第4章：OpenAI API
├── chapter05_langchain_basics/ # 第5章：LangChain基础
├── chapter06_langchain_advanced/ # 第6章：LangChain高级
├── chapter07_vector_db/        # 第7章：向量数据库
├── chapter08_document/         # 第8章：文档处理
├── chapter09_rag_basics/       # 第9章：RAG基础
├── chapter10_rag_advanced/     # 第10章：RAG进阶
├── chapter11_rag_evaluation/   # 第11章：RAG评估
├── chapter11_5_knowledge_graph/ # 第11.5章：知识图谱
├── chapter12_agent_basics/     # 第12章：Agent基础
├── chapter13_tool_calling/     # 第13章：Tool Calling
├── chapter14_agent_advanced/   # 第14章：Agent进阶
├── chapter15_18_finetuning/    # 第15-18章：模型微调
├── chapter19_21_projects/      # 第19-21章：综合实战
├── chapter22_25_engineering/   # 第22-25章：工程化
└── notebooks/                  # Jupyter Notebooks
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp env.example .env
# 编辑.env填入你的API Key
```

### 3. 运行代码

```bash
# 进入对应章节目录
cd chapter02_environment
python hello_ai.py
```

## 📚 课程大纲

| 阶段 | 章节 | 主要内容 |
|------|------|----------|
| 基础入门 | 1-3章 | AI认知、环境配置、Prompt工程 |
| 核心技能 | 4-6章 | OpenAI API、LangChain |
| 高级应用 | 7-11章 | 向量数据库、文档处理、RAG |
| Agent开发 | 12-14章 | Agent、Tool Calling |
| 模型微调 | 15-18章 | LoRA微调、数据准备 |
| 综合实战 | 19-21章 | 企业级项目 |
| 工程化 | 22-25章 | 测试、部署、成本优化 |

## 🛠️ 技术栈

- **语言**: Python 3.10+
- **LLM框架**: LangChain
- **向量数据库**: ChromaDB
- **本地LLM**: LM Studio
- **云端LLM**: OpenAI API

## 📖 学习建议

1. **跟着课程走**：每个章节目录都有README说明
2. **动手敲代码**：不要只看，要亲自运行
3. **修改实验**：尝试修改代码看效果
4. **做项目**：学完后做自己的项目

## 📝 视频脚本

每个章节都有配套的口播文案：
- 位于各阶段目录下的 `第X章口播文案.md`
- 可用于B站视频录制

## 🤝 贡献

欢迎提交Issue和PR！

---

*课程持续更新中...*
