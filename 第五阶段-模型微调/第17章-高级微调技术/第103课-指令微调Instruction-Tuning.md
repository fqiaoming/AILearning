![高级微调技术](./images/advanced_ft.svg)
*图：高级微调技术*

# 第103课：指令微调（Instruction Tuning）

> **本课目标**：掌握指令微调技术，提升模型指令遵循能力
> 
> **核心技能**：指令构造、数据格式、Alpaca方法、实战应用
> 
> **学习时长**：95分钟

---

## 📖 口播文案（7分钟）
![Lora](./images/lora.svg)
*图：Lora*


### 🎯 前言

"前面我们学习了基础微调技术。

但你可能发现一个问题：

**模型不听话！**

**问题场景：**

```
你的需求：
"请用JSON格式输出3个城市的信息"

基础微调模型输出：
"北京是中国的首都，人口约2200万...
上海是中国的经济中心，位于长江入海口...
广州是广东省的省会..."

❌ 完全没有按JSON格式！

期望输出：
{
  "cities": [
    {"name": "北京", "population": 22000000},
    {"name": "上海", "population": 24000000},
    {"name": "广州", "population": 15000000}
  ]
}

✅ 这才是想要的！
```

**核心问题：模型不理解"指令"！**

**今天要学习的：指令微调（Instruction Tuning）**

**让模型学会听话，遵循指令！**

---

### 💡 什么是指令微调？

**传统微调 vs 指令微调：**

```
【传统微调】

训练数据：
"这部电影很好看" → "正面评价"
"这家餐厅很难吃" → "负面评价"

学到的能力：
• 情感分类

局限：
• 只会这一个任务
• 无法泛化

【指令微调】

训练数据：
指令："判断这段文本的情感"
输入："这部电影很好看"
输出："正面评价"

指令："将以下内容翻译成英文"
输入："你好"
输出："Hello"

指令："用JSON格式总结"
输入："北京是首都"
输出：{"city": "北京", "type": "首都"}

学到的能力：
• 理解各种指令
• 按要求执行
• 泛化能力强

革命性的区别！
```

**指令微调的威力：**

```
【没有指令微调】

问："天气怎么样？"
答："天气很好，阳光明媚..."
（不知道你想要什么）

【指令微调后】

问："用JSON格式告诉我今天天气"
答：{"weather": "sunny", "temp": 25}

问："用一句话总结今天天气"
答："今天天气晴朗，气温25度"

问："用emoji表情说明天气"
答："☀️ 🌡️25°C"

同样的问题，不同的指令，
模型都能准确理解和执行！
```

**指令微调的核心要素：**

```
【三要素】

1. 指令（Instruction）
   • 明确的任务描述
   • "请翻译"、"请总结"、"请分类"

2. 输入（Input）
   • 要处理的内容
   • 可选（有些任务不需要）

3. 输出（Output）
   • 期望的结果
   • 必须符合指令要求

【标准格式】

### 指令：
{任务描述}

### 输入：
{待处理内容}

### 输出：
{期望结果}
```

**经典案例：Alpaca**

```
【斯坦福Alpaca项目】

2023年3月，斯坦福大学：
• 用52K指令数据
• 微调LLaMA 7B
• 仅用600美元
• 达到GPT-3.5的80%能力

震撼全球！

核心方法：
1. 用GPT-3.5生成52K指令数据
2. 指令微调LLaMA
3. 开源所有代码和数据

证明：
• 小数据也能出效果
• 指令微调是关键
• 成本可以很低
```

**指令数据构造：**

```
【Self-Instruct方法】

Step 1: 种子任务
• 人工设计175个种子指令
• 涵盖不同任务类型

Step 2: 生成新指令
• 用GPT-3.5看种子
• 生成新的指令
• 自动筛选去重

Step 3: 生成输出
• 对每个指令
• 生成对应输出

结果：
• 52K高质量指令数据
• 任务多样化
• 覆盖面广

成本：
• API费用约$500
• 人工审核$100

总计：$600！
```

**指令类型分类：**

