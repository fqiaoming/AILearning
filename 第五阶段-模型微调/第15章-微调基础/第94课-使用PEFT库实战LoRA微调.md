![模型微调流程](./images/finetune.svg)
*图：模型微调流程*

# 第94课：使用PEFT库实战LoRA微调

> **本课目标**：掌握HuggingFace PEFT库进行高效LoRA微调
> 
> **核心技能**：PEFT配置、训练流程、模型保存加载、实战技巧
> 
> **学习时长**：95分钟

---

## 📖 口播文案（6分钟）
![Hyperparams](./images/hyperparams.svg)
*图：Hyperparams*


### 🎯 前言

"上节课我们从零实现了LoRA，理解了底层原理。

但实际项目中，你不需要自己写LoRA！

**有一个神器：HuggingFace PEFT库！**

**PEFT = Parameter-Efficient Fine-Tuning**
**参数高效微调 = 一行代码搞定LoRA！**

**PEFT库有多强大？**

**对比：手写 vs PEFT**

**手写LoRA（上节课）：**
```python
# 需要200+行代码
class LoRALayer(nn.Module):
    def __init__(...):
        # 定义A、B矩阵
        ...
    
    def forward(...):
        # 实现前向传播
        ...

# 还要手动：
# • 找到所有目标层
# • 替换为LoRA层
# • 处理保存加载
# • 实现合并逻辑
# ...

费时费力！
```

**使用PEFT库：**
```python
from peft import LoraConfig, get_peft_model

# 配置LoRA（3行代码）
config = LoraConfig(
    r=8,
    target_modules=["q_proj", "v_proj"]
)

# 应用LoRA（1行代码）
model = get_peft_model(model, config)

# 完成！✅
```

**差距：200行 vs 4行！**

**PEFT库的5大优势：**

**优势1：开箱即用**
```
支持所有主流模型：
• LLaMA、Qwen
• GPT、Mistral
• BLOOM、Falcon
• ...

无需手动适配！
```

**优势2：配置灵活**
```python
LoraConfig(
    r=8,                    # 秩
    lora_alpha=16,          # 缩放因子
    target_modules=[...],   # 目标模块
    lora_dropout=0.1,       # Dropout
    bias="none",            # 偏置处理
    task_type="CAUSAL_LM"   # 任务类型
)

所有参数都可调！
```

**优势3：自动优化**
```
自动处理：
• 内存优化
• 梯度检查点
• 混合精度训练
• 分布式训练

不需要你操心！
```

**优势4：无缝集成**
```python
# 与Transformers完美集成
from transformers import Trainer

trainer = Trainer(
    model=peft_model,  # 直接使用
    args=training_args,
    train_dataset=dataset,
)

trainer.train()  # 开始训练！
```

**优势5：生态丰富**
```
• 官方文档完善
• 社区支持强
• 示例代码多
• 持续更新

遇到问题有人帮！
```

**PEFT支持的方法：**

```
【不只是LoRA】

PEFT支持多种方法：

1. LoRA (Low-Rank Adaptation)
   • 最流行
   • 效果最好
   • 推荐使用

2. Prefix Tuning
   • 只训练prefix
   • 参数更少

3. P-Tuning
   • 提示学习
   • 适合小数据

4. Prompt Tuning
   • 软提示
   • 极简方法

5. AdaLoRA
   • 自适应LoRA
   • 更智能

6. (IA)³
   • 注意力缩放
   • 参数极少

但最常用的还是：LoRA！
```

**完整的PEFT微调流程：**

```
【5步搞定微调】

Step 1: 加载基础模型
model = AutoModelForCausalLM.from_pretrained(...)

Step 2: 配置LoRA
config = LoraConfig(r=8, ...)

Step 3: 应用LoRA
model = get_peft_model(model, config)

Step 4: 训练
trainer.train()

Step 5: 保存
model.save_pretrained("output/")

完成！
```

**PEFT的内存优化：**

