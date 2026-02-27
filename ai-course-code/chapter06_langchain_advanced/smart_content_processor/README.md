# 🧠 智能内容处理系统 - Smart Content Processor

第6章第36课的综合实战项目，整合Chain高级应用的所有知识点。

## 项目结构

```
smart_content_processor/
├── src/
│   ├── __init__.py       # 包初始化
│   ├── config.py         # 配置管理
│   ├── monitor.py        # 系统监控（Callback）
│   ├── analyzer.py       # 文章类型分析器（Router决策）
│   ├── processor.py      # 内容处理Pipeline（SequentialChain）
│   ├── router.py         # 智能路由系统
│   └── system.py         # 主系统入口
├── tests/
│   └── test_system.py    # 测试套件
├── main.py               # 演示入口
├── .env                  # 环境变量
├── requirements.txt      # 依赖
└── README.md             # 本文件
```

## 系统架构

```
用户输入文章
     ↓
[ArticleAnalyzer] → 分析类型（tech/news/general）
     ↓
[SmartRouter] → 路由到对应处理器
     ↓
[ContentProcessor - SequentialChain]
  ├─ 1. 总结生成（根据类型定制提示词）
  ├─ 2. 关键词提取
  ├─ 3. 英文翻译
  └─ 4. 配图建议
     ↓
[SystemMonitor] → 性能监控 + 成本统计
     ↓
[Memory] → 记录处理历史
     ↓
返回结果
```

## 涉及的LangChain知识点

| 课程 | 知识点 | 在本项目中的应用 |
|------|--------|-----------------|
| 第30课 | SequentialChain | 4步处理流水线 |
| 第31课 | RouterChain | 文章类型路由 |
| 第32课 | Memory | 处理历史记录 |
| 第33课 | Callback | 系统监控面板 |
| 第35课 | 性能优化 | InMemoryCache缓存 |

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动LM Studio并加载模型

# 3. 运行演示
python main.py

# 4. 运行测试
python tests/test_system.py
```

## 演示模式

运行 `python main.py` 后可选择：
1. 单篇文章处理
2. 批量处理
3. 缓存性能对比
4. 交互式处理
5. 运行全部演示

## 简历亮点

```
• 开发智能内容处理系统，支持文章自动分析、总结、翻译
• 使用RouterChain实现智能路由，SequentialChain编排处理流程
• 基于Callback实现完整的性能监控和成本统计
• 集成InMemoryCache缓存，重复请求加速数倍
• 模块化架构设计，支持批量处理和交互式处理
```
