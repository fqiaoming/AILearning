![工作流程](./images/workflow.svg)
*图：Few-shot和CoT让AI学会"看例子"和"分步思考"*

# 第12课：Few-shot Learning与Chain-of-Thought技巧

> 📚 **课程信息**
> - 所属模块：第一模块 - AI基础与环境搭建  
> - 章节：第3章 - 提示词工程精通（第5/8课）
> - 学习目标：掌握Few-shot和CoT两大高级技巧，显著提升输出准确率
> - 预计时间：70-80分钟
> - 前置知识：第08-11课

---

## 📢 课程导入

### 前言

你有没有发现，有时候你给AI说一堆要求，它还是理解错你的意思？但如果你给它看两个例子，它瞬间就懂了！这就是今天要讲的核心技巧——Few-shot Learning（少样本学习）！

更神奇的是，有一个技巧能让AI的推理能力提升几十个百分点——只需要在提示词里加一句"让我们一步步思考"！这就是Chain-of-Thought（思维链）技巧。这两个技巧是OpenAI和Google研究团队的重大发现，被证明能大幅提升AI的表现！

---

### 核心价值点

**第一，Few-shot是最被低估但最有效的提示词技巧。**

很多研究表明：给AI看3个例子，效果比写100行要求还好！为什么？因为例子是最直观的说明方式。就像教小孩，你说"注意语法、逻辑、结构"，他听不懂；你给他看三篇范文，他瞬间就明白了！

而且Few-shot不需要训练模型，不需要额外成本，只需要在提示词里加几个例子！投入产出比简直太高了！Google的研究显示，3个好例子能让准确率提升50%以上！

**第二，Chain-of-Thought是让AI学会"慢思考"的关键。**

AI默认会直接给答案，但复杂问题需要分步推理。CoT就是教AI"把思考过程写出来"，就像你做数学题要写解题步骤一样！加了CoT后，AI在数学、逻辑、推理类任务上的准确率能提升30-50%！

最神奇的是，只需要在提示词加一句"Let's think step by step"，就能激活AI的推理能力！这是Google研究团队2022年的重大发现，彻底改变了提示词工程！

**第三，Few-shot和CoT可以完美结合使用。**

想象一下：你给AI看几个例子（Few-shot），每个例子都展示了完整的思考过程（CoT），AI就能学会"既理解格式，又学会推理"！这是目前最强的提示词组合技巧，被称为"Few-shot CoT"！

这个技巧在复杂任务上的表现，甚至接近了经过特殊训练的模型！这意味着，你用提示词就能达到模型微调的效果，省下几万块的微调成本！

**第四，掌握这两个技巧，你就掌握了提示词工程的精髓。**

如果说前面学的框架（RTCF、CRISPE、CO-STAR）是"结构"，那Few-shot和CoT就是"内核"！结构告诉你怎么组织提示词，而这两个技巧告诉你怎么让AI真正理解你的意图、学会推理。

很多AI工程师工作多年，也不一定深入理解这两个技巧。你学完这节课，提示词工程能力会超过90%的从业者！

---

### 行动号召

今天这一课会教你：
- Zero-shot、One-shot、Few-shot的区别
- 如何设计高质量的Few-shot示例
- Chain-of-Thought的原理和使用方法
- Few-shot + CoT的组合技巧
- 真实场景的应用案例

**学完这节课，你的提示词准确率能提升50%以上！**

---

## 📖 知识讲解

### 1. Few-shot Learning详解

#
![Input Output](./images/input_output.svg)
*图：Input Output*

### 1.1 三种学习模式

```
Zero-shot（零样本学习）：
- 不给任何示例
- 只给任务描述
- AI纯靠理解来完成

One-shot（单样本学习）：
- 给1个示例
- AI参考这个示例
- 理解基本模式

Few-shot（少样本学习）：
- 给2-5个示例
- AI学习示例的规律
- 准确率大幅提升
```

**效果对比（以文本分类为例）：**

