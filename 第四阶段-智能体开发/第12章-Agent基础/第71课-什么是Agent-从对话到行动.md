![Agent架构设计](./images/agent.svg)
*图：Agent架构设计*

# 第71课：什么是Agent？从对话到行动

> **本课目标**：理解Agent的本质，掌握从ChatBot到Agent的跨越
> 
> **核心技能**：Agent概念、架构设计、核心能力
> 
> **实战案例**：对比ChatBot vs Agent
> 
> **学习时长**：70分钟

---

## 📖 口播文案（5分钟）
![Action](./images/action.svg)
*图：Action*


### 🎯 前言

"恭喜你！完成了70节课的学习,掌握了RAG系统的全部技能！

今天，我们要开启一个全新的篇章：**Agent智能体开发**！

**重要更新：2025年LangChain 1.0正式发布！**

LangChain 1.0带来了革命性的Agent开发体验：
- ✅ **不到10行代码**即可创建Agent
- ✅ **基于LangGraph构建**，提供持久化、流式输出、人机交互
- ✅ **标准化模型接口**，轻松切换不同LLM提供商
- ✅ **生产就绪**，稳定的1.0 API

**什么是Agent？为什么要学Agent？**

我先给你看两个对话场景，你来感受一下区别：

**场景A：普通ChatBot**

```
用户："帮我查一下明天北京的天气"

ChatBot回复：
"抱歉，我是一个语言模型，无法查询实时天气信息。
你可以访问天气网站或使用天气APP查询。"

用户："..."（失望）
```

**场景B：Agent**

```
用户："帮我查一下明天北京的天气"

Agent思考：
1. 用户想知道明天北京的天气
2. 我需要调用天气API
3. 执行：调用天气API，城市=北京，日期=明天

Agent回复：
"已为您查询，明天北京天气：
• 温度：15-25℃
• 天气：多云转晴
• 风力：3-4级
建议：适合外出，建议穿长袖。"

用户："太棒了！"（满意）
```

**看到区别了吗？**

```
ChatBot（对话型）：
• 只能聊天
• 不能行动
• 信息有限（训练数据）
• 被动响应

Agent（行动型）：
• 能聊天 ✅
• 能行动 ✅
• 可以访问外部工具 ✅
• 主动规划和执行 ✅
```

**再看一个更复杂的例子：**

**任务：帮我预订明天晚上7点的餐厅**

**ChatBot的回复：**
```
"我可以给你一些建议：
1. 你可以打开美团APP
2. 搜索附近的餐厅
3. 选择适合的餐厅
4. 进行预订
祝你用餐愉快！"

（完全没有帮到忙 ❌）
```

**Agent的执行过程：**
```
Agent思考：
"用户想预订明天晚上7点的餐厅，我需要：
1. 获取用户的位置
2. 查询附近的餐厅
3. 筛选有空位的
4. 帮用户预订"

Agent行动：
【步骤1】调用地理位置API → 获取到：北京市朝阳区
【步骤2】调用餐厅查询API → 找到30家餐厅
【步骤3】调用预订API，查询空位 → 5家有空位
【步骤4】展示给用户："找到5家餐厅，推荐..."
【步骤5】用户选择后，调用预订API → 预订成功

Agent回复：
"已为您成功预订！
• 餐厅：海底捞(朝阳大悦城店)
• 时间：明天晚上7:00
• 人数：2人
• 预订号：HD20231115001
已发送短信提醒到您的手机。"

（完美完成任务 ✅）
```

**这就是Agent的强大之处！**

**Agent的三大核心能力：**

**1. 思考（Reasoning）**
```
• 理解用户意图
• 分解复杂任务
• 制定执行计划
• 推理下一步行动

就像人类的大脑！
```

**2. 行动（Action）**
```
• 调用外部工具
• 执行具体操作
• 获取实时信息
• 改变外部状态

就像人类的手脚！
```

**3. 记忆（Memory）**
```
• 记住上下文
• 学习过往经验
• 跟踪任务进展
• 持久化状态

就像人类的记忆！
```

**Agent的实际应用场景：**

**1. 智能客服**
```
传统客服：只能回答FAQ
Agent客服：
• 自动查询订单
• 自动处理退款
• 自动安排物流
• 自动升级工单
```

