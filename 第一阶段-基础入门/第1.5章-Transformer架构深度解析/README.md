# 第1.5章：Transformer架构深度解析

## 📚 课程概述

本章深入讲解Transformer架构的核心原理，并提供完整的可运行代码示例。

## 📖 课程列表

### 第04.1课：Transformer原理 - 注意力机制深度剖析
- **内容**：Self-Attention机制原理和数学推导
- **代码**：
  - `self_attention.py` - 从零实现Self-Attention
  - `visualize_attention.py` - 可视化注意力权重
  - `text_attention.py` - 在真实文本上测试

### 第04.2课：Transformer架构 - 编码器与解码器
- **内容**：Multi-Head Attention和完整Transformer架构
- **代码**：
  - `multi_head_attention.py` - Multi-Head Attention实现
  - `encoder_block.py` - 完整的Encoder Block
  - `visualize_multihead.py` - 可视化多头注意力

### 第04.3课：位置编码与Layer Normalization详解
- **内容**：位置编码的数学原理和LayerNorm
- **代码**：
  - `positional_encoding.py` - 位置编码实现和可视化
  - `layer_normalization.py` - Layer Norm实现和对比
  - `transformer_input.py` - 完整的输入处理流程

### 第04.4课：实战 - 从零实现Mini-Transformer
- **内容**：整合所有组件，实现完整Transformer
- **代码**：
  - `mini_transformer.py` - 完整的Mini-Transformer
  - `train_transformer.py` - 训练循环示例
  - `compare_configs.py` - 对比不同配置

## 🚀 快速开始

### 环境要求

```bash
# Python 3.10+
python --version

# 安装依赖
pip install numpy matplotlib
```

### 运行示例

```bash
# 进入本章目录
cd "/Users/qiao/AI学习/第一阶段-基础入门/第1.5章-Transformer架构深度解析"

# 运行第一课的代码
python self_attention.py
python visualize_attention.py
python text_attention.py

# 运行第二课的代码
python multi_head_attention.py
python encoder_block.py
python visualize_multihead.py

# 运行第三课的代码
python positional_encoding.py
python layer_normalization.py
python transformer_input.py

# 运行第四课的代码（完整Transformer）
python mini_transformer.py
python train_transformer.py
python compare_configs.py
```

## 📊 代码结构

```
第1.5章-Transformer架构深度解析/
├── 第04.1课-Transformer原理-注意力机制深度剖析.md
├── 第04.2课-Transformer架构-编码器与解码器.md
├── 第04.3课-位置编码与Layer-Normalization详解.md
├── 第04.4课-实战-从零实现Mini-Transformer.md
└── README.md (本文件)
```

## ✅ 学习检查清单

完成本章后，你应该能够：
- [ ] 理解Self-Attention的数学原理
- [ ] 实现Multi-Head Attention
- [ ] 理解位置编码的作用
- [ ] 知道为什么用Layer Norm而不是Batch Norm
- [ ] 从零实现一个完整的Transformer Encoder
- [ ] 可视化注意力权重
- [ ] 理解Transformer的每个组件

## 💡 代码特点

1. ✅ **纯NumPy实现**：不依赖PyTorch/TensorFlow，便于理解原理
2. ✅ **完整可运行**：所有代码都经过测试，可以直接运行
3. ✅ **详细注释**：每个函数都有清晰的注释和参数说明
4. ✅ **可视化丰富**：提供注意力权重、位置编码等多种可视化
5. ✅ **循序渐进**：从简单到复杂，逐步构建完整模型

## 🎯 下一步

完成本章后，你将对Transformer有深入的理解，这将帮助你：
- 更好地使用GPT、BERT等预训练模型
- 理解LangChain等框架的底层原理
- 进行模型微调和优化
- 设计新的模型架构

继续学习：`第二阶段-核心技能/第4章-OpenAI-API/`

---

**🎉 祝学习愉快！如有问题，请查看课程文档或运行代码示例。**


