![Agent架构设计](./images/agent.svg)
*图：Agent架构设计*

# 第72课：Agent核心组件：Planning、Memory、Tools、Action

> **本课目标**：深入理解Agent的四大核心组件及其实现
> 
> **核心技能**：Planning规划、Memory记忆、Tools工具、Action执行
> 
> **实战案例**：构建完整的模块化Agent
> 
> **学习时长**：85分钟

---

## 📖 口播文案（5分钟）
![Action](./images/action.svg)
*图：Action*


### 🎯 前言

"上节课我们理解了Agent的本质：从对话到行动的跨越。

今天我们要深入Agent的内部，拆解Agent的四大核心组件！

**为什么要理解组件？**

就像修车，你得先知道发动机、变速箱、刹车系统是怎么工作的，才能修好车！

**Agent也一样！**

想要开发强大的Agent，必须深入理解每个组件的作用和实现！

**Agent的四大核心组件：**

```
1. Planning（规划）- Agent的大脑
2. Memory（记忆）- Agent的记忆系统
3. Tools（工具）- Agent的手脚
4. Action（行动）- Agent的执行引擎
```

**先看一个真实案例，感受组件协作：**

**任务：帮我计划一次北京3日游**

```
【用户】帮我计划北京3日游

【Planning规划组件】
  分析：这是一个复杂任务，需要分解
  
  规划步骤：
  1. 了解用户偏好（预算、兴趣）
  2. 查询北京景点信息
  3. 规划每日行程
  4. 计算预算
  5. 生成完整计划

【Memory记忆组件】
  短期记忆：
  - 当前任务：北京3日游规划
  - 已完成：了解偏好
  - 待完成：查询景点...
  
  长期记忆：
  - 用户之前喜欢历史文化
  - 预算通常在5000元左右

【Action执行组件】
  执行步骤1：询问用户偏好
  → 用户回复：喜欢历史文化，预算5000
  
  执行步骤2：调用景点查询工具
  → 调用 search_attractions("北京", "历史文化")
  
  执行步骤3：调用天气API
  → 调用 get_weather("北京", "未来3天")
  
  执行步骤4：生成行程
  → 基于景点和天气规划路线

【Tools工具组件】
  可用工具：
  ✅ search_attractions - 景点查询
  ✅ get_weather - 天气查询
  ✅ calculate_budget - 预算计算
  ✅ search_hotels - 酒店查询
  ✅ search_restaurants - 餐厅推荐

【最终输出】
  为您规划好了北京3日游：
  
  Day 1：故宫 → 天安门 → 王府井
  Day 2：长城 → 鸟巢 → 水立方
  Day 3：颐和园 → 圆明园
  
  预算明细：
  - 门票：800元
  - 住宿：1200元
  - 餐饮：1500元
  - 交通：500元
  总计：4000元（在预算内）
```

**看到了吗？四个组件完美协作！**

**现在让我详细拆解每个组件：**

**1. Planning（规划）- Agent的大脑**

```
作用：
• 分解复杂任务
• 制定执行计划
• 决定下一步行动
• 调整执行策略

关键技术：
• Task Decomposition（任务分解）
• Plan Generation（计划生成）
• Reflection（反思）
```

**2. Memory（记忆）- Agent的记忆系统**

```
作用：
• 记住对话历史
• 存储任务状态
• 学习过往经验
• 跨会话持久化

类型：
• Short-term Memory（短期记忆）：当前对话
• Long-term Memory（长期记忆）：持久化存储
• Working Memory（工作记忆）：任务执行状态
```

**3. Tools（工具）- Agent的手脚**

```
作用：
• 与外部系统交互
• 获取实时信息
• 执行具体操作
• 扩展Agent能力

类型：
• API调用工具
• 数据库工具
• 文件操作工具
• 计算工具
```

**4. Action（行动）- Agent的执行引擎**

```
作用：
• 选择合适的工具
• 准备工具参数
• 执行工具调用
• 处理执行结果

流程：
• Tool Selection（工具选择）
• Parameter Preparation（参数准备）
• Execution（执行）
• Result Processing（结果处理）
```