```
【8大类型】

1. 问答型
   "回答以下问题：什么是AI？"

2. 生成型
   "写一首关于春天的诗"

3. 改写型
   "将以下内容改写得更专业"

4. 总结型
   "总结以下文章的要点"

5. 翻译型
   "将以下内容翻译成英文"

6. 分类型
   "判断这段文本的情感倾向"

7. 抽取型
   "从文本中提取所有人名"

8. 推理型
   "根据以下信息推理结论"

覆盖全面！
```

**数据质量要求：**

```
【高质量指令数据】

✅ 好的示例：

指令：请用JSON格式提取文本中的关键信息
输入：苹果公司于2024年1月发布了新款iPhone
输出：
{
  "company": "苹果公司",
  "date": "2024年1月",
  "product": "新款iPhone",
  "event": "发布"
}

特点：
• 指令清晰
• 输入具体
• 输出准确
• 格式规范

❌ 差的示例：

指令：处理一下
输入：一些文本
输出：处理结果

问题：
• 指令模糊
• 输入随意
• 输出不明确
```

**效果对比：**

```
【相同模型，不同训练】

模型：Qwen2-7B

基础微调（1万条QA数据）：
• 准确回答问题：85%
• 遵循格式要求：40%
• 多任务能力：30%

指令微调（1万条指令数据）：
• 准确回答问题：90%
• 遵循格式要求：92%
• 多任务能力：88%

指令微调完胜！
```

**实际应用场景：**

```
场景1：智能客服
指令："作为客服，用友好的语气回答客户问题"
→ 模型学会客服风格

场景2：代码助手
指令："根据需求生成Python代码，并添加注释"
→ 模型生成带注释的代码

场景3：内容创作
指令："写一篇500字的科技新闻，风格专业"
→ 模型生成专业新闻稿

场景4：数据分析
指令："分析以下数据，用表格和图表呈现"
→ 模型生成结构化分析

适用广泛！
```

**与基础微调的对比：**

```
【数据需求】
基础微调：需要大量特定任务数据
指令微调：多样化指令数据

【泛化能力】
基础微调：只会训练的任务
指令微调：可以迁移到新任务

【训练成本】
基础微调：每个任务都要重新训练
指令微调：一次训练，多任务适用

【效果】
基础微调：单任务效果好
指令微调：多任务都不错

结论：
指令微调是通用AI的基础！
```

**今天这一课，我要带你：**

**第一部分：指令微调原理**
- 核心概念
- 与传统微调的区别
- 理论基础

**第二部分：数据构造方法**
- Self-Instruct
- Alpaca方法
- 数据格式

**第三部分：实战训练**
- 完整代码
- 训练流程
- 效果评估

**第四部分：高级技巧**
- 多任务平衡
- 质量控制
- 最佳实践

**第五部分：实战案例**
- 多功能助手
- 完整实现
- 部署应用

学完这一课，你将掌握指令微调的精髓！

准备好了吗？让我们开始！"

---

## 📚 第一部分：指令微调原理

### 一、指令数据格式

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class InstructionExample:
    """指令示例"""
    instruction: str  # 任务指令
    input: Optional[str] = None  # 输入内容（可选）
    output: str = ""  # 期望输出
    
    def to_dict(self) -> Dict:
        """转为字典"""
        data = {
            "instruction": self.instruction,
            "output": self.output
        }
        if self.input:
            data["input"] = self.input
        return data
    
    def to_prompt(self) -> str:
        """转为prompt格式"""
        if self.input:
            prompt = f"""### 指令：
{self.instruction}

### 输入：
{self.input}

### 输出：
{self.output}"""
        else:
            prompt = f"""### 指令：
{self.instruction}

### 输出：
{self.output}"""
        
        return prompt