```
任务：情感分类（正面/负面）

Zero-shot准确率：60-70%
One-shot准确率：75-80%
Few-shot准确率（3个示例）：85-92%
Few-shot准确率（5个示例）：90-95%
```

---

#### 1.2 为什么Few-shot如此有效？

**原理1：模式识别**
```
AI通过示例识别出输入输出的模式：
- 输入格式是什么样的
- 输出格式应该怎么写
- 边界情况如何处理
```

**原理2：歧义消除**
```
文字描述可能有歧义，但示例是明确的：

描述："输出要简洁"
→ AI不知道多简洁

示例："输入：xxx → 输出：5个字"
→ AI立刻明白
```

**原理3：隐式知识传递**
```
示例能传递很多隐式信息：
- 语言风格
- 专业程度
- 细节处理
- 异常情况
```

---

#### 1.3 Few-shot示例设计原则

**原则1：代表性**
```
示例要覆盖典型情况：

✅ 好的选择：
- 示例1：简单情况
- 示例2：中等复杂度
- 示例3：边界情况

❌ 不好的选择：
- 三个示例都很简单
- 都是同一类型
```

**原则2：多样性**
```
示例之间要有差异：

任务：情感分类

✅ 好的多样性：
- 示例1：明确的正面（"太棒了！"）
- 示例2：明确的负面（"太差了！"）
- 示例3：微妙的正面（"还不错"）

❌ 不好的多样性：
- 示例1："很好"
- 示例2："非常好"
- 示例3："特别好"
（都太相似）
```

**原则3：质量高于数量**
```
研究显示：
- 3个高质量示例 > 10个低质量示例
- 超过5个示例，收益递减
- 最佳数量：2-3个

原因：
- 质量差的示例会误导AI
- 示例太多占用token，成本高
- AI可能过拟合某个示例
```

**原则4：格式一致**
```
所有示例的格式必须完全一致：

✅ 格式一致：
示例1：
输入：今天天气真好
输出：正面

示例2：
输入：这个产品太烂了
输出：负面

❌ 格式不一致：
示例1：
Q：今天天气真好
A：正面情感

示例2：
输入：这个产品太烂了
输出类别：负面
（格式混乱，AI会困惑）
```

---

### 2. Chain-of-Thought (CoT) 详解

#### 2.1 什么是CoT？

```
Chain-of-Thought（思维链）：
让AI把推理过程展示出来，而不是直接给答案

核心理念：
"思考过程比答案更重要"

类比：
就像数学考试，老师要求你写解题步骤，
不是直接写答案
```

#### 2.2 CoT的神奇效果

**经典实验（Google Research, 2022）：**

```
任务：数学应用题
"Roger有5个网球。他又买了2罐网球，
每罐3个球。他现在有多少个球？"

Zero-CoT（直接问答）：
AI答案：10个 ❌（错误！）
准确率：17.7%

With CoT（加思考过程）：
提示词："Let's think step by step"
AI回答：
"Roger开始有5个球。
他买了2罐，每罐3个，所以是2×3=6个。
总共是5+6=11个球。"
答案：11个 ✅（正确！）
准确率：78.7%

提升：61个百分点！
```

---

#### 2.3 CoT的使用方式

**方式1：Zero-shot CoT（最简单）**

```
只需要在问题后面加一句魔法咒语：

英文："Let's think step by step"
中文："让我们一步步思考"

示例：
任务：判断一个数是否是质数

提示词：
判断97是否是质数。Let's think step by step.

AI输出：
让我们一步步分析：
1. 质数的定义是只能被1和自身整除
2. 检查97能否被2整除：97是奇数，不能
3. 检查能否被3整除：9+7=16，不是3的倍数
4. 检查能否被5整除：末位不是0或5
5. 检查能否被7整除：97÷7=13...6
6. 继续检查到√97≈9.8
7. 都不能整除
结论：97是质数✓
```

**方式2：Few-shot CoT（最强大）**