**组件之间如何协作？**

```
Planning → "我需要查天气"
    ↓
Memory → "记住这是第2步"
    ↓
Action → "选择get_weather工具"
    ↓
Tools → "执行天气查询"
    ↓
Result → 返回结果
    ↓
Planning → "基于天气规划行程"
    ↓
循环...
```

**今天这一课，我要带你：**

**第一部分：Planning规划组件**
- 任务分解
- 计划生成
- 反思机制

**第二部分：Memory记忆组件**
- 短期记忆
- 长期记忆
- 记忆检索

**第三部分：Tools工具组件**
- 工具定义
- 工具注册
- 工具调用

**第四部分：Action执行组件**
- 工具选择
- 参数提取
- 结果处理

**第五部分：完整实现**
- 模块化Agent
- 组件集成
- 实战案例

学完这一课，你将掌握Agent的核心原理！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【四大组件的关系】

Planning（大脑）:
  "我要做什么？怎么做？"

Memory（记忆）:
  "我之前做过什么？现在在哪一步？"

Tools（手脚）:
  "我能做什么？有哪些工具？"

Action（执行）:
  "具体怎么执行？参数是什么？"

【协作模式】

Planning制定计划 → Memory记录状态
         ↓
Action选择工具 → Tools执行操作
         ↓
Memory更新状态 → Planning调整计划
```

---

## 📚 第一部分：Planning规划组件

### 一、Planning的核心功能

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "待执行"
    IN_PROGRESS = "执行中"
    COMPLETED = "已完成"
    FAILED = "失败"

@dataclass
class Task:
    """任务定义"""
    task_id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = None  # 依赖的任务ID
    result: Optional[any] = None
    
class PlanningModule:
    """规划模块"""
    
    def __init__(self, llm):
        self.llm = llm
        self.tasks: List[Task] = []
    
    def decompose_task(
        self,
        goal: str,
        verbose: bool = True
    ) -> List[Task]:
        """
        任务分解
        
        将复杂目标分解为可执行的子任务
        """
        if verbose:
            print("\n" + "="*60)
            print("【Planning】任务分解")
            print("="*60)
            print(f"目标: {goal}")
        
        # 使用LLM进行任务分解
        prompt = f"""请将以下目标分解为具体的、可执行的子任务。

目标：{goal}

要求：
1. 每个子任务应该是具体的、可执行的
2. 子任务之间应该有逻辑顺序
3. 考虑任务之间的依赖关系

请以JSON格式返回任务列表：
[
    {{
        "task_id": "task_1",
        "description": "任务描述",
        "dependencies": []
    }},
    ...
]

JSON："""
        
        response = self.llm.invoke(prompt)
        
        import json
        try:
            tasks_data = json.loads(response.content)
        except:
            # 解析失败，返回单个任务
            tasks_data = [{
                "task_id": "task_1",
                "description": goal,
                "dependencies": []
            }]
        
        # 创建Task对象
        tasks = []
        for task_data in tasks_data:
            task = Task(
                task_id=task_data['task_id'],
                description=task_data['description'],
                dependencies=task_data.get('dependencies', [])
            )
            tasks.append(task)
        
        self.tasks = tasks
        
        if verbose:
            print(f"\n分解为 {len(tasks)} 个子任务:")
            for i, task in enumerate(tasks, 1):
                deps = f"(依赖: {', '.join(task.dependencies)})" if task.dependencies else ""
                print(f"  {i}. [{task.task_id}] {task.description} {deps}")
        
        return tasks
    
    def get_next_task(self) -> Optional[Task]:
        """
        获取下一个可执行的任务
        
        考虑依赖关系，返回可以立即执行的任务
        """
        for task in self.tasks:
            if task.status != TaskStatus.PENDING:
                continue
            
            # 检查依赖是否都完成
            if task.dependencies:
                dependencies_completed = all(
                    self._get_task_by_id(dep_id).status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )
                if not dependencies_completed:
                    continue
            
            return task
        
        return None
    
    def _get_task_by_id(self, task_id: str) -> Optional[Task]:
        """通过ID获取任务"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def mark_task_completed(self, task_id: str, result: any):
        """标记任务完成"""
        task = self._get_task_by_id(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.result = result
    
    def mark_task_failed(self, task_id: str):
        """标记任务失败"""
        task = self._get_task_by_id(task_id)
        if task:
            task.status = TaskStatus.FAILED
    
    def reflect_and_replan(
        self,
        current_situation: str,
        verbose: bool = True
    ) -> List[Task]:
        """
        反思与重新规划
        
        基于当前情况，调整计划
        """
        if verbose:
            print("\n【Planning】反思与重新规划")
            print(f"当前情况: {current_situation}")
        
        # 这里可以基于当前情况重新生成计划
        # 简化实现：保持原计划
        return self.tasks

# 演示
def demo_planning_module():
    """演示Planning模块"""
    
    from langchain.chat_models import ChatOpenAI
    
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    planner = PlanningModule(llm)
    
    # 测试任务分解
    goal = "帮我规划北京3日游"
    tasks = planner.decompose_task(goal, verbose=True)
    
    # 获取下一个任务
    print("\n获取下一个可执行任务:")
    next_task = planner.get_next_task()
    if next_task:
        print(f"  {next_task.description}")

# demo_planning_module()
```

