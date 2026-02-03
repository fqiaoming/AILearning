![高级微调技术](./images/advanced_ft.svg)
*图：高级微调技术*

# 第102课：微调实战-Qwen模型中文微调案例

> **本课目标**：完整实战Qwen模型中文场景微调
> 
> **核心技能**：Qwen微调、中文优化、完整流程、生产部署
> 
> **学习时长**：100分钟

---

## 📖 口播文案（7分钟）
![Lora](./images/lora.svg)
*图：Lora*


### 🎯 前言

"上节课我们对比了LLaMA和Qwen。

今天，**我们要实战微调Qwen模型！**

**完整案例：中文客服助手**

**项目背景：**

```
某电商平台需要：
• 智能客服机器人
• 理解中文口语
• 处理售前售后
• 准确回答政策

需求：
• 准确率>90%
• 响应时间<2s
• 支持多轮对话
• 理解复杂问题

选择：Qwen2-7B
原因：
• 中文能力强
• 大小适中
• 效果优秀
```

**为什么选Qwen？**

```
【对比测试】

通用GPT-4：
• 中文理解：✅ 优秀
• 专业知识：❌ 不了解
• 成本：❌ 高($0.03/1K tokens)
• 数据安全：❌ 上传第三方

LLaMA 3 8B微调：
• 中文理解：⚠️  需大量数据
• 专业知识：✅ 可以学
• 成本：✅ 低
• 数据安全：✅ 本地

Qwen2-7B微调：
• 中文理解：✅ 天然优秀
• 专业知识：✅ 快速学习
• 成本：✅ 低
• 数据安全：✅ 本地

最优选择！
```

**项目目标：**

```
输入：
"我昨天买的手机什么时候能到？订单号12345"

通用Qwen输出：
"请您提供订单详情，我帮您查询物流信息"

微调后输出：
"您好！订单12345显示：
• 商品：iPhone 15 Pro
• 下单时间：2024-06-01 14:30
• 当前状态：已发货
• 预计送达：2024-06-03（明天）
• 物流公司：顺丰速运
• 快递单号：SF1234567890

有其他问题随时咨询😊"

专业！准确！贴心！
```

**完整流程：**

```
阶段1: 数据准备（2小时）
• 收集客服对话
• 清洗标注
• 格式转换

阶段2: 环境配置（30分钟）
• 安装依赖
• 下载模型
• 配置GPU

阶段3: 模型微调（4小时）
• LoRA配置
• 开始训练
• 监控过程

阶段4: 测试评估（1小时）
• 准确率测试
• 响应时间测试
• 边界case测试

阶段5: 部署上线（2小时）
• 模型导出
• API封装
• 压力测试

总计：约10小时
```

**数据准备：**

```
【数据格式】

标准对话格式：

{
  "messages": [
    {
      "role": "system",
      "content": "你是电商客服助手..."
    },
    {
      "role": "user", 
      "content": "我的订单什么时候到？"
    },
    {
      "role": "assistant",
      "content": "请提供您的订单号..."
    },
    {
      "role": "user",
      "content": "订单号12345"
    },
    {
      "role": "assistant",
      "content": "查询到您的订单..."
    }
  ]
}

支持多轮对话！

【数据规模】

最少：1000条
推荐：5000条
更多：10000+条

质量>数量！
```

**训练配置：**

```yaml
model:
  name: "Qwen/Qwen2-7B"
  load_in_4bit: true

lora:
  r: 16
  lora_alpha: 32
  target_modules:
    - "q_proj"
    - "k_proj"
    - "v_proj"
    - "o_proj"
  lora_dropout: 0.05

training:
  num_epochs: 3
  batch_size: 4
  learning_rate: 2e-5
  gradient_checkpointing: true
  fp16: true

硬件需求：
• 单张RTX 3090 (24GB)
• 或RTX 4090
• 或A100

训练时间：
• 5000条数据：4小时
• 10000条数据：8小时
```

**预期效果：**

```
【评估指标】

微调前（Qwen2-7B Base）：
• 专业准确率：60%
• 响应相关性：70%
• 语言流畅度：90%

微调后（Fine-tuned）：
• 专业准确率：95%  ⬆️ 35%
• 响应相关性：96%  ⬆️ 26%
• 语言流畅度：95%  ⬆️ 5%

显著提升！

【实际案例】

问题："退货要扣钱吗？"

微调前：
"一般情况下，退货可能需要扣除一定费用..."
（泛泛而谈）

微调后：
"根据我们的退货政策：
• 7天无理由退货：不扣费
• 商品完好：全额退款
• 运费：首单买家承担，商家原因商家承担
• 特殊商品（生鲜、定制）：不支持退货

请问您的商品是？"
（专业准确）
```

