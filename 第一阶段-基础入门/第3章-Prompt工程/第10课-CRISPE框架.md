![注意力流程](./images/attention_flow.svg)
*图：CRISPE框架让AI更精准地理解你的意图*

# 第10课：CRISPE提示词框架实战

> 📚 **课程信息**
> - 所属模块：第一模块 - AI基础与环境搭建  
> - 章节：第3章 - 提示词工程精通（第3/8课）
> - 学习目标：掌握CRISPE框架，能根据场景选择合适的框架
> - 预计时间：60-70分钟
> - 前置知识：第08-09课

---

## 📢 课程导入

### 前言

上一课我们学了RTCF框架，效果立竿见影。但你知道吗？业界还有一个更强大、更专业的提示词框架——CRISPE框架！这个框架是OpenAI官方推荐的，也是很多AI产品团队内部使用的标准。

CRISPE比RTCF多了一个维度：Examples（示例）。这个看似简单的增加，却能让AI的输出准确度提升百分之五十以上！为什么？因为给AI看示例，就像给员工看标准答案一样，效果完全不一样！

---

### 核心价值点

**第一，CRISPE是OpenAI官方推荐的提示词框架。**

你去看OpenAI的官方文档，会发现他们一直在强调一个概念：Few-shot Learning（少样本学习）。什么意思？就是给AI看几个示例，它就能理解你要什么。CRISPE框架把这个理念系统化了，让你能规范地使用示例。

而且CRISPE在企业级应用中使用非常广泛。很多AI产品团队发现，用了CRISPE框架后，用户投诉率下降了一半，满意度大幅提升。为什么？因为输出更稳定、更符合预期！

**第二，Examples（示例）是最被低估的提示词技巧。**

很多人写提示词，花大力气写角色、写任务、写要求，但就是不给示例。结果AI理解偏差，输出不符合预期。但如果你给AI看两三个好的示例，它立刻就懂了！

就像教小孩写作文，你说"要有起承转合"，他听不懂；你给他看三篇范文，他瞬间就明白了。AI也是一样的道理！给示例比说一堆要求有效得多！

**第三，CRISPE框架特别适合需要固定格式输出的场景。**

如果你的AI应用需要：
- 统一的输出格式（比如客服回复）
- 稳定的输出风格（比如品牌文案）
- 精确的分类结果（比如情感分析）

那CRISPE就是你的不二选择！通过提供标准示例，你能让AI的输出非常稳定，就像训练过的员工一样可靠。

**第四，掌握CRISPE和RTCF两个框架，你就掌握了90%的提示词场景。**

什么时候用RTCF？什么时候用CRISPE？怎么组合使用？这些都是有套路的！学会这两个框架，你就能应对绝大部分AI开发场景。而且在面试的时候，能深入讲解这两个框架，面试官会刮目相看！

---

### 行动号召

今天这一课，我会教你：
- CRISPE的五大要素
- 如何设计有效的示例
- CRISPE vs RTCF的选择策略
- 实战中的应用技巧

**学完CRISPE，你的提示词工程能力会再上一个台阶！**

---

## 📖 知识讲解

### 1. CRISPE框架概述

#
![Input Output](./images/input_output.svg)
*图：Input Output*

### 1.1 什么是CRISPE

```
CRISPE是一个系统化的提示词框架，包含五大要素：

C - Capacity and Role（能力与角色）
R - Insight（洞察/背景）
I - Statement（陈述/任务）
S - Personality（个性/风格）
E - Experiment（实验/示例）
```

#### 1.2 CRISPE的起源

```
来源：OpenAI的研究团队和社区实践
应用：企业级AI产品开发
特点：特别强调示例（Few-shot）的作用

适用场景：
✅ 需要固定格式输出
✅ 需要稳定的输出风格
✅ 需要准确的分类判断
✅ 需要模仿特定写作风格
```

---

### 2. CRISPE五大要素详解