---

## 💻 第二部分：Memory记忆组件

### 一、Memory的类型与实现

```python
from datetime import datetime
from typing import List, Dict, Any
from collections import deque

class ConversationMessage:
    """对话消息"""
    def __init__(self, role: str, content: str, timestamp: datetime = None):
        self.role = role  # 'user' or 'assistant' or 'system'
        self.content = content
        self.timestamp = timestamp or datetime.now()

class MemoryModule:
    """记忆模块"""
    
    def __init__(
        self,
        short_term_limit: int = 10,
        working_memory_size: int = 5
    ):
        # 短期记忆（最近N轮对话）
        self.short_term_memory: deque = deque(maxlen=short_term_limit)
        
        # 工作记忆（当前任务相关）
        self.working_memory: Dict[str, Any] = {}
        
        # 长期记忆（持久化存储）
        self.long_term_memory: List[Dict] = []
    
    def add_message(self, role: str, content: str):
        """添加对话消息到短期记忆"""
        message = ConversationMessage(role, content)
        self.short_term_memory.append(message)
    
    def get_conversation_history(
        self,
        last_n: int = None
    ) -> List[Dict]:
        """获取对话历史"""
        messages = list(self.short_term_memory)
        
        if last_n:
            messages = messages[-last_n:]
        
        return [
            {'role': msg.role, 'content': msg.content}
            for msg in messages
        ]
    
    def set_working_memory(self, key: str, value: Any):
        """设置工作记忆"""
        self.working_memory[key] = value
    
    def get_working_memory(self, key: str, default: Any = None) -> Any:
        """获取工作记忆"""
        return self.working_memory.get(key, default)
    
    def clear_working_memory(self):
        """清空工作记忆"""
        self.working_memory = {}
    
    def save_to_long_term(self, key: str, value: Any):
        """保存到长期记忆"""
        self.long_term_memory.append({
            'key': key,
            'value': value,
            'timestamp': datetime.now()
        })
    
    def search_long_term(self, query: str) -> List[Dict]:
        """搜索长期记忆"""
        # 简化实现：关键词匹配
        results = []
        for memory in self.long_term_memory:
            if query.lower() in str(memory['value']).lower():
                results.append(memory)
        return results
    
    def get_context(self, verbose: bool = False) -> str:
        """获取完整上下文（用于LLM）"""
        context_parts = []
        
        # 对话历史
        history = self.get_conversation_history(last_n=5)
        if history:
            context_parts.append("【对话历史】")
            for msg in history:
                context_parts.append(f"{msg['role']}: {msg['content']}")
        
        # 工作记忆
        if self.working_memory:
            context_parts.append("\n【工作记忆】")
            for key, value in self.working_memory.items():
                context_parts.append(f"- {key}: {value}")
        
        context = "\n".join(context_parts)
        
        if verbose:
            print("\n" + "="*60)
            print("【Memory】当前上下文")
            print("="*60)
            print(context)
        
        return context

# 演示
def demo_memory_module():
    """演示Memory模块"""
    
    memory = MemoryModule()
    
    # 添加对话历史
    memory.add_message('user', '帮我查北京天气')
    memory.add_message('assistant', '北京今天20-28℃，晴')
    memory.add_message('user', '那明天呢？')
    
    # 设置工作记忆
    memory.set_working_memory('current_city', '北京')
    memory.set_working_memory('task', '天气查询')
    
    # 保存到长期记忆
    memory.save_to_long_term('user_preference', {'likes': ['历史', '文化']})
    
    # 获取上下文
    context = memory.get_context(verbose=True)

demo_memory_module()
```