```
【显存占用对比】

场景：微调7B模型

不使用PEFT：
• 模型：14GB
• 梯度：14GB
• 优化器：28GB
• 总计：56GB+
需要：A100 (80GB)

使用PEFT：
• 模型：14GB（冻结）
• LoRA参数：100MB
• 梯度：100MB
• 优化器：200MB
• 总计：15GB
需要：RTX 3090 (24GB) ✅

差距：3.7倍！
```

**PEFT的训练速度：**

```
【速度对比】

7B模型，5000条数据，3个epoch

全量微调：
• 单卡3090：无法运行
• 单卡A100：18小时
• 成本：$300+

PEFT LoRA：
• 单卡3090：6小时
• 单卡A100：3小时
• 成本：$75

快4-6倍！
便宜4倍！
```

**PEFT的实战技巧：**

**技巧1：选择合适的目标模块**
```python
# 推荐配置
target_modules = [
    "q_proj",    # Query投影（必选）
    "v_proj",    # Value投影（必选）
    "k_proj",    # Key投影（可选）
    "o_proj",    # Output投影（可选）
]

经验：
• 简单任务：只用q_proj, v_proj
• 复杂任务：加上k_proj, o_proj
```

**技巧2：根据显存调整rank**
```
显存充足（24GB+）：
rank = 16-32

显存一般（12-24GB）：
rank = 8-16

显存紧张（<12GB）：
rank = 4-8

原则：能大就大，但别过拟合
```

**技巧3：使用8bit量化**
```python
# 加载模型时量化
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,  # 8bit量化
    device_map="auto"
)

显存减半！
```

**技巧4：梯度检查点**
```python
model.gradient_checkpointing_enable()

# 显存减少30-50%
# 速度略慢10-20%

值得！
```

**技巧5：混合精度训练**
```python
training_args = TrainingArguments(
    fp16=True,  # 混合精度
    ...
)

速度提升2倍！
显存减少50%！
```

**PEFT的保存和加载：**

```python
【保存】
# 只保存LoRA权重（小！）
model.save_pretrained("lora_weights/")

# 文件大小：10-100MB

【加载】
# 先加载基础模型
base_model = AutoModelForCausalLM.from_pretrained(...)

# 再加载LoRA
from peft import PeftModel
model = PeftModel.from_pretrained(
    base_model,
    "lora_weights/"
)

# 完成！

【合并】
# 合并LoRA到基础模型
model = model.merge_and_unload()

# 保存完整模型
model.save_pretrained("merged_model/")
```

**常见问题与解决：**

**问题1：显存不足**
```
解决方案：
1. 降低rank (16→8→4)
2. 减少batch_size
3. 启用梯度检查点
4. 使用8bit量化
5. 减少序列长度
```

**问题2：loss不下降**
```
解决方案：
1. 检查数据格式
2. 调整学习率
3. 增加target_modules
4. 增加rank
5. 检查数据质量
```

**问题3：过拟合**
```
解决方案：
1. 降低rank
2. 增加dropout
3. 减少epoch
4. 增加数据量
5. 使用early stopping
```

**今天这一课，我要带你：**

**第一部分：PEFT库入门**
- 安装配置
- 核心概念
- 基本用法

**第二部分：LoRA配置详解**
- 所有参数
- 推荐配置
- 场景选择

**第三部分：完整训练流程**
- 数据准备
- 模型配置
- 训练监控
- 保存加载

**第四部分：性能优化**
- 内存优化
- 速度优化
- 分布式训练

**第五部分：实战案例**
- 完整代码
- 常见问题
- 最佳实践

学完这一课，你将掌握PEFT实战！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【站在巨人肩膀上】

不要重复造轮子
用最好的工具

PEFT = 微调的标准工具

【工具 + 理解 = 完美】

上节课：理解原理
本节课：使用工具

理论 + 实践 = 掌握微调
```

---

## 📚 第一部分：PEFT库入门

### 一、安装与环境配置

```bash
# 安装PEFT
pip install peft

# 安装依赖
pip install transformers
pip install datasets
pip install accelerate
pip install bitsandbytes  # 用于8bit量化

