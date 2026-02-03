![Agent进阶架构](./images/agent.svg)
*图：Agent进阶架构*

# 第89课：BabyAGI架构与实现

> **本课目标**：深入理解BabyAGI的架构和实现，掌握任务驱动型自主Agent
> 
> **核心技能**：任务管理、优先级队列、向量记忆、迭代执行
> 
> **实战案例**：实现Mini-BabyAGI
> 
> **学习时长**：90分钟

---

## 📖 口播文案（6分钟）
![Agent Debug](./images/agent_debug.svg)
*图：Agent Debug*


### 🎯 前言

"上节课我们学习了AutoGPT的原理。

今天我们要学习另一个革命性项目：**BabyAGI！**

**BabyAGI是什么？**

如果说AutoGPT是复杂而强大的系统，
那BabyAGI就是：**简洁而优雅的自主Agent！**

**AutoGPT vs BabyAGI对比：**

**AutoGPT：**
```
架构：复杂
组件：多个（Planner、Executor、Critic、Memory）
代码量：大（数千行）
特点：功能全面，但较重

适合：复杂场景
```

**BabyAGI：**
```
架构：简洁
核心：任务循环
代码量：小（最初只有140行！）
特点：简单优雅，核心清晰

适合：快速原型、学习理解
```

**BabyAGI的核心理念：**

**理念1：任务驱动（Task-Driven）**
```
不是：
• 制定完整计划
• 一次性规划所有步骤

而是：
• 专注当前任务
• 完成后生成新任务
• 持续迭代前进

就像：
走一步，看一步
根据情况调整
```

**理念2：优先级队列（Priority Queue）**
```
所有任务排队：
1. 高优先级任务
2. 中优先级任务
3. 低优先级任务

永远执行最重要的任务！

就像：
待办清单，重要的先做
```

**理念3：向量记忆（Vector Memory）**
```
每个任务的结果：
• 转为向量
• 存储起来
• 后续可搜索

就像：
大脑的长期记忆
可以随时调取
```

**BabyAGI的工作流程：**

```
【初始状态】
目标："研究Python异步编程并写教程"

任务队列：
1. [优先级10] 开始研究Python异步编程

【第1轮迭代】

Step 1: 取出最高优先级任务
任务："开始研究Python异步编程"

Step 2: 执行任务
• 搜索相关资料
• 阅读文档
结果："asyncio是Python的异步框架..."

Step 3: 保存到向量记忆
Embedding(结果) → 向量数据库

Step 4: 生成新任务
基于结果，创建新任务：
• [优先级9] 深入学习asyncio模块
• [优先级8] 研究async/await语法
• [优先级7] 了解事件循环原理

Step 5: 添加到任务队列
队列更新：
1. [10] 开始研究... (完成)
2. [9] 深入学习asyncio
3. [8] 研究async/await
4. [7] 了解事件循环

【第2轮迭代】

Step 1: 取出任务
任务："深入学习asyncio模块"

Step 2: 执行（同上）

Step 3-5: 继续循环...

【持续迭代直到目标达成】
```

**BabyAGI vs AutoGPT的关键区别：**

```
【规划方式】
AutoGPT: 一次规划多个任务
BabyAGI: 动态生成任务

【任务管理】
AutoGPT: 任务列表 + 依赖关系
BabyAGI: 优先级队列

【记忆系统】
AutoGPT: 多种记忆机制
BabyAGI: 专注向量记忆

【复杂度】
AutoGPT: 较复杂
BabyAGI: 极简

【适用场景】
AutoGPT: 复杂的多步骤项目
BabyAGI: 研究型、创造型任务
```

**BabyAGI的核心优势：**

**优势1：极简设计**
```
最初版本只有140行代码！

核心循环：
while True:
    # 1. 取任务
    task = task_queue.pop(0)
    
    # 2. 执行
    result = execute(task)
    
    # 3. 记忆
    memory.add(result)
    
    # 4. 生成新任务
    new_tasks = create_tasks(result, objective)
    
    # 5. 添加到队列
    task_queue.extend(new_tasks)

简单到极致！
```