#### 2.1 C - Capacity and Role（能力与角色）

**定义：**
- 定义AI的能力边界和角色定位
- 类似RTCF中的Role，但更强调"能力"

**写法：**

```
模板1：角色 + 能力
你是一位Python专家，精通Web开发和数据库设计

模板2：角色 + 能力 + 限制
你是一位前端工程师，擅长React和Vue，但不熟悉后端

模板3：能力列表
你具备以下能力：
- 深入理解RESTful API设计
- 熟悉微服务架构
- 有5年以上的生产环境经验
```

**示例：**

```
✅ 好的Capacity：
你是一位资深技术文档工程师，具备以下能力：
- 能将复杂技术概念转化为通俗易懂的语言
- 擅长设计清晰的文档结构
- 熟悉Markdown和技术写作规范
- 了解开发者的阅读习惯和痛点

❌ 不好的Capacity：
你很聪明（太模糊）
```

---

#### 2.2 R - Insight（洞察/背景）

**定义：**
- 提供任务的背景信息和上下文
- 帮助AI理解"为什么"要做这个任务

**写法：**

```
模板1：问题背景
当前问题：用户反馈系统响应慢
期望结果：优化后响应时间<100ms

模板2：业务背景
业务场景：这是一个电商平台的秒杀功能
用户规模：日活10万，秒杀时并发1万

模板3：历史背景
之前尝试：已经优化过数据库索引
当前效果：仍然不理想，需要新方案
```

**示例：**

```
✅ 好的Insight：
背景洞察：
我们正在开发一个面向中小企业的SaaS产品。目标用户是
没有技术背景的业务人员，他们需要简单易懂的帮助文档。
当前问题：现有文档太技术化，用户看不懂，客服压力大。
期望效果：新文档让用户能自助解决80%的问题。

❌ 不好的Insight：
需要写文档（没有背景信息）
```

---

#### 2.3 I - Statement（陈述/任务）

**定义：**
- 明确、具体地陈述要完成的任务
- 类似RTCF中的Task

**写法：**

```
模板1：直接陈述
任务：设计一个用户登录API接口

模板2：分步陈述
任务分解：
1. 定义接口路径和方法
2. 设计请求参数
3. 设计响应格式
4. 列出可能的错误码

模板3：输入输出陈述
输入：用户名和密码
处理：验证身份，生成token
输出：登录结果和用户信息
```

**示例：**

```
✅ 好的Statement：
任务陈述：
为我们的API文档编写一个"快速开始"章节。
要求包含：
- 环境准备（3步以内）
- 第一个API调用示例（完整代码）
- 预期结果说明
- 常见问题（2-3个）
目标：让开发者在5分钟内完成第一次成功调用。

❌ 不好的Statement：
写个文档（太模糊）
```

---

#### 2.4 S - Personality（个性/风格）

**定义：**
- 定义AI输出的风格和语气
- 这是CRISPE特有的要素

**常见风格类型：**

```
专业严谨型：
语言风格：专业、严谨、正式
适合场景：技术文档、商务报告

通俗易懂型：
语言风格：简单、直白、多用比喻
适合场景：科普文章、新手教程

幽默风趣型：
语言风格：轻松、有趣、适当调侃
适合场景：营销文案、社交媒体

简洁高效型：
语言风格：简短、直接、要点明确
适合场景：新闻摘要、工作汇报
```

**示例：**

```
✅ 好的Personality设置：

风格要求：
- 语气：友好、耐心、鼓励性
- 语言：通俗易懂，避免专业术语
- 表达：多用"你可以"而不是"你应该"
- 举例：每个概念都配一个生活化的比喻
- 长度：每段不超过3句话，保持轻松感

❌ 不好的Personality：
要有趣一点（太模糊）
```

---

#### 2.5 E - Experiment（实验/示例）⭐核心要素

