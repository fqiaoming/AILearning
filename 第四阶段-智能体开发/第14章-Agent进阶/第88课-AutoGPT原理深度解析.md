![Agent进阶架构](./images/agent.svg)
*图：Agent进阶架构*

# 第88课：AutoGPT原理深度解析

> **本课目标**：深入理解AutoGPT的架构和实现原理，掌握自主Agent开发
> 
> **核心技能**：自主规划、长期记忆、目标分解、自我反思
> 
> **实战案例**：实现Mini-AutoGPT
> 
> **学习时长**：95分钟

---

## 📖 口播文案（6分钟）
![Agent Debug](./images/agent_debug.svg)
*图：Agent Debug*


### 🎯 前言

"前面我们学习了Agent的安全性和可观测性。

今天我们要深入研究一个革命性的项目：**AutoGPT！**

**AutoGPT是什么？**

简单说：**能自主完成复杂任务的Agent！**

**传统Agent vs AutoGPT：**

**传统Agent：**
```
用户："帮我写一篇文章"

Agent执行：
1. 生成文章 ✅
2. 完成

特点：
• 单步执行
• 需要明确指令
• 无法处理复杂任务
```

**AutoGPT：**
```
用户："创建一个成功的科技博客"

AutoGPT自主规划：
1. 研究热门科技话题
2. 分析竞争对手
3. 设计博客架构
4. 创建内容日历
5. 撰写第一批文章
6. SEO优化
7. 社交媒体推广
...

特点：
• 多步自主执行
• 自己拆解任务
• 持续到达目标
```

**AutoGPT的革命性在哪里？**

**革命点1：自主规划（Autonomous Planning）**
```
用户给一个高层次目标：
"帮我创业，做一个有利可图的在线业务"

AutoGPT自己规划：
Step 1: 市场调研
  - 搜索热门市场
  - 分析竞争情况
  - 评估市场规模

Step 2: 商业模式设计
  - 选择商业模式
  - 计算成本
  - 预测收入

Step 3: 产品开发
  - 设计产品
  - 开发MVP
  - 测试

...

完全自主！不需要你每步指导！
```

**革命点2：长期记忆（Long-term Memory）**
```
传统Agent：
每次对话都是新的，忘记之前的内容

AutoGPT：
• 记住所有历史
• 学习经验教训
• 持续改进策略

示例：
Day 1: 尝试方案A → 失败
Day 2: AutoGPT记住失败，尝试方案B
Day 3: 基于B的成功，优化为方案C

持续进化！
```

**革命点3：自我反思（Self-reflection）**
```
AutoGPT会问自己：
• "这个计划合理吗？"
• "我还缺少什么信息？"
• "有更好的方法吗？"
• "上次为什么失败？"

然后调整策略！

就像人类的思考过程！
```

**革命点4：无限循环（Continuous Loop）**
```
传统Agent：
任务 → 执行 → 完成

AutoGPT：
目标 → 规划 → 执行 → 评估 → 调整 → 继续...

直到目标达成！
```

**AutoGPT的核心架构：**

```
┌─────────────────────────────────────┐
│         User Goal (用户目标)          │
│    "创建一个成功的科技博客"             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    Planner (规划器)                  │
│    • 分解目标为子任务                 │
│    • 制定执行计划                     │
│    • 评估优先级                       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    Executor (执行器)                 │
│    • 执行计划中的任务                 │
│    • 调用工具                         │
│    • 收集结果                         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    Memory (记忆系统)                 │
│    • 短期记忆：当前上下文             │
│    • 长期记忆：向量数据库             │
│    • 经验总结                         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    Critic (评估器)                   │
│    • 评估执行结果                     │
│    • 判断是否达到目标                 │
│    • 决定下一步                       │
└──────────────┬──────────────────────┘
               │
               ▼
        目标达成？
        /        \
      是          否
      ↓           ↓
     结束        循环
```

**AutoGPT的执行流程：**

```
【第1步】接收目标
用户："创建一个待办事项应用"

【第2步】规划
AutoGPT思考：
"需要做什么？
1. 需求分析
2. 技术选型
3. 架构设计
4. 编码实现
5. 测试
6. 部署"

【第3步】执行第一个任务
任务1: 需求分析
• 搜索类似应用
• 分析功能
• 整理需求文档

【第4步】评估进展
"需求分析完成 ✅
下一步：技术选型"

【第5步】继续执行
任务2: 技术选型
• 研究技术栈
• 对比优缺点
• 做出决策

【第6步】自我反思
"我选择的技术栈合适吗？
有没有更好的选择？
需要调整吗？"

【第7步】持续循环
直到应用完成！
```

**真实AutoGPT案例：**