**优势2：灵活性强**
```
因为简单：
• 容易理解
• 容易修改
• 容易扩展

可以快速：
• 添加新功能
• 调整策略
• 实验不同方法
```

**优势3：专注核心**
```
不做花哨的功能
只做最核心的事：
• 任务管理
• 任务执行
• 任务生成

把核心做到极致！
```

**BabyAGI的实战案例：**

**案例1：研究任务**
```
目标："研究区块链技术的最新发展"

BabyAGI执行：

迭代1: "了解区块链基础概念"
→ 生成任务：
  • 研究共识机制
  • 学习智能合约
  • 了解DeFi

迭代2: "研究共识机制"
→ 生成任务：
  • PoW vs PoS对比
  • 新型共识算法
  • 性能分析

迭代3-N: 持续深入...

最终：
完整的区块链技术研究报告
包含最新发展趋势
```

**案例2：创作任务**
```
目标："创作一个科幻短篇小说"

BabyAGI执行：

迭代1: "构思故事背景"
→ 未来世界、AI觉醒

迭代2: "设计主要角色"
→ 人类科学家、AI系统

迭代3: "规划故事情节"
→ 发现、冲突、高潮、结局

迭代4-N: 具体写作...

最终：
完整的科幻短篇小说
结构完整、情节连贯
```

**BabyAGI的改进空间：**

**改进1：更智能的任务生成**
```
当前：
基于上一个任务结果生成

改进：
• 考虑全局目标
• 分析已完成任务
• 识别知识缺口
• 生成更精准的任务
```

**改进2：更好的任务排序**
```
当前：
简单的优先级数字

改进：
• 重要性评分
• 依赖关系分析
• 动态调整优先级
• 避免阻塞
```

**改进3：更强的记忆检索**
```
当前：
简单的向量搜索

改进：
• 多维度检索
• 时间衰减
• 重要性加权
• 知识图谱
```

**今天这一课，我要带你：**

**第一部分：BabyAGI架构**
- 核心组件
- 工作流程
- 设计哲学

**第二部分：任务管理系统**
- 优先级队列
- 任务生成
- 任务执行

**第三部分：向量记忆系统**
- Embedding存储
- 相似度搜索
- 上下文检索

**第四部分：完整实现**
- Mini-BabyAGI
- 实际应用
- 优化改进

**第五部分：对比分析**
- BabyAGI vs AutoGPT
- 适用场景
- 最佳实践

学完这一课，你将完全理解自主Agent！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【BabyAGI = 极简的自主Agent】

不追求：
• 功能全面
• 架构复杂

追求：
• 核心清晰
• 简洁优雅
• 易于理解

【少即是多（Less is More）】

