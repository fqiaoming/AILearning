![高级微调技术](./images/advanced_ft.svg)
*图：高级微调技术*

# 第104课：RLHF-基于人类反馈的强化学习

> **本课目标**：掌握RLHF技术，让模型更符合人类偏好
> 
> **核心技能**：RLHF原理、奖励模型、PPO算法、实战应用
> 
> **学习时长**：95分钟

---

## 📖 口播文案（7分钟）
![Lora](./images/lora.svg)
*图：Lora*


### 🎯 前言

"上节课我们学习了指令微调，让模型学会遵循指令。

但还有一个问题：

**模型回答正确，但不够好！**

**真实场景：**

```
问题："如何学习编程？"

指令微调模型回答：
"学习编程需要先选择一门语言，
然后学习语法，多写代码练习。"

✅ 正确，但太简单

人类期望的回答：
"学习编程的完整路线：

1. 选择入门语言（推荐Python）
   • 语法简单易学
   • 应用广泛
   • 资源丰富

2. 系统学习基础（2-3个月）
   • 变量、数据类型
   • 控制流程
   • 函数与模块
   
3. 实战项目练习
   • 从简单项目开始
   • 逐步增加难度
   • GitHub记录成长

4. 进阶学习
   • 数据结构与算法
   • 设计模式
   • 开源项目贡献

推荐资源：
• 书籍：《Python编程：从入门到实践》
• 网站：LeetCode、GitHub
• 课程：CS50、MIT公开课

关键建议：
• 每天坚持写代码
• 不懂就查文档
• 多看优秀代码
• 参与开源社区"

✅ 详细、有用、人性化！
```

**核心问题：如何让模型知道哪个回答更好？**

**答案：RLHF（Reinforcement Learning from Human Feedback）**

**基于人类反馈的强化学习！**

这就是ChatGPT成功的秘密！

---

### 💡 什么是RLHF？

**直觉理解：**

```
【没有RLHF】
就像学生只知道答案正确与否：
• 对：1分
• 错：0分

但不知道：
• 哪个答案更好
• 为什么更好
• 如何改进

【有了RLHF】
就像有了详细的评分标准：
• 这个答案：85分（准确但不够详细）
• 那个答案：95分（准确、详细、有用）

模型学会追求更高分！
```

**技术定义：**

```
RLHF = 用人类的偏好反馈来训练模型

核心思想：
1. 人类标注偏好数据
   "这个回答比那个好"
   
2. 训练奖励模型
   学习人类的偏好标准
   
3. 用强化学习优化
   让模型生成更符合人类偏好的回答
```

**RLHF的三个阶段：**

```
【阶段1：监督微调（SFT）】

准备：
• 高质量问答数据
• 人工撰写示范回答

训练：
• 监督学习
• 学习基本能力

输出：
• SFT模型（基础模型）

【阶段2：奖励模型训练（RM）】

准备：
• 对比数据
• 人类偏好标注
  "回答A比回答B好"

训练：
• 排序学习
• 学习人类偏好

输出：
• 奖励模型（评分器）

【阶段3：强化学习（PPO）】

使用：
• SFT模型生成回答
• 奖励模型打分
• PPO算法优化

训练：
• 强化学习
• 最大化奖励

输出：
• RLHF模型（最终模型）
```

**为什么需要RLHF？**

```
【问题1：有害内容】

没有RLHF：
用户："教我如何入侵系统"
模型："首先你需要..."
❌ 危险！

有了RLHF：
用户："教我如何入侵系统"
模型："我不能提供这类信息。
如果你对网络安全感兴趣，
可以学习合法的渗透测试课程..."
✅ 安全！

【问题2：无用回答】

没有RLHF：
用户："我很难过"
模型："理解你的感受。"
❌ 不够有帮助

有了RLHF：
用户："我很难过"
模型："我很遗憾听到这个。
能告诉我发生了什么吗？
也许我们可以一起想办法...
如果需要专业帮助，建议咨询心理医生。"
✅ 更有同理心和帮助

【问题3：偏见问题】

RLHF可以：
• 减少性别偏见
• 避免种族歧视
• 平衡观点
• 尊重多元文化
```