**案例1：自主创业研究**
```
目标："找到一个有利可图的在线业务机会"

AutoGPT执行了50+步：
• 搜索当前热门市场
• 分析市场趋势报告
• 研究竞争对手
• 计算启动成本
• 评估利润空间
• 分析风险因素
• 生成商业计划书
• 给出具体建议

结果：
提供了3个详细的商业机会
包含完整的分析和执行计划

人类可能需要几周
AutoGPT几小时完成！
```

**案例2：自动代码生成**
```
目标："创建一个天气查询网站"

AutoGPT自主完成：
• 设计网站架构
• 选择技术栈（React + Node.js）
• 查找天气API
• 生成前端代码
• 生成后端代码
• 编写测试
• 创建部署脚本
• 生成README文档

结果：
完整可运行的项目
包含所有必要文件！
```

**AutoGPT的挑战：**

**挑战1：成本高**
```
问题：
每个循环都需要调用LLM
一个任务可能需要50+次调用

成本：
GPT-4: $0.03/1K tokens
复杂任务: $1-$10

解决方案：
• 使用更便宜的模型
• 优化Prompt
• 限制循环次数
```

**挑战2：可能陷入循环**
```
问题：
AutoGPT可能重复执行相同任务

示例：
搜索 → 分析 → 觉得信息不够 → 再搜索 → 再分析 → ...

解决方案：
• 循环检测
• 最大迭代限制
• 进展评估
```

**挑战3：质量不稳定**
```
问题：
不是每次都能完美完成任务

原因：
• LLM的随机性
• 规划可能不完善
• 工具调用可能失败

解决方案：
• 多次尝试
• 人工监督
• 关键步骤人工审核
```

**今天这一课，我要带你：**

**第一部分：AutoGPT架构**
- 核心组件
- 工作流程
- 设计模式

**第二部分：规划系统**
- 目标分解
- 任务规划
- 优先级排序

**第三部分：记忆系统**
- 短期记忆
- 长期记忆
- 向量数据库

**第四部分：自我反思**
- 进展评估
- 策略调整
- 经验学习

**第五部分：完整实战**
- Mini-AutoGPT实现
- 实际应用
- 最佳实践

学完这一课，你将能创建自主Agent！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【AutoGPT = 自主的AI Agent】

传统Agent：
• 被动响应
• 单步执行
• 需要明确指令

AutoGPT：
• 主动规划
• 多步执行
• 自主决策

【关键是"自主性"】

不是：
• 让AI做单个任务