通过极简设计：
• 抓住核心本质
• 避免过度设计
• 保持灵活性
```

---

## 📚 第一部分：BabyAGI核心架构

### 一、完整的BabyAGI实现

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import heapq
from collections import deque
import time

@dataclass
class Task:
    """任务"""
    task_id: int
    task_name: str
    priority: int
    
    def __lt__(self, other):
        # 用于优先队列排序（优先级高的先执行）
        return self.priority > other.priority

class TaskQueue:
    """任务队列（优先级队列）"""
    
    def __init__(self):
        self.queue = []
        self.next_task_id = 1
    
    def add_task(self, task_name: str, priority: int) -> Task:
        """添加任务"""
        task = Task(
            task_id=self.next_task_id,
            task_name=task_name,
            priority=priority
        )
        
        heapq.heappush(self.queue, task)
        self.next_task_id += 1
        
        return task
    
    def get_next_task(self) -> Optional[Task]:
        """获取下一个任务"""
        if self.queue:
            return heapq.heappop(self.queue)
        return None
    
    def is_empty(self) -> bool:
        """是否为空"""
        return len(self.queue) == 0
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务（用于显示）"""
        return sorted(self.queue, reverse=True)

class VectorMemory:
    """向量记忆系统（简化版）"""
    
    def __init__(self):
        self.memories: List[Dict] = []
    
    def add(self, task_name: str, result: str):
        """添加记忆"""
        memory = {
            'task': task_name,
            'result': result,
            'timestamp': time.time()
        }
        self.memories.append(memory)
    
    def get_relevant_context(
        self,
        query: str,
        top_k: int = 3
    ) -> str:
        """获取相关上下文（简化版）"""
        
        # 实际应用中这里应该用向量相似度搜索
        # 这里简化为返回最近的几条记忆
        
        recent_memories = self.memories[-top_k:]
        
        context_parts = []
        for memory in recent_memories:
            context_parts.append(
                f"Task: {memory['task']}\n"
                f"Result: {memory['result']}"
            )
        
        return "\n\n".join(context_parts)

class TaskExecutor:
    """任务执行器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def execute_task(
        self,
        task: Task,
        objective: str,
        context: str
    ) -> str:
        """执行任务"""
        
        prompt = f"""
You are an AI that performs tasks based on an objective.

Objective: {objective}

Previous context:
{context}

Current task: {task.task_name}

Complete this task and provide the result. Be specific and thorough.
"""
        
        response = self.llm.invoke(prompt)
        return response.content

class TaskCreator:
    """任务创建器"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def create_new_tasks(
        self,
        result: str,
        task_description: str,
        objective: str,
        existing_tasks: List[Task]
    ) -> List[Task]:
        """基于执行结果创建新任务"""
        
        existing_task_names = [t.task_name for t in existing_tasks]
        
        prompt = f"""
You are a task creation AI.

Objective: {objective}

Last completed task: {task_description}
Result: {result}

Existing tasks:
{chr(10).join(f"- {t}" for t in existing_task_names)}

Based on the result, create new tasks to achieve the objective.
Do not create duplicate tasks.

Return tasks as JSON array:
[
    {{"task": "task description", "priority": 8}},
    ...
]
"""
        
        response = self.llm.invoke(prompt)
        
        # 解析新任务
        try:
            import json
            new_tasks_data = json.loads(response.content)
            
            new_tasks = []
            for task_data in new_tasks_data:
                new_tasks.append({
                    'task_name': task_data['task'],
                    'priority': task_data.get('priority', 5)
                })
            
            return new_tasks
            
        except:
            return []

class BabyAGI:
    """BabyAGI实现"""
    
    def __init__(
        self,
        llm,
        max_iterations: int = 10,
        verbose: bool = True
    ):
        self.llm = llm
        self.max_iterations = max_iterations
        self.verbose = verbose
        
        # 核心组件
        self.task_queue = TaskQueue()
        self.memory = VectorMemory()
        self.executor = TaskExecutor(llm)
        self.creator = TaskCreator(llm)
    
    def run(self, objective: str, first_task: str = None):
        """
        运行BabyAGI
        
        Args:
            objective: 最终目标
            first_task: 第一个任务（可选）
        """
        
        if self.verbose:
            print("\n" + "="*60)
            print(f"🎯 目标: {objective}")
            print("="*60)
        
        # 添加初始任务
        if first_task is None:
            first_task = f"开始执行目标：{objective}"
        
        self.task_queue.add_task(first_task, priority=10)
        
        # 主循环
        iteration = 0
        
        while not self.task_queue.is_empty() and iteration < self.max_iterations:
            iteration += 1
            
            if self.verbose:
                print(f"\n{'─'*60}")
                print(f"迭代 {iteration}")
                print(f"{'─'*60}")
            
            # 1. 获取下一个任务
            task = self.task_queue.get_next_task()
            
            if self.verbose:
                print(f"\n📋 当前任务:")
                print(f"  ID: {task.task_id}")
                print(f"  名称: {task.task_name}")
                print(f"  优先级: {task.priority}")
            
            # 2. 获取相关上下文
            context = self.memory.get_relevant_context(task.task_name)
            
            # 3. 执行任务
            if self.verbose:
                print(f"\n🔨 执行任务...")
            
            result = self.executor.execute_task(task, objective, context)
            
            if self.verbose:
                print(f"\n✅ 任务结果:")
                print(f"  {result[:200]}...")
            
            # 4. 保存到记忆
            self.memory.add(task.task_name, result)
            
            # 5. 创建新任务
            if self.verbose:
                print(f"\n🆕 生成新任务...")
            
            new_tasks = self.creator.create_new_tasks(
                result=result,
                task_description=task.task_name,
                objective=objective,
                existing_tasks=self.task_queue.get_all_tasks()
            )
            
            # 6. 添加到队列
            for new_task in new_tasks:
                self.task_queue.add_task(
                    new_task['task_name'],
                    new_task['priority']
                )
            
            if self.verbose and new_tasks:
                print(f"  创建了{len(new_tasks)}个新任务")
                for nt in new_tasks:
                    print(f"    • [{nt['priority']}] {nt['task_name']}")
            
            # 显示当前队列
            if self.verbose:
                remaining = self.task_queue.get_all_tasks()
                if remaining:
                    print(f"\n📝 待办任务 ({len(remaining)}):")
                    for i, t in enumerate(remaining[:5], 1):
                        print(f"  {i}. [{t.priority}] {t.task_name}")
                    if len(remaining) > 5:
                        print(f"  ... 还有{len(remaining)-5}个任务")
        
        # 完成
        if self.verbose:
            print("\n" + "="*60)
            print("🎉 BabyAGI完成")
            print("="*60)
            print(f"\n执行了{iteration}次迭代")
            print(f"生成了{len(self.memory.memories)}条记忆")
        
        return self.memory.memories

# 演示（需要真实LLM）
def demo_baby_agi():
    """演示BabyAGI"""
    
    print("="*60)
    print("BabyAGI演示")
    print("="*60)
    print("\n注意：需要真实的LLM才能运行")
    print("这里展示架构和流程")
    
    # 使用时：
    # baby_agi = BabyAGI(llm, max_iterations=10)
    # baby_agi.run(
    #     objective="研究Python异步编程并写一篇教程",
    #     first_task="了解Python异步编程的基础概念"
    # )

demo_baby_agi()
```

