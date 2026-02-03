![模型量化优化](./images/quantization.svg)
*图：模型量化优化*

# 第96课：量化技术-4bit与8bit量化实战

> **本课目标**：掌握模型量化技术，大幅降低显存占用
> 
> **核心技能**：量化原理、4bit/8bit量化、QLoRA、实战应用
> 
> **学习时长**：90分钟

---

## 📖 口播文案（6分钟）
![Qlora](./images/qlora.svg)
*图：Qlora*


### 🎯 前言

"上节课我们完成了第一个微调项目。

但你可能遇到了一个大问题：**显存不够！**

**7B模型就要14GB显存，13B要26GB，70B要140GB！**

普通人根本玩不起！

但今天，我要告诉你一个**黑科技：量化！**

**量化 = 让大模型变小的魔法！**

**显存占用对比：**

```
【7B模型加载显存】

FP16（正常）：
• 模型大小：14GB
• 需要显卡：RTX 4090 (24GB)
• 价格：1万+

8bit量化：
• 模型大小：7GB  (-50%)
• 需要显卡：RTX 3090 (24GB)
• 价格：5千+

4bit量化：
• 模型大小：3.5GB  (-75%)
• 需要显卡：RTX 3060 (12GB)
• 价格：2千+

差距：4倍！
```

**更震撼的是：**

```
【70B模型对比】

FP16：
• 显存：140GB
• 设备：8×A100
• 成本：$50万+
• 普通人：❌ 完全玩不起

4bit量化：
• 显存：35GB
• 设备：2×RTX 3090
• 成本：1万+
• 普通人：✅ 勉强能玩

差距：50倍！
```

**什么是量化？**

**直觉理解：**
```
【图片类比】

原图（PNG，无损）：
• 大小：10MB
• 质量：完美

JPEG（有损压缩）：
• 大小：1MB  (-90%)
• 质量：几乎看不出差别

量化就是模型的"有损压缩"！
```

**技术理解：**
```
【数值精度降低】

FP32（单精度）：
• 32位表示一个数
• 范围：±3.4×10^38
• 精度：极高

FP16（半精度）：
• 16位表示一个数
• 范围：±65504
• 精度：够用

INT8（8位整数）：
• 8位表示一个数
• 范围：-128~127
• 精度：略低

INT4（4位整数）：
• 4位表示一个数
• 范围：-8~7
• 精度：较低

精度越低，占用越小！
```

**量化的3大优势：**

**优势1：显存暴降**
```
7B模型：

FP16: 14GB
INT8: 7GB   (-50%)
INT4: 3.5GB (-75%)

13B模型：

FP16: 26GB
INT8: 13GB  (-50%)
INT4: 6.5GB (-75%)

70B模型：

FP16: 140GB
INT8: 70GB  (-50%)
INT4: 35GB  (-75%)

降低2-4倍！
```

**优势2：速度提升**
```
量化后：

推理速度：提升1.5-2倍
计算效率：提升
功耗：降低

为什么？
• 更小的数据传输
• 更快的计算
• 更好的缓存利用
```

**优势3：成本暴降**
```
不量化：
• 需要高端GPU
• 云端费用高
• 部署成本高

量化后：
• 可用中端GPU
• 云端费用低
• 部署成本低

省钱！
```

**量化的代价：**

```
【精度损失】

理论上：
精度降低 → 性能下降

实际上：
8bit: 几乎无损（<1%差距）
4bit: 轻微损失（1-3%差距）

可接受！
```

**4bit vs 8bit对比：**

```
【8bit量化】

优点：
• 精度几乎无损
• 稳定可靠
• 兼容性好

缺点：
• 显存只省50%
• 提升有限

适合：
• 追求稳定
• 显存紧张
• 生产环境

【4bit量化】

优点：
• 显存省75%
• 更激进
• 能跑更大模型

缺点：
• 精度略有损失
• 需要特殊技巧

适合：
• 极度缺显存
• 追求极致
• 实验研究

推荐：先用8bit，不够再4bit
```

**QLoRA：量化+LoRA的完美组合！**

```
【普通LoRA】

7B模型微调：
• 基础模型：14GB (FP16)
• LoRA参数：0.1GB
• 梯度：0.1GB
• 优化器：0.2GB
总计：14.4GB

【QLoRA】

7B模型微调：
• 基础模型：3.5GB (4bit量化)
• LoRA参数：0.1GB
• 梯度：0.1GB
• 优化器：0.2GB
总计：3.9GB

差距：3.7倍！

QLoRA = 在量化模型上做LoRA微调
```