```
在示例中展示思考过程：

示例1：
问题：小明有15元，买了3支铅笔，每支2元，还剩多少钱？
思考过程：
1. 计算铅笔总价：3×2=6元
2. 计算剩余：15-6=9元
答案：9元

示例2：
问题：一个班30人，女生比男生多6人，男生有多少人？
思考过程：
1. 设男生x人，女生(x+6)人
2. 方程：x+(x+6)=30
3. 求解：2x=24，x=12
答案：12人

现在，请解决：
问题：[你的问题]
```

---

#### 2.4 CoT适用场景

**✅ 强烈推荐使用CoT的场景：**

```
1. 数学计算
   - 应用题
   - 多步计算
   - 逻辑推理

2. 复杂推理
   - 因果分析
   - 逻辑推断
   - 决策制定

3. 多步骤任务
   - 问题诊断
   - 方案设计
   - 代码调试

4. 需要解释的场景
   - 教育场景（学生需要看懂过程）
   - 审核场景（需要知道理由）
   - 专业咨询（需要推理依据）
```

**⚠️ 不必使用CoT的场景：**

```
1. 简单查询
   - "Python是什么语言？"
   - "今天星期几？"

2. 记忆型任务
   - 翻译
   - 总结
   - 改写

3. 创意生成
   - 写诗
   - 取名字
   - 头脑风暴

4. 严格格式输出
   - JSON生成
   - 代码生成
   - 表格制作
```

---

### 3. Few-shot + CoT 组合技巧

#### 3.1 组合的威力

```
单独使用Few-shot：准确率85%
单独使用CoT：准确率78%
组合使用：准确率92%！

原因：
- Few-shot教会AI格式和模式
- CoT教会AI如何推理
- 组合后既有格式又有推理
```

---

#### 3.2 组合使用模板

**模板1：标准Few-shot CoT**

```
任务描述：[明确任务]

示例1：
输入：[输入1]
思考过程：
步骤1：[推理步骤1]
步骤2：[推理步骤2]
步骤3：[推理步骤3]
输出：[输出1]

示例2：
输入：[输入2]
思考过程：
步骤1：[推理步骤1]
步骤2：[推理步骤2]
步骤3：[推理步骤3]
输出：[输出2]

示例3：
输入：[输入3]
思考过程：
步骤1：[推理步骤1]
步骤2：[推理步骤2]
步骤3：[推理步骤3]
输出：[输出3]

---
现在，请处理：
输入：[新输入]
```

---

#### 3.3 实际案例

**案例1：代码调试**

```
任务：诊断Python代码错误并给出修复建议

示例1：
代码：
def sum_list(lst):
    total = 0
    for i in lst:
        total += i
    return total
print(sum_list([1, 2, 'a', 4]))

思考过程：
1. 分析代码逻辑：累加列表元素
2. 识别问题：列表中有字符串'a'
3. 错误类型：TypeError，不能将str和int相加
4. 出错位置：for循环中的total += i
5. 修复方案：添加类型检查或try-except

诊断：TypeError - 列表包含非数字元素
修复建议：
```python
def sum_list(lst):
    total = 0
    for i in lst:
        if isinstance(i, (int, float)):
            total += i
        else:
            print(f"跳过非数字元素：{i}")
    return total
```

示例2：
代码：
def divide(a, b):
    return a / b
result = divide(10, 0)

思考过程：
1. 分析代码：除法操作
2. 识别问题：除数为0
3. 错误类型：ZeroDivisionError
4. 风险：程序会崩溃
5. 修复方案：添加除数检查

诊断：ZeroDivisionError - 除数为零
修复建议：
```python
def divide(a, b):
    if b == 0:
        return "错误：除数不能为0"
    return a / b
```

---
现在，请诊断以下代码：
```python
def get_first_element(lst):
    return lst[0]
result = get_first_element([])
```
```

---

### 4. 高级技巧和注意事项

#### 4.1 示例顺序的影响