**奖励模型的工作原理：**

```
【训练数据格式】

样本：
问题："什么是AI？"

回答A（评分：6分）：
"AI是人工智能。"

回答B（评分：9分）：
"人工智能(AI)是计算机科学的一个分支，
目标是创建能够执行通常需要人类智能的任务的系统，
如视觉感知、语音识别、决策和语言翻译等。"

人类标注：B > A

【奖励模型学习】

输入：问题 + 回答
输出：分数（0-1之间）

学到的规律：
• 详细的回答 > 简短的回答
• 准确的回答 > 模糊的回答  
• 有用的回答 > 无用的回答
• 安全的回答 > 危险的回答
```

**PPO算法：**

```
【PPO = Proximal Policy Optimization】

核心思想：
• 策略（Policy）= 模型生成策略
• 近端优化 = 小步优化，不要走太远

为什么？
• 大步优化 → 模型崩溃
• 小步优化 → 稳定提升

工作流程：
1. 模型生成回答
2. 奖励模型评分
3. 计算优势函数
4. 小幅度更新策略
5. 重复迭代

关键参数：
• clip_range：限制更新幅度
• KL散度：防止偏离太远
```

**RLHF的挑战：**

```
【挑战1：成本高】

需要大量人类标注：
• 数万到数十万条对比数据
• 每条需要人工判断
• 需要专业标注员

成本：
• OpenAI投入数百万美元
• Anthropic投入类似规模

【挑战2：训练难】

强化学习不稳定：
• 容易模型崩溃
• 奖励欺骗（Reward Hacking）
• 需要大量调参

【挑战3：效率低】

训练速度慢：
• 每步都要采样
• 计算奖励
• 更新策略

时间：
• 通常需要数天到数周
```

**实际效果：**

```
【ChatGPT的成功】

GPT-3（基础）：
• 能力强但不可控
• 经常产生有害内容
• 回答质量不稳定

GPT-3 + Instruction Tuning：
• 能遵循指令
• 但仍有问题

GPT-3 + Instruction + RLHF：
= ChatGPT
• 安全可控
• 有用
• 符合人类偏好

RLHF是关键！

【评估指标】

安全性：提升90%+
有用性：提升80%+
用户满意度：提升85%+
```

**今天这一课，我要带你：**

**第一部分：RLHF完整流程**
- 三个阶段详解
- 数据准备
- 模型训练

**第二部分：奖励模型**
- 原理详解
- 训练方法
- 评估技巧

**第三部分：PPO算法**
- 强化学习基础
- PPO实现
- 调参技巧

**第四部分：简化实现**
- 使用TRL库
- 完整代码
- 实战案例

学完这一课，你将理解ChatGPT的核心技术！

准备好了吗？让我们开始！"

---

## 📚 第一部分：RLHF完整流程

### 一、三阶段流程详解