class InstructionDataset:
    """指令数据集"""
    
    @staticmethod
    def create_diverse_examples() -> List[InstructionExample]:
        """创建多样化指令示例"""
        
        examples = []
        
        # 1. 问答型
        examples.append(InstructionExample(
            instruction="请回答以下问题",
            input="什么是机器学习？",
            output="机器学习是人工智能的一个分支，它使计算机系统能够从数据中学习和改进，而无需显式编程。主要包括监督学习、无监督学习和强化学习三大类。"
        ))
        
        # 2. 生成型
        examples.append(InstructionExample(
            instruction="写一首关于春天的五言绝句",
            input=None,
            output="春风拂柳丝，\n花开满枝头。\n燕子归来时，\n万物皆复苏。"
        ))
        
        # 3. 格式转换
        examples.append(InstructionExample(
            instruction="将以下信息转换为JSON格式",
            input="公司名称：阿里巴巴，成立时间：1999年，创始人：马云",
            output='{\n  "company": "阿里巴巴",\n  "founded": "1999年",\n  "founder": "马云"\n}'
        ))
        
        # 4. 总结型
        examples.append(InstructionExample(
            instruction="用一句话总结以下文章",
            input="人工智能技术近年来发展迅速，在图像识别、自然语言处理、自动驾驶等领域取得了重大突破。深度学习作为AI的核心技术，推动了这些进展。",
            output="近年来人工智能特别是深度学习技术在多个领域取得重大突破。"
        ))
        
        # 5. 翻译型
        examples.append(InstructionExample(
            instruction="将以下中文翻译成英文",
            input="你好，世界！",
            output="Hello, World!"
        ))
        
        # 6. 分类型
        examples.append(InstructionExample(
            instruction="判断以下文本的情感倾向（正面/负面/中性）",
            input="这部电影真是太精彩了，强烈推荐！",
            output="正面"
        ))
        
        # 7. 抽取型
        examples.append(InstructionExample(
            instruction="从文本中提取所有人名",
            input="今天，张三和李四一起去见了王五。",
            output="张三、李四、王五"
        ))
        
        # 8. 推理型
        examples.append(InstructionExample(
            instruction="根据以下信息进行逻辑推理",
            input="所有的猫都是动物。加菲是一只猫。",
            output="因此，加菲是动物。这是一个三段论推理，从大前提和小前提推出结论。"
        ))
        
        return examples
    
    @staticmethod
    def print_examples():
        """打印示例"""
        
        print("="*60)
        print("指令数据格式示例")
        print("="*60)
        
        examples = InstructionDataset.create_diverse_examples()
        
        for i, example in enumerate(examples, 1):
            print(f"\n【示例{i}】")
            print(example.to_prompt())
            print("\n" + "-"*60)

# 演示
dataset = InstructionDataset()
dataset.print_examples()
```

---

## 💻 第二部分：Self-Instruct数据生成

### 一、自动生成指令数据

```python
import random
from typing import List

class SelfInstructGenerator:
    """Self-Instruct数据生成器"""
    
    def __init__(self):
        """初始化"""
        
        # 种子指令模板
        self.seed_templates = [
            "请{verb}{object}",
            "如何{verb}{object}",
            "什么是{object}",
            "解释{object}的概念",
            "列举{number}个{object}",
            "比较{object1}和{object2}",
            "将{object}转换为{format}格式",
        ]
        
        # 动词库
        self.verbs = [
            "分析", "总结", "翻译", "改写", "生成",
            "分类", "提取", "判断", "计算", "解释"
        ]
        
        # 对象库
        self.objects = [
            "文本", "数据", "信息", "内容", "代码",
            "问题", "答案", "文章", "段落", "句子"
        ]
        
        # 格式库
        self.formats = [
            "JSON", "表格", "列表", "Markdown",
            "HTML", "CSV", "XML"
        ]
    
    def generate_instruction(self) -> str:
        """生成指令"""
        
        template = random.choice(self.seed_templates)
        
        instruction = template.format(
            verb=random.choice(self.verbs),
            object=random.choice(self.objects),
            object1=random.choice(self.objects),
            object2=random.choice(self.objects),
            format=random.choice(self.formats),
            number=random.randint(3, 10)
        )
        
        return instruction
    
    def generate_batch(self, num_samples: int = 10) -> List[str]:
        """批量生成指令"""
        
        instructions = []
        seen = set()
        
        while len(instructions) < num_samples:
            instruction = self.generate_instruction()
            if instruction not in seen:
                instructions.append(instruction)
                seen.add(instruction)
        
        return instructions
    
    def print_generated_instructions(self, num_samples: int = 10):
        """打印生成的指令"""
        
        print("\n" + "="*60)
        print("Self-Instruct生成的指令")
        print("="*60)
        
        instructions = self.generate_batch(num_samples)
        
        for i, instruction in enumerate(instructions, 1):
            print(f"\n{i}. {instruction}")

