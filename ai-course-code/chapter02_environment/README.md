# 第2章：环境配置

本章代码用于验证Python环境和LM Studio是否配置正确。

## 文件说明

| 文件 | 说明 | 对应课程 |
|------|------|----------|
| test_env.py | 环境验证脚本 | 第05课-Python环境配置 |
| hello_ai.py | 第一个AI程序 | 第05课-Python环境配置 |
| test_lm_studio.py | LM Studio API测试 | 第06课-LM-Studio安装 |
| ai_client.py | 统一AI客户端（支持切换） | 第07课-本地vs云端模型 |

## 使用方法

```bash
# 1. 验证Python环境
python test_env.py

# 2. 运行第一个AI程序（需要先启动LM Studio）
python hello_ai.py

# 3. 完整测试LM Studio API
python test_lm_studio.py

# 4. 测试模型切换功能
python ai_client.py
```

## 前置条件

1. Python 3.10+ 已安装
2. 已创建并激活虚拟环境
3. 已安装依赖：`pip install openai python-dotenv`
4. LM Studio 已安装并加载模型
5. LM Studio Local Server 已启动（端口1234）

