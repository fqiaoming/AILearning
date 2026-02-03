![模型微调流程](./images/finetune.svg)
*图：模型微调流程*

# 第93课：LoRA原理与实现详解

> **本课目标**：深入理解LoRA的数学原理和实现方法
> 
> **核心技能**：低秩分解、参数高效微调、LoRA实现、超参数调优
> 
> **学习时长**：95分钟

---

## 📖 口播文案（6分钟）
![Hyperparams](./images/hyperparams.svg)
*图：Hyperparams*


### 🎯 前言

"前两节课我们学习了微调理论和数据准备。

今天要学习微调领域最重要的技术：**LoRA！**

**LoRA = Low-Rank Adaptation**
**低秩适应 = 参数高效微调的革命！**

**为什么LoRA这么重要？**

**看一个对比：**

**全量微调：**
```
7B模型参数：7,000,000,000个
需要更新：7,000,000,000个 ❌
显存需求：80GB+
训练时间：24小时
成本：$500+

普通人：完全做不起！
```

**LoRA微调：**
```
7B模型参数：7,000,000,000个
需要更新：7,000,000个（0.1%！）✅
显存需求：12GB
训练时间：4小时
成本：$50

普通人：完全可以！
```

**差距：**
- 参数：减少99.9%
- 显存：减少85%
- 时间：减少83%
- 成本：减少90%

**这就是LoRA的威力！**

**LoRA的核心思想：**

**直觉理解：**
```
假设你要学习一门新技能：

方法1：全量学习
• 重新学习所有知识
• 花费大量时间

方法2：增量学习（LoRA）
• 保留已有知识
• 只学新的部分
• 效率高！

LoRA就是增量学习！
```

**技术理解：**
```
模型权重矩阵：W (大矩阵)

全量微调：
W_new = W + ΔW
需要训练：整个ΔW

LoRA：
ΔW ≈ A × B (低秩分解)
A是小矩阵 (d × r)
B是小矩阵 (r × d)
r << d (秩很小)

需要训练：A和B（小很多！）
```

**举个具体例子：**
```
假设权重矩阵W：
大小：4096 × 4096
参数量：16,777,216个

全量微调：
需要更新：16,777,216个参数

LoRA（r=8）：
矩阵A：4096 × 8 = 32,768个
矩阵B：8 × 4096 = 32,768个
总计：65,536个参数

减少：99.6%！
```

**LoRA的4大优势：**

**优势1：显存需求低**
```
全量微调7B模型：
• 模型：14GB
• 梯度：14GB
• 优化器状态：28GB
• 激活值：24GB
总计：80GB

LoRA微调7B模型：
• 模型：14GB（冻结）
• LoRA参数：0.5GB
• 梯度：0.5GB
• 优化器状态：1GB
总计：16GB

一张3090就够！
```

**优势2：训练速度快**
```
全量微调：
• 反向传播：整个模型
• 参数更新：所有参数
• 时间：24小时

LoRA微调：
• 反向传播：只LoRA层
• 参数更新：极少参数
• 时间：4小时

快6倍！
```

**优势3：切换方便**
```
训练多个LoRA：
• 医疗LoRA：10MB
• 法律LoRA：10MB
• 金融LoRA：10MB

使用时：
Base Model + 医疗LoRA = 医疗模型
Base Model + 法律LoRA = 法律模型

一个基座，多个专家！
```

**优势4：效果接近全量**
```
多项研究表明：

在很多任务上：
LoRA效果 ≈ 全量微调效果

差距：通常<2%

但资源需求：降低90%+

性价比极高！
```

**LoRA的数学原理：**

```
【低秩分解】

原理：
一个大矩阵可以分解为两个小矩阵的乘积

数学表达：
W ∈ R^(d×k)
≈ A × B
其中：
A ∈ R^(d×r)
B ∈ R^(r×k)
r << min(d, k)

为什么有效？
因为神经网络的权重更新
实际上是低秩的！

【前向传播】

原始：
h = W·x

LoRA：
h = W·x + (A·B)·x
    ↑     ↑
  冻结   可训练

【反向传播】

只计算A和B的梯度
W保持不变

参数量：
W: d×k (冻结)
A: d×r (训练)
B: r×k (训练)

训练参数：r(d+k) << d×k
```