# 验证安装
python -c "import peft; print(peft.__version__)"
```

### 二、核心概念与基本用法

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
import torch

class PEFTQuickStart:
    """PEFT快速入门"""
    
    def __init__(self, model_name: str = "gpt2"):
        """
        初始化
        
        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def basic_usage(self):
        """基本用法演示"""
        
        print("="*60)
        print("PEFT基本用法")
        print("="*60)
        
        # 1. 加载基础模型
        print("\n1. 加载基础模型...")
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # 统计原始参数
        total_params = sum(p.numel() for p in model.parameters())
        print(f"   总参数: {total_params:,}")
        
        # 2. 配置LoRA
        print("\n2. 配置LoRA...")
        lora_config = LoraConfig(
            r=8,                              # LoRA秩
            lora_alpha=16,                    # 缩放因子
            target_modules=["c_attn"],        # 目标模块（GPT2）
            lora_dropout=0.1,                 # Dropout
            bias="none",                      # 不训练bias
            task_type=TaskType.CAUSAL_LM      # 任务类型
        )
        print(f"   LoRA配置: {lora_config}")
        
        # 3. 应用LoRA
        print("\n3. 应用LoRA...")
        model = get_peft_model(model, lora_config)
        
        # 统计可训练参数
        trainable_params = sum(
            p.numel() for p in model.parameters() if p.requires_grad
        )
        all_params = sum(p.numel() for p in model.parameters())
        trainable_percent = 100 * trainable_params / all_params
        
        print(f"   总参数: {all_params:,}")
        print(f"   可训练参数: {trainable_params:,}")
        print(f"   可训练比例: {trainable_percent:.4f}%")
        
        # 4. 打印模型结构
        print("\n4. 模型结构:")
        model.print_trainable_parameters()
        
        return model, tokenizer
    
    def test_inference(self, model, tokenizer):
        """测试推理"""
        
        print("\n" + "="*60)
        print("测试推理")
        print("="*60)
        
        # 测试文本
        prompt = "Hello, I am a"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # 生成
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=20,
                do_sample=True,
                temperature=0.7
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\nPrompt: {prompt}")
        print(f"Generated: {generated_text}")

# 演示
demo = PEFTQuickStart()
model, tokenizer = demo.basic_usage()
demo.test_inference(model, tokenizer)
```

---

## 💻 第二部分：LoRA配置详解

### 一、完整配置参数

