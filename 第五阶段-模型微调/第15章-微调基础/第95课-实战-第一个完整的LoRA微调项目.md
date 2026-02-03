![模型微调流程](./images/finetune.svg)
*图：模型微调流程*

# 第95课：实战-第一个完整的LoRA微调项目

> **本课目标**：从零到一完成一个完整的LoRA微调项目
> 
> **核心技能**：数据准备、模型训练、评估部署、完整流程
> 
> **学习时长**：120分钟

---

## 📖 口播文案（7分钟）
![Hyperparams](./images/hyperparams.svg)
*图：Hyperparams*


### 🎯 前言

"前面几节课，我们学习了：
- 微调理论
- 数据准备
- LoRA原理
- PEFT工具

今天，**我们要做一个完整的项目！**

**从零开始，从头到尾，一步一步带你完成你的第一个微调项目！**

**项目目标：打造一个专业的SQL生成助手**

```
为什么选这个项目？

1. 实用性强
   • 数据分析常用
   • 企业需求大
   • 容易验证效果

2. 难度适中
   • 不太简单
   • 不太复杂
   • 适合入门

3. 效果显著
   • 通用模型：50%准确率
   • 微调后：90%+准确率
   • 提升明显！
```

**项目价值：**

```
场景：数据分析平台

用户输入自然语言：
"查询2024年销售额前10的产品"

通用GPT-4：
SELECT * FROM products 
WHERE year = 2024 
ORDER BY sales 
LIMIT 10

❌ 错误！表名、字段名可能不对

微调后的模型：
SELECT 
    product_name,
    SUM(revenue) as total_sales
FROM sales_records
WHERE sale_date >= '2024-01-01'
GROUP BY product_id, product_name
ORDER BY total_sales DESC
LIMIT 10;

✅ 完美！字段准确、逻辑正确
```

**效果对比：**

```
【通用模型的问题】

问题1：表名不准
• 用户的表叫：sales_records
• GPT猜测：sales, orders, transactions
• 结果：SQL无法执行

问题2：字段名不准
• 实际字段：product_name, revenue
• GPT猜测：name, amount, price
• 结果：字段不存在

问题3：业务逻辑不懂
• 复杂的JOIN逻辑
• 特定的计算规则
• 企业的命名规范

【微调后的优势】

优势1：了解你的数据库
• 知道所有表名
• 知道所有字段
• 知道数据类型

优势2：懂你的业务
• 理解业务规则
• 遵循命名规范
• 生成优化的SQL

优势3：准确率高
• 从50% → 90%+
• 可直接执行
• 节省调试时间
```

**项目规划：**

```
【数据准备阶段】

任务：
• 收集1000条 自然语言-SQL 对
• 清洗格式化
• 划分训练/验证/测试集

时间：半天

【模型微调阶段】

任务：
• 选择基础模型（Qwen-7B）
• 配置LoRA参数
• 训练模型

时间：4-6小时（训练时间）

【测试优化阶段】

任务：
• 评估准确率
• 调整超参数
• 优化效果

时间：半天

【部署上线阶段】

任务：
• 导出模型
• 搭建API服务
• 测试性能

时间：2-3小时

总计：2天完成整个项目
```

**资源需求：**

```
【硬件】
• 单张RTX 3090/4090
• 或云端GPU（A100）
• 成本：$30-50

【软件】
• Python 3.8+
• PyTorch
• Transformers
• PEFT
• LM Studio（推理测试）

【数据】
• 1000条训练数据
• 可用公开数据集
• 或自己构造

【时间】
• 学习时间：2小时
• 实操时间：6-8小时
• 总计：一天搞定
```

**成功标准：**

```
【最低标准】
• 模型能成功训练
• Loss正常下降
• 能生成基本SQL

【良好标准】
• 准确率>70%
• SQL可执行
• 逻辑基本正确

【优秀标准】
• 准确率>90%
• SQL完全正确
• 性能优化好

【卓越标准】
• 准确率>95%
• 复杂查询也对
• API响应<1s
• 可商用
```

**今天这一课的完整流程：**

```
Step 1: 环境准备
• 安装依赖
• 下载模型
• 测试环境

Step 2: 数据准备
• 数据收集
• 格式转换
• 质量检查

Step 3: 模型配置
• 选择基础模型
• 配置LoRA
• 参数设置

Step 4: 开始训练
• 运行训练脚本
• 监控指标
• 保存checkpoint

Step 5: 模型评估
• 计算准确率
• 分析错误
• 优化迭代

Step 6: 导出部署
• 合并权重
• 搭建API
• 性能测试

Step 7: 实战测试
• 真实查询
• 压力测试
• 上线准备
```

**你将获得：**