**LoRA的关键超参数：**

**参数1：秩（rank, r）**
```
r = 1-4：
• 参数最少
• 适合简单任务

r = 8-16：
• 推荐值
• 平衡性能和成本

r = 32-64：
• 参数较多
• 适合复杂任务

一般建议：从8开始
```

**参数2：Alpha（缩放因子）**
```
作用：控制LoRA的影响力

h = W·x + (alpha/r)·(A·B)·x

alpha = r：标准设置
alpha = 2r：增强影响
alpha = r/2：减弱影响

一般建议：alpha = r
```

**参数3：目标模块**
```
可以对以下模块应用LoRA：
• Query矩阵（推荐）
• Value矩阵（推荐）
• Key矩阵
• Output矩阵

一般建议：
Query + Value即可
```

**LoRA vs 其他方法：**

```
【LoRA vs 全量微调】
参数：0.1% vs 100%
显存：20% vs 100%
速度：快6倍
效果：相近

【LoRA vs Adapter】
参数：更少
速度：更快（无额外层）
效果：更好

【LoRA vs Prefix Tuning】
参数：相近
速度：更快
效果：更好

LoRA：综合最优！
```

**今天这一课，我要带你：**

**第一部分：数学原理深入**
- 低秩分解
- 矩阵运算
- 梯度计算

**第二部分：实现细节**
- LoRA层实现
- 前向后向传播
- 参数初始化

**第三部分：代码实战**
- PyTorch实现
- HuggingFace集成
- 完整示例

**第四部分：超参数调优**
- Rank选择
- Alpha设置
- 模块选择

**第五部分：最佳实践**
- 使用建议
- 常见问题
- 性能优化

学完这一课，你将完全掌握LoRA！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【LoRA = 站在巨人肩膀上的艺术】

不改变巨人（Base Model）
只添加小的调整（LoRA）

结果：
• 保留通用能力
• 获得专业能力
• 成本极低

【低秩 = 信息压缩的智慧】

大多数信息
可以用更少的参数表示

就像：
• JPEG压缩图片
• MP3压缩音频
• LoRA压缩参数更新
```

---

## 📚 第一部分：LoRA数学原理

### 一、低秩分解详解

```python
import numpy as np
import matplotlib.pyplot as plt

class LowRankDecomposition:
    """低秩分解演示"""
    
    @staticmethod
    def demonstrate_low_rank():
        """演示低秩分解"""
        
        print("="*60)
        print("低秩分解原理演示")
        print("="*60)
        
        # 创建一个大矩阵
        d, k = 1000, 1000
        print(f"\n原始矩阵大小: {d} × {k}")
        print(f"参数量: {d * k:,} = {d*k/1e6:.1f}M")
        
        # 低秩分解
        r = 8  # 秩
        A = np.random.randn(d, r)
        B = np.random.randn(r, k)
        
        print(f"\n低秩分解 (rank={r}):")
        print(f"  矩阵A: {d} × {r}")
        print(f"  矩阵B: {r} × {k}")
        print(f"  参数量: {d*r + r*k:,} = {(d*r + r*k)/1e6:.3f}M")
        
        # 计算压缩比
        original_params = d * k
        lora_params = d * r + r * k
        compression_ratio = original_params / lora_params
        
        print(f"\n压缩比: {compression_ratio:.1f}x")
        print(f"参数减少: {(1 - lora_params/original_params)*100:.2f}%")
        
        # 不同rank的对比
        print(f"\n不同rank的参数量对比:")
        print(f"{'Rank':<10} {'参数量':<15} {'压缩比':<10} {'参数减少'}")
        print("-"*60)
        
        for r in [1, 2, 4, 8, 16, 32, 64]:
            params = d * r + r * k
            ratio = original_params / params
            reduction = (1 - params/original_params) * 100
            print(f"{r:<10} {params:>12,}  {ratio:>8.1f}x  {reduction:>8.2f}%")
    
    @staticmethod
    def visualize_rank_effect():
        """可视化rank的影响"""
        
        # 创建一个低秩矩阵
        d = 100
        true_rank = 5
        
        # 真实的低秩矩阵
        A_true = np.random.randn(d, true_rank)
        B_true = np.random.randn(true_rank, d)
        W_true = A_true @ B_true
        
        # 用不同的rank重建
        ranks = [1, 2, 5, 10, 20, 50]
        errors = []
        
        for r in ranks:
            # SVD分解
            U, s, Vt = np.linalg.svd(W_true, full_matrices=False)
            
            # 保留前r个奇异值
            W_approx = U[:, :r] @ np.diag(s[:r]) @ Vt[:r, :]
            
            # 计算误差
            error = np.linalg.norm(W_true - W_approx, 'fro')
            errors.append(error)
        
        print(f"\n不同rank的重建误差:")
        for r, e in zip(ranks, errors):
            print(f"  rank={r:2d}: 误差={e:.2f}")