```
研究发现：示例的顺序会影响结果

✅ 好的顺序：
- 从简单到复杂
- 典型案例在前，边界案例在后
- 正面案例和负面案例交叉出现

❌ 不好的顺序：
- 所有正面案例放一起
- 最复杂的案例放第一个
- 随机乱序
```

#### 4.2 示例与任务的相似度

```
研究发现：
示例与实际任务越相似，效果越好

策略：
- 如果知道任务类型，选择相似示例
- 如果任务多样，准备多组示例
- 动态选择最相关的示例
```

#### 4.3 CoT的长度控制

```
CoT不是越长越好：

✅ 合适的CoT：
- 3-5个关键推理步骤
- 每步清晰明确
- 逻辑连贯

❌ 过长的CoT：
- 10+个步骤，冗余
- 占用大量token
- 可能包含无关信息
```

---

## 💻 Demo案例：Few-shot与CoT实战

### 案例说明

通过实际代码展示Few-shot和CoT的效果对比。

### 代码实现

创建`few_shot_cot_demo.py`：

```python
"""
Few-shot Learning 和 Chain-of-Thought 实战演示
对比不同方法的效果差异
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LOCAL_LLM_BASE_URL"),
    api_key=os.getenv("LOCAL_LLM_API_KEY")
)


def get_response(prompt: str, temperature: float = 0.3) -> str:
    """获取AI回复"""
    response = client.chat.completions.create(
        model=os.getenv("LOCAL_LLM_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=1000
    )
    return response.choices[0].message.content


def demo_zero_shot():
    """演示1：Zero-shot（基准）"""
    print("\n" + "="*80)
    print("演示1：Zero-shot（不给示例）")
    print("="*80)
    
    prompt = """任务：判断评论的情感倾向（正面/负面/中性）

评论：外观不错，但是用起来有点卡，整体还算可以接受

请给出判断："""
    
    print(f"提示词：\n{prompt}")
    print("\n" + "-"*80)
    response = get_response(prompt)
    print(f"AI判断：\n{response}")
    print("\n💡 特点：仅凭理解，可能不够准确")


def demo_few_shot():
    """演示2：Few-shot（给示例）"""
    print("\n" + "="*80)
    print("演示2：Few-shot（给3个示例）")
    print("="*80)
    
    prompt = """任务：判断评论的情感倾向（正面/负面/中性）

示例1：
评论：这个产品真的超级好用，强烈推荐！
判断：正面

示例2：
评论：质量太差了，完全不值这个价，后悔购买
判断：负面

示例3：
评论：还行吧，没什么特别的，也没什么大问题
判断：中性

---
现在，请判断以下评论：
评论：外观不错，但是用起来有点卡，整体还算可以接受
判断："""
    
    print(f"提示词：\n{prompt}")
    print("\n" + "-"*80)
    response = get_response(prompt)
    print(f"AI判断：\n{response}")
    print("\n💡 特点：通过示例学习模式，更准确")


def demo_zero_shot_cot():
    """演示3：Zero-shot CoT（魔法咒语）"""
    print("\n" + "="*80)
    print("演示3：Zero-shot CoT（加'让我们一步步思考'）")
    print("="*80)
    
    prompt = """任务：判断评论的情感倾向（正面/负面/中性）

评论：外观不错，但是用起来有点卡，整体还算可以接受

让我们一步步分析这个评论的情感倾向："""
    
    print(f"提示词：\n{prompt}")
    print("\n" + "-"*80)
    response = get_response(prompt, temperature=0.5)
    print(f"AI分析：\n{response}")
    print("\n💡 特点：展示推理过程，结论更有说服力")


def demo_few_shot_cot():
    """演示4：Few-shot CoT（最强组合）"""
    print("\n" + "="*80)
    print("演示4：Few-shot CoT（示例+思考过程）")
    print("="*80)
    
    prompt = """任务：判断评论的情感倾向（正面/负面/中性）

示例1：
评论：这个产品真的超级好用，强烈推荐！
思考过程：
1. 关键词分析："超级好用"、"强烈推荐" - 明确的正面词汇
2. 语气判断：感叹号，情绪激动，表达喜爱
3. 整体态度：完全正面，没有负面因素
判断：正面

示例2：
评论：质量太差了，完全不值这个价，后悔购买
思考过程：
1. 关键词分析："太差"、"不值"、"后悔" - 明确的负面词汇
2. 语气判断：失望和不满的情绪
3. 整体态度：完全负面，强烈不推荐
判断：负面

示例3：
评论：还行吧，没什么特别的，也没什么大问题
思考过程：
1. 关键词分析："还行"、"没什么特别" - 平淡的描述
2. 语气判断：neither正面nor负面，态度中立
3. 整体态度：可以接受但不突出，neither推荐nor反对
判断：中性

---
现在，请分析以下评论：
评论：外观不错，但是用起来有点卡，整体还算可以接受

思考过程："""
    
    print(f"提示词：\n{prompt}")
    print("\n" + "-"*80)
    response = get_response(prompt, temperature=0.3)
    print(f"AI分析：\n{response}")
    print("\n💡 特点：既有格式学习，又有推理能力，最强！")


def demo_math_problem():
    """演示5：数学问题上的CoT效果"""
    print("\n" + "="*80)
    print("演示5：数学应用题 - CoT的威力")
    print("="*80)
    
    # 不使用CoT
    prompt_no_cot = """解决这个问题：
小明有24元，买了3支钢笔，每支5元，还买了一本笔记本9元。
他还剩多少钱？

答案："""
    
    print("【不使用CoT】")
    print(f"提示词：\n{prompt_no_cot}")
    print("-" * 80)
    response1 = get_response(prompt_no_cot, temperature=0.1)
    print(f"AI回答：\n{response1}")
    
    # 使用CoT
    prompt_with_cot = """解决这个问题：
小明有24元，买了3支钢笔，每支5元，还买了一本笔记本9元。
他还剩多少钱？

让我们一步步计算："""
    
    print("\n【使用CoT】")
    print(f"提示词：\n{prompt_with_cot}")
    print("-" * 80)
    response2 = get_response(prompt_with_cot, temperature=0.1)
    print(f"AI回答：\n{response2}")
    print("\n💡 对比：CoT让计算过程清晰，准确率更高")


def demo_code_debugging():
    """演示6：代码调试中的Few-shot CoT"""
    print("\n" + "="*80)
    print("演示6：代码调试 - Few-shot CoT应用")
    print("="*80)
    
    prompt = """任务：诊断Python代码问题并给出修复建议

示例：
代码：
```python
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
```

思考过程：
1. 代码功能：计算列表平均值
2. 潜在问题：如果列表为空，len(numbers)=0
3. 错误类型：ZeroDivisionError（除以零）
4. 触发条件：传入空列表
5. 影响：程序崩溃

诊断：空列表导致除零错误
修复建议：
```python
def calculate_average(numbers):
    if not numbers:  # 检查空列表
        return 0  # 或者raise ValueError("列表不能为空")
    total = sum(numbers)
    return total / len(numbers)