**定义：**
- 提供具体的输入输出示例
- 让AI通过示例理解你的期望
- 这是CRISPE最重要的特色！

**为什么示例如此重要？**

```
研究表明：
- 0个示例：准确率60%
- 1个示例：准确率75%
- 2-3个示例：准确率85-90%
- 5个以上：准确率90-95%

最佳实践：提供2-3个示例
- 太少：AI理解不充分
- 太多：占用太多token，成本高
```

**示例类型：**

**类型1：输入输出示例**
```
示例1：
输入：今天天气真好
输出：正面情感，情感分数：0.8

示例2：
输入：这个产品太烂了
输出：负面情感，情感分数：-0.9

示例3：
输入：还可以吧
输出：中性情感，情感分数：0.1
```

**类型2：完整对话示例**
```
示例对话1：
用户：如何重置密码？
客服：您好！重置密码很简单，请点击登录页面的"忘记密码"链接，
输入您的邮箱，我们会发送重置链接。如有问题随时联系我！😊
```

**类型3：代码示例**
```
示例：
任务：实现数组求和函数
输出：
def sum_array(arr):
    """计算数组元素总和"""
    return sum(arr)

# 测试
print(sum_array([1, 2, 3]))  # 输出：6
```

---

### 3. CRISPE完整示例

#### 示例1：客服机器人

```
【Capacity - 能力与角色】
你是一位专业的在线客服，具备以下能力：
- 快速理解用户问题的核心
- 用简洁友好的语言回答
- 必要时引导用户到正确的资源
- 保持耐心和同理心

【Insight - 背景洞察】
背景：这是一个SaaS产品的在线客服系统
用户群体：中小企业主，技术水平一般
常见问题：账号、支付、功能使用
目标：一次性解决用户问题，减少重复咨询

【Statement - 任务陈述】
任务：根据用户的问题，给出准确、友好的回复
要求：
- 回复长度：50-100字
- 如果问题复杂，引导用户查看帮助文档或联系人工客服
- 回复结束要询问是否还有其他问题

【Personality - 风格个性】
语气：友好、专业、有耐心
表达方式：
- 称呼用户为"您"
- 多用emoji增强亲和力（但不过度）
- 避免专业术语，多用通俗语言
- 语气积极正面，即使是拒绝也要委婉

【Experiment - 示例】
示例1：
用户问题：如何导出数据？
客服回复：您好！导出数据很简单～在数据列表页面，点击右上角的
"导出"按钮，选择导出格式（Excel或CSV）即可下载。导出的文件
会包含所有筛选条件下的数据。有其他问题随时问我！😊

示例2：
用户问题：为什么我的账号被封了？
客服回复：抱歉给您带来不便！账号被限制通常是因为触发了安全策略
（如短时间内大量操作）。建议您查看邮箱中的通知说明，或联系我们
的人工客服（电话：400-xxx-xxxx）进行解封。我们会尽快帮您处理！💪

示例3：
用户问题：怎么取消订阅？
客服回复：明白了！您可以这样取消订阅：进入【设置】→【订阅管理】
→点击【取消订阅】。取消后会立即生效，剩余时间的费用会按比例
退还到您的账户。如果遇到问题，我随时在！😊
```

---

#### 示例2：代码生成

```
【Capacity - 能力与角色】
你是一位资深的Python工程师，具备：
- 10年以上Python开发经验
- 深入理解算法和数据结构
- 注重代码质量和可读性
- 熟悉Python最佳实践和PEP规范

【Insight - 背景洞察】
场景：正在开发一个数据处理系统
技术栈：Python 3.10 + pandas
团队规范：
- 必须有类型注解
- 必须有完整的文档字符串
- 必须有错误处理
- 代码要符合PEP 8

【Statement - 任务陈述】
任务：根据给定的功能需求，编写Python函数
要求：
1. 函数签名要清晰，参数类型标注完整
2. 包含详细的文档字符串（Google风格）
3. 核心逻辑要有注释
4. 包含异常处理
5. 提供简单的使用示例

【Personality - 风格】
代码风格：
- 清晰 > 简洁（宁愿多写几行，也要易读）
- 变量命名要见名知意
- 适当添加空行增强可读性
- 注释要说明"为什么"而不是"是什么"

【Experiment - 示例】
示例1：
需求：实现一个函数，验证邮箱格式是否正确
输出：
```python
import re
from typing import Union