---

## 💻 第二部分：优先级队列优化

### 一、智能优先级管理

```python
class SmartPriorityQueue:
    """智能优先级队列"""
    
    def __init__(self):
        self.queue = []
        self.task_history: Dict[str, int] = {}  # 任务执行次数
        self.next_task_id = 1
    
    def add_task(
        self,
        task_name: str,
        base_priority: int,
        task_type: str = "normal"
    ) -> Task:
        """
        添加任务（智能优先级）
        
        优先级计算：
        • 基础优先级
        • 任务类型加成
        • 历史执行次数惩罚（避免重复）
        """
        
        # 计算最终优先级
        priority = base_priority
        
        # 任务类型加成
        type_bonus = {
            'critical': 5,
            'important': 2,
            'normal': 0,
            'low': -2
        }
        priority += type_bonus.get(task_type, 0)
        
        # 重复任务惩罚
        exec_count = self.task_history.get(task_name, 0)
        priority -= exec_count * 2  # 每次重复降低2优先级
        
        # 创建任务
        task = Task(
            task_id=self.next_task_id,
            task_name=task_name,
            priority=priority
        )
        
        heapq.heappush(self.queue, task)
        self.next_task_id += 1
        
        return task
    
    def mark_completed(self, task: Task):
        """标记任务完成"""
        self.task_history[task.task_name] = \
            self.task_history.get(task.task_name, 0) + 1
    
    def rebalance_priorities(self):
        """重新平衡优先级"""
        
        # 提取所有任务
        all_tasks = []
        while self.queue:
            all_tasks.append(heapq.heappop(self.queue))
        
        # 重新计算优先级
        for task in all_tasks:
            # 长时间等待的任务提高优先级
            task.priority += 1
        
        # 重新入队
        for task in all_tasks:
            heapq.heappush(self.queue, task)
```

