# 🤖 智能客服系统 - 提示词工程实战项目

第3章第15课的完整实战项目，从零搭建一个企业级智能客服系统。

## 项目结构

```
intelligent_customer_service/
├── prompts/                    # 提示词目录
│   ├── intent_recognition.md  # 意图识别提示词
│   ├── response_generation/   # 回复生成提示词
│   │   ├── order_query.md     # 订单查询
│   │   ├── refund.md          # 退换货
│   │   ├── product_inquiry.md # 商品咨询
│   │   └── complaint.md       # 投诉建议
│   └── handoff_detection.md   # 转人工判断
├── src/                        # 源代码
│   ├── __init__.py
│   ├── bot.py                  # 主逻辑（对话流程编排）
│   ├── intent_classifier.py   # 意图分类器
│   ├── response_generator.py  # 回复生成器
│   └── utils.py                # 工具函数
├── tests/                      # 测试
│   ├── test_data/
│   │   ├── intent_test.json   # 意图识别测试数据
│   │   └── response_test.json # 回复质量测试数据
│   ├── test_intent.py         # 意图识别测试
│   └── test_response.py       # 回复质量测试
├── .env.example                # 环境变量模板
├── requirements.txt            # 依赖
└── README.md                   # 本文件
```

## 功能特点

1. **意图识别**：基于Few-shot提示词，识别6类用户意图
   - 订单查询、退换货、商品咨询、投诉建议、账户问题、其他

2. **智能回复**：根据意图使用不同提示词模板生成个性化回复

3. **转人工判断**：4条规则自动判断是否需要转接人工客服

4. **对话历史**：支持多轮对话，上下文感知

5. **测试体系**：意图准确率测试 + 回复质量测试

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，确保 LM Studio 配置正确

# 3. 启动 LM Studio 并加载模型

# 4. 交互式测试
python -m src.bot

# 5. 运行意图识别测试
python tests/test_intent.py

# 6. 运行回复质量测试
python tests/test_response.py
```

## 示例对话

```
用户：我的订单什么时候到？
[意图：order_query，置信度：0.90]
客服：您好！您可以在"我的订单"页面查看物流详情...

用户：你们服务太差了！
[意图：complaint，置信度：0.90]
客服：非常抱歉给您带来不好的体验...
[系统]：已转人工客服
```

## 涉及的提示词技巧

- **Few-shot**：意图识别中提供6个示例
- **角色设定**：每个回复模板都设定了"专业电商客服"角色
- **输出约束**：限制回复长度、要求包含特定要点
- **上下文注入**：将对话历史注入提示词实现多轮对话

## 简历亮点

```
• 独立开发智能客服系统，意图识别准确率90%+
• 设计并优化多个提示词模板，覆盖6类用户意图
• 建立提示词测试体系，包含准确率测试和回复质量测试
• 掌握RTCF/CRISPE/CO-STAR等提示词框架的实战应用
```