**QLoRA的黑科技：**

```
关键技术1：NF4量化
• Normal Float 4bit
• 专门为神经网络设计
• 保留更多信息

关键技术2：Double Quantization
• 量化常数也量化
• 进一步省显存

关键技术3：Paged Optimizers
• 使用分页内存
• 避免OOM
• 自动管理

结果：
4bit模型 + LoRA微调
效果接近16bit！
```

**量化的实战场景：**

```
场景1：个人开发者
• 设备：单张3090 (24GB)
• 需求：微调13B模型

方案：
• 4bit量化
• QLoRA微调
• 完美解决！

场景2：小团队
• 设备：双3090 (48GB)
• 需求：微调70B模型

方案：
• 4bit量化 (35GB)
• 分布式训练
• 可以跑！

场景3：推理部署
• 设备：CPU服务器
• 需求：低成本推理

方案：
• 4bit量化
• GGUF格式
• CPU也能跑！
```

**常见问题：**

**Q1: 量化会损失多少精度？**
```
实测结果：

8bit量化：
• 通用任务：<0.5%差距
• 几乎感知不到

4bit量化：
• 通用任务：1-2%差距
• 可接受范围

极端情况：
• 数学推理：可能损失更多
• 需要实测
```

**Q2: 量化后能继续微调吗？**
```
可以！

方法1：QLoRA
• 在量化模型上加LoRA
• 效果很好

方法2：量化感知训练
• 训练时就考虑量化
• 效果最好但复杂
```

**Q3: 不同量化方法怎么选？**
```
选择策略：

显存充足（24GB+）：
→ 不量化或8bit

显存一般（12-24GB）：
→ 8bit量化

显存紧张（<12GB）：
→ 4bit量化

推理部署：
→ 根据设备选择
```

**今天这一课，我要带你：**

**第一部分：量化原理**
- 数值表示
- 量化方法
- 精度分析

**第二部分：8bit量化实战**
- bitsandbytes库
- 加载量化模型
- 性能测试

**第三部分：4bit量化实战**
- NF4量化
- GPTQ/AWQ
- 效果对比

**第四部分：QLoRA微调**
- QLoRA原理
- 完整流程
- 最佳实践

**第五部分：量化模型导出**
- GGUF格式
- 部署方案
- 性能优化

学完这一课，显存不足不再是问题！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【量化 = 用更少做更多】

不是：
• 降低模型能力
• 牺牲效果

而是：
• 智能压缩
• 保留核心能力
• 大幅降低成本

【精度和成本的平衡】

不需要极致精度
可以接受小幅损失

换来的是：
• 普通人也能玩大模型
• 部署成本大幅降低
• 推理速度显著提升

值得！
```

---

## 📚 第一部分：量化原理

### 一、数值表示与精度

```python
import numpy as np
import struct