---

## 🎯 第三部分：BabyAGI vs AutoGPT

### 一、详细对比分析

```python
class ComparisonAnalysis:
    """BabyAGI vs AutoGPT对比"""
    
    @staticmethod
    def print_comparison():
        """打印对比表"""
        
        print("\n" + "="*80)
        print("BabyAGI vs AutoGPT 详细对比")
        print("="*80)
        
        comparisons = [
            {
                'aspect': '架构复杂度',
                'babyagi': '极简（~200行核心代码）',
                'autogpt': '复杂（数千行代码）',
                'winner': 'BabyAGI'
            },
            {
                'aspect': '规划能力',
                'babyagi': '动态生成（边做边规划）',
                'autogpt': '一次性规划（提前规划）',
                'winner': 'AutoGPT'
            },
            {
                'aspect': '任务管理',
                'babyagi': '优先级队列',
                'autogpt': '任务列表+依赖',
                'winner': '各有优势'
            },
            {
                'aspect': '记忆系统',
                'babyagi': '向量记忆（单一）',
                'autogpt': '多种记忆机制',
                'winner': 'AutoGPT'
            },
            {
                'aspect': '易于理解',
                'babyagi': '非常容易',
                'autogpt': '较复杂',
                'winner': 'BabyAGI'
            },
            {
                'aspect': '易于修改',
                'babyagi': '非常容易',
                'autogpt': '需要理解整体',
                'winner': 'BabyAGI'
            },
            {
                'aspect': '功能全面性',
                'babyagi': '核心功能',
                'autogpt': '功能丰富',
                'winner': 'AutoGPT'
            },
            {
                'aspect': '适用场景',
                'babyagi': '研究、创作、原型',
                'autogpt': '复杂项目、生产',
                'winner': '看场景'
            },
        ]
        
        print(f"\n{'方面':<15} {'BabyAGI':<25} {'AutoGPT':<25} {'推荐':<10}")
        print("-"*80)
        
        for comp in comparisons:
            print(f"{comp['aspect']:<15} {comp['babyagi']:<25} "
                  f"{comp['autogpt']:<25} {comp['winner']:<10}")
        
        print("\n" + "="*80)
        print("总结：")
        print("  BabyAGI: 简洁优雅，快速原型，易于学习")
        print("  AutoGPT: 功能强大，适合复杂任务")
        print("="*80)

# 演示
ComparisonAnalysis.print_comparison()
```

---

## 📝 课后练习

### 练习1：实现完整的向量记忆
使用Faiss或Chroma实现真正的向量搜索

### 练习2：添加任务依赖
实现任务之间的依赖关系管理

### 练习3：可视化Dashboard
创建BabyAGI的实时监控面板

---

## 🎓 知识总结

### 核心要点

1. **BabyAGI架构**
   - 任务队列
   - 向量记忆
   - 执行循环
   - 任务生成

2. **设计哲学**
   - 极简主义
   - 核心清晰
   - 易于理解

3. **vs AutoGPT**
   - 复杂度不同
   - 适用场景不同
   - 各有优势

4. **最佳实践**
   - 合理的迭代限制
   - 避免任务重复
   - 智能优先级管理

---

## 🚀 下节预告

下一课：**第90课：【项目】智能办公助手完整实现**

- 需求分析
- 架构设计
- 完整实现
- 部署上线

**第四模块收官之作！** 🎊

---

**💪 记住：BabyAGI用极简设计诠释了自主Agent的本质！**

**下一课见！** 🎉