**部署方案：**

```
【方案1：FastAPI + vLLM】

优点：
• 性能好
• 并发高
• 成本低

适合：
• 中小规模
• 自有服务器

【方案2：LM Studio】

优点：
• 简单易用
• 开箱即用
• 支持多模型

适合：
• 快速原型
• 本地测试

【方案3：TensorRT-LLM】

优点：
• 速度最快
• 延迟最低

适合：
• 高并发
• 对延迟敏感

推荐：先用方案1，压力大再方案3
```

**成本分析：**

```
【训练成本】

硬件：
• 租用A100：$2/小时 × 4小时 = $8
• 或自有GPU：电费约$2

数据标注：
• 5000条 × $0.1/条 = $500
• （如果需要）

总计：$510（一次性）

【推理成本】

自部署（单卡3090）：
• 硬件：$1500（一次性）
• 电费：$50/月
• 维护：$100/月

API调用（如果用GPT-4）：
• 100万次/月
• 500 tokens/次
• $0.03/1K tokens
• = $15,000/月

节省：99%！
```

**今天这一课，我要带你：**

**第一部分：数据准备**
- 数据收集
- 格式转换
- 质量检查

**第二部分：环境配置**
- 依赖安装
- 模型下载
- 配置验证

**第三部分：模型训练**
- LoRA配置
- 训练监控
- 效果评估

**第四部分：测试优化**
- 准确率测试
- 速度优化
- 问题修复

**第五部分：部署上线**
- API封装
- 压力测试
- 生产部署

从零到一，完整实战！

准备好了吗？让我们开始！"

---

## 📚 第一部分：数据准备

### 一、客服对话数据构建