**2. 智能办公助手**
```
传统助手：只能查询
Agent助手：
• 自动发送邮件
• 自动预订会议室
• 自动生成报告
• 自动整理文档
```

**3. 代码助手**
```
传统工具：代码补全
Agent助手：
• 自动查找文档
• 自动运行代码
• 自动修复Bug
• 自动生成测试
```

**4. 数据分析助手**
```
传统BI：手动查询
Agent助手：
• 自动连接数据库
• 自动分析数据
• 自动生成图表
• 自动发送报告
```

**今天这一课，我要带你：**

**第一部分：Agent核心概念**
- Agent定义
- Agent vs ChatBot
- Agent的价值

**第二部分：Agent架构**
- 核心组件
- 工作流程
- 设计模式

**第三部分：Agent能力矩阵**
- 感知能力
- 推理能力
- 行动能力
- 学习能力

**第四部分：简单实现**
- 最简Agent
- 工具调用
- 完整流程

**第五部分：实战案例**
- 天气查询Agent
- 计算器Agent
- 对比分析

学完这一课，你将理解Agent的本质和价值！

准备好进入Agent的世界了吗？让我们开始！"

---

### 💡 核心理念

```
【从对话到行动的跨越】

ChatBot时代：
  用户问 → AI答
  仅限对话

Agent时代：
  用户说 → AI想 → AI做 → 完成任务
  从对话到行动！

【Agent = 大脑 + 手脚】

大脑（LLM）：
  • 理解意图
  • 规划方案
  • 推理决策

手脚（Tools）：
  • 执行操作
  • 获取信息
  • 改变状态
```

---

## 📚 第一部分：Agent核心概念

### 一、什么是Agent？

```python
from typing import List, Dict, Callable
from dataclasses import dataclass

@dataclass
class AgentDefinition:
    """Agent定义"""
    
    # Agent的核心特征
    characteristics = {
        '自主性': 'Autonomous - 能够独立决策和行动',
        '反应性': 'Reactive - 能够感知环境并响应',
        '主动性': 'Proactive - 能够主动采取行动',
        '社交性': 'Social - 能够与其他Agent或人类交互'
    }
    
    # Agent vs 其他系统
    comparisons = {
        'vs ChatBot': {
            'ChatBot': '只能对话，不能行动',
            'Agent': '既能对话，又能行动'
        },
        'vs RPA': {
            'RPA': '固定流程，不能思考',
            'Agent': '智能规划，自主决策'
        },
        'vs API': {
            'API': '被动调用，需要编程',
            'Agent': '主动执行，自然语言控制'
        }
    }
    
    # Agent的核心能力
    core_abilities = [
        '理解自然语言',
        '制定执行计划',
        '调用外部工具',
        '处理执行结果',
        '自我纠错',
        '持续学习'
    ]

# 可视化展示
def visualize_agent_concept():
    """可视化Agent概念"""
    
    print("="*60)
    print("什么是Agent？")
    print("="*60)
    
    definition = AgentDefinition()
    
    print("\n【核心特征】")
    for char, desc in definition.characteristics.items():
        print(f"  • {char}（{desc.split(' - ')[0]}）")
        print(f"    {desc.split(' - ')[1]}")
    
    print("\n【对比分析】")
    for comparison, details in definition.comparisons.items():
        print(f"\n  {comparison}")
        for system, capability in details.items():
            print(f"    {system}: {capability}")
    
    print("\n【核心能力】")
    for i, ability in enumerate(definition.core_abilities, 1):
        print(f"  {i}. {ability}")

visualize_agent_concept()
```

### 二、Agent vs ChatBot 深度对比

