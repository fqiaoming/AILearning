# 第3章：Prompt工程

本章代码展示提示词工程的各种技巧和实战项目。

## 文件说明

| 文件 | 说明 | 对应课程 |
|------|------|----------|
| 01_prompt_basics.py | 提示词基础对比 | 第08课-提示词是什么 |
| 02_rtcf_framework.py | RTCF框架演示 | 第09课-提示词四大要素 |
| 03_crispe_framework.py | CRISPE框架演示 | 第10课-CRISPE框架 |
| 04_costar_framework.py | CO-STAR框架演示 | 第11课-CO-STAR框架 |
| 05_fewshot_cot.py | Few-shot与CoT技巧 | 第12课-Few-shot与CoT |
| 06_prompt_testing.py | 提示词测试评估 | 第13课-提示词测试评估 |
| customer_service/ | 智能客服实战项目 | 第15课-提示词工程实战 |

## 使用方法

```bash
# 1. 基础对比演示
python 01_prompt_basics.py

# 2. 各框架演示
python 02_rtcf_framework.py
python 03_crispe_framework.py
python 04_costar_framework.py

# 3. Few-shot和CoT演示
python 05_fewshot_cot.py

# 4. 智能客服实战项目
cd customer_service
python bot.py
```

## 前置条件

1. 已配置Python环境
2. 已安装依赖：`pip install openai python-dotenv`
3. LM Studio已启动并加载模型