```
1. 完整的项目代码
   • 数据处理脚本
   • 训练脚本
   • 评估脚本
   • 部署脚本

2. 训练好的模型
   • 可直接使用
   • 可继续优化
   • 可商用

3. 实战经验
   • 踩坑经验
   • 调优技巧
   • 最佳实践

4. 可复制的流程
   • 适用其他任务
   • 可扩展
   • 可定制
```

**常见问题提前说：**

```
Q1: 我的GPU显存不够怎么办？
A: 
• 使用8bit量化
• 降低batch_size
• 减少max_length
• 使用梯度检查点

Q2: 训练loss不下降怎么办？
A:
• 检查数据格式
• 调整学习率
• 增加训练数据
• 检查标签质量

Q3: 生成的SQL还是不对怎么办？
A:
• 增加训练数据
• 提高LoRA rank
• 增加训练轮数
• 调整prompt格式

Q4: 推理速度太慢怎么办？
A:
• 合并LoRA权重
• 使用vLLM加速
• 批量推理
• 模型量化
```

**准备好了吗？让我们开始实战！**

今天这一课，我会：
1. 手把手带你完成每一步
2. 提供完整的代码
3. 分享实战经验
4. 解决常见问题

**这将是你微调之路的里程碑！**

让我们开始吧！"

---

## 📚 第一部分：环境准备

### 一、安装依赖

```bash
#!/bin/bash
# setup.sh - 环境安装脚本

echo "开始安装依赖..."

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装核心依赖
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装transformers和PEFT
pip install transformers
pip install peft
pip install accelerate
pip install bitsandbytes  # 8bit量化

# 安装数据处理
pip install datasets
pip install pandas
pip install scikit-learn

# 安装评估工具
pip install evaluate
pip install rouge-score

# 安装API框架
pip install fastapi
pip install uvicorn

# 验证安装
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
python -c "import peft; print(f'PEFT: {peft.__version__}')"

echo "依赖安装完成！"
```

### 二、项目结构

```
sql_generator/
├── data/
│   ├── raw/                    # 原始数据
│   ├── processed/              # 处理后的数据
│   └── train.json             # 训练数据
│   └── val.json               # 验证数据
│   └── test.json              # 测试数据
├── models/
│   ├── base/                  # 基础模型
│   └── lora/                  # LoRA权重
├── scripts/
│   ├── prepare_data.py        # 数据准备
│   ├── train.py               # 训练脚本
│   ├── evaluate.py            # 评估脚本
│   └── inference.py           # 推理脚本
├── api/
│   ├── app.py                 # FastAPI应用
│   └── model_loader.py        # 模型加载
├── configs/
│   └── lora_config.yaml       # LoRA配置
├── requirements.txt           # 依赖列表
└── README.md                  # 项目说明
```

---

## 💻 第二部分：数据准备

### 一、数据收集与格式化