def validate_email(email: str) -> bool:
    """
    验证邮箱格式是否正确
    
    Args:
        email: 待验证的邮箱地址
        
    Returns:
        bool: 邮箱格式正确返回True，否则返回False
        
    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
    """
    # 邮箱正则表达式：用户名@域名.后缀
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    try:
        return bool(re.match(pattern, email))
    except (TypeError, AttributeError):
        # 输入不是字符串类型
        return False

# 使用示例
print(validate_email("test@example.com"))  # True
print(validate_email("invalid"))  # False
```

示例2：
需求：实现一个函数，安全地从字典中获取嵌套值
输出：
```python
from typing import Any, Optional, List

def safe_get(data: dict, keys: List[str], default: Any = None) -> Optional[Any]:
    """
    安全地从嵌套字典中获取值
    
    Args:
        data: 目标字典
        keys: 键的路径列表，如['user', 'profile', 'name']
        default: 获取失败时的默认值
        
    Returns:
        获取到的值，失败则返回default
        
    Examples:
        >>> data = {'user': {'profile': {'name': 'Alice'}}}
        >>> safe_get(data, ['user', 'profile', 'name'])
        'Alice'
        >>> safe_get(data, ['user', 'age'], default=0)
        0
    """
    try:
        result = data
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        # KeyError: 键不存在
        # TypeError: 中间某个值不是字典
        return default

# 使用示例
data = {'user': {'profile': {'name': 'Alice', 'age': 25}}}
print(safe_get(data, ['user', 'profile', 'name']))  # 'Alice'
print(safe_get(data, ['user', 'email'], default='N/A'))  # 'N/A'
```
```

---

### 4. CRISPE vs RTCF 对比

#### 4.1 框架对比

| 维度 | RTCF | CRISPE |
|------|------|--------|
| **要素数量** | 4个 | 5个 |
| **核心特色** | 简洁实用 | 强调示例 |
| **学习难度** | ⭐⭐ 简单 | ⭐⭐⭐ 中等 |
| **适用场景** | 通用 | 需要固定格式 |
| **输出稳定性** | ⭐⭐⭐ 中 | ⭐⭐⭐⭐⭐ 高 |
| **灵活性** | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中 |

#### 4.2 选择策略

**使用RTCF的场景：**

```
✅ 探索性任务
- 不确定输出格式
- 需要AI发挥创造力
- 任务比较开放

✅ 简单任务
- 一次性任务
- 输出格式不重要
- 快速验证想法

✅ 不需要稳定输出
- 每次输出可以不同
- 追求多样性

示例：
- 头脑风暴
- 创意写作
- 探索性分析
```

**使用CRISPE的场景：**

```
✅ 生产环境应用
- 需要稳定的输出
- 固定的格式要求
- 用户体验一致性

✅ 分类/标注任务
- 情感分析
- 意图识别
- 内容分类

✅ 格式化输出
- 生成固定格式文档
- API响应格式
- 数据转换

示例：
- 客服机器人
- 代码生成
- 数据标注
- 文档生成
```

---

### 5. 组合使用技巧

#### 技巧1：RTCF起草，CRISPE精炼

```
第一步：用RTCF快速验证想法
- 快速写一个简单的提示词
- 测试基本效果

第二步：如果效果不稳定
- 改用CRISPE框架
- 添加2-3个示例
- 稳定输出质量
```

#### 技巧2：结合使用