```python
class SystemComparison:
    """系统对比分析"""
    
    @staticmethod
    def compare_capabilities():
        """对比能力"""
        
        comparison_table = {
            '能力维度': ['ChatBot', 'RAG', 'Agent'],
            '自然语言理解': ['✅', '✅', '✅'],
            '生成回复': ['✅', '✅', '✅'],
            '访问知识库': ['❌', '✅', '✅'],
            '调用外部工具': ['❌', '❌', '✅'],
            '执行实际操作': ['❌', '❌', '✅'],
            '自主规划任务': ['❌', '❌', '✅'],
            '多步骤推理': ['❌', '部分', '✅'],
            '错误处理与重试': ['❌', '❌', '✅'],
            '学习与改进': ['❌', '❌', '✅']
        }
        
        return comparison_table
    
    @staticmethod
    def print_comparison():
        """打印对比表"""
        
        print("\n" + "="*60)
        print("ChatBot vs RAG vs Agent 能力对比")
        print("="*60 + "\n")
        
        comparison = SystemComparison.compare_capabilities()
        
        # 打印表头
        header = f"{'能力维度':<20} {'ChatBot':<12} {'RAG':<12} {'Agent':<12}"
        print(header)
        print("-" * 60)
        
        # 打印每行
        dimensions = list(comparison.keys())[1:]  # 跳过'能力维度'
        for i, dimension in enumerate(dimensions):
            row = f"{dimension:<20} {comparison['ChatBot'][i]:<12} {comparison['RAG'][i]:<12} {comparison['Agent'][i]:<12}"
            print(row)
        
        print("\n" + "="*60)
        print("结论：Agent = ChatBot + RAG + Tools + Planning")
        print("="*60)

SystemComparison.print_comparison()
```

### 三、真实案例对比

```python
class RealWorldExample:
    """真实案例对比"""
    
    @staticmethod
    def weather_query_example():
        """天气查询案例"""
        
        print("\n" + "="*60)
        print("案例1：天气查询")
        print("="*60)
        
        print("\n用户：明天北京天气怎么样？")
        
        print("\n【ChatBot的回复】")
        print("  抱歉，我无法查询实时天气。")
        print("  我的训练数据只到2023年10月。")
        print("  建议您访问天气网站查询。")
        print("  ❌ 没有解决问题")
        
        print("\n【RAG的回复】")
        print("  根据知识库中的信息...")
        print("  （但知识库里没有实时天气数据）")
        print("  ❌ 同样无法回答")
        
        print("\n【Agent的执行过程】")
        print("  1. 理解意图：用户想知道明天北京的天气")
        print("  2. 制定计划：调用天气API")
        print("  3. 执行操作：")
        print("     - 调用API: get_weather(city='北京', date='明天')")
        print("     - 获取结果: 15-25℃, 多云")
        print("  4. 生成回复：")
        print("     明天北京天气：15-25℃，多云")
        print("     建议穿长袖外套")
        print("  ✅ 完美解决问题")
    
    @staticmethod
    def booking_example():
        """预订案例"""
        
        print("\n" + "="*60)
        print("案例2：餐厅预订")
        print("="*60)
        
        print("\n用户：帮我订明晚7点的餐厅，4个人")
        
        print("\n【ChatBot的回复】")
        print("  您可以通过以下方式预订餐厅：")
        print("  1. 打开美团APP")
        print("  2. 搜索附近餐厅")
        print("  3. 选择合适的餐厅")
        print("  4. 进行预订")
        print("  ❌ 只给建议，没有实际帮助")
        
        print("\n【Agent的执行过程】")
        print("  1. 理解需求：明晚7点，4人，需要预订餐厅")
        print("  2. 制定计划：")
        print("     - 获取用户位置")
        print("     - 查询附近餐厅")
        print("     - 筛选有空位的")
        print("     - 展示推荐")
        print("     - 帮助预订")
        print("  3. 执行操作：")
        print("     [调用] get_location() → 北京朝阳区")
        print("     [调用] search_restaurants(location, time) → 找到30家")
        print("     [调用] check_availability() → 5家有空位")
        print("     [展示] 推荐列表给用户")
        print("     [调用] make_reservation() → 预订成功")
        print("  4. 完成确认：")
        print("     ✅ 已成功预订海底捞")
        print("     ✅ 明晚7点，4人")
        print("     ✅ 预订号：HD20231115001")
        print("  ✅ 完整完成任务")

    @staticmethod
    def run_examples():
        """运行所有案例"""
        RealWorldExample.weather_query_example()
        RealWorldExample.booking_example()

RealWorldExample.run_examples()
```

---

## 💻 第二部分：Agent架构

### Agent核心架构图

