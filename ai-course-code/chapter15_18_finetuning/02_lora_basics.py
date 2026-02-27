"""
第15-18章-模型微调：LoRA基础
对应课程：第83-84课

LoRA = Low-Rank Adaptation
核心思想：冻结原始权重，只训练小的"补丁"
"""


def demo_lora_principle():
    """LoRA原理"""
    print("=" * 60)
    print("LoRA原理")
    print("=" * 60)
    
    print("""
传统微调的问题：
- 7B模型有70亿参数
- 全部训练需要大量显存
- 每个任务都要保存完整模型

LoRA的解决方案：
- 冻结原始模型权重（不更新）
- 添加小的"低秩矩阵"
- 只训练这些小矩阵

数学原理（简化版）：
原始权重: W (很大的矩阵)
LoRA补丁: A × B (两个小矩阵相乘)

推理时: W + A × B

参数对比：
- 原始W: 1000 × 1000 = 1,000,000参数
- LoRA: 1000 × 8 + 8 × 1000 = 16,000参数
- 减少了98%的可训练参数！
""")


def demo_lora_config():
    """LoRA配置参数"""
    print("\n" + "=" * 60)
    print("LoRA关键参数")
    print("=" * 60)
    
    print("""
1. rank (r)
   - 低秩矩阵的秩
   - 越大效果越好，但参数越多
   - 常用值：8, 16, 32, 64
   - 推荐从8开始

2. alpha
   - 缩放系数
   - 通常设为rank的2倍
   - alpha/rank = 缩放比例

3. target_modules
   - 要添加LoRA的层
   - 常见选择：q_proj, v_proj, k_proj, o_proj
   - 也可以加MLP层

4. dropout
   - 防止过拟合
   - 常用值：0.05, 0.1
""")
    
    # 配置示例
    config_example = """
# LoRA配置示例（使用PEFT库）
from peft import LoraConfig

lora_config = LoraConfig(
    r=8,                    # 秩
    lora_alpha=16,          # 缩放系数
    target_modules=[        # 目标层
        "q_proj",
        "v_proj",
        "k_proj",
        "o_proj"
    ],
    lora_dropout=0.05,      # dropout
    bias="none",            # 是否训练bias
    task_type="CAUSAL_LM"   # 任务类型
)
"""
    print(config_example)


def demo_training_code():
    """训练代码框架"""
    print("\n" + "=" * 60)
    print("LoRA训练代码框架")
    print("=" * 60)
    
    code = """
# Step 1: 加载基座模型
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-7B-Instruct",
    torch_dtype=torch.float16
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")

# Step 2: 添加LoRA
from peft import get_peft_model

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# 输出：trainable params: 4,194,304 || all params: 7,615,616,000
# 只训练0.05%的参数！

# Step 3: 准备数据
from datasets import load_dataset
dataset = load_dataset("json", data_files="train.json")

# Step 4: 训练
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=100
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

trainer.train()

# Step 5: 保存LoRA权重
model.save_pretrained("./lora_weights")
"""
    print(code)


def demo_merge_and_deploy():
    """合并与部署"""
    print("\n" + "=" * 60)
    print("合并LoRA权重与部署")
    print("=" * 60)
    
    print("""
训练完成后，有两种使用方式：

方式1：动态加载（推荐开发阶段）
- 保持基座模型和LoRA权重分离
- 运行时动态加载
- 方便切换不同的LoRA

方式2：合并权重（推荐部署阶段）
- 将LoRA权重合并到基座模型
- 生成完整的微调后模型
- 推理更快，部署更简单
""")
    
    merge_code = """
# 合并LoRA权重
from peft import PeftModel

# 加载基座模型
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B-Instruct")

# 加载LoRA权重
model = PeftModel.from_pretrained(base_model, "./lora_weights")

# 合并
merged_model = model.merge_and_unload()

# 保存合并后的模型
merged_model.save_pretrained("./merged_model")
tokenizer.save_pretrained("./merged_model")
"""
    print(merge_code)


if __name__ == "__main__":
    demo_lora_principle()
    demo_lora_config()
    demo_training_code()
    demo_merge_and_deploy()
    
    print("\n" + "=" * 60)
    print("✅ LoRA基础学习完成！")
    print("\n关键记忆：")
    print("  • LoRA只训练0.05%的参数")
    print("  • rank从8开始，效果不好再增大")
    print("  • 训练完可以合并权重部署")

