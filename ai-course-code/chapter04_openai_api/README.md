# 第4章：OpenAI API

本章代码展示OpenAI API的各种用法，包括Chat Completions、Function Calling、Streaming等。

## 文件说明

| 文件 | 说明 | 对应课程 |
|------|------|----------|
| 01_api_basics.py | API基础调用 | 第16课-OpenAI API入门 |
| 02_function_calling.py | Function Calling | 第17课-Function Calling入门 |
| 03_streaming.py | 流式响应 | 第18课-Streaming与异步处理 |
| 04_error_handling.py | 错误处理与重试 | 第19课-错误处理与重试策略 |
| 05_token_management.py | Token管理 | 第20课-Token管理与成本优化 |
| 06_api_security.py | API安全 | 第21课-API安全最佳实践 |

## Notebook

本章提供完整的Jupyter Notebook，位于 `../notebooks/04_openai_api.ipynb`

## 使用方法

```bash
# 1. 配置API Key（二选一）
# 方案A：使用本地LM Studio（免费）
# 确保LM Studio已启动

# 方案B：使用OpenAI API
# 编辑 .env 文件，设置 OPENAI_API_KEY

# 2. 运行示例
python 01_api_basics.py
python 02_function_calling.py
python 03_streaming.py
```

## 前置条件

1. 已安装依赖：`pip install openai python-dotenv tiktoken tenacity`
2. 二选一：
   - LM Studio已启动（免费本地测试）
   - 或已配置OpenAI API Key