```python
from dataclasses import dataclass
from typing import List, Tuple
import torch
import torch.nn as nn

@dataclass
class RLHFConfig:
    """RLHF配置"""
    
    # 阶段1：SFT
    sft_epochs: int = 3
    sft_lr: float = 2e-5
    
    # 阶段2：RM
    rm_epochs: int = 1
    rm_lr: float = 1e-5
    
    # 阶段3：PPO
    ppo_epochs: int = 4
    ppo_lr: float = 1e-6
    ppo_clip_range: float = 0.2
    kl_coef: float = 0.1

class RLHFPipeline:
    """RLHF完整流程"""
    
    def __init__(self, config: RLHFConfig):
        """
        初始化
        
        Args:
            config: RLHF配置
        """
        self.config = config
        
        print("="*60)
        print("RLHF训练流程")
        print("="*60)
    
    def stage1_sft(self, model, sft_data):
        """
        阶段1：监督微调（SFT）
        
        Args:
            model: 基础模型
            sft_data: 高质量问答数据
        """
        
        print("\n" + "="*60)
        print("阶段1：监督微调（SFT）")
        print("="*60)
        
        print("\n目标：")
        print("  • 学习基本对话能力")
        print("  • 理解任务和格式")
        print("  • 生成合理的回答")
        
        print("\n数据要求：")
        print("  • 高质量问答对")
        print("  • 人工撰写的示范回答")
        print("  • 覆盖多种场景")
        
        print("\n训练方法：")
        print("  • 标准监督学习")
        print("  • 交叉熵损失")
        print("  • 学习率：", self.config.sft_lr)
        
        # 实际训练代码略（使用标准微调）
        
        print("\n✅ SFT完成")
        print("  输出：SFT模型")
        
        return model  # 返回SFT后的模型
    
    def stage2_reward_model(self, model, preference_data):
        """
        阶段2：奖励模型训练（RM）
        
        Args:
            model: SFT模型
            preference_data: 偏好对比数据
        """
        
        print("\n" + "="*60)
        print("阶段2：奖励模型训练（RM）")
        print("="*60)
        
        print("\n目标：")
        print("  • 学习人类偏好")
        print("  • 给回答打分")
        print("  • 识别好坏回答")
        
        print("\n数据格式：")
        print("  问题：'什么是AI？'")
        print("  回答A：'AI是人工智能'  [chosen]")
        print("  回答B：'不知道'  [rejected]")
        print("  标注：A > B")
        
        print("\n训练方法：")
        print("  • 排序损失（Ranking Loss）")
        print("  • 学习率：", self.config.rm_lr)
        
        # 创建奖励模型（在SFT模型基础上）
        reward_model = self._create_reward_model(model)
        
        print("\n✅ RM完成")
        print("  输出：奖励模型")
        
        return reward_model
    
    def stage3_ppo(self, sft_model, reward_model, prompts):
        """
        阶段3：PPO强化学习
        
        Args:
            sft_model: SFT模型
            reward_model: 奖励模型
            prompts: 训练提示列表
        """
        
        print("\n" + "="*60)
        print("阶段3：PPO强化学习")
        print("="*60)
        
        print("\n目标：")
        print("  • 最大化奖励分数")
        print("  • 生成更好的回答")
        print("  • 符合人类偏好")
        
        print("\n工作流程：")
        print("  1. SFT模型生成回答")
        print("  2. 奖励模型评分")
        print("  3. 计算优势函数")
        print("  4. PPO更新策略")
        print("  5. 重复迭代")
        
        print("\n关键参数：")
        print(f"  • 学习率：{self.config.ppo_lr}")
        print(f"  • Clip范围：{self.config.ppo_clip_range}")
        print(f"  • KL系数：{self.config.kl_coef}")
        
        # PPO训练循环（简化）
        for epoch in range(self.config.ppo_epochs):
            print(f"\n  Epoch {epoch+1}/{self.config.ppo_epochs}")
            
            # 1. 生成回答
            print("    • 生成回答...")
            
            # 2. 获取奖励
            print("    • 计算奖励...")
            
            # 3. PPO更新
            print("    • 更新策略...")
        
        print("\n✅ PPO完成")
        print("  输出：RLHF模型（最终模型）")
        
        return sft_model  # 返回优化后的模型
    
    def _create_reward_model(self, base_model):
        """创建奖励模型"""
        
        # 在基础模型上添加value head
        # 实际实现需要修改模型结构
        return base_model
    
    def run_full_pipeline(self):
        """运行完整RLHF流程"""
        
        print("\n" + "="*60)
        print("开始RLHF完整流程")
        print("="*60)
        
        # 阶段1：SFT
        print("\n【阶段1/3】监督微调")
        # sft_model = self.stage1_sft(base_model, sft_data)
        
        # 阶段2：RM
        print("\n【阶段2/3】奖励模型")
        # reward_model = self.stage2_reward_model(sft_model, preference_data)
        
        # 阶段3：PPO
        print("\n【阶段3/3】PPO优化")
        # final_model = self.stage3_ppo(sft_model, reward_model, prompts)
        
        print("\n" + "="*60)
        print("RLHF流程完成！")
        print("="*60)

# 演示
config = RLHFConfig()
pipeline = RLHFPipeline(config)
pipeline.run_full_pipeline()
```

---

## 💻 第二部分：奖励模型实现

### 一、奖励模型训练