class QuantizationDemo:
    """量化演示"""
    
    @staticmethod
    def demonstrate_precision():
        """演示不同精度的数值表示"""
        
        print("="*60)
        print("数值精度对比")
        print("="*60)
        
        # 测试值
        test_value = 3.141592653589793
        
        # FP32
        fp32_value = np.float32(test_value)
        fp32_bytes = struct.pack('f', fp32_value)
        
        # FP16
        fp16_value = np.float16(test_value)
        fp16_bytes = struct.pack('e', fp16_value)
        
        # INT8 (量化到-128~127)
        int8_value = np.clip(int(test_value * 40), -128, 127)  # 缩放因子40
        
        # INT4 (量化到-8~7)
        int4_value = np.clip(int(test_value * 2), -8, 7)  # 缩放因子2
        
        print(f"\n原始值: {test_value}")
        print(f"\nFP32 (32位):")
        print(f"  值: {fp32_value}")
        print(f"  误差: {abs(fp32_value - test_value):.10f}")
        print(f"  大小: {len(fp32_bytes)} bytes")
        
        print(f"\nFP16 (16位):")
        print(f"  值: {fp16_value}")
        print(f"  误差: {abs(fp16_value - test_value):.10f}")
        print(f"  大小: {len(fp16_bytes)} bytes")
        
        print(f"\nINT8 (8位):")
        print(f"  量化值: {int8_value}")
        print(f"  还原值: {int8_value / 40}")
        print(f"  误差: {abs(int8_value/40 - test_value):.10f}")
        print(f"  大小: 1 byte")
        
        print(f"\nINT4 (4位):")
        print(f"  量化值: {int4_value}")
        print(f"  还原值: {int4_value / 2}")
        print(f"  误差: {abs(int4_value/2 - test_value):.10f}")
        print(f"  大小: 0.5 byte")
    
    @staticmethod
    def calculate_memory_savings():
        """计算显存节省"""
        
        print("\n" + "="*60)
        print("显存占用计算")
        print("="*60)
        
        # 模型大小（参数数量）
        model_sizes = {
            "7B": 7e9,
            "13B": 13e9,
            "70B": 70e9
        }
        
        # 不同精度的字节数
        bytes_per_param = {
            "FP32": 4,
            "FP16": 2,
            "INT8": 1,
            "INT4": 0.5
        }
        
        print(f"\n{'模型':<10} {'精度':<10} {'显存(GB)':<15} {'节省'}")
        print("-"*60)
        
        for model_name, num_params in model_sizes.items():
            fp16_size = num_params * bytes_per_param["FP16"] / 1e9
            
            for precision, bytes_pp in bytes_per_param.items():
                size_gb = num_params * bytes_pp / 1e9
                savings = (1 - size_gb / fp16_size) * 100 if precision != "FP16" else 0
                
                print(f"{model_name:<10} {precision:<10} {size_gb:>10.1f}  "
                      f"{f'{savings:.0f}%' if savings > 0 else '-':>10}")

# 演示
demo = QuantizationDemo()
demo.demonstrate_precision()
demo.calculate_memory_savings()
```

---

## 💻 第二部分：8bit量化实战

### 一、使用bitsandbytes进行8bit量化

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

class EightBitQuantization:
    """8bit量化实战"""
    
    def __init__(self, model_name: str = "gpt2"):
        """
        初始化
        
        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_8bit_model(self):
        """加载8bit量化模型"""
        
        print("="*60)
        print("8bit量化模型加载")
        print("="*60)
        
        # 配置8bit量化
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0,          # 量化阈值
            llm_int8_has_fp16_weight=False,  # 不保留FP16权重
        )
        
        print("\n1. 加载tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        print("\n2. 加载8bit量化模型...")
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 查看显存占用
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1e9
            print(f"\n显存占用: {memory_used:.2f} GB")
        
        return model, tokenizer
    
    def compare_with_fp16(self):
        """对比FP16和8bit"""
        
        print("\n" + "="*60)
        print("FP16 vs 8bit 对比")
        print("="*60)
        
        if not torch.cuda.is_available():
            print("需要GPU才能测试")
            return
        
        # 加载FP16模型
        print("\n【FP16模型】")
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        
        model_fp16 = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        fp16_memory = torch.cuda.max_memory_allocated() / 1e9
        print(f"显存占用: {fp16_memory:.2f} GB")
        
        del model_fp16
        torch.cuda.empty_cache()
        
        # 加载8bit模型
        print("\n【8bit模型】")
        torch.cuda.reset_peak_memory_stats()
        
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        model_8bit = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto"
        )
        
        int8_memory = torch.cuda.max_memory_allocated() / 1e9
        print(f"显存占用: {int8_memory:.2f} GB")
        
        # 对比
        print(f"\n【对比】")
        print(f"FP16: {fp16_memory:.2f} GB")
        print(f"8bit: {int8_memory:.2f} GB")
        print(f"节省: {fp16_memory - int8_memory:.2f} GB ({(1-int8_memory/fp16_memory)*100:.1f}%)")
        
        del model_8bit
        torch.cuda.empty_cache()

# 演示
demo = EightBitQuantization()

# 加载8bit模型
model, tokenizer = demo.load_8bit_model()

# 对比测试（需要GPU）
if torch.cuda.is_available():
    demo.compare_with_fp16()
```

---

## 🎯 第三部分：4bit量化实战

### 一、QLoRA微调

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