---

## 🎯 第三部分：Tools工具组件

### 一、Tool的定义与管理

```python
from typing import Callable, Any, Dict
from dataclasses import dataclass
import inspect

@dataclass
class ToolParameter:
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True

class Tool:
    """工具定义"""
    
    def __init__(
        self,
        name: str,
        func: Callable,
        description: str,
        parameters: List[ToolParameter] = None
    ):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters or self._extract_parameters()
    
    def _extract_parameters(self) -> List[ToolParameter]:
        """从函数签名自动提取参数"""
        sig = inspect.signature(self.func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            param_type = param.annotation.__name__ if param.annotation != inspect.Parameter.empty else 'Any'
            parameters.append(ToolParameter(
                name=param_name,
                type=param_type,
                description=f"参数{param_name}",
                required=param.default == inspect.Parameter.empty
            ))
        
        return parameters
    
    def run(self, **kwargs) -> Any:
        """执行工具"""
        try:
            result = self.func(**kwargs)
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def to_dict(self) -> Dict:
        """转为字典（用于LLM）"""
        return {
            'name': self.name,
            'description': self.description,
            'parameters': [
                {
                    'name': p.name,
                    'type': p.type,
                    'description': p.description,
                    'required': p.required
                }
                for p in self.parameters
            ]
        }

class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """注册工具"""
        self.tools[tool.name] = tool
        print(f"✅ 注册工具: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Tool]:
        """列出所有工具"""
        return list(self.tools.values())
    
    def get_tools_description(self) -> str:
        """获取所有工具的描述（用于LLM）"""
        descriptions = []
        for tool in self.tools.values():
            params_desc = ", ".join([
                f"{p.name}({p.type})"
                for p in tool.parameters
            ])
            descriptions.append(
                f"- {tool.name}({params_desc}): {tool.description}"
            )
        return "\n".join(descriptions)

# 演示
def demo_tool_registry():
    """演示Tool Registry"""
    
    # 创建工具注册中心
    registry = ToolRegistry()
    
    # 定义一些工具函数
    def get_weather(city: str) -> str:
        """获取天气"""
        return f"{city}的天气是晴天"
    
    def calculate(expression: str) -> float:
        """计算数学表达式"""
        return eval(expression)
    
    def search_web(query: str) -> str:
        """搜索网络"""
        return f"搜索结果for {query}"
    
    # 注册工具
    registry.register(Tool(
        name="get_weather",
        func=get_weather,
        description="获取指定城市的天气信息"
    ))
    
    registry.register(Tool(
        name="calculate",
        func=calculate,
        description="计算数学表达式"
    ))
    
    registry.register(Tool(
        name="search_web",
        func=search_web,
        description="在网络上搜索信息"
    ))
    
    # 列出所有工具
    print("\n" + "="*60)
    print("【Tools】已注册工具")
    print("="*60)
    print(registry.get_tools_description())
    
    # 使用工具
    print("\n测试工具调用:")
    tool = registry.get_tool("get_weather")
    result = tool.run(city="北京")
    print(f"  {result}")

demo_tool_registry()
```

---

## ⚡ 第四部分：Action执行组件

### 一、Action的执行流程