```
可以同时使用两个框架的要素：

RTCF的简洁 + CRISPE的示例
= 最佳实践！

具体做法：
【Role】你是...
【Task】任务是...
【Context】背景是...
【Format】输出格式...
【Examples】示例如下...
```

---

## 💻 Demo案例：CRISPE框架实战

### 案例说明

使用CRISPE框架开发三个实用功能，展示其在不同场景下的应用。

### 代码实现

创建`crispe_framework_demo.py`：

```python
"""
CRISPE框架实战演示
展示CRISPE框架在不同场景下的应用
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LOCAL_LLM_BASE_URL"),
    api_key=os.getenv("LOCAL_LLM_API_KEY")
)


def get_response(prompt: str, temperature: float = 0.7) -> str:
    """获取AI回复"""
    response = client.chat.completions.create(
        model=os.getenv("LOCAL_LLM_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=1000
    )
    return response.choices[0].message.content


def demo_customer_service():
    """演示1：智能客服（CRISPE框架）"""
    print("\n" + "="*80)
    print("演示1：智能客服机器人 - 使用CRISPE框架")
    print("="*80)
    
    crispe_prompt = """【Capacity - 能力与角色】
你是一位专业的电商平台客服，具备：
- 快速理解用户问题并给出解决方案
- 友好耐心的沟通能力
- 熟悉常见的订单、物流、退换货问题

【Insight - 背景洞察】
平台：某大型电商平台
用户群体：普通消费者，各年龄层都有
主要诉求：快速解决问题，希望得到明确答复
服务标准：响应快、态度好、解决问题

【Statement - 任务陈述】
任务：根据用户问题，提供专业的客服回复
要求：
1. 回复长度：50-100字
2. 语气友好，措辞礼貌
3. 给出明确的解决步骤
4. 如需人工介入，提供联系方式

【Personality - 风格】
语气：温暖、专业、有同理心
表达：简洁明了，避免套话
态度：即使是拒绝，也要委婉说明原因

【Experiment - 示例】
示例1：
用户问题：我的订单还没发货，怎么回事？
客服回复：您好！我查到您的订单目前还在仓库打包中，预计今天下午
发货，明天就能看到物流信息啦～您可以在"我的订单"中查看实时状态。
如有疑问随时联系我！😊

示例2：
用户问题：这个商品可以退货吗？
客服回复：当然可以退货！商品签收后7天内，在未使用、包装完好的
情况下都可以申请退货。您可以在订单详情页点击"申请退货"，填写
退货原因，我们会尽快审核处理的！

示例3：
用户问题：你们的客服电话是多少？
客服回复：我们的客服热线是400-xxx-xxxx，工作时间是9:00-21:00。
不过我也可以帮您解决问题哦～请问您遇到了什么困难呢？

现在，请回复以下用户问题：
用户问题：我收到的商品有破损，怎么办？"""
    
    print("\n使用CRISPE框架的提示词：")
    print(crispe_prompt)
    print("\n" + "-"*80)
    print("AI回复：")
    response = get_response(crispe_prompt, temperature=0.7)
    print(response)


def demo_sentiment_analysis():
    """演示2：情感分析（CRISPE框架）"""
    print("\n" + "="*80)
    print("演示2：评论情感分析 - 使用CRISPE框架")
    print("="*80)
    
    crispe_prompt = """【Capacity - 能力与角色】
你是一位专业的文本情感分析师，擅长：
- 准确识别文本的情感倾向
- 理解隐含的情绪表达
- 区分客观陈述和主观情感

【Insight - 背景洞察】
应用场景：电商产品评论分析
业务目的：了解用户满意度，发现产品问题
准确性要求：误判率需要控制在5%以内

【Statement - 任务陈述】
任务：分析用户评论的情感倾向
输出：JSON格式，包含情感类别和置信度

【Personality - 风格】
分析风格：客观、准确、有依据
特别注意：反讽、含蓄表达、情感混合

【Experiment - 示例】
示例1：
评论：这个手机真的太好用了！电池续航给力，拍照效果棒！
输出：
{
  "sentiment": "positive",
  "confidence": 0.95,
  "key_points": ["好用", "续航给力", "拍照棒"],
  "reason": "多个正面词汇，情感明确"
}

示例2：
评论：价格倒是便宜，但是质量真不行，用了两天就坏了
输出：
{
  "sentiment": "negative",
  "confidence": 0.9,
  "key_points": ["质量不行", "用两天就坏"],
  "reason": "虽然提到便宜，但核心是质量问题，整体负面"
}

示例3：
评论：还可以吧，没什么特别的
输出：
{
  "sentiment": "neutral",
  "confidence": 0.85,
  "key_points": ["还可以", "没什么特别"],
  "reason": "态度模棱两可，没有明确正负面"
}

现在，请分析以下评论：
评论：外观设计很漂亮，但是用起来有点卡，希望后续能优化"""
    
    print("\n使用CRISPE框架的提示词：")
    print(crispe_prompt)
    print("\n" + "-"*80)
    print("AI分析结果：")
    response = get_response(crispe_prompt, temperature=0.3)
    print(response)


def demo_code_review():
    """演示3：代码审查（CRISPE框架）"""
    print("\n" + "="*80)
    print("演示3：代码审查助手 - 使用CRISPE框架")
    print("="*80)
    
    code_to_review = """
def calc(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
"""
    
    crispe_prompt = f"""【Capacity - 能力与角色】
你是一位资深的Python代码审查专家，具备：
- 深入理解Python最佳实践
- 能发现潜在的bug和性能问题
- 注重代码可读性和可维护性
- 了解常见的安全漏洞

【Insight - 背景洞察】
代码审查场景：团队协作开发，代码提交前的审查
团队规范：PEP 8、类型注解、错误处理、单元测试
质量标准：可读性、健壮性、性能、安全性

【Statement - 任务陈述】
任务：审查Python代码，给出改进建议
输出格式：
1. 代码质量评分（1-10分）
2. 发现的问题（列表，每个问题包含类型、描述、严重程度）
3. 改进建议（具体可执行）
4. 优化后的代码（可选）

【Personality - 风格】
审查态度：客观、建设性、友好
反馈方式：
- 先肯定做得好的地方
- 再指出问题和改进空间
- 给出具体的改进方案
- 避免使用指责性语言

【Experiment - 示例】
示例1：
待审查代码：
def add(x, y):
    return x + y

审查结果：
评分：7/10

优点：
- 函数命名清晰
- 逻辑简单明了

问题：
1. [规范性-中] 缺少类型注解
2. [文档性-中] 缺少文档字符串
3. [健壮性-低] 没有参数验证

建议：
添加类型注解和文档，增强代码的可读性和可维护性

优化后：
def add(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    \"\"\"计算两个数的和\"\"\"
    return x + y

---

现在，请审查以下代码：

{code_to_review}"""
    
    print("\n使用CRISPE框架的提示词：")
    print(crispe_prompt[:500] + "...")
    print("\n" + "-"*80)
    print("代码审查结果：")
    response = get_response(crispe_prompt, temperature=0.3)
    print(response)


def demo_comparison():
    """演示4：RTCF vs CRISPE对比"""
    print("\n" + "="*80)
    print("演示4：RTCF vs CRISPE 效果对比")
    print("="*80)
    
    task = "将以下文本分类为：投诉、咨询、建议、表扬\n文本：你们的快递太慢了，等了三天还没到"
    
    # 使用RTCF
    rtcf_prompt = f"""【Role】你是文本分类专家
【Task】{task}
【Context】电商客服场景
【Format】输出：分类结果"""
    
    print("\n【使用RTCF框架】")
    print(rtcf_prompt)
    print("-" * 80)
    response1 = get_response(rtcf_prompt, temperature=0.1)
    print(f"结果：{response1}")
    
    # 使用CRISPE（增加示例）
    crispe_prompt = f"""【Capacity】你是文本分类专家
【Insight】电商客服文本分类，准确率要求>90%
【Statement】{task}
【Personality】客观准确
【Examples】
示例1：文本："这个功能怎么用？" → 分类：咨询
示例2：文本："你们产品真棒！" → 分类：表扬
示例3：文本："建议增加夜间模式" → 分类：建议
示例4：文本："我要退款！质量太差" → 分类：投诉"""
    
    print("\n【使用CRISPE框架（有示例）】")
    print(crispe_prompt)
    print("-" * 80)
    response2 = get_response(crispe_prompt, temperature=0.1)
    print(f"结果：{response2}")
    
    print("\n💡 对比总结：")
    print("- RTCF简洁但可能不够准确")
    print("- CRISPE通过示例让AI更准确理解任务")
    print("- 分类任务强烈推荐使用CRISPE + 示例")


def main():
    """主函数"""
    print("🎯 CRISPE框架实战演示")
    print("="*80)
    print("展示CRISPE框架在不同场景的应用")
    print("="*80)
    
    # 运行演示
    demo_customer_service()
    demo_sentiment_analysis()
    demo_code_review()
    demo_comparison()
    
    print("\n" + "="*80)
    print("✅ 演示完成！")
    print("\n💡 核心总结：")
    print("1. CRISPE = Capacity + Insight + Statement + Personality + Experiment")
    print("2. Examples（示例）是CRISPE的核心，能大幅提升准确率")
    print("3. CRISPE适合需要稳定输出的生产环境")
    print("4. 2-3个示例是最佳实践，既准确又不浪费token")
    print("5. RTCF适合探索，CRISPE适合生产")
    print("="*80)


if __name__ == "__main__":
    main()
```

