![Agent架构设计](./images/agent.svg)
*图：Agent架构设计*

# 第74课：Agent架构模式对比

> **本课目标**：掌握多种Agent架构模式，根据场景选择最优方案
> 
> **核心技能**：ReAct、Plan-and-Execute、ReWOO、Reflexion
> 
> **实战案例**：不同架构模式的对比实战
> 
> **学习时长**：80分钟

---

## 📖 口播文案（5分钟）
![Action](./images/action.svg)
*图：Action*


### 🎯 前言

"前面三节课我们学习了Agent的基础和ReAct框架。

今天我们要学习：**Agent的各种架构模式！**

**为什么要学习不同的架构？**

就像盖房子，有平房、楼房、别墅，不同的需求要用不同的设计！

**Agent也一样！**

不同的任务场景，需要不同的Agent架构！

**先看几个场景，感受差异：**

**场景1：简单查询**
```
任务：查询北京明天的天气

最佳架构：ReAct（简单快速）
执行步骤：
1. Thought: 需要查天气
2. Action: 调用天气API
3. Answer: 明天北京晴，20-28℃

✅ 1次调用，2秒完成
```

**场景2：复杂规划**
```
任务：帮我规划一个7天日本旅游行程，
     包括机票、酒店、景点、餐厅推荐

ReAct方式（不好）：
边想边做，可能反复调整
预计：15-20次工具调用，1分钟

Plan-and-Execute方式（更好）：
1. 先完整规划：
   Day1: 机票+酒店+浅草寺
   Day2: 富士山+温泉
   ...
2. 再依次执行

✅ 更有条理，10次调用，30秒
```

**场景3：需要反思的任务**
```
任务：写一篇关于AI的文章，
     要求专业、准确、有深度

ReAct方式（不够）：
写完就结束

Reflexion方式（更好）：
1. 生成初稿
2. 自我评估：
   - 是否专业？
   - 是否准确？
   - 是否有深度？
3. 发现问题：缺少案例
4. 改进：补充案例
5. 再次评估
6. 完成

✅ 质量更高！
```

**今天我们要学习四大主流架构：**

**1. ReAct（推理-行动）**
```
特点：
• 边想边做
• 灵活应变
• 适合简单-中等任务

优势：
✅ 实现简单
✅ 容错性好
✅ 适应性强

劣势：
❌ 可能走弯路
❌ 调用次数多
❌ 不够系统

适用场景：
• 简单查询
• 信息检索
• 单步骤任务
```

**2. Plan-and-Execute（先计划-后执行）**
```
特点：
• 先完整规划
• 再依次执行
• 适合复杂任务

优势：
✅ 有条不紊
✅ 避免重复
✅ 效率更高

劣势：
❌ 计划可能不完美
❌ 不够灵活
❌ 实现复杂

适用场景：
• 多步骤任务
• 需要规划的任务
• 资源受限场景
```

**3. ReWOO（推理无观察）**
```
特点：
• 一次性规划所有步骤
• 并行执行
• 最后汇总

优势：
✅ 可以并行
✅ 速度快
✅ 成本低

劣势：
❌ 无法根据中间结果调整
❌ 容错性差
❌ 适用范围窄

适用场景：
• 独立的多任务
• 可并行的任务
• 对速度要求高
```

**4. Reflexion（反思）**
```
特点：
• 生成 → 评估 → 改进
• 持续迭代
• 追求质量

优势：
✅ 质量更高
✅ 可以自我改进
✅ 适合创作任务

劣势：
❌ 时间长
❌ 成本高
❌ 可能过度优化

适用场景：
• 内容创作
• 代码生成
• 需要高质量输出
```

**架构选择决策树：**

```
任务分析
    ↓
简单查询？
    ↙Yes → ReAct（快速简单）
    ↘No
需要复杂规划？
    ↙Yes → Plan-and-Execute（有条理）
    ↘No
可以并行执行？
    ↙Yes → ReWOO（速度快）
    ↘No
需要高质量输出？
    ↙Yes → Reflexion（质量高）
    ↘No → ReAct（默认选择）
```

**真实案例对比：**

**任务：帮我写一个Python爬虫，爬取豆瓣电影Top250**

**ReAct方式：**
```
1. 生成代码
2. 完成
耗时：30秒
质量：基础可用，可能有bug
```

**Reflexion方式：**
```
1. 生成初始代码
2. 自我评估：
   - 有没有错误处理？❌
   - 有没有反爬虫机制？❌
   - 代码规范吗？一般
3. 改进版本1：
   - 添加异常处理
   - 添加延迟
4. 再次评估：
   - 数据存储方式？可以优化
5. 最终版本：
   - 完善的错误处理
   - 反爬虫策略
   - 数据持久化
   - 日志记录

耗时：2分钟
质量：生产可用，健壮性强
```

