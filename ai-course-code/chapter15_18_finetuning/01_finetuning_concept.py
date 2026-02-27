"""
第15-18章-模型微调：微调概念
对应课程：第79-80课

微调 = 在预训练模型基础上，用自己的数据继续训练
让通用模型变成专用模型
"""


def demo_why_finetune():
    """为什么要微调"""
    print("=" * 60)
    print("为什么要微调？")
    print("=" * 60)
    
    print("""
场景：你要做一个法律咨询AI

方案1：直接用GPT
- 通用能力强
- 但法律专业知识不够深
- 可能会"胡说八道"

方案2：RAG增强
- 检索法律文档
- 结合LLM回答
- 但理解能力受限于基础模型

方案3：微调专用模型
- 用大量法律数据训练
- 模型"学会"法律知识
- 回答更专业、更准确

什么时候用微调？
✅ 需要特定领域专业能力
✅ 需要特定的输出风格/格式
✅ 通用模型效果不够好
✅ 有足够的训练数据

什么时候不需要？
❌ 通用任务，GPT已经够好
❌ 没有足够的训练数据
❌ 资源有限（微调需要GPU）
""")


def demo_finetune_types():
    """微调类型"""
    print("\n" + "=" * 60)
    print("微调类型")
    print("=" * 60)
    
    print("""
1. 全参数微调（Full Fine-tuning）
   - 更新模型所有参数
   - 效果最好
   - 但需要大量GPU内存
   - 7B模型需要约60GB显存
   
2. LoRA微调（推荐）
   - 只训练小部分参数
   - 效果接近全参数
   - 显存需求大幅降低
   - 7B模型约16GB显存
   
3. QLoRA微调
   - LoRA + 量化
   - 进一步降低显存
   - 7B模型约8GB显存
   - 适合消费级GPU

对比：
┌─────────────┬─────────┬─────────┬─────────┐
│ 方法        │ 显存    │ 效果    │ 速度    │
├─────────────┼─────────┼─────────┼─────────┤
│ 全参数微调   │ 很高    │ 最好    │ 慢      │
│ LoRA        │ 中等    │ 很好    │ 快      │
│ QLoRA       │ 低      │ 好      │ 较快    │
└─────────────┴─────────┴─────────┴─────────┘
""")


def demo_finetune_process():
    """微调流程"""
    print("\n" + "=" * 60)
    print("微调完整流程")
    print("=" * 60)
    
    print("""
Step 1: 准备数据
- 收集领域数据
- 清洗、标注
- 转换为训练格式

Step 2: 选择基座模型
- Qwen2、Llama3、ChatGLM...
- 根据任务选择大小

Step 3: 配置训练参数
- 学习率、batch_size
- LoRA参数（rank、alpha）
- 训练轮数

Step 4: 开始训练
- 加载模型和数据
- 启动训练
- 监控Loss

Step 5: 评估模型
- 测试集评估
- 人工测试
- 对比基座模型

Step 6: 部署使用
- 合并LoRA权重
- 量化压缩
- 部署上线
""")


def demo_data_format():
    """数据格式"""
    print("\n" + "=" * 60)
    print("训练数据格式")
    print("=" * 60)
    
    print("""
常用格式：Alpaca格式

{
  "instruction": "用户的指令/问题",
  "input": "可选的输入内容",
  "output": "期望的回答"
}

示例1：问答
{
  "instruction": "什么是合同法？",
  "input": "",
  "output": "合同法是调整平等主体之间..."
}

示例2：带输入
{
  "instruction": "翻译成英文",
  "input": "今天天气真好",
  "output": "The weather is really nice today."
}

示例3：对话格式
{
  "conversations": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的？"}
  ]
}
""")


if __name__ == "__main__":
    demo_why_finetune()
    demo_finetune_types()
    demo_finetune_process()
    demo_data_format()
    
    print("\n" + "=" * 60)
    print("✅ 微调概念学习完成！")
    print("\n关键记忆：")
    print("  • 微调让通用模型变专用模型")
    print("  • LoRA是最佳性价比选择")
    print("  • 数据质量 > 数据数量")