# 演示
demo = LowRankDecomposition()
demo.demonstrate_low_rank()
demo.visualize_rank_effect()
```

### 二、LoRA前向和反向传播

```python
import torch
import torch.nn as nn

class LoRALayer(nn.Module):
    """LoRA层实现"""
    
    def __init__(
        self,
        in_features: int,
        out_features: int,
        rank: int = 8,
        alpha: float = 16.0,
        dropout: float = 0.0
    ):
        """
        初始化LoRA层
        
        Args:
            in_features: 输入维度
            out_features: 输出维度
            rank: LoRA秩
            alpha: 缩放因子
            dropout: Dropout率
        """
        super().__init__()
        
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        
        # LoRA矩阵
        # A: (in_features, rank)
        # B: (rank, out_features)
        self.lora_A = nn.Parameter(torch.zeros(in_features, rank))
        self.lora_B = nn.Parameter(torch.zeros(rank, out_features))
        
        # Dropout
        self.dropout = nn.Dropout(p=dropout) if dropout > 0 else nn.Identity()
        
        # 缩放因子
        self.scaling = alpha / rank
        
        # 初始化
        self.reset_parameters()
    
    def reset_parameters(self):
        """初始化参数"""
        # A使用Kaiming初始化
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        # B初始化为0（重要！）
        nn.init.zeros_(self.lora_B)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播
        
        LoRA输出 = x @ (A @ B) * scaling
        """
        
        # x: (batch, seq_len, in_features)
        # A: (in_features, rank)
        # B: (rank, out_features)
        
        # 计算 x @ A
        x_A = x @ self.lora_A  # (batch, seq_len, rank)
        
        # 应用dropout
        x_A = self.dropout(x_A)
        
        # 计算 (x @ A) @ B
        output = x_A @ self.lora_B  # (batch, seq_len, out_features)
        
        # 应用缩放
        output = output * self.scaling
        
        return output
    
    def extra_repr(self) -> str:
        """额外的表示信息"""
        return f'in_features={self.in_features}, out_features={self.out_features}, ' \
               f'rank={self.rank}, alpha={self.alpha}'

class LinearWithLoRA(nn.Module):
    """带LoRA的线性层"""
    
    def __init__(
        self,
        linear: nn.Linear,
        rank: int = 8,
        alpha: float = 16.0,
        dropout: float = 0.0
    ):
        """
        为现有的线性层添加LoRA
        
        Args:
            linear: 原始线性层（将被冻结）
            rank: LoRA秩
            alpha: 缩放因子
            dropout: Dropout率
        """
        super().__init__()
        
        # 冻结原始权重
        self.linear = linear
        for param in self.linear.parameters():
            param.requires_grad = False
        
        # 添加LoRA
        self.lora = LoRALayer(
            linear.in_features,
            linear.out_features,
            rank=rank,
            alpha=alpha,
            dropout=dropout
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播
        
        output = linear(x) + lora(x)
        """
        # 原始线性层（冻结）
        base_output = self.linear(x)
        
        # LoRA增量
        lora_output = self.lora(x)
        
        # 组合
        return base_output + lora_output