**今天这一课，我要带你：**

**第一部分：四大架构详解**
- ReAct架构
- Plan-and-Execute架构
- ReWOO架构
- Reflexion架构

**第二部分：架构对比**
- 性能对比
- 成本对比
- 适用场景

**第三部分：架构实现**
- Plan-and-Execute实现
- Reflexion实现

**第四部分：架构选择**
- 决策树
- 最佳实践

**第五部分：实战案例**
- 不同架构实战
- 效果对比

学完这一课，你将能根据场景选择最优架构！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【没有最好的架构，只有最合适的】

简单任务 → ReAct
复杂规划 → Plan-and-Execute
并行任务 → ReWOO
高质量 → Reflexion

【权衡三角】

        速度
       /    \
      /      \
    成本 ---- 质量
    
不同架构在三者间权衡！
```

---

## 📚 第一部分：四大架构详解

### 一、ReAct架构（已学习）

```python
"""
ReAct架构回顾

核心流程：
Thought → Action → Observation → Thought → ...

特点：
• 边想边做
• 灵活应变
• 实时调整

优势：
• 实现简单
• 容错性好
• 适应性强

劣势：
• 可能走弯路
• 调用次数多

适用场景：
• 简单-中等复杂度任务
• 需要灵活应变的场景
"""
```

### 二、Plan-and-Execute架构

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ExecutionStep:
    """执行步骤"""
    step_id: int
    description: str
    tool_name: str
    tool_input: str
    status: str = "pending"  # pending, completed, failed
    result: str = None

class PlanAndExecuteAgent:
    """Plan-and-Execute Agent"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
    
    def run(self, task: str, verbose: bool = True) -> str:
        """
        运行Plan-and-Execute流程
        
        两阶段：
        1. Planning阶段：生成完整执行计划
        2. Execution阶段：依次执行计划
        """
        if verbose:
            print("\n" + "🎯"*30)
            print("Plan-and-Execute Agent")
            print("🎯"*30)
            print(f"\n任务: {task}\n")
        
        # ===== 阶段1：Planning =====
        if verbose:
            print("="*60)
            print("【阶段1】规划 (Planning)")
            print("="*60)
        
        plan = self._generate_plan(task, verbose)
        
        # ===== 阶段2：Execution =====
        if verbose:
            print("\n" + "="*60)
            print("【阶段2】执行 (Execution)")
            print("="*60)
        
        results = self._execute_plan(plan, verbose)
        
        # ===== 生成最终答案 =====
        final_answer = self._generate_final_answer(task, results, verbose)
        
        if verbose:
            print("\n" + "="*60)
            print(f"✅ 最终答案: {final_answer}")
            print("="*60)
        
        return final_answer
    
    def _generate_plan(self, task: str, verbose: bool) -> List[ExecutionStep]:
        """生成执行计划"""
        
        tools_desc = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        
        prompt = f"""你是一个规划专家。请为以下任务制定详细的执行计划。

任务：{task}

可用工具：
{tools_desc}

要求：
1. 将任务分解为具体步骤
2. 每个步骤指定使用的工具
3. 步骤之间要有逻辑顺序
4. 尽量减少步骤数

以JSON格式返回计划：
[
    {{
        "step_id": 1,
        "description": "步骤描述",
        "tool_name": "工具名称",
        "tool_input": "工具输入"
    }},
    ...
]

JSON："""
        
        response = self.llm.invoke(prompt)
        
        import json
        try:
            plan_data = json.loads(response.content)
        except:
            plan_data = [{
                "step_id": 1,
                "description": task,
                "tool_name": list(self.tools.keys())[0],
                "tool_input": task
            }]
        
        # 创建ExecutionStep对象
        plan = [
            ExecutionStep(**step_data)
            for step_data in plan_data
        ]
        
        if verbose:
            print(f"\n生成执行计划（共{len(plan)}步）：\n")
            for step in plan:
                print(f"  步骤{step.step_id}: {step.description}")
                print(f"    工具: {step.tool_name}({step.tool_input})")
        
        return plan
    
    def _execute_plan(self, plan: List[ExecutionStep], verbose: bool) -> List[ExecutionStep]:
        """执行计划"""
        
        for step in plan:
            if verbose:
                print(f"\n执行步骤{step.step_id}: {step.description}")
            
            # 执行工具
            tool = self.tools.get(step.tool_name)
            
            if not tool:
                step.status = "failed"
                step.result = f"工具{step.tool_name}不存在"
                if verbose:
                    print(f"  ❌ 失败: {step.result}")
                continue
            
            try:
                result = tool.run(step.tool_input)
                step.status = "completed"
                step.result = str(result)
                
                if verbose:
                    print(f"  ✅ 成功: {step.result}")
            except Exception as e:
                step.status = "failed"
                step.result = str(e)
                
                if verbose:
                    print(f"  ❌ 失败: {step.result}")
        
        return plan
    
    def _generate_final_answer(
        self,
        task: str,
        results: List[ExecutionStep],
        verbose: bool
    ) -> str:
        """生成最终答案"""
        
        # 汇总执行结果
        results_summary = "\n".join([
            f"步骤{step.step_id}: {step.description}\n结果: {step.result}"
            for step in results
        ])
        
        prompt = f"""任务：{task}

执行结果：
{results_summary}

请基于执行结果，给出完整的最终答案。

答案："""
        
        response = self.llm.invoke(prompt)
        return response.content

# 演示
def demo_plan_and_execute():
    """演示Plan-and-Execute"""
    
    from langchain.chat_models import ChatOpenAI
    
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
    
    tools = [
        SimpleTool(
            "calculate",
            lambda x: eval(x),
            "计算数学表达式"
        ),
        SimpleTool(
            "search",
            lambda x: f"搜索结果for {x}",
            "搜索信息"
        )
    ]
    
    # 创建Agent
    agent = PlanAndExecuteAgent(llm, tools)
    
    # 测试
    task = "计算(23 + 47) * 3，然后搜索这个数字的含义"
    answer = agent.run(task, verbose=True)

# demo_plan_and_execute()
```