```python
import json
from typing import List, Dict
from pathlib import Path
import random

class CustomerServiceDataBuilder:
    """客服数据构建器"""
    
    def __init__(self):
        """初始化"""
        self.system_prompt = """你是一个专业的电商客服助手。

你的职责：
1. 友好、专业地回答客户问题
2. 提供准确的订单、物流、售后信息
3. 遵守公司政策和流程
4. 保护客户隐私

你应该：
• 使用礼貌、亲切的语言
• 提供具体、详细的信息
• 主动询问必要信息
• 快速解决问题

你不应该：
• 泄露客户信息
• 做出超出权限的承诺
• 使用不当语言
"""
    
    def create_sample_data(self) -> List[Dict]:
        """创建示例数据"""
        
        samples = []
        
        # 样本1：订单查询
        samples.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "我的订单什么时候能到？"},
                {"role": "assistant", "content": "您好！请提供您的订单号，我帮您查询物流信息。"},
                {"role": "user", "content": "订单号12345"},
                {"role": "assistant", "content": """查询到您的订单信息：
• 订单号：12345
• 商品：iPhone 15 Pro 256GB 黑色
• 下单时间：2024-06-01 14:30
• 当前状态：已发货
• 物流公司：顺丰速运
• 快递单号：SF1234567890
• 预计送达：明天（2024-06-03）

您可以在"我的订单"中实时查看物流详情。还有其他问题吗？😊"""}
            ]
        })
        
        # 样本2：退货咨询
        samples.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "我买的衣服不合适，能退吗？"},
                {"role": "assistant", "content": """当然可以！我们支持7天无理由退货。

退货条件：
• 商品未使用、吊牌完整
• 包装完好无损
• 不影响二次销售

退货流程：
1. 在"我的订单"中申请退货
2. 填写退货原因
3. 打印退货单
4. 寄回商品（建议使用顺丰）
5. 商品签收后2-3个工作日退款

退款金额：商品金额全额退，运费买家承担（除非是商品质量问题）

请问您要现在申请退货吗？我可以帮您操作。"""}
            ]
        })
        
        # 样本3：优惠券使用
        samples.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "我的优惠券为什么用不了？"},
                {"role": "assistant", "content": "您好！优惠券无法使用可能有以下原因，请您核实：\n\n1. 使用期限：优惠券是否已过期？\n2. 使用条件：是否满足最低消费金额？\n3. 商品限制：是否适用于当前商品？\n4. 账号限制：是否限制首次购买？\n\n请告诉我您的优惠券编号，我帮您详细查看。"},
                {"role": "user", "content": "券码：SAVE100"},
                {"role": "assistant", "content": """查询到您的优惠券信息：
• 券码：SAVE100
• 面额：100元
• 使用条件：满499元可用
• 适用商品：全场商品（除特价区）
• 有效期：2024-06-01 至 2024-06-30
• 状态：可使用

您当前的购物车金额是多少？是否已满足使用条件？如果还有问题，我可以协助您检查购物车配置。"""}
            ]
        })
        
        # 样本4：投诉处理
        samples.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "你们的快递太慢了！我要投诉！"},
                {"role": "assistant", "content": """非常抱歉给您带来不愉快的体验！我完全理解您的心情。

请提供您的订单号，我立即帮您：
1. 联系物流公司催单
2. 查询延迟原因
3. 为您申请补偿

如果超过承诺时间未送达，我们将：
• 全额退运费
• 赠送优惠券
• 优先处理后续订单

请给我们一次机会改善，订单号是多少？"""}
            ]
        })
        
        # 样本5：商品咨询
        samples.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "iPhone 15和15 Pro有什么区别？"},
                {"role": "assistant", "content": """iPhone 15 vs iPhone 15 Pro 主要区别：

【屏幕】
• 15：6.1英寸 OLED，60Hz
• 15 Pro：6.1英寸 OLED，120Hz（更流畅）

【处理器】
• 15：A16芯片
• 15 Pro：A17 Pro芯片（性能更强）

【摄像头】
• 15：双摄（48MP主摄+12MP超广角）
• 15 Pro：三摄（48MP主摄+12MP超广角+12MP长焦，支持3倍光学变焦）

【材质】
• 15：铝合金边框
• 15 Pro：钛合金边框（更轻、更耐用）

【价格】
• 15：5999元起
• 15 Pro：7999元起

如果您注重：
• 性价比 → 选iPhone 15
• 摄影、游戏 → 选iPhone 15 Pro

需要我帮您下单吗？"""}
            ]
        })
        
        return samples
    
    def save_dataset(
        self,
        samples: List[Dict],
        output_dir: str = "data/customer_service"
    ):
        """保存数据集"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 划分数据集
        random.shuffle(samples)
        n = len(samples)
        
        train_size = int(n * 0.8)
        val_size = int(n * 0.1)
        
        train_data = samples[:train_size]
        val_data = samples[train_size:train_size + val_size]
        test_data = samples[train_size + val_size:]
        
        # 保存
        with open(output_path / "train.json", 'w', encoding='utf-8') as f:
            json.dump(train_data, f, ensure_ascii=False, indent=2)
        
        with open(output_path / "val.json", 'w', encoding='utf-8') as f:
            json.dump(val_data, f, ensure_ascii=False, indent=2)
        
        with open(output_path / "test.json", 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {output_dir}")
        print(f"  训练集: {len(train_data)}条")
        print(f"  验证集: {len(val_data)}条")
        print(f"  测试集: {len(test_data)}条")

# 演示
builder = CustomerServiceDataBuilder()
samples = builder.create_sample_data()

print("="*60)
print("客服数据构建")
print("="*60)

print(f"\n创建了 {len(samples)} 条示例数据")
print("\n示例对话：")
print(json.dumps(samples[0], ensure_ascii=False, indent=2))

# 保存数据集
builder.save_dataset(samples * 200)  # 扩展到1000条
```

---

## 💻 第二部分：Qwen模型微调

### 一、完整训练脚本

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from datasets import load_dataset
import torch