# 演示
def demo_lora_layer():
    """演示LoRA层"""
    
    print("\n" + "="*60)
    print("LoRA层演示")
    print("="*60)
    
    # 创建原始线性层
    in_features = 768
    out_features = 768
    linear = nn.Linear(in_features, out_features)
    
    print(f"\n原始线性层:")
    print(f"  参数量: {sum(p.numel() for p in linear.parameters()):,}")
    
    # 添加LoRA
    rank = 8
    linear_with_lora = LinearWithLoRA(linear, rank=rank)
    
    lora_params = sum(p.numel() for p in linear_with_lora.lora.parameters())
    total_trainable = sum(p.numel() for p in linear_with_lora.parameters() if p.requires_grad)
    
    print(f"\n添加LoRA (rank={rank}):")
    print(f"  LoRA参数: {lora_params:,}")
    print(f"  可训练参数: {total_trainable:,}")
    print(f"  参数比例: {total_trainable / (in_features * out_features) * 100:.2f}%")
    
    # 测试前向传播
    batch_size = 4
    seq_len = 128
    x = torch.randn(batch_size, seq_len, in_features)
    
    with torch.no_grad():
        output = linear_with_lora(x)
    
    print(f"\n前向传播:")
    print(f"  输入shape: {x.shape}")
    print(f"  输出shape: {output.shape}")

demo_lora_layer()
```

---

## 💻 第二部分：完整LoRA实现

### 一、应用LoRA到Transformer

```python
import math

def apply_lora_to_model(
    model: nn.Module,
    target_modules: List[str] = ["q_proj", "v_proj"],
    rank: int = 8,
    alpha: float = 16.0,
    dropout: float = 0.0
):
    """
    为模型的指定模块应用LoRA
    
    Args:
        model: 目标模型
        target_modules: 要应用LoRA的模块名称
        rank: LoRA秩
        alpha: 缩放因子
        dropout: Dropout率
    """
    
    lora_config = {
        'rank': rank,
        'alpha': alpha,
        'dropout': dropout,
        'target_modules': target_modules
    }
    
    # 记录应用的LoRA层
    lora_layers = []
    
    # 遍历模型的所有模块
    for name, module in model.named_modules():
        # 检查是否是目标模块
        if any(target in name for target in target_modules):
            if isinstance(module, nn.Linear):
                # 获取父模块和子模块名
                parent_name, child_name = name.rsplit('.', 1)
                parent = model.get_submodule(parent_name)
                
                # 替换为带LoRA的线性层
                lora_layer = LinearWithLoRA(
                    module,
                    rank=rank,
                    alpha=alpha,
                    dropout=dropout
                )
                
                setattr(parent, child_name, lora_layer)
                lora_layers.append(name)
    
    print(f"\n应用LoRA到 {len(lora_layers)} 个模块:")
    for layer in lora_layers:
        print(f"  • {layer}")
    
    # 统计参数
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"\n参数统计:")
    print(f"  总参数: {total_params:,}")
    print(f"  可训练: {trainable_params:,}")
    print(f"  比例: {trainable_params/total_params*100:.2f}%")
    
    return lora_config

# LoRA合并
def merge_lora_weights(model: nn.Module):
    """
    将LoRA权重合并到基础模型中
    
    用于推理时的优化
    """
    
    for module in model.modules():
        if isinstance(module, LinearWithLoRA):
            # 计算合并后的权重
            # W_new = W + scaling * (A @ B)
            lora_weight = (
                module.lora.lora_A @ module.lora.lora_B
            ) * module.lora.scaling
            
            # 合并到原始权重
            module.linear.weight.data += lora_weight.T
            
    print("LoRA权重已合并到基础模型")

# LoRA保存和加载
def save_lora_weights(model: nn.Module, path: str):
    """保存LoRA权重"""
    
    lora_state_dict = {}
    
    for name, module in model.named_modules():
        if isinstance(module, LinearWithLoRA):
            lora_state_dict[f"{name}.lora_A"] = module.lora.lora_A
            lora_state_dict[f"{name}.lora_B"] = module.lora.lora_B
    
    torch.save(lora_state_dict, path)
    print(f"LoRA权重已保存到: {path}")

def load_lora_weights(model: nn.Module, path: str):
    """加载LoRA权重"""
    
    lora_state_dict = torch.load(path)
    
    for name, param in lora_state_dict.items():
        # 设置到对应的模块
        module_name, param_name = name.rsplit('.', 1)
        module = model.get_submodule(module_name)
        
        if param_name == "lora_A":
            module.lora_A.data = param
        elif param_name == "lora_B":
            module.lora_B.data = param
    
    print(f"LoRA权重已加载from: {path}")