```python
class AgentArchitecture:
    """Agent架构设计"""
    
    components = {
        '感知模块 (Perception)': {
            '作用': '接收和理解输入',
            '包含': ['自然语言理解', '意图识别', '实体提取']
        },
        '规划模块 (Planning)': {
            '作用': '制定执行计划',
            '包含': ['任务分解', '步骤规划', '优先级排序']
        },
        '记忆模块 (Memory)': {
            '作用': '存储和检索信息',
            '包含': ['短期记忆', '长期记忆', '工作记忆']
        },
        '工具模块 (Tools)': {
            '作用': '执行实际操作',
            '包含': ['API调用', '数据库查询', '文件操作']
        },
        '行动模块 (Action)': {
            '作用': '执行决策',
            '包含': ['工具选择', '参数准备', '结果处理']
        },
        '反馈模块 (Feedback)': {
            '作用': '评估和调整',
            '包含': ['结果验证', '错误处理', '策略调整']
        }
    }
    
    @staticmethod
    def visualize_architecture():
        """可视化架构"""
        
        print("\n" + "="*60)
        print("Agent核心架构")
        print("="*60)
        
        print("""
┌─────────────────────────────────────────────────────┐
│                    用户输入                          │
└──────────────────┬──────────────────────────────────┘
                   ↓
        ┌──────────────────────┐
        │   感知模块 (Perception)   │
        │  • 理解自然语言          │
        │  • 识别意图             │
        └──────────┬───────────────┘
                   ↓
        ┌──────────────────────┐
        │   规划模块 (Planning)     │
        │  • 分解任务             │
        │  • 制定计划             │
        └──────────┬───────────────┘
                   ↓
        ┌──────────────────────┐
        │   记忆模块 (Memory)       │  ←→ 持久化存储
        │  • 上下文记忆           │
        │  • 历史经验             │
        └──────────┬───────────────┘
                   ↓
        ┌──────────────────────┐
        │   行动模块 (Action)       │
        │  • 选择工具             │
        │  • 执行操作             │
        └──────────┬───────────────┘
                   ↓
        ┌──────────────────────┐
        │   工具模块 (Tools)        │
        │  • 天气API             │
        │  • 数据库               │
        │  • 文件系统             │
        └──────────┬───────────────┘
                   ↓
        ┌──────────────────────┐
        │   反馈模块 (Feedback)     │
        │  • 验证结果             │
        │  • 错误处理             │
        │  • 继续/完成            │
        └──────────┬───────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│                    用户输出                          │
└─────────────────────────────────────────────────────┘
        """)
        
        print("="*60)
        
        # 详细说明each模块
        for module, details in AgentArchitecture.components.items():
            print(f"\n【{module}】")
            print(f"  作用: {details['作用']}")
            print(f"  包含:")
            for item in details['包含']:
                print(f"    • {item}")

AgentArchitecture.visualize_architecture()
```

---

## 🎯 第三部分：最简Agent实现

### 一、最简单的Agent