而是：
• 让AI自己规划
• 自己执行
• 自己评估
• 自己改进
```

---

## 📚 第一部分：AutoGPT核心架构

### 一、基础组件实现

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import json

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    """任务"""
    task_id: str
    description: str
    status: TaskStatus
    priority: int
    result: Optional[str] = None
    reasoning: Optional[str] = None

@dataclass
class Goal:
    """目标"""
    goal_id: str
    description: str
    success_criteria: List[str]
    tasks: List[Task] = field(default_factory=list)

class Planner:
    """规划器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def create_plan(self, goal: str) -> List[Task]:
        """
        根据目标创建执行计划
        
        策略：
        1. 分解目标为子任务
        2. 确定任务依赖
        3. 分配优先级
        """
        
        prompt = f"""
Given the following goal, break it down into a series of specific, actionable tasks.

Goal: {goal}

Create a step-by-step plan. For each task, provide:
1. A clear description
2. Priority (1-10, higher is more important)
3. Dependencies (which tasks must be completed first)

Format as JSON array:
[
    {{
        "task_id": "1",
        "description": "...",
        "priority": 8,
        "dependencies": []
    }},
    ...
]
"""
        
        response = self.llm.invoke(prompt)
        
        # 解析任务列表
        try:
            tasks_data = json.loads(response.content)
            
            tasks = []
            for task_data in tasks_data:
                task = Task(
                    task_id=task_data["task_id"],
                    description=task_data["description"],
                    status=TaskStatus.PENDING,
                    priority=task_data["priority"]
                )
                tasks.append(task)
            
            return tasks
            
        except:
            # 解析失败，返回空列表
            return []
    
    def replan(
        self,
        original_goal: str,
        completed_tasks: List[Task],
        current_situation: str
    ) -> List[Task]:
        """
        根据当前情况重新规划
        
        当发现计划不合适时调用
        """
        
        completed_str = "\n".join([
            f"- {task.description}: {task.result}"
            for task in completed_tasks
        ])
        
        prompt = f"""
Original Goal: {original_goal}

Completed Tasks:
{completed_str}

Current Situation: {current_situation}

Based on the progress so far, create a new plan for the remaining work.
What tasks should be done next to achieve the goal?

Format as JSON array (same format as before).
"""
        
        response = self.llm.invoke(prompt)
        
        # 解析新任务列表
        # （实现同create_plan）
        
        return []

class Executor:
    """执行器"""
    
    def __init__(self, llm, tools: Dict):
        self.llm = llm
        self.tools = tools
    
    def execute_task(self, task: Task, context: Dict) -> str:
        """
        执行单个任务
        
        Args:
            task: 要执行的任务
            context: 上下文信息（之前任务的结果等）
        
        Returns:
            执行结果
        """
        
        # 构建执行Prompt
        prompt = self._build_execution_prompt(task, context)
        
        # 调用LLM决定如何执行
        response = self.llm.invoke(
            prompt,
            tools=[tool.to_dict() for tool in self.tools.values()]
        )
        
        # 处理工具调用
        if hasattr(response, 'tool_calls') and response.tool_calls:
            # 执行工具
            results = []
            for tool_call in response.tool_calls:
                result = self._execute_tool(tool_call)
                results.append(result)
            
            # 总结结果
            summary = self._summarize_results(task, results)
            return summary
        else:
            # 直接返回LLM的回答
            return response.content
    
    def _build_execution_prompt(self, task: Task, context: Dict) -> str:
        """构建执行Prompt"""
        
        context_str = json.dumps(context, ensure_ascii=False, indent=2)
        
        prompt = f"""
Task: {task.description}

Context from previous tasks:
{context_str}

Execute this task. You can use available tools or provide direct answer.
Be specific and thorough.
"""
        
        return prompt
    
    def _execute_tool(self, tool_call) -> str:
        """执行工具"""
        
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        tool = self.tools.get(tool_name)
        if not tool:
            return f"Error: Tool {tool_name} not found"
        
        try:
            result = tool.run(**arguments)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _summarize_results(self, task: Task, results: List[str]) -> str:
        """总结执行结果"""
        
        results_str = "\n".join(results)
        
        prompt = f"""
Task: {task.description}

Execution results:
{results_str}

Provide a concise summary of what was accomplished.
"""
        
        response = self.llm.invoke(prompt)
        return response.content

class Critic:
    """评估器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def evaluate_progress(
        self,
        goal: str,
        completed_tasks: List[Task],
        remaining_tasks: List[Task]
    ) -> Dict:
        """
        评估进展
        
        Returns:
            {
                'progress_percentage': 0-100,
                'is_on_track': bool,
                'suggestions': List[str],
                'should_replan': bool
            }
        """
        
        completed_str = "\n".join([
            f"- {task.description}: {task.result}"
            for task in completed_tasks
        ])
        
        remaining_str = "\n".join([
            f"- {task.description}"
            for task in remaining_tasks
        ])
        
        prompt = f"""
Goal: {goal}

Completed Tasks:
{completed_str}

Remaining Tasks:
{remaining_str}

Evaluate the progress:
1. What percentage of the goal has been achieved? (0-100)
2. Are we on track to achieve the goal?
3. Should we adjust the plan?
4. Any suggestions for improvement?

Respond in JSON:
{{
    "progress_percentage": 60,
    "is_on_track": true,
    "should_replan": false,
    "suggestions": ["suggestion 1", "suggestion 2"]
}}
"""
        
        response = self.llm.invoke(prompt)
        
        try:
            evaluation = json.loads(response.content)
            return evaluation
        except:
            return {
                'progress_percentage': 50,
                'is_on_track': True,
                'should_replan': False,
                'suggestions': []
            }

class MiniAutoGPT:
    """Mini AutoGPT实现"""
    
    def __init__(self, llm, tools: Dict, max_iterations: int = 20):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations
        
        # 核心组件
        self.planner = Planner(llm)
        self.executor = Executor(llm, tools)
        self.critic = Critic(llm)
        
        # 记忆
        self.completed_tasks: List[Task] = []
        self.context: Dict = {}
    
    def run(self, goal: str, verbose: bool = True):
        """
        执行目标
        
        主循环：
        1. 规划
        2. 执行
        3. 评估
        4. 决定是否继续
        """
        
        if verbose:
            print("\n" + "="*60)
            print(f"🎯 目标: {goal}")
            print("="*60)
        
        # 初始规划
        tasks = self.planner.create_plan(goal)
        
        if verbose:
            print(f"\n📋 初始计划：{len(tasks)}个任务")
            for task in tasks:
                print(f"  {task.task_id}. {task.description}")
        
        # 主循环
        for iteration in range(self.max_iterations):
            if verbose:
                print(f"\n--- 迭代 {iteration + 1} ---")
            
            # 检查是否还有任务
            pending_tasks = [t for t in tasks if t.status == TaskStatus.PENDING]
            
            if not pending_tasks:
                if verbose:
                    print("✅ 所有任务完成！")
                break
            
            # 选择下一个任务（优先级最高的）
            next_task = max(pending_tasks, key=lambda t: t.priority)
            
            if verbose:
                print(f"\n🔨 执行任务: {next_task.description}")
            
            # 执行任务
            next_task.status = TaskStatus.IN_PROGRESS
            
            try:
                result = self.executor.execute_task(next_task, self.context)
                next_task.result = result
                next_task.status = TaskStatus.COMPLETED
                
                # 更新上下文
                self.context[next_task.task_id] = result
                self.completed_tasks.append(next_task)
                
                if verbose:
                    print(f"  ✅ 完成: {result[:100]}...")
                
            except Exception as e:
                next_task.status = TaskStatus.FAILED
                if verbose:
                    print(f"  ❌ 失败: {str(e)}")
            
            # 评估进展
            remaining = [t for t in tasks if t.status == TaskStatus.PENDING]
            evaluation = self.critic.evaluate_progress(
                goal,
                self.completed_tasks,
                remaining
            )
            
            if verbose:
                print(f"\n📊 进展: {evaluation['progress_percentage']}%")
                if evaluation.get('suggestions'):
                    print("💡 建议:")
                    for suggestion in evaluation['suggestions']:
                        print(f"  • {suggestion}")
            
            # 是否需要重新规划
            if evaluation.get('should_replan', False):
                if verbose:
                    print("\n🔄 重新规划...")
                
                new_tasks = self.planner.replan(
                    goal,
                    self.completed_tasks,
                    f"Progress: {evaluation['progress_percentage']}%"
                )
                
                # 添加新任务
                for new_task in new_tasks:
                    if new_task.task_id not in [t.task_id for t in tasks]:
                        tasks.append(new_task)
        
        # 最终总结
        if verbose:
            print("\n" + "="*60)
            print("🎉 任务完成")
            print("="*60)
            print(f"\n完成的任务：{len(self.completed_tasks)}")
            for task in self.completed_tasks:
                print(f"  ✅ {task.description}")
        
        return self.completed_tasks

# 演示（需要真实LLM）
def demo_mini_autogpt():
    """演示Mini AutoGPT"""
    
    print("="*60)
    print("Mini AutoGPT演示")
    print("="*60)
    print("\n注意：需要真实的LLM才能运行")
    print("这里只展示架构和流程")
    
    # 模拟工具
    tools = {
        "search": type('SearchTool', (), {
            'run': lambda query: f"搜索结果：{query}相关信息...",
            'to_dict': lambda: {}
        })(),
    }
    
    # 创建AutoGPT（需要真实LLM）
    # autogpt = MiniAutoGPT(llm, tools)
    # autogpt.run("研究Python异步编程并写一篇教程")

demo_mini_autogpt()
```