### 三、Reflexion架构（反思）

```python
class ReflexionAgent:
    """Reflexion Agent - 带反思的Agent"""
    
    def __init__(self, llm, max_iterations: int = 3):
        self.llm = llm
        self.max_iterations = max_iterations
    
    def run(self, task: str, verbose: bool = True) -> str:
        """
        运行Reflexion流程
        
        循环：
        1. Generate（生成）
        2. Evaluate（评估）
        3. Reflect（反思）
        4. Improve（改进）
        """
        if verbose:
            print("\n" + "🔄"*30)
            print("Reflexion Agent")
            print("🔄"*30)
            print(f"\n任务: {task}\n")
        
        current_output = None
        reflections = []
        
        for iteration in range(self.max_iterations):
            if verbose:
                print("="*60)
                print(f"迭代 {iteration + 1}/{self.max_iterations}")
                print("="*60)
            
            # 1. Generate
            if verbose:
                print("\n【步骤1】生成")
            
            current_output = self._generate(
                task,
                current_output,
                reflections,
                verbose
            )
            
            # 2. Evaluate
            if verbose:
                print("\n【步骤2】评估")
            
            evaluation = self._evaluate(task, current_output, verbose)
            
            # 3. 如果评估通过，结束
            if evaluation['passed']:
                if verbose:
                    print(f"\n✅ 评估通过！质量分数: {evaluation['score']}")
                break
            
            # 4. Reflect
            if verbose:
                print("\n【步骤3】反思")
            
            reflection = self._reflect(
                task,
                current_output,
                evaluation,
                verbose
            )
            reflections.append(reflection)
        
        if verbose:
            print("\n" + "="*60)
            print(f"最终输出:")
            print(current_output)
            print("="*60)
        
        return current_output
    
    def _generate(
        self,
        task: str,
        previous_output: str,
        reflections: List[str],
        verbose: bool
    ) -> str:
        """生成输出"""
        
        if previous_output is None:
            # 首次生成
            prompt = f"任务：{task}\n\n请完成任务："
        else:
            # 改进版本
            reflections_text = "\n".join([
                f"{i+1}. {ref}"
                for i, ref in enumerate(reflections)
            ])
            
            prompt = f"""任务：{task}

之前的版本：
{previous_output}

发现的问题：
{reflections_text}

请生成改进版本："""
        
        response = self.llm.invoke(prompt)
        output = response.content
        
        if verbose:
            print(f"  生成的输出（前200字）:\n  {output[:200]}...")
        
        return output
    
    def _evaluate(
        self,
        task: str,
        output: str,
        verbose: bool
    ) -> Dict:
        """评估输出质量"""
        
        prompt = f"""请评估以下输出的质量。

任务：{task}

输出：
{output}

评估标准：
1. 是否完成任务？
2. 质量如何？
3. 有什么问题？

以JSON格式返回：
{{
    "score": 0-10的分数,
    "passed": true/false (分数>=8才通过),
    "issues": ["问题1", "问题2", ...]
}}

JSON："""
        
        response = self.llm.invoke(prompt)
        
        import json
        try:
            evaluation = json.loads(response.content)
        except:
            evaluation = {
                "score": 5,
                "passed": False,
                "issues": ["解析失败"]
            }
        
        if verbose:
            print(f"  分数: {evaluation['score']}/10")
            print(f"  通过: {'是' if evaluation['passed'] else '否'}")
            if evaluation['issues']:
                print(f"  问题:")
                for issue in evaluation['issues']:
                    print(f"    - {issue}")
        
        return evaluation
    
    def _reflect(
        self,
        task: str,
        output: str,
        evaluation: Dict,
        verbose: bool
    ) -> str:
        """反思并给出改进建议"""
        
        issues_text = "\n".join(evaluation['issues'])
        
        prompt = f"""任务：{task}

当前输出：
{output}

发现的问题：
{issues_text}

请分析原因并给出具体的改进建议："""
        
        response = self.llm.invoke(prompt)
        reflection = response.content
        
        if verbose:
            print(f"  改进建议:\n  {reflection}")
        
        return reflection

# 演示
def demo_reflexion():
    """演示Reflexion"""
    
    from langchain.chat_models import ChatOpenAI
    
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0.7
    )
    
    agent = ReflexionAgent(llm, max_iterations=3)
    
    task = "写一个Python函数，实现快速排序算法，要求有完善的注释和错误处理"
    
    result = agent.run(task, verbose=True)

# demo_reflexion()
```