```

---

## 🎯 第三部分：超参数调优指南

### 一、Rank选择策略

```python
class LoRAHyperparameterGuide:
    """LoRA超参数选择指南"""
    
    @staticmethod
    def recommend_rank(
        task_complexity: str,
        data_size: int,
        model_size: str
    ) -> Dict:
        """
        推荐rank值
        
        Args:
            task_complexity: 任务复杂度 ("simple", "medium", "complex")
            data_size: 数据量
            model_size: 模型大小 ("7B", "13B", "70B")
        """
        
        recommendations = {
            "simple": {
                "7B": {"rank": 4, "alpha": 8},
                "13B": {"rank": 4, "alpha": 8},
                "70B": {"rank": 8, "alpha": 16}
            },
            "medium": {
                "7B": {"rank": 8, "alpha": 16},
                "13B": {"rank": 8, "alpha": 16},
                "70B": {"rank": 16, "alpha": 32}
            },
            "complex": {
                "7B": {"rank": 16, "alpha": 32},
                "13B": {"rank": 16, "alpha": 32},
                "70B": {"rank": 32, "alpha": 64}
            }
        }
        
        base_config = recommendations[task_complexity][model_size]
        
        # 根据数据量调整
        if data_size < 1000:
            # 数据少，降低rank避免过拟合
            base_config["rank"] = max(4, base_config["rank"] // 2)
        elif data_size > 10000:
            # 数据多，可以增加rank
            base_config["rank"] = min(64, base_config["rank"] * 2)
        
        return {
            "rank": base_config["rank"],
            "alpha": base_config["alpha"],
            "reasoning": f"任务复杂度: {task_complexity}, "
                        f"模型大小: {model_size}, "
                        f"数据量: {data_size}"
        }
    
    @staticmethod
    def print_recommendations():
        """打印推荐配置表"""
        
        print("\n" + "="*80)
        print("LoRA超参数推荐表")
        print("="*80)
        
        print(f"\n{'任务复杂度':<15} {'模型':<10} {'Rank':<10} {'Alpha':<10} {'说明'}")
        print("-"*80)
        
        tasks = [
            ("simple", "简单任务", "分类、简单QA"),
            ("medium", "中等任务", "对话、摘要"),
            ("complex", "复杂任务", "代码生成、推理")
        ]
        
        for task_key, task_name, desc in tasks:
            for model in ["7B", "13B", "70B"]:
                config = LoRAHyperparameterGuide.recommend_rank(
                    task_key, 5000, model
                )
                print(f"{task_name:<15} {model:<10} {config['rank']:<10} "
                      f"{config['alpha']:<10} {desc if model=='7B' else ''}")

# 演示
guide = LoRAHyperparameterGuide()
guide.print_recommendations()

# 具体推荐
print("\n示例：为你的任务推荐配置")
config = guide.recommend_rank(
    task_complexity="medium",
    data_size=3000,
    model_size="7B"
)
print(f"\n推荐配置:")
print(f"  Rank: {config['rank']}")
print(f"  Alpha: {config['alpha']}")
print(f"  原因: {config['reasoning']}")
```

---

## 📝 课后练习

### 练习1：实现LoRA层
从零实现一个LoRA层

### 练习2：参数对比
对比不同rank的效果

### 练习3：应用LoRA
为一个小模型应用LoRA

---

## 🎓 知识总结

### 核心要点

1. **LoRA原理**
   - 低秩分解
   - 参数高效
   - 效果接近全量

2. **实现细节**
   - A、B矩阵
   - 缩放因子
   - 初始化策略

3. **超参数**
   - Rank：4-32
   - Alpha：通常=2×rank
   - 目标模块：q_proj, v_proj

4. **最佳实践**
   - 从rank=8开始
   - 根据任务调整
   - 注意过拟合

---

## 🚀 下节预告

下一课：**第94课：使用HuggingFace PEFT库实战**

- PEFT库介绍
- LoRA配置
- 训练流程
- 完整示例

**开始实战微调！** 🔥

---

**💪 记住：LoRA是微调的最佳选择！**

**下一课见！** 🎉
