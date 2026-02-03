![Agent架构设计](./images/agent.svg)
*图：Agent架构设计*

# 第73课：ReAct框架：推理与行动循环

> **本课目标**：掌握ReAct框架，实现Reasoning + Acting的完美结合
> 
> **核心技能**：ReAct原理、思考链、行动循环
> 
> **实战案例**：构建ReAct Agent
> 
> **学习时长**：80分钟

---

## 📖 口播文案（5分钟）
![Action](./images/action.svg)
*图：Action*


### 🎯 前言

"前面两节课我们学习了Agent的基础和核心组件。

今天我们要学习Agent领域最重要的框架：**ReAct**！

**什么是ReAct？为什么它这么重要？**

ReAct = Reasoning（推理） + Acting（行动）

这是一个革命性的框架，让Agent能够像人类一样思考和行动！

**先看一个对比，感受ReAct的威力：**

**任务：23 * 47 + 189 = ?**

**普通Agent（直接行动）：**

```
用户："23 * 47 + 189 = ?"

Agent：
  [Action] 调用计算器
  [Observation] 错误：表达式太复杂

❌ 失败了！
```

**ReAct Agent（思考 + 行动）：**

```
用户："23 * 47 + 189 = ?"

Thought（思考）:
  "这个表达式有两个运算：乘法和加法。
   我需要先算23 * 47，再加189。"

Action（行动）:
  调用计算器: 23 * 47

Observation（观察）:
  结果: 1081

Thought（思考）:
  "现在我得到了1081，接下来要加189"

Action（行动）:
  调用计算器: 1081 + 189

Observation（观察）:
  结果: 1270

Thought（思考）:
  "完成了！答案是1270"

Answer（回答）:
  23 * 47 + 189 = 1270

✅ 成功！
```

**看到区别了吗？**

```
普通Agent：
  直接行动 → 失败

ReAct Agent：
  思考 → 行动 → 观察 → 思考 → 行动 → ...
  像人类一样解决问题！
```

**ReAct的核心循环：**

```
1. Thought（思考）
   "我需要做什么？"
   "下一步应该怎么做？"
   
2. Action（行动）
   执行具体操作
   调用工具
   
3. Observation（观察）
   工具返回什么？
   结果是什么？
   
4. Thought（再思考）
   "结果符合预期吗？"
   "需要继续吗？"
   "达成目标了吗？"
```

**再看一个复杂例子：**

**任务：帮我查询明天北京的天气，如果会下雨就帮我预订室内活动**

**ReAct Agent的执行过程：**

```
Thought 1:
  "用户想知道明天北京的天气，
   并且如果下雨要预订室内活动。
   首先我需要查询天气。"

Action 1:
  get_weather(city="北京", date="明天")

Observation 1:
  明天北京：多云转雨，15-22℃，降水概率80%

Thought 2:
  "看来明天会下雨，降水概率80%很高。
   根据用户要求，我需要推荐室内活动。
   我应该搜索北京的室内活动。"

Action 2:
  search_indoor_activities(city="北京")

Observation 2:
  找到5个室内活动：
  1. 博物馆（¥50）
  2. 电影院（¥60）
  3. 密室逃脱（¥150）
  4. 室内游泳（¥80）
  5. 保龄球（¥100）

Thought 3:
  "我已经得到了天气信息和室内活动列表。
   现在我可以给用户一个完整的建议了。"

Answer:
  "明天北京会下雨（降水概率80%），温度15-22℃。
   
   为您推荐以下室内活动：
   1. 博物馆 - 文化体验，¥50
   2. 电影院 - 休闲娱乐，¥60
   3. 密室逃脱 - 团队挑战，¥150
   
   如果需要，我可以帮您预订。"

✅ 完美完成！
```

**ReAct的优势：**

**1. 可解释性强**
```
每一步思考都清晰可见
用户知道Agent在想什么
便于调试和优化
```

**2. 容错能力强**
```
如果一步失败，可以重新思考
可以调整策略
不会卡死
```

**3. 处理复杂任务**
```
可以分步骤完成
可以根据中间结果调整
适合多步骤推理
```

**4. 更像人类**
```
模拟人类的思考过程
边想边做
根据反馈调整
```

**今天这一课，我要带你：**

**第一部分：ReAct原理**
- 核心概念
- 执行流程
- 设计模式

**第二部分：ReAct实现**
- Prompt设计
- 循环控制
- 状态管理

**第三部分：ReAct优化**
- 提前终止
- 错误处理
- 性能优化

**第四部分：完整案例**
- 多步推理
- 工具调用
- 实战演练

**第五部分：最佳实践**
- Prompt工程
- 调试技巧
- 常见问题

学完这一课，你将掌握最强大的Agent框架！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【ReAct = 人类的思考方式】

人类解决问题：
1. 想一想（Thought）
2. 做一做（Action）
3. 看结果（Observation）
4. 再想想（Thought）
5. 继续做（Action）
...