class QwenFineTuner:
    """Qwen微调器"""
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2-7B",
        output_dir: str = "./qwen_customer_service"
    ):
        """
        初始化
        
        Args:
            model_name: 模型名称
            output_dir: 输出目录
        """
        self.model_name = model_name
        self.output_dir = output_dir
        
        print(f"="*60)
        print(f"Qwen模型微调")
        print(f"="*60)
        print(f"\n模型: {model_name}")
        print(f"输出: {output_dir}")
    
    def load_model_and_tokenizer(self):
        """加载模型和tokenizer"""
        
        print(f"\n{'='*60}")
        print("加载模型")
        print(f"{'='*60}")
        
        # 配置4bit量化
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        # 加载模型
        print("\n1. 加载Qwen模型...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 准备4bit训练
        self.model = prepare_model_for_kbit_training(self.model)
        
        # 加载tokenizer
        print("\n2. 加载tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        # Qwen的pad_token设置
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.model.config.eos_token_id
        
        print("\n✅ 模型和tokenizer加载完成")
    
    def setup_lora(self):
        """配置LoRA"""
        
        print(f"\n{'='*60}")
        print("配置LoRA")
        print(f"{'='*60}")
        
        # Qwen2的target_modules
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj"
            ],
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        print("\nLoRA配置:")
        print(f"  Rank: {lora_config.r}")
        print(f"  Alpha: {lora_config.lora_alpha}")
        print(f"  Target modules: {lora_config.target_modules}")
        
        # 应用LoRA
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
    
    def prepare_dataset(self, data_dir: str = "data/customer_service"):
        """准备数据集"""
        
        print(f"\n{'='*60}")
        print("准备数据集")
        print(f"{'='*60}")
        
        # 加载数据
        dataset = load_dataset(
            "json",
            data_files={
                "train": f"{data_dir}/train.json",
                "validation": f"{data_dir}/val.json"
            }
        )
        
        print(f"\n训练样本: {len(dataset['train'])}")
        print(f"验证样本: {len(dataset['validation'])}")
        
        # 数据预处理
        def preprocess_function(examples):
            """预处理函数"""
            
            model_inputs = {
                "input_ids": [],
                "attention_mask": [],
                "labels": []
            }
            
            for messages in examples["messages"]:
                # 构建对话文本
                text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=False
                )
                
                # Tokenize
                tokenized = self.tokenizer(
                    text,
                    truncation=True,
                    max_length=2048,
                    padding="max_length"
                )
                
                model_inputs["input_ids"].append(tokenized["input_ids"])
                model_inputs["attention_mask"].append(tokenized["attention_mask"])
                model_inputs["labels"].append(tokenized["input_ids"])
            
            return model_inputs
        
        # 应用预处理
        self.train_dataset = dataset["train"].map(
            preprocess_function,
            batched=True,
            remove_columns=dataset["train"].column_names
        )
        
        self.eval_dataset = dataset["validation"].map(
            preprocess_function,
            batched=True,
            remove_columns=dataset["validation"].column_names
        )
        
        print("\n✅ 数据准备完成")
    
    def train(
        self,
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 2e-5
    ):
        """训练模型"""
        
        print(f"\n{'='*60}")
        print("开始训练")
        print(f"{'='*60}")
        
        # 训练参数
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=learning_rate,
            
            # 优化
            fp16=True,
            gradient_checkpointing=True,
            gradient_accumulation_steps=4,
            max_grad_norm=1.0,
            
            # 优化器
            optim="paged_adamw_32bit",
            weight_decay=0.01,
            warmup_ratio=0.1,
            
            # 保存
            save_strategy="steps",
            save_steps=100,
            save_total_limit=3,
            
            # 评估
            evaluation_strategy="steps",
            eval_steps=100,
            load_best_model_at_end=True,
            
            # 日志
            logging_steps=10,
            logging_dir=f"{self.output_dir}/logs",
            report_to="tensorboard",
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
        print(f"\n开始训练...")
        print(f"  Epochs: {num_epochs}")
        print(f"  Batch size: {batch_size}")
        print(f"  Learning rate: {learning_rate}")
        
        trainer.train()
        
        # 保存最终模型
        print(f"\n保存最终模型...")
        trainer.save_model(f"{self.output_dir}/final_model")
        
        print(f"\n✅ 训练完成！")
        print(f"模型保存在: {self.output_dir}/final_model")
    
    def run(self, data_dir: str = "data/customer_service"):
        """运行完整流程"""
        
        self.load_model_and_tokenizer()
        self.setup_lora()
        self.prepare_dataset(data_dir)
        self.train()

# 使用示例
"""
# 创建微调器
finetuner = QwenFineTuner(
    model_name="Qwen/Qwen2-7B",
    output_dir="./qwen_customer_service"
)

# 运行微调
finetuner.run(data_dir="data/customer_service")
"""

print("Qwen微调器已就绪")
```

---

## 📝 课后作业

### 作业1：完整实战
完成Qwen模型微调全流程

### 作业2：效果测试
测试微调前后的效果对比

### 作业3：部署上线
将模型部署为API服务

---

## 🎓 知识总结

### 核心要点

1. **Qwen优势**
   - 中文能力强
   - 训练数据少
   - 效果优秀

2. **微调配置**
   - 4bit量化
   - LoRA rank=16
   - 多target modules

3. **数据准备**
   - 对话格式
   - 多轮支持
   - 质量优先

4. **实战经验**
   - 从小开始
   - 持续优化
   - 充分测试

---

## 🚀 下节预告

下一课：**第103课：指令微调（Instruction Tuning）**

- 指令微调原理
- 数据构造
- 效果提升
- 最佳实践

**掌握高级微调技术！** 🔥

---

**💪 恭喜完成Qwen实战！你已掌握中文模型微调！**

**下一课见！** 🎉