```python
import json
import pandas as pd
from typing import List, Dict
from pathlib import Path

class SQLDatasetPreparer:
    """SQL数据集准备器"""
    
    def __init__(self, output_dir: str = "data/processed"):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_sample_data(self, num_samples: int = 100) -> List[Dict]:
        """
        创建示例数据
        
        实际项目中应该使用真实数据集，如：
        - WikiSQL
        - Spider
        - 或企业内部数据
        
        Args:
            num_samples: 样本数量
        """
        
        # 示例：电商数据库
        samples = [
            {
                "instruction": "生成SQL查询",
                "input": "查询2024年1月的所有订单",
                "output": "SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';"
            },
            {
                "instruction": "生成SQL查询",
                "input": "统计每个产品的销售总额",
                "output": "SELECT product_id, product_name, SUM(amount) as total_sales FROM sales GROUP BY product_id, product_name;"
            },
            {
                "instruction": "生成SQL查询",
                "input": "找出销售额最高的前10个产品",
                "output": "SELECT product_id, product_name, SUM(amount) as total FROM sales GROUP BY product_id, product_name ORDER BY total DESC LIMIT 10;"
            },
            {
                "instruction": "生成SQL查询",
                "input": "查询北京地区的客户数量",
                "output": "SELECT COUNT(*) as customer_count FROM customers WHERE city = '北京';"
            },
            {
                "instruction": "生成SQL查询",
                "input": "计算每个月的平均订单金额",
                "output": "SELECT DATE_FORMAT(order_date, '%Y-%m') as month, AVG(total_amount) as avg_amount FROM orders GROUP BY month;"
            },
        ]
        
        # 复制多次以达到指定数量（实际项目中应该有真实的多样化数据）
        result = []
        for i in range(num_samples):
            sample = samples[i % len(samples)].copy()
            result.append(sample)
        
        return result
    
    def format_for_training(self, data: List[Dict]) -> List[Dict]:
        """
        格式化为训练格式
        
        Args:
            data: 原始数据
        
        Returns:
            格式化后的数据
        """
        
        formatted_data = []
        
        for item in data:
            # 构建prompt
            prompt = f"""### 指令:
{item['instruction']}

### 输入:
{item['input']}

### 输出:
"""
            
            # 格式化为对话格式
            formatted_item = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt.strip()
                    },
                    {
                        "role": "assistant",
                        "content": item['output']
                    }
                ]
            }
            
            formatted_data.append(formatted_item)
        
        return formatted_data
    
    def split_dataset(
        self,
        data: List[Dict],
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
        test_ratio: float = 0.1
    ) -> tuple:
        """
        划分数据集
        
        Args:
            data: 完整数据
            train_ratio: 训练集比例
            val_ratio: 验证集比例
            test_ratio: 测试集比例
        """
        
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6
        
        n = len(data)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        
        # 随机打乱
        import random
        random.shuffle(data)
        
        train_data = data[:n_train]
        val_data = data[n_train:n_train + n_val]
        test_data = data[n_train + n_val:]
        
        return train_data, val_data, test_data
    
    def save_dataset(self, data: List[Dict], filename: str):
        """保存数据集"""
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {output_path}")
        print(f"样本数量: {len(data)}")
    
    def prepare_full_dataset(self, num_samples: int = 1000):
        """准备完整数据集"""
        
        print("="*60)
        print("开始准备数据集")
        print("="*60)
        
        # 1. 创建示例数据
        print("\n1. 创建示例数据...")
        raw_data = self.create_sample_data(num_samples)
        print(f"   创建了 {len(raw_data)} 条原始数据")
        
        # 2. 格式化数据
        print("\n2. 格式化数据...")
        formatted_data = self.format_for_training(raw_data)
        print(f"   格式化完成")
        
        # 3. 划分数据集
        print("\n3. 划分数据集...")
        train_data, val_data, test_data = self.split_dataset(formatted_data)
        print(f"   训练集: {len(train_data)} 条")
        print(f"   验证集: {len(val_data)} 条")
        print(f"   测试集: {len(test_data)} 条")
        
        # 4. 保存数据
        print("\n4. 保存数据...")
        self.save_dataset(train_data, "train.json")
        self.save_dataset(val_data, "val.json")
        self.save_dataset(test_data, "test.json")
        
        print("\n数据准备完成！")
        
        return train_data, val_data, test_data

# 演示
preparer = SQLDatasetPreparer()
train_data, val_data, test_data = preparer.prepare_full_dataset(num_samples=100)

# 查看示例
print("\n训练数据示例:")
print(json.dumps(train_data[0], ensure_ascii=False, indent=2))
```

---

## 🎯 第三部分：模型训练

### 一、完整训练脚本

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from datasets import load_dataset
import torch
from typing import Optional