ReAct就是模拟这个过程！

【循环结构】

Thought → Action → Observation
   ↑                    ↓
   └────────────────────┘
        循环直到完成
```

---

## 📚 第一部分：ReAct原理

### 一、ReAct核心概念

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class StepType(Enum):
    """步骤类型"""
    THOUGHT = "Thought"      # 思考
    ACTION = "Action"        # 行动
    OBSERVATION = "Observation"  # 观察
    ANSWER = "Answer"        # 最终答案

@dataclass
class ReActStep:
    """ReAct步骤"""
    step_number: int
    step_type: StepType
    content: str
    
    def __str__(self):
        return f"{self.step_type.value} {self.step_number}: {self.content}"

class ReActTrace:
    """ReAct执行轨迹"""
    
    def __init__(self):
        self.steps: List[ReActStep] = []
        self.final_answer: Optional[str] = None
    
    def add_thought(self, content: str):
        """添加思考步骤"""
        step_num = len([s for s in self.steps if s.step_type == StepType.THOUGHT]) + 1
        self.steps.append(ReActStep(step_num, StepType.THOUGHT, content))
    
    def add_action(self, content: str):
        """添加行动步骤"""
        step_num = len([s for s in self.steps if s.step_type == StepType.ACTION]) + 1
        self.steps.append(ReActStep(step_num, StepType.ACTION, content))
    
    def add_observation(self, content: str):
        """添加观察步骤"""
        step_num = len([s for s in self.steps if s.step_type == StepType.OBSERVATION]) + 1
        self.steps.append(ReActStep(step_num, StepType.OBSERVATION, content))
    
    def set_answer(self, answer: str):
        """设置最终答案"""
        self.final_answer = answer
        self.steps.append(ReActStep(0, StepType.ANSWER, answer))
    
    def print_trace(self):
        """打印执行轨迹"""
        print("\n" + "="*60)
        print("ReAct执行轨迹")
        print("="*60 + "\n")
        
        for step in self.steps:
            if step.step_type == StepType.THOUGHT:
                print(f"💭 {step}")
            elif step.step_type == StepType.ACTION:
                print(f"🔧 {step}")
            elif step.step_type == StepType.OBSERVATION:
                print(f"👁️  {step}")
            elif step.step_type == StepType.ANSWER:
                print(f"\n✅ {step}")
            print()

# 演示
def demo_react_trace():
    """演示ReAct轨迹"""
    
    trace = ReActTrace()
    
    # 模拟执行过程
    trace.add_thought("我需要先计算23 * 47")
    trace.add_action("calculate(23 * 47)")
    trace.add_observation("结果: 1081")
    
    trace.add_thought("现在需要加189")
    trace.add_action("calculate(1081 + 189)")
    trace.add_observation("结果: 1270")
    
    trace.add_thought("计算完成，得到最终答案")
    trace.set_answer("23 * 47 + 189 = 1270")
    
    trace.print_trace()

demo_react_trace()
```

---

## 💻 第二部分：ReAct Agent实现

### 一、ReAct Agent核心实现