---

## 💻 第二部分：长期记忆系统

### 一、向量记忆实现

```python
class VectorMemory:
    """向量记忆系统"""
    
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.memories: List[Dict] = []
        self.embeddings: List = []
    
    def add_memory(self, content: str, metadata: Dict = None):
        """添加记忆"""
        
        # 生成embedding
        embedding = self.embedding_model.embed(content)
        
        memory = {
            'content': content,
            'metadata': metadata or {},
            'timestamp': time.time()
        }
        
        self.memories.append(memory)
        self.embeddings.append(embedding)
    
    def search_memory(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """搜索相关记忆"""
        
        # 查询embedding
        query_embedding = self.embedding_model.embed(query)
        
        # 计算相似度
        similarities = []
        for i, emb in enumerate(self.embeddings):
            sim = self._cosine_similarity(query_embedding, emb)
            similarities.append((sim, i))
        
        # 排序并返回top_k
        similarities.sort(reverse=True)
        
        results = []
        for sim, idx in similarities[:top_k]:
            memory = self.memories[idx].copy()
            memory['similarity'] = sim
            results.append(memory)
        
        return results
    
    def _cosine_similarity(self, vec1, vec2):
        """计算余弦相似度"""
        import numpy as np
        return np.dot(vec1, vec2) / (
            np.linalg.norm(vec1) * np.linalg.norm(vec2)
        )
```

---

## 📝 课后练习

### 练习1：实现完整的记忆系统
使用向量数据库实现长期记忆

### 练习2：添加反思机制
让Agent能够从失败中学习

### 练习3：实现目标树
支持复杂的嵌套目标

---

## 🎓 知识总结

### 核心要点

1. **AutoGPT架构**
   - Planner规划器
   - Executor执行器
   - Critic评估器
   - Memory记忆系统

2. **自主性**
   - 目标分解
   - 自主规划
   - 持续执行
   - 自我评估

3. **长期记忆**
   - 向量存储
   - 相关检索
   - 经验积累

4. **关键挑战**
   - 成本控制
   - 循环检测
   - 质量保证

---

## 🚀 下节预告

下一课：**第89课：BabyAGI架构与实现**

- BabyAGI原理
- 任务管理
- 优先级队列
- 实现对比

**探索另一个自主Agent！** 🍼

---

**💪 记住：AutoGPT代表了Agent的未来方向！**

**下一课见！** 🎉