### 运行演示

```bash
# 确保LM Studio服务运行中
python crispe_framework_demo.py
```

---

## 🎯 CRISPE使用技巧总结

### 1. 示例设计原则

```
✅ 好的示例：
- 代表性强（覆盖典型情况）
- 多样性好（正面、负面、边界情况）
- 格式统一（严格遵循输出格式）
- 数量适中（2-3个最佳）

❌ 不好的示例：
- 太相似（示例1和示例2几乎一样）
- 太简单（没有代表性）
- 格式不统一（让AI混乱）
- 太多（浪费token，增加成本）
```

### 2. 五要素优先级

```
必须有：Statement（任务）+ Experiment（示例）
推荐有：Capacity（角色）+ Insight（背景）
可选：Personality（风格）

最简CRISPE：Statement + 2个Examples
完整CRISPE：全部5个要素
```

### 3. 常见错误

```
❌ 错误1：示例质量差
提供的示例本身就有问题，AI会学到错误模式

❌ 错误2：示例不一致
几个示例风格、格式不统一，AI不知道follow哪个

❌ 错误3：过度依赖示例
示例太多（5+个），占用大量token，成本高

❌ 错误4：忽略Insight
没有提供背景，AI不理解为什么要这样做
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解CRISPE五大要素
- [ ] 能设计有效的示例
- [ ] 知道何时用RTCF何时用CRISPE
- [ ] 能用CRISPE框架开发生产级提示词
- [ ] 理解示例对输出质量的影响

---

## 📝 下一课预告

**第11课：CO-STAR提示词框架实战**

还有一个框架？是的！下一课我们将学习：
- CO-STAR框架的6个要素
- 三大框架的对比和选择
- 框架组合使用技巧
- 企业级提示词工程最佳实践

**三大框架齐全，你就是提示词工程专家！**

---

**🎉 恭喜你完成第10课！**

你已经掌握了CRISPE框架，提示词工程能力再上一层楼！

**下一步：** 打开 `第11课-CO-STAR框架.md`