class QLoRATrainer:
    """QLoRA训练器（4bit量化 + LoRA）"""
    
    def __init__(self, model_name: str = "gpt2"):
        """
        初始化
        
        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_4bit_model(self):
        """加载4bit量化模型"""
        
        print("="*60)
        print("4bit量化模型加载（QLoRA）")
        print("="*60)
        
        # 配置4bit量化
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,                      # 4bit量化
            bnb_4bit_quant_type="nf4",              # NF4量化类型
            bnb_4bit_compute_dtype=torch.float16,   # 计算时用FP16
            bnb_4bit_use_double_quant=True,         # 双重量化
        )
        
        print("\n量化配置:")
        print("  • 4bit量化: NF4")
        print("  • 计算精度: FP16")
        print("  • 双重量化: 开启")
        
        # 加载模型
        print("\n加载4bit模型...")
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 加载tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # 查看显存
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1e9
            print(f"\n显存占用: {memory_used:.2f} GB")
        
        return model, tokenizer
    
    def prepare_for_training(self, model):
        """准备训练"""
        
        print("\n" + "="*60)
        print("准备QLoRA训练")
        print("="*60)
        
        # 准备模型
        print("\n1. 准备量化模型...")
        model = prepare_model_for_kbit_training(model)
        
        # 配置LoRA
        print("\n2. 配置LoRA...")
        lora_config = LoraConfig(
            r=16,                           # LoRA秩
            lora_alpha=32,                  # 缩放因子
            target_modules=["c_attn"],      # 目标模块
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # 应用LoRA
        print("\n3. 应用LoRA...")
        model = get_peft_model(model, lora_config)
        
        # 打印参数信息
        model.print_trainable_parameters()
        
        # 查看显存
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1e9
            print(f"\n总显存占用: {memory_used:.2f} GB")
        
        return model
    
    def compare_all_methods(self):
        """对比所有量化方法"""
        
        print("\n" + "="*60)
        print("量化方法全面对比")
        print("="*60)
        
        if not torch.cuda.is_available():
            print("需要GPU才能测试")
            return
        
        results = {}
        
        # FP16
        print("\n【测试FP16】")
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        results["FP16"] = torch.cuda.max_memory_allocated() / 1e9
        del model
        torch.cuda.empty_cache()
        
        # 8bit
        print("\n【测试8bit】")
        torch.cuda.reset_peak_memory_stats()
        
        config_8bit = BitsAndBytesConfig(load_in_8bit=True)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=config_8bit,
            device_map="auto"
        )
        results["8bit"] = torch.cuda.max_memory_allocated() / 1e9
        del model
        torch.cuda.empty_cache()
        
        # 4bit
        print("\n【测试4bit】")
        torch.cuda.reset_peak_memory_stats()
        
        config_4bit = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=config_4bit,
            device_map="auto"
        )
        results["4bit"] = torch.cuda.max_memory_allocated() / 1e9
        del model
        torch.cuda.empty_cache()
        
        # 打印结果
        print("\n" + "="*60)
        print("对比结果")
        print("="*60)
        
        print(f"\n{'方法':<10} {'显存(GB)':<15} {'相对FP16':<15} {'节省'}")
        print("-"*60)
        
        fp16_mem = results["FP16"]
        for method, memory in results.items():
            relative = memory / fp16_mem
            savings = (1 - relative) * 100
            print(f"{method:<10} {memory:>10.2f}  {relative:>12.2f}x  {savings:>10.1f}%")

# 演示
trainer = QLoRATrainer()

# 加载4bit模型
model, tokenizer = trainer.load_4bit_model()

# 准备训练
model = trainer.prepare_for_training(model)

# 全面对比（需要GPU）
if torch.cuda.is_available():
    trainer.compare_all_methods()
```

---

## 📝 课后练习

### 练习1：量化对比
对比不同量化方法的效果

### 练习2：QLoRA微调
使用QLoRA微调一个模型

### 练习3：精度测试
测试量化对精度的影响

---

## 🎓 知识总结

### 核心要点

1. **量化原理**
   - 降低数值精度
   - 减少显存占用
   - 轻微精度损失

2. **量化方法**
   - 8bit: 稳定，省50%
   - 4bit: 激进，省75%
   - QLoRA: 4bit+LoRA

3. **实战技巧**
   - NF4量化类型
   - 双重量化
   - FP16计算

4. **最佳实践**
   - 优先8bit
   - 不够用4bit
   - QLoRA微调

---

## 🚀 下节预告

下一课：**第97课：梯度检查点与混合精度训练**

- 梯度检查点原理
- 混合精度训练
- 显存优化技巧
- 速度提升方法

**继续优化训练！** 🔥

---

**💪 记住：量化让大模型触手可及！**

**下一课见！** 🎉