```

---
现在，请诊断以下代码：
```python
def find_max(lst):
    max_num = lst[0]
    for num in lst:
        if num > max_num:
            max_num = num
    return max_num

result = find_max([])
```

思考过程："""
    
    print(f"提示词：\n{prompt}")
    print("\n" + "-"*80)
    response = get_response(prompt, temperature=0.3)
    print(f"AI诊断：\n{response}")
    print("\n💡 应用：Few-shot CoT在代码审查中很实用")


def demo_comparison_summary():
    """演示7：效果对比总结"""
    print("\n" + "="*80)
    print("演示7：四种方法效果对比总结")
    print("="*80)
    
    print("""
┌─────────────────┬──────────┬──────────┬──────────────┬────────┐
│ 方法            │ 准确率   │ 可解释性 │ Token消耗    │ 适用场景│
├─────────────────┼──────────┼──────────┼──────────────┼────────┤
│ Zero-shot       │ ⭐⭐⭐   │ ⭐⭐     │ 低           │ 简单任务│
│ Few-shot        │ ⭐⭐⭐⭐ │ ⭐⭐⭐   │ 中           │ 格式化  │
│ Zero-shot CoT   │ ⭐⭐⭐⭐ │ ⭐⭐⭐⭐ │ 低           │ 推理任务│
│ Few-shot CoT    │ ⭐⭐⭐⭐⭐│ ⭐⭐⭐⭐⭐│ 高           │ 复杂任务│
└─────────────────┴──────────┴──────────┴──────────────┴────────┘

选择策略：
1. 简单查询 → Zero-shot（最经济）
2. 格式要求高 → Few-shot（学习格式）
3. 需要推理 → Zero-shot CoT（展示过程）
4. 复杂任务 → Few-shot CoT（最强但成本高）

实际应用建议：
- 开发阶段：用Zero-shot快速验证
- 测试阶段：尝试Few-shot看是否提升
- 生产环境：根据准确率要求和成本预算选择
- 关键任务：使用Few-shot CoT保证质量
""")


def main():
    """主函数"""
    print("🎯 Few-shot Learning 与 Chain-of-Thought 实战演示")
    print("="*80)
    print("对比不同技巧的效果差异")
    print("="*80)
    
    # 运行所有演示
    demo_zero_shot()
    demo_few_shot()
    demo_zero_shot_cot()
    demo_few_shot_cot()
    demo_math_problem()
    demo_code_debugging()
    demo_comparison_summary()
    
    print("\n" + "="*80)
    print("✅ 演示完成！")
    print("\n💡 核心总结：")
    print("1. Few-shot：通过示例学习格式和模式")
    print("2. CoT：展示推理过程，提升准确率")
    print("3. Few-shot CoT：最强组合，准确率最高")
    print("4. 'Let's think step by step' 是魔法咒语")
    print("5. 示例质量 > 数量，2-3个高质量示例最佳")
    print("6. 根据任务复杂度和成本选择合适方法")
    print("="*80)


if __name__ == "__main__":
    main()
```