# 演示
generator = SelfInstructGenerator()
generator.print_generated_instructions(20)
```

---

## 🎯 第三部分：指令微调实战

### 一、完整训练流程

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import torch

class InstructionTuner:
    """指令微调器"""
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2-7B",
        output_dir: str = "./instruction_tuned_model"
    ):
        """
        初始化
        
        Args:
            model_name: 基础模型
            output_dir: 输出目录
        """
        self.model_name = model_name
        self.output_dir = output_dir
        
        print("="*60)
        print("指令微调训练器")
        print("="*60)
    
    def prepare_instruction_data(
        self,
        examples: List[InstructionExample]
    ) -> Dataset:
        """准备指令数据"""
        
        print("\n准备指令数据...")
        
        # 转换为对话格式
        data = []
        for example in examples:
            # 构建prompt
            if example.input:
                user_message = f"""{example.instruction}

{example.input}"""
            else:
                user_message = example.instruction
            
            data.append({
                "messages": [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": example.output}
                ]
            })
        
        dataset = Dataset.from_list(data)
        print(f"  数据量: {len(dataset)}")
        
        return dataset
    
    def train(
        self,
        train_dataset: Dataset,
        eval_dataset: Dataset = None,
        num_epochs: int = 3
    ):
        """训练模型"""
        
        print("\n" + "="*60)
        print("开始指令微调训练")
        print("="*60)
        
        # 加载模型和tokenizer
        print("\n1. 加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 配置LoRA
        print("\n2. 配置LoRA...")
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
        
        # 训练参数
        print("\n3. 配置训练参数...")
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=4,
            learning_rate=2e-5,
            fp16=True,
            gradient_checkpointing=True,
            logging_steps=10,
            save_steps=100,
            evaluation_strategy="steps" if eval_dataset else "no",
            eval_steps=100 if eval_dataset else None,
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
        )
        
        # 开始训练
        print("\n4. 开始训练...")
        trainer.train()
        
        # 保存模型
        print("\n5. 保存模型...")
        trainer.save_model(f"{self.output_dir}/final")
        
        print("\n✅ 指令微调完成！")

# 使用示例
"""
# 准备数据
examples = InstructionDataset.create_diverse_examples()

# 创建微调器
tuner = InstructionTuner()

# 准备数据集
train_dataset = tuner.prepare_instruction_data(examples)

# 训练
tuner.train(train_dataset)
"""

print("指令微调器已就绪")
```

---

## 📝 课后练习

### 练习1：数据构造
构造100条指令数据

### 练习2：指令微调
使用指令数据微调模型

### 练习3：效果对比
对比指令微调前后效果

---

## 🎓 知识总结

### 核心要点

1. **指令微调本质**
   - 让模型学会理解指令
   - 提升泛化能力
   - 多任务适用

2. **数据构造**
   - 指令+输入+输出
   - 多样化覆盖
   - 质量优先

3. **Self-Instruct**
   - 种子指令
   - 自动生成
   - 低成本

4. **实战要点**
   - 格式规范
   - 多任务平衡
   - 充分评估

---

## 🚀 下节预告

下一课：**第104课：RLHF-基于人类反馈的强化学习**

- RLHF原理
- PPO算法
- 奖励模型
- 实战应用

**掌握ChatGPT核心技术！** 🔥

---

**💪 记住：指令微调是通用AI的基础！**

**下一课见！** 🎉