```python
class ReActAgent:
    """ReAct Agent实现"""
    
    def __init__(self, llm, tools, max_iterations: int = 10):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
    
    def run(self, question: str, verbose: bool = True) -> str:
        """运行ReAct循环"""
        
        if verbose:
            print("\n" + "🚀"*30)
            print("ReAct Agent启动")
            print("🚀"*30)
            print(f"\n问题: {question}\n")
        
        trace = ReActTrace()
        
        # ReAct循环
        for iteration in range(self.max_iterations):
            if verbose:
                print(f"{'='*60}")
                print(f"迭代 {iteration + 1}")
                print(f"{'='*60}\n")
            
            # 生成下一步（Thought + Action 或 Answer）
            next_step = self._generate_next_step(question, trace, verbose)
            
            # 检查是否得到最终答案
            if next_step['type'] == 'answer':
                trace.set_answer(next_step['content'])
                if verbose:
                    print(f"✅ 得到最终答案！\n")
                break
            
            # Thought
            thought = next_step['thought']
            trace.add_thought(thought)
            if verbose:
                print(f"💭 Thought: {thought}\n")
            
            # Action
            action_name = next_step['action']
            action_input = next_step['action_input']
            action_str = f"{action_name}({action_input})"
            trace.add_action(action_str)
            if verbose:
                print(f"🔧 Action: {action_str}\n")
            
            # Execute Action → Observation
            observation = self._execute_action(action_name, action_input)
            trace.add_observation(observation)
            if verbose:
                print(f"👁️  Observation: {observation}\n")
        
        # 打印完整轨迹
        if verbose:
            trace.print_trace()
        
        return trace.final_answer or "未能得到答案"
    
    def _generate_next_step(
        self,
        question: str,
        trace: ReActTrace,
        verbose: bool
    ) -> dict:
        """生成下一步"""
        
        # 构建Prompt
        tools_desc = self._get_tools_description()
        history = self._format_trace(trace)
        
        prompt = f"""你是一个会使用ReAct框架的智能助手。

可用工具：
{tools_desc}

问题：{question}

{history}

请按照ReAct格式继续：
1. 如果还没有得到答案，输出：
   Thought: <你的思考>
   Action: <工具名称>
   Action Input: <工具输入>

2. 如果已经得到答案，输出：
   Thought: <总结性思考>
   Answer: <最终答案>

你的回复："""
        
        response = self.llm.invoke(prompt)
        content = response.content.strip()
        
        if verbose:
            print(f"LLM输出:\n{content}\n")
        
        # 解析输出
        return self._parse_llm_output(content)
    
    def _get_tools_description(self) -> str:
        """获取工具描述"""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)
    
    def _format_trace(self, trace: ReActTrace) -> str:
        """格式化执行轨迹"""
        if not trace.steps:
            return ""
        
        history_parts = []
        for step in trace.steps:
            history_parts.append(f"{step.step_type.value}: {step.content}")
        
        return "\n".join(history_parts)
    
    def _parse_llm_output(self, content: str) -> dict:
        """解析LLM输出"""
        
        lines = content.strip().split('\n')
        
        result = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('Thought:'):
                result['thought'] = line.replace('Thought:', '').strip()
            elif line.startswith('Action:'):
                result['action'] = line.replace('Action:', '').strip()
            elif line.startswith('Action Input:'):
                result['action_input'] = line.replace('Action Input:', '').strip()
            elif line.startswith('Answer:'):
                result['type'] = 'answer'
                result['content'] = line.replace('Answer:', '').strip()
                return result
        
        result['type'] = 'action'
        return result
    
    def _execute_action(self, action_name: str, action_input: str) -> str:
        """执行动作"""
        
        tool = self.tools.get(action_name)
        
        if not tool:
            return f"错误：工具 {action_name} 不存在"
        
        try:
            result = tool.run(action_input)
            if isinstance(result, dict) and 'success' in result:
                if result['success']:
                    return str(result['result'])
                else:
                    return f"错误：{result['error']}"
            return str(result)
        except Exception as e:
            return f"错误：{str(e)}"

# 完整演示
def demo_react_agent():
    """演示ReAct Agent"""
    
    from langchain.chat_models import ChatOpenAI
    
    # 初始化LLM
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    # 定义工具
    class SimpleTool:
        def __init__(self, name, func, description):
            self.name = name
            self.func = func
            self.description = description
        
        def run(self, input_str):
            return self.func(input_str)
    
    def calculate(expression):
        """计算器"""
        try:
            result = eval(expression)
            return result
        except:
            return "计算错误"
    
    def get_weather(city):
        """天气查询"""
        weather_data = {
            '北京': '明天：多云转雨，15-22℃，降水概率80%',
            '上海': '明天：晴，18-25℃',
            '深圳': '明天：多云，22-28℃'
        }
        return weather_data.get(city, '未知城市')
    
    tools = [
        SimpleTool(
            name="calculate",
            func=calculate,
            description="计算数学表达式，输入表达式如'2+3'"
        ),
        SimpleTool(
            name="get_weather",
            func=get_weather,
            description="获取指定城市明天的天气，输入城市名"
        )
    ]
    
    # 创建ReAct Agent
    agent = ReActAgent(llm, tools, max_iterations=5)
    
    # 测试问题
    questions = [
        "23 * 47 + 189 等于多少？",
        "明天北京会下雨吗？"
    ]
    
    for question in questions:
        answer = agent.run(question, verbose=True)
        print(f"\n{'='*60}")
        print(f"最终答案: {answer}")
        print(f"{'='*60}\n\n")

# demo_react_agent()
```

---

## 📝 课后练习

### 练习1：添加重试机制
如果工具调用失败，自动重试

### 练习2：优化Prompt
改进Prompt以提高解析准确率

### 练习3：添加更多工具
实现搜索、翻译等工具

---

## 🎓 知识总结

### 核心要点

1. **ReAct框架**
   - Reasoning + Acting
   - 思考 → 行动 → 观察循环
   - 模拟人类解决问题

2. **ReAct优势**
   - 可解释性强
   - 容错能力强
   - 处理复杂任务
   - 更像人类思考

3. **实现要点**
   - Prompt设计
   - 输出解析
   - 循环控制
   - 状态管理

4. **最佳实践**
   - 限制迭代次数
   - 清晰的工具描述
   - 良好的错误处理

---

## 🎉 第12章完成！

恭喜！你已经掌握了Agent开发的基础：
- ✅ Agent概念与价值
- ✅ 核心组件实现
- ✅ ReAct框架

---

## 🚀 下一章预告

**第13章：Tool Calling工具开发（7课）**

- Tool Calling原理
- Function Calling
- 自定义工具开发
- 多工具Agent

**深入工具开发！** 🛠️

---

**💪 记住：ReAct = 像人类一样思考和行动！**

**下一课见！** 🎉