### 运行演示

```bash
python few_shot_cot_demo.py
```

---

## 🎯 最佳实践总结

### 1. Few-shot设计清单

```
✅ 示例数量：2-3个（最多5个）
✅ 示例质量：精心挑选，代表性强
✅ 格式一致：严格统一，不能混乱
✅ 覆盖边界：包含典型和边界情况
✅ 顺序合理：从简单到复杂
✅ 真实场景：贴近实际应用
```

### 2. CoT使用建议

```
✅ 适用场景：推理、计算、多步骤任务
✅ 魔法咒语："Let's think step by step"
✅ 步骤清晰：3-5步，每步明确
✅ 逻辑连贯：步骤之间有因果关系
✅ 结论明确：最后给出清晰答案
```

### 3. 组合使用策略

```
简单任务：
Zero-shot即可

中等任务：
Few-shot（3个示例）

复杂推理：
Zero-shot CoT

最高要求：
Few-shot CoT（2-3个完整示例+推理）
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解Few-shot的原理和作用
- [ ] 能设计高质量的Few-shot示例
- [ ] 掌握CoT技巧的使用方法
- [ ] 能组合使用Few-shot和CoT
- [ ] 能根据场景选择合适方法

---

## 📝 下一课预告

**第13课：提示词测试与优化方法**

学会了写提示词，如何评估效果？如何系统优化？下一课我们将学习：
- 提示词测试的方法
- 效果评估指标
- 系统化优化流程
- A/B测试技巧

**让你的提示词工程更加科学和系统！**

---

**🎉 恭喜你完成第12课！**

你已经掌握了Few-shot和CoT这两个核心技巧！

**下一步：** 打开 `第13课-提示词测试评估.md`