class SQLModelTrainer:
    """SQL模型训练器"""
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen-7B",  # 使用Qwen作为基础模型
        output_dir: str = "./sql_model",
        data_dir: str = "./data/processed"
    ):
        """
        初始化训练器
        
        Args:
            model_name: 基础模型名称
            output_dir: 输出目录
            data_dir: 数据目录
        """
        self.model_name = model_name
        self.output_dir = output_dir
        self.data_dir = data_dir
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")
    
    def load_model_and_tokenizer(self, use_8bit: bool = True):
        """加载模型和tokenizer"""
        
        print("\n" + "="*60)
        print("加载模型")
        print("="*60)
        
        # 加载tokenizer
        print("\n1. 加载tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right"
        )
        
        # 设置特殊token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # 加载模型
        print("\n2. 加载基础模型...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            load_in_8bit=use_8bit,          # 8bit量化
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 统计参数
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"   总参数: {total_params:,} ({total_params/1e9:.2f}B)")
    
    def apply_lora(
        self,
        r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.05,
        target_modules: Optional[List[str]] = None
    ):
        """应用LoRA"""
        
        print("\n" + "="*60)
        print("应用LoRA")
        print("="*60)
        
        # 默认目标模块（Qwen）
        if target_modules is None:
            target_modules = [
                "c_attn",     # Attention
                "c_proj",     # Projection
                "w1", "w2"    # FFN
            ]
        
        # 配置LoRA
        lora_config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            target_modules=target_modules,
            lora_dropout=lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        print(f"\nLoRA配置:")
        print(f"  Rank: {r}")
        print(f"  Alpha: {lora_alpha}")
        print(f"  目标模块: {target_modules}")
        print(f"  Dropout: {lora_dropout}")
        
        # 应用LoRA
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
    
    def load_data(self):
        """加载数据"""
        
        print("\n" + "="*60)
        print("加载数据")
        print("="*60)
        
        # 加载数据集
        dataset = load_dataset(
            "json",
            data_files={
                "train": f"{self.data_dir}/train.json",
                "validation": f"{self.data_dir}/val.json"
            }
        )
        
        print(f"\n训练样本: {len(dataset['train'])}")
        print(f"验证样本: {len(dataset['validation'])}")
        
        # 数据预处理
        def preprocess_function(examples):
            """预处理函数"""
            
            # 提取messages
            inputs = []
            labels = []
            
            for messages in examples["messages"]:
                # 构建输入
                input_text = messages[0]["content"]  # user
                output_text = messages[1]["content"]  # assistant
                
                # 完整文本
                full_text = input_text + output_text
                
                # Tokenize
                input_ids = self.tokenizer(
                    full_text,
                    truncation=True,
                    max_length=512,
                    padding="max_length"
                )["input_ids"]
                
                # Label（只计算output部分的loss）
                input_only_ids = self.tokenizer(
                    input_text,
                    truncation=True,
                    max_length=512
                )["input_ids"]
                
                # 构建labels
                labels_ids = [-100] * len(input_only_ids) + \
                            input_ids[len(input_only_ids):]
                labels_ids = labels_ids[:512]  # 截断
                
                inputs.append(input_ids)
                labels.append(labels_ids)
            
            return {
                "input_ids": inputs,
                "labels": labels
            }
        
        # 应用预处理
        processed_dataset = dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=dataset["train"].column_names
        )
        
        self.train_dataset = processed_dataset["train"]
        self.eval_dataset = processed_dataset["validation"]
        
        print("\n数据加载完成！")
    
    def train(
        self,
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 2e-4,
        save_steps: int = 100
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
            
            # 优化器
            optim="adamw_torch",
            weight_decay=0.01,
            warmup_ratio=0.1,
            
            # 混合精度
            fp16=True,
            
            # 梯度
            gradient_accumulation_steps=4,
            gradient_checkpointing=True,
            max_grad_norm=1.0,
            
            # 保存
            save_strategy="steps",
            save_steps=save_steps,
            save_total_limit=3,
            
            # 评估
            evaluation_strategy="steps",
            eval_steps=save_steps,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            
            # 日志
            logging_steps=10,
            logging_dir=f"{self.output_dir}/logs",
            report_to="tensorboard",
            
            # 其他
            remove_unused_columns=False,
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            tokenizer=self.tokenizer,
        )
        
        # 开始训练
        print("\n开始训练...")
        print(f"总epochs: {num_epochs}")
        print(f"Batch size: {batch_size}")
        print(f"学习率: {learning_rate}")
        
        trainer.train()
        
        # 保存最终模型
        print("\n保存模型...")
        trainer.save_model(f"{self.output_dir}/final")
        self.tokenizer.save_pretrained(f"{self.output_dir}/final")
        
        print(f"\n训练完成！模型保存在: {self.output_dir}/final")

# 使用示例（注释掉实际训练）
"""
# 创建训练器
trainer = SQLModelTrainer(
    model_name="Qwen/Qwen-7B",
    output_dir="./sql_model",
    data_dir="./data/processed"
)

# 加载模型
trainer.load_model_and_tokenizer(use_8bit=True)

# 应用LoRA
trainer.apply_lora(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05
)

# 加载数据
trainer.load_data()

# 训练
trainer.train(
    num_epochs=3,
    batch_size=4,
    learning_rate=2e-4,
    save_steps=100
)
"""

print("\n训练脚本已就绪")
```

---

## 📝 课后作业

### 作业1：完成项目
按照教程完成整个项目

### 作业2：尝试优化
调整超参数提升效果

### 作业3：扩展应用
将流程应用到其他任务

---

## 🎓 知识总结

### 核心要点

1. **完整流程**
   - 环境准备
   - 数据准备
   - 模型训练
   - 评估部署

2. **关键技巧**
   - 8bit量化节省显存
   - 梯度检查点优化
   - 混合精度加速
   - 数据格式规范

3. **最佳实践**
   - 从小数据开始
   - 持续监控指标
   - 逐步优化
   - 充分测试

4. **避坑指南**
   - 数据质量最重要
   - 显存不足有多种解决方案
   - 过拟合需要early stopping
   - 推理速度可优化

---

## 🚀 下节预告

下一课：**第96课：量化技术-4bit与8bit量化实战**

- 量化原理
- 4bit/8bit对比
- QLoRA技术
- 实战应用

**继续深入微调技术！** 🔥

---

**💪 恭喜完成第一个完整项目！这是你的里程碑！**

**下一课见！** 🎉