```python
from typing import List, Dict, Any, Callable

class SimpleTool:
    """简单工具定义"""
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
    
    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class SimpleAgent:
    """最简单的Agent实现"""
    
    def __init__(self, llm, tools: List[SimpleTool]):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.conversation_history = []
    
    def run(self, user_input: str, verbose: bool = True) -> str:
        """运行Agent"""
        
        if verbose:
            print("\n" + "="*60)
            print("Agent执行过程")
            print("="*60)
            print(f"\n用户输入: {user_input}")
        
        # 步骤1：理解意图并决定是否需要工具
        decision = self._decide_action(user_input, verbose)
        
        # 步骤2：如果需要工具，执行工具
        if decision['need_tool']:
            tool_result = self._use_tool(
                decision['tool_name'],
                decision['tool_input'],
                verbose
            )
            
            # 步骤3：基于工具结果生成最终回复
            final_answer = self._generate_final_answer(
                user_input,
                tool_result,
                verbose
            )
        else:
            # 直接回答，不需要工具
            final_answer = decision['direct_answer']
        
        if verbose:
            print(f"\n最终回复: {final_answer}")
            print("="*60)
        
        return final_answer
    
    def _decide_action(self, user_input: str, verbose: bool) -> Dict:
        """决定是否需要使用工具"""
        
        if verbose:
            print(f"\n【步骤1】决策")
        
        # 构建工具列表描述
        tools_desc = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        
        prompt = f"""你是一个智能助手，可以使用以下工具：

{tools_desc}

用户输入：{user_input}

请分析：
1. 是否需要使用工具？
2. 如果需要，使用哪个工具？
3. 工具的输入参数是什么？

请以JSON格式回复：
{{
    "need_tool": true/false,
    "tool_name": "工具名称" (如果需要工具),
    "tool_input": "工具输入" (如果需要工具),
    "direct_answer": "直接回答" (如果不需要工具)
}}

JSON："""
        
        response = self.llm.invoke(prompt)
        
        import json
        try:
            decision = json.loads(response.content)
        except:
            # 如果解析失败，默认不使用工具
            decision = {
                'need_tool': False,
                'direct_answer': response.content
            }
        
        if verbose:
            if decision['need_tool']:
                print(f"  需要工具: {decision['tool_name']}")
                print(f"  工具输入: {decision['tool_input']}")
            else:
                print(f"  不需要工具，直接回答")
        
        return decision
    
    def _use_tool(self, tool_name: str, tool_input: Any, verbose: bool) -> Any:
        """使用工具"""
        
        if verbose:
            print(f"\n【步骤2】执行工具")
            print(f"  调用: {tool_name}({tool_input})")
        
        tool = self.tools.get(tool_name)
        if not tool:
            return f"错误：工具 {tool_name} 不存在"
        
        try:
            result = tool.run(tool_input)
            
            if verbose:
                print(f"  结果: {result}")
            
            return result
        except Exception as e:
            return f"错误：工具执行失败 - {str(e)}"
    
    def _generate_final_answer(
        self,
        user_input: str,
        tool_result: Any,
        verbose: bool
    ) -> str:
        """生成最终答案"""
        
        if verbose:
            print(f"\n【步骤3】生成最终回复")
        
        prompt = f"""用户问题：{user_input}

工具返回结果：{tool_result}

请基于工具结果，给用户一个友好、完整的回复。

回复："""
        
        response = self.llm.invoke(prompt)
        return response.content

# 演示
def demo_simple_agent():
    """演示简单Agent"""
    
    from langchain.chat_models import ChatOpenAI
    
    # 初始化LLM
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    # 定义工具
    def get_weather(city: str) -> str:
        """获取天气（模拟）"""
        # 实际应用中这里会调用真实的天气API
        weather_data = {
            '北京': '15-25℃，多云',
            '上海': '18-28℃，晴',
            '深圳': '22-30℃，多云转雨'
        }
        return weather_data.get(city, '未知城市')
    
    def calculate(expression: str) -> float:
        """计算器"""
        try:
            return eval(expression)
        except:
            return "计算错误"
    
    # 创建工具列表
    tools = [
        SimpleTool(
            name="get_weather",
            func=get_weather,
            description="获取指定城市的天气信息，输入城市名称"
        ),
        SimpleTool(
            name="calculate",
            func=calculate,
            description="计算数学表达式，输入表达式如'2+3*4'"
        )
    ]
    
    # 创建Agent
    agent = SimpleAgent(llm, tools)
    
    # 测试
    test_queries = [
        "明天北京天气怎么样？",
        "帮我算一下 123 * 456",
        "你好，介绍一下你自己"
    ]
    
    for query in test_queries:
        answer = agent.run(query, verbose=True)
        print("\n" + "-"*60 + "\n")

# demo_simple_agent()
```

---

## 📝 课后练习

### 练习1：扩展SimpleAgent
添加更多工具（搜索、翻译等）

### 练习2：添加记忆功能
让Agent记住之前的对话

### 练习3：错误处理
实现工具调用失败时的重试机制

---

## 🎓 知识总结

### 核心要点

1. **Agent = ChatBot + Tools + Planning**
   - ChatBot只能对话
   - Agent能够行动

2. **Agent的核心特征**
   - 自主性：独立决策
   - 反应性：感知环境
   - 主动性：主动行动
   - 社交性：协作交互

3. **Agent架构**
   - 感知：理解输入
   - 规划：制定计划
   - 记忆：存储信息
   - 行动：执行操作
   - 反馈：评估调整

4. **Agent的价值**
   - 解决实际问题
   - 提高工作效率
   - 自动化复杂任务

---

## 🚀 下节预告

下一课：**第72课：Agent核心组件详解**

- Planning（规划）
- Memory（记忆）
- Tools（工具）
- Action（行动）

**深入Agent的每个组件！** 🎯

---

**💪 记住：Agent = 从对话到行动的跨越！**

**下一课见！** 🎉