---

## 💻 第二部分：架构对比分析

### 架构对比表

```python
class ArchitectureComparison:
    """架构对比分析"""
    
    @staticmethod
    def print_comparison():
        """打印对比表"""
        
        print("\n" + "="*80)
        print("Agent架构对比")
        print("="*80 + "\n")
        
        comparison = {
            '指标': ['ReAct', 'Plan-Execute', 'ReWOO', 'Reflexion'],
            '实现复杂度': ['⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐'],
            '执行速度': ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐'],
            '灵活性': ['⭐⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐⭐⭐'],
            '容错能力': ['⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐⭐⭐⭐⭐'],
            '输出质量': ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐⭐'],
            '调用成本': ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐'],
            '适用复杂度': ['简单-中等', '中等-复杂', '简单', '任意']
        }
        
        # 打印表格
        header = f"{'指标':<15} {'ReAct':<15} {'Plan-Execute':<15} {'ReWOO':<15} {'Reflexion':<15}"
        print(header)
        print("-" * 80)
        
        for metric in list(comparison.keys())[1:]:
            row = f"{metric:<15} {comparison['ReAct'][list(comparison.keys()).index(metric)-1]:<15} {comparison['Plan-Execute'][list(comparison.keys()).index(metric)-1]:<15} {comparison['ReWOO'][list(comparison.keys()).index(metric)-1]:<15} {comparison['Reflexion'][list(comparison.keys()).index(metric)-1]:<15}"
            print(row)
        
        print("\n" + "="*80)
        print("选择建议")
        print("="*80)
        print("""
        简单查询、单步任务 → ReAct
        复杂规划、多步任务 → Plan-and-Execute
        并行任务、速度优先 → ReWOO
        高质量输出、内容创作 → Reflexion
        """)

ArchitectureComparison.print_comparison()
```

---

## 📝 课后练习

### 练习1：实现ReWOO
实现并行执行的ReWOO架构

### 练习2：混合架构
结合多种架构的优势

### 练习3：架构选择器
实现自动选择最优架构的系统

---

## 🎓 知识总结

### 核心要点

1. **四大架构**
   - ReAct：灵活应变
   - Plan-and-Execute：先计划后执行
   - ReWOO：并行执行
   - Reflexion：反思改进

2. **选择原则**
   - 简单任务 → ReAct
   - 复杂规划 → Plan-and-Execute
   - 并行任务 → ReWOO
   - 高质量 → Reflexion

3. **权衡考虑**
   - 速度 vs 质量
   - 成本 vs 效果
   - 简单 vs 功能

---

## 🚀 下节预告

下一课：**第75课：实战-第一个完整的Agent应用**

- 完整Agent实现
- 工具集成
- 错误处理
- 实战部署

**构建完整的生产级Agent！** 🎯

---

**💪 记住：根据场景选择最优架构！**

**下一课见！** 🎉