```python
from peft import LoraConfig
from typing import Optional, List

def create_lora_config(
    # 基础参数
    r: int = 8,
    lora_alpha: int = 16,
    lora_dropout: float = 0.1,
    
    # 目标模块
    target_modules: Optional[List[str]] = None,
    
    # 高级参数
    bias: str = "none",
    fan_in_fan_out: bool = False,
    modules_to_save: Optional[List[str]] = None,
    
    # 任务类型
    task_type: str = "CAUSAL_LM"
) -> LoraConfig:
    """
    创建LoRA配置
    
    Args:
        r: LoRA秩（越大越强，但参数越多）
        lora_alpha: 缩放因子（通常=r或2*r）
        lora_dropout: Dropout率（防止过拟合）
        
        target_modules: 目标模块列表
        
        bias: 偏置处理方式
            - "none": 不训练bias
            - "all": 训练所有bias
            - "lora_only": 只训练LoRA的bias
        
        fan_in_fan_out: 权重是否转置（某些模型需要）
        modules_to_save: 额外需要训练的模块
        
        task_type: 任务类型
            - "CAUSAL_LM": 因果语言模型
            - "SEQ_2_SEQ_LM": 序列到序列
            - "SEQ_CLS": 序列分类
            - "TOKEN_CLS": 词分类
    """
    
    config = LoraConfig(
        r=r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        target_modules=target_modules,
        bias=bias,
        fan_in_fan_out=fan_in_fan_out,
        modules_to_save=modules_to_save,
        task_type=task_type
    )
    
    return config

# 不同模型的推荐配置
class LoraConfigPresets:
    """LoRA配置预设"""
    
    @staticmethod
    def llama_config(complexity: str = "medium") -> LoraConfig:
        """LLaMA模型配置"""
        
        configs = {
            "simple": {
                "r": 8,
                "lora_alpha": 16,
                "target_modules": ["q_proj", "v_proj"]
            },
            "medium": {
                "r": 16,
                "lora_alpha": 32,
                "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]
            },
            "complex": {
                "r": 32,
                "lora_alpha": 64,
                "target_modules": [
                    "q_proj", "v_proj", "k_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"
                ]
            }
        }
        
        cfg = configs[complexity]
        
        return LoraConfig(
            r=cfg["r"],
            lora_alpha=cfg["lora_alpha"],
            target_modules=cfg["target_modules"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
    
    @staticmethod
    def qwen_config(complexity: str = "medium") -> LoraConfig:
        """Qwen模型配置"""
        
        configs = {
            "simple": {
                "r": 8,
                "lora_alpha": 16,
                "target_modules": ["c_attn"]
            },
            "medium": {
                "r": 16,
                "lora_alpha": 32,
                "target_modules": ["c_attn", "c_proj"]
            },
            "complex": {
                "r": 32,
                "lora_alpha": 64,
                "target_modules": ["c_attn", "c_proj", "w1", "w2"]
            }
        }
        
        cfg = configs[complexity]
        
        return LoraConfig(
            r=cfg["r"],
            lora_alpha=cfg["lora_alpha"],
            target_modules=cfg["target_modules"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
    
    @staticmethod
    def print_all_presets():
        """打印所有预设配置"""
        
        print("\n" + "="*60)
        print("LoRA配置预设")
        print("="*60)
        
        print("\n【LLaMA系列】")
        for complexity in ["simple", "medium", "complex"]:
            config = LoraConfigPresets.llama_config(complexity)
            print(f"\n{complexity.upper()}:")
            print(f"  Rank: {config.r}")
            print(f"  Alpha: {config.lora_alpha}")
            print(f"  目标模块: {config.target_modules}")
        
        print("\n【Qwen系列】")
        for complexity in ["simple", "medium", "complex"]:
            config = LoraConfigPresets.qwen_config(complexity)
            print(f"\n{complexity.upper()}:")
            print(f"  Rank: {config.r}")
            print(f"  Alpha: {config.lora_alpha}")
            print(f"  目标模块: {config.target_modules}")

# 演示
LoraConfigPresets.print_all_presets()
```

---

## 🎯 第三部分：完整训练流程

### 一、端到端训练示例

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
import torch