```python
class ActionModule:
    """行动执行模块"""
    
    def __init__(self, llm, tool_registry: ToolRegistry):
        self.llm = llm
        self.tool_registry = tool_registry
    
    def execute(
        self,
        task_description: str,
        context: str = "",
        verbose: bool = True
    ) -> Dict:
        """
        执行任务
        
        流程：
        1. 选择合适的工具
        2. 提取工具参数
        3. 执行工具调用
        4. 处理执行结果
        """
        if verbose:
            print("\n" + "="*60)
            print("【Action】执行任务")
            print("="*60)
            print(f"任务: {task_description}")
        
        # 步骤1：选择工具
        tool_name, tool_params = self._select_tool_and_params(
            task_description,
            context,
            verbose
        )
        
        if not tool_name:
            return {
                'success': False,
                'message': '无需使用工具',
                'direct_answer': tool_params  # 这时tool_params是直接回答
            }
        
        # 步骤2：执行工具
        result = self._execute_tool(
            tool_name,
            tool_params,
            verbose
        )
        
        return result
    
    def _select_tool_and_params(
        self,
        task: str,
        context: str,
        verbose: bool
    ) -> tuple:
        """选择工具并提取参数"""
        
        if verbose:
            print("\n  【步骤1】选择工具")
        
        tools_desc = self.tool_registry.get_tools_description()
        
        prompt = f"""你是一个智能助手，可以使用以下工具：

{tools_desc}

上下文：
{context}

任务：{task}

请分析：
1. 是否需要使用工具？
2. 如果需要，选择哪个工具？
3. 工具的参数是什么？

以JSON格式回复：
{{
    "need_tool": true/false,
    "tool_name": "工具名称" (如果需要),
    "tool_params": {{"param1": "value1"}} (如果需要),
    "direct_answer": "直接回答" (如果不需要工具)
}}

JSON："""
        
        response = self.llm.invoke(prompt)
        
        import json
        try:
            decision = json.loads(response.content)
        except:
            decision = {'need_tool': False, 'direct_answer': response.content}
        
        if decision['need_tool']:
            tool_name = decision['tool_name']
            tool_params = decision['tool_params']
            
            if verbose:
                print(f"    选择工具: {tool_name}")
                print(f"    参数: {tool_params}")
            
            return tool_name, tool_params
        else:
            if verbose:
                print(f"    无需工具")
            return None, decision.get('direct_answer', '')
    
    def _execute_tool(
        self,
        tool_name: str,
        tool_params: Dict,
        verbose: bool
    ) -> Dict:
        """执行工具"""
        
        if verbose:
            print(f"\n  【步骤2】执行工具")
            print(f"    调用: {tool_name}({tool_params})")
        
        tool = self.tool_registry.get_tool(tool_name)
        
        if not tool:
            return {
                'success': False,
                'error': f'工具 {tool_name} 不存在'
            }
        
        result = tool.run(**tool_params)
        
        if verbose:
            if result['success']:
                print(f"    ✅ 成功: {result['result']}")
            else:
                print(f"    ❌ 失败: {result['error']}")
        
        return result
```

---

## 📝 课后练习

### 练习1：增强Planning
实现更智能的任务分解算法

### 练习2：持久化Memory
使用数据库持久化长期记忆

### 练习3：扩展Tools
添加更多实用工具

---

## 🎓 知识总结

### 核心要点

1. **四大核心组件**
   - Planning：任务分解与规划
   - Memory：短期、长期、工作记忆
   - Tools：工具注册与管理
   - Action：工具选择与执行

2. **组件协作**
   - Planning制定计划
   - Memory提供上下文
   - Action选择并执行工具
   - Tools完成具体操作

3. **设计原则**
   - 模块化：各组件独立
   - 可扩展：易于添加新功能
   - 可维护：清晰的接口

---

## 🚀 下节预告

下一课：**第73课：ReAct框架深入**

- ReAct原理
- Reasoning + Acting
- 实战实现

**掌握最经典的Agent框架！** 🎯

---

**💪 记住：理解组件，才能构建强大Agent！**

**下一课见！** 🎉