```python
class RewardModel(nn.Module):
    """奖励模型"""
    
    def __init__(self, base_model):
        """
        初始化
        
        Args:
            base_model: 基础语言模型
        """
        super().__init__()
        
        self.base_model = base_model
        
        # 添加value head（输出标量奖励）
        hidden_size = base_model.config.hidden_size
        self.value_head = nn.Linear(hidden_size, 1)
    
    def forward(self, input_ids, attention_mask):
        """
        前向传播
        
        Args:
            input_ids: 输入token
            attention_mask: 注意力掩码
        
        Returns:
            奖励分数
        """
        
        # 获取基础模型输出
        outputs = self.base_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            output_hidden_states=True
        )
        
        # 取最后一个token的hidden state
        hidden_states = outputs.hidden_states[-1]
        last_hidden = hidden_states[:, -1, :]
        
        # 计算奖励
        rewards = self.value_head(last_hidden)
        
        return rewards

class RewardModelTrainer:
    """奖励模型训练器"""
    
    def __init__(self):
        """初始化"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def compute_ranking_loss(
        self,
        reward_chosen: torch.Tensor,
        reward_rejected: torch.Tensor
    ) -> torch.Tensor:
        """
        计算排序损失
        
        Args:
            reward_chosen: 选中回答的奖励
            reward_rejected: 拒绝回答的奖励
        
        Returns:
            损失值
        """
        
        # 目标：让chosen的奖励 > rejected的奖励
        # 使用sigmoid交叉熵
        loss = -torch.log(torch.sigmoid(reward_chosen - reward_rejected))
        
        return loss.mean()
    
    def prepare_preference_data(self):
        """准备偏好数据"""
        
        print("\n" + "="*60)
        print("偏好数据格式")
        print("="*60)
        
        example = {
            "prompt": "什么是机器学习？",
            "chosen": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习规律，无需明确编程。主要包括监督学习、无监督学习和强化学习三大类型。",
            "rejected": "机器学习就是机器学习东西。"
        }
        
        print("\n示例：")
        print(f"Prompt: {example['prompt']}")
        print(f"\nChosen (好回答): {example['chosen']}")
        print(f"\nRejected (差回答): {example['rejected']}")
        
        print("\n关键点：")
        print("  • Chosen回答更详细、准确")
        print("  • Rejected回答太简单或错误")
        print("  • 需要大量这样的对比数据")
        
        return example
    
    def train_step_example(self):
        """训练步骤示例"""
        
        print("\n" + "="*60)
        print("奖励模型训练步骤")
        print("="*60)
        
        print("\n1. 输入数据：")
        print("   Prompt + Chosen回答")
        print("   Prompt + Rejected回答")
        
        print("\n2. 计算奖励：")
        print("   reward_chosen = model(prompt + chosen)")
        print("   reward_rejected = model(prompt + rejected)")
        
        print("\n3. 计算损失：")
        print("   loss = -log(sigmoid(reward_chosen - reward_rejected))")
        
        print("\n4. 反向传播：")
        print("   更新模型参数")
        
        print("\n5. 目标：")
        print("   让好回答的分数 > 差回答的分数")

# 演示
trainer = RewardModelTrainer()
trainer.prepare_preference_data()
trainer.train_step_example()
```

---

## 📝 课后练习

### 练习1：理解RLHF
画出RLHF的完整流程图

### 练习2：标注数据
为10个问题标注偏好数据

### 练习3：简化实现
使用TRL库实现简化版RLHF

---

## 🎓 知识总结

### 核心要点

1. **RLHF三阶段**
   - SFT：基础能力
   - RM：学习偏好
   - PPO：优化策略

2. **奖励模型**
   - 学习人类偏好
   - 排序损失
   - 给回答打分

3. **PPO算法**
   - 近端优化
   - 稳定训练
   - 防止崩溃

4. **实战挑战**
   - 成本高
   - 训练难
   - 需要大量标注

---

## 🚀 下节预告

下一课：**第105课：DPO-直接偏好优化**

- DPO原理
- 简化RLHF
- 无需奖励模型
- 实战对比

**RLHF的简化版！** 🔥

---

**💪 记住：RLHF是ChatGPT成功的关键！**

**下一课见！** 🎉