class LoraTrainer:
    """LoRA训练器"""
    
    def __init__(
        self,
        model_name: str,
        output_dir: str = "./lora_output",
        lora_r: int = 8,
        lora_alpha: int = 16
    ):
        """
        初始化
        
        Args:
            model_name: 基础模型名称
            output_dir: 输出目录
            lora_r: LoRA秩
            lora_alpha: LoRA alpha
        """
        self.model_name = model_name
        self.output_dir = output_dir
        self.lora_r = lora_r
        self.lora_alpha = lora_alpha
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")
    
    def prepare_model(self):
        """准备模型"""
        
        print("\n" + "="*60)
        print("准备模型")
        print("="*60)
        
        # 1. 加载基础模型
        print("\n1. 加载基础模型...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 2. 加载tokenizer
        print("2. 加载tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        # 设置pad_token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # 3. 配置LoRA
        print("3. 配置LoRA...")
        lora_config = LoraConfig(
            r=self.lora_r,
            lora_alpha=self.lora_alpha,
            target_modules=["c_attn"],  # 根据模型调整
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        # 4. 应用LoRA
        print("4. 应用LoRA...")
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
    
    def prepare_data(self, dataset_name: str = "wikitext"):
        """准备数据"""
        
        print("\n" + "="*60)
        print("准备数据")
        print("="*60)
        
        # 1. 加载数据集
        print("\n1. 加载数据集...")
        if dataset_name == "wikitext":
            dataset = load_dataset("wikitext", "wikitext-2-raw-v1")
            train_dataset = dataset["train"]
            eval_dataset = dataset["validation"]
        else:
            # 自定义数据集
            dataset = load_dataset("json", data_files=dataset_name)
            train_dataset = dataset["train"]
            eval_dataset = None
        
        print(f"   训练样本: {len(train_dataset)}")
        if eval_dataset:
            print(f"   验证样本: {len(eval_dataset)}")
        
        # 2. 数据预处理
        print("\n2. 数据预处理...")
        
        def preprocess_function(examples):
            # Tokenize
            result = self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=512,
                padding="max_length"
            )
            result["labels"] = result["input_ids"].copy()
            return result
        
        train_dataset = train_dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=train_dataset.column_names
        )
        
        if eval_dataset:
            eval_dataset = eval_dataset.map(
                preprocess_function,
                batched=True,
                remove_columns=eval_dataset.column_names
            )
        
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset
        
        print("   数据准备完成!")
    
    def train(
        self,
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 2e-4,
        save_steps: int = 500
    ):
        """训练模型"""
        
        print("\n" + "="*60)
        print("开始训练")
        print("="*60)
        
        # 训练参数
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=learning_rate,
            
            # 优化
            fp16=True,                          # 混合精度
            gradient_accumulation_steps=4,      # 梯度累积
            gradient_checkpointing=True,        # 梯度检查点
            
            # 保存策略
            save_strategy="steps",
            save_steps=save_steps,
            save_total_limit=3,
            
            # 评估策略
            evaluation_strategy="steps" if self.eval_dataset else "no",
            eval_steps=save_steps if self.eval_dataset else None,
            
            # 日志
            logging_steps=100,
            logging_dir=f"{self.output_dir}/logs",
            
            # 其他
            load_best_model_at_end=True if self.eval_dataset else False,
            report_to="none"
        )
        
        # 数据整理器
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # 创建Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            data_collator=data_collator
        )
        
        # 开始训练
        print("\n开始训练...")
        trainer.train()
        
        # 保存模型
        print("\n保存模型...")
        trainer.save_model(self.output_dir)
        
        print(f"\n训练完成! 模型保存在: {self.output_dir}")
    
    def save_lora_weights(self, save_path: str):
        """只保存LoRA权重"""
        
        self.model.save_pretrained(save_path)
        print(f"LoRA权重已保存到: {save_path}")

# 演示（注释掉实际训练，仅展示用法）
"""
# 创建训练器
trainer = LoraTrainer(
    model_name="gpt2",
    output_dir="./lora_gpt2",
    lora_r=8,
    lora_alpha=16
)

# 准备模型
trainer.prepare_model()

# 准备数据
trainer.prepare_data()

# 训练
trainer.train(
    num_epochs=3,
    batch_size=4,
    learning_rate=2e-4
)

# 保存
trainer.save_lora_weights("./lora_weights")
"""

print("\n训练器已就绪（代码示例）")
```

---

## 📝 课后练习

### 练习1：配置LoRA
为不同任务选择合适的LoRA配置

### 练习2：训练模型
使用PEFT训练一个小模型

### 练习3：性能对比
对比不同rank的效果

---

## 🎓 知识总结

### 核心要点

1. **PEFT优势**
   - 开箱即用
   - 配置灵活
   - 自动优化
   - 无缝集成

2. **LoRA配置**
   - rank: 8-32
   - alpha: 16-64
   - target_modules: 根据模型
   - dropout: 0.05-0.1

3. **训练流程**
   - 加载模型
   - 应用LoRA
   - 准备数据
   - 训练保存

4. **性能优化**
   - 8bit量化
   - 混合精度
   - 梯度检查点
   - 批量累积

---

## 🚀 下节预告

下一课：**第95课：实战-第一个LoRA微调项目**

- 完整项目
- 从数据到部署
- 性能评估
- 避坑指南

**实战出真知！** 🔥

---

**💪 记住：PEFT是微调的最佳工具！**

**下一课见！** 🎉
