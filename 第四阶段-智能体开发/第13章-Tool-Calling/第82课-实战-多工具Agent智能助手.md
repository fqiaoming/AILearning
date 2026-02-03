![Tool Calling流程](./images/tool_calling.svg)
*图：Tool Calling流程*

# 第82课：实战-多工具Agent智能助手

> **本课目标**：整合所有工具，构建完整的多功能Agent智能助手
> 
> **核心技能**：工具集成、任务规划、智能决策、错误恢复
> 
> **实战案例**：全能个人助手Agent
> 
> **学习时长**：90分钟

---

## 📖 口播文案（6分钟）
![Tool Chain](./images/tool_chain.svg)
*图：Tool Chain*


### 🎯 前言

"前面7节课，我们学习了Tool Calling的方方面面。

今天是第13章的收官之作：**构建真正的多工具Agent智能助手！**

**什么是多工具Agent？**

就是：**一个Agent，搞定所有事！**

**看一个真实任务：**

```
用户："帮我分析一下上个月的销售数据，
      生成报告并发送给团队"

普通Agent：
"抱歉，这太复杂了..."

多工具Agent：
✅ 步骤1：使用数据库工具查询销售数据
   → SELECT * FROM sales WHERE month='2024-10'

✅ 步骤2：使用Python工具分析数据
   → 计算总额、增长率、趋势

✅ 步骤3：使用文件工具生成报告
   → 写入report.md

✅ 步骤4：使用搜索工具找团队邮箱
   → 查询团队成员

✅ 步骤5：发送邮件（模拟）
   → 报告已发送

完美完成！🎉
```

**多工具Agent的核心能力：**

**1. 任务理解与规划**
```
用户输入：复杂任务
    ↓
Agent分析：
• 需要哪些工具？
• 执行顺序是什么？
• 如何处理依赖？
    ↓
生成执行计划：
Step 1: 工具A
Step 2: 工具B（依赖Step 1）
Step 3: 工具C
```

**2. 智能工具选择**
```
场景："查询北京的天气"

Agent思考：
• 需要实时数据 → 不用数据库
• 需要外部信息 → 用API工具
• 选择：WeatherAPI ✅

场景："分析销售数据"

Agent思考：
• 需要历史数据 → 用数据库
• 需要计算统计 → 用Python工具
• 选择：DatabaseTool + PythonREPL ✅
```

**3. 工具协同**
```
任务："把Excel数据导入数据库"

协同流程：
文件工具读取 → Python解析 → 数据库写入

任务："生成可视化报告"

协同流程：
数据库查询 → Python分析 → 文件工具保存图表
```

**4. 错误处理与重试**
```
Step 1: 查询数据库
  → 失败：连接超时

Agent决策：
• 重试3次
• 仍然失败
• 切换到备用方案：读取本地文件

Step 2: 继续执行...
```

**真实复杂场景示例：**

**场景：智能日报生成**

```
用户："生成今天的工作日报"

Agent执行：

【步骤1】查询今日任务完成情况
工具：DatabaseTool
SQL: SELECT * FROM tasks WHERE date='2024-11-15' AND status='completed'
结果：完成了5个任务

【步骤2】读取工作日志
工具：FileReadTool
文件：logs/2024-11-15.log
结果：工作8小时，开会2小时

【步骤3】查询今日代码提交
工具：APITool（GitHub）
结果：提交了3次，新增200行代码

【步骤4】分析数据生成摘要
工具：PythonREPL
计算：完成率、代码量、时间分配

【步骤5】搜索相关信息
工具：SearchTool
查询：今日技术新闻

【步骤6】生成报告
工具：FileWriteTool
格式：Markdown
内容：
- 任务完成情况
- 代码贡献
- 学习笔记
- 明日计划

【步骤7】格式化输出
工具：LLM生成
优化：语言流畅、结构清晰

✅ 完整日报生成！
```

**多工具Agent的架构：**

```
【架构层次】

1. 用户交互层
   • 接收用户输入
   • 展示执行过程
   • 返回最终结果

2. 任务规划层
   • 理解用户意图
   • 分解复杂任务
   • 生成执行计划

3. 工具调度层
   • 选择合适工具
   • 管理工具执行
   • 处理工具结果

4. 工具执行层
   • Calculator
   • Search
   • DateTime
   • Weather
   • Translate
   • Database
   • FileSystem
   • PythonREPL

5. 监控日志层
   • 执行日志
   • 性能监控
   • 错误追踪
```

**今天这一课，我要带你：**

**第一部分：工具集成**
- 整合所有工具
- 统一接口
- 工具注册

**第二部分：任务规划**
- ReAct框架应用
- 执行计划生成
- 依赖管理

**第三部分：智能调度**
- 工具选择策略
- 并行执行
- 错误恢复

**第四部分：监控与日志**
- 执行追踪
- 性能分析
- 调试工具

**第五部分：完整实战**
- 个人助手Agent
- 复杂任务处理
- 生产级实现

学完这一课，你将拥有真正的AI助手！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【多工具Agent = 瑞士军刀】

单一工具：
• 只能做一件事
• 遇到新问题就卡住

多工具Agent：
• 有十八般武艺
• 灵活组合解决问题

【关键是"智能决策"】

不是工具多就厉害
而是：
• 知道什么时候用什么工具
• 知道如何组合工具
• 知道如何处理失败
```

---

## 📚 第一部分：工具集成框架

### 一、完整的工具管理器

```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time
import json

@dataclass
class ToolExecutionResult:
    """工具执行结果"""
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float = 0.0

class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.tool_metadata: Dict[str, Dict] = {}
    
    def register(
        self,
        tool,
        category: str = "general",
        priority: int = 5
    ):
        """
        注册工具
        
        Args:
            tool: 工具实例
            category: 工具类别
            priority: 优先级（1-10，越大越优先）
        """
        self.tools[tool.name] = tool
        self.tool_metadata[tool.name] = {
            'category': category,
            'priority': priority,
            'description': tool.description,
            'usage_count': 0,
            'success_count': 0,
            'avg_execution_time': 0.0
        }
    
    def get_tool(self, name: str):
        """获取工具"""
        return self.tools.get(name)
    
    def get_all_tools(self) -> List:
        """获取所有工具"""
        return list(self.tools.values())
    
    def get_tools_by_category(self, category: str) -> List:
        """按类别获取工具"""
        return [
            tool for name, tool in self.tools.items()
            if self.tool_metadata[name]['category'] == category
        ]
    
    def update_statistics(
        self,
        tool_name: str,
        success: bool,
        execution_time: float
    ):
        """更新工具统计信息"""
        
        if tool_name not in self.tool_metadata:
            return
        
        meta = self.tool_metadata[tool_name]
        meta['usage_count'] += 1
        
        if success:
            meta['success_count'] += 1
        
        # 更新平均执行时间
        old_avg = meta['avg_execution_time']
        count = meta['usage_count']
        meta['avg_execution_time'] = (
            (old_avg * (count - 1) + execution_time) / count
        )
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return self.tool_metadata.copy()

class MultiToolAgent:
    """多工具Agent"""
    
    def __init__(self, llm):
        self.llm = llm
        self.registry = ToolRegistry()
        
        # 执行历史
        self.execution_history = []
        
        # 配置
        self.max_iterations = 10
        self.verbose = True
    
    def register_tool(
        self,
        tool,
        category: str = "general",
        priority: int = 5
    ):
        """注册工具"""
        self.registry.register(tool, category, priority)
    
    def run(self, user_input: str) -> str:
        """执行任务"""
        
        if self.verbose:
            print("\n" + "="*60)
            print(f"🤖 任务：{user_input}")
            print("="*60)
        
        # 构建消息
        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt()
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        # 获取工具定义
        tools = [
            tool.to_dict()
            for tool in self.registry.get_all_tools()
        ]
        
        # ReAct循环
        for iteration in range(self.max_iterations):
            if self.verbose:
                print(f"\n--- 迭代 {iteration + 1} ---")
            
            # 调用LLM
            response = self.llm.invoke(messages, tools=tools)
            
            # 检查是否有工具调用
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # 执行工具
                tool_results = self._execute_tools(response.tool_calls)
                
                # 添加assistant消息
                messages.append(response.message)
                
                # 添加工具结果
                for result in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": result['tool_call_id'],
                        "content": result['content']
                    })
                
                continue
            else:
                # 没有工具调用，任务完成
                if self.verbose:
                    print(f"\n✅ 任务完成")
                    print(f"📊 统计：执行了{len(self.execution_history)}个工具")
                
                return response.content
        
        return "任务超时：达到最大迭代次数"
    
    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        
        tool_descriptions = []
        for tool in self.registry.get_all_tools():
            tool_descriptions.append(
                f"• {tool.name}: {tool.description}"
            )
        
        prompt = f"""你是一个智能助手，可以使用多种工具完成任务。

可用工具：
{chr(10).join(tool_descriptions)}

工作流程：
1. 分析用户需求
2. 选择合适的工具
3. 执行工具获取结果
4. 综合结果回答用户

注意：
• 优先使用专用工具
• 可以多次调用工具
• 工具可以组合使用
• 遇到错误时尝试其他方案
"""
        
        return prompt
    
    def _execute_tools(
        self,
        tool_calls: List
    ) -> List[Dict]:
        """执行工具调用"""
        
        results = []
        
        for tool_call in tool_calls:
            result = self._execute_single_tool(tool_call)
            results.append(result)
        
        return results
    
    def _execute_single_tool(self, tool_call) -> Dict:
        """执行单个工具"""
        
        import json
        
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if self.verbose:
            print(f"\n🔧 执行工具：{tool_name}")
            print(f"   参数：{arguments}")
        
        start_time = time.time()
        
        try:
            # 获取工具
            tool = self.registry.get_tool(tool_name)
            
            if not tool:
                raise Exception(f"工具不存在：{tool_name}")
            
            # 执行工具
            result = tool.run(**arguments)
            
            execution_time = time.time() - start_time
            
            # 更新统计
            self.registry.update_statistics(
                tool_name,
                success=True,
                execution_time=execution_time
            )
            
            # 记录历史
            self.execution_history.append(
                ToolExecutionResult(
                    tool_name=tool_name,
                    success=True,
                    result=result,
                    execution_time=execution_time
                )
            )
            
            if self.verbose:
                print(f"   ✅ 成功 ({execution_time:.2f}s)")
                print(f"   结果：{str(result)[:100]}...")
            
            return {
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # 更新统计
            self.registry.update_statistics(
                tool_name,
                success=False,
                execution_time=execution_time
            )
            
            # 记录历史
            self.execution_history.append(
                ToolExecutionResult(
                    tool_name=tool_name,
                    success=False,
                    result=None,
                    error=str(e),
                    execution_time=execution_time
                )
            )
            
            if self.verbose:
                print(f"   ❌ 失败 ({execution_time:.2f}s)")
                print(f"   错误：{str(e)}")
            
            return {
                "tool_call_id": tool_call.id,
                "content": f"工具执行失败：{str(e)}"
            }
    
    def get_execution_report(self) -> str:
        """获取执行报告"""
        
        if not self.execution_history:
            return "没有执行历史"
        
        # 统计信息
        total = len(self.execution_history)
        success = sum(1 for r in self.execution_history if r.success)
        failed = total - success
        total_time = sum(r.execution_time for r in self.execution_history)
        
        # 构建报告
        lines = []
        lines.append("\n" + "="*60)
        lines.append("📊 执行报告")
        lines.append("="*60)
        lines.append(f"\n总计执行：{total}次")
        lines.append(f"  成功：{success}次 ({success/total*100:.1f}%)")
        lines.append(f"  失败：{failed}次 ({failed/total*100:.1f}%)")
        lines.append(f"  总耗时：{total_time:.2f}秒")
        lines.append(f"  平均耗时：{total_time/total:.2f}秒")
        
        # 工具使用统计
        tool_stats = {}
        for r in self.execution_history:
            if r.tool_name not in tool_stats:
                tool_stats[r.tool_name] = {'count': 0, 'success': 0}
            tool_stats[r.tool_name]['count'] += 1
            if r.success:
                tool_stats[r.tool_name]['success'] += 1
        
        lines.append("\n工具使用情况：")
        for tool_name, stats in sorted(
            tool_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        ):
            lines.append(
                f"  • {tool_name}: {stats['count']}次 "
                f"(成功率{stats['success']/stats['count']*100:.0f}%)"
            )
        
        return "\n".join(lines)
```

---

## 💻 第二部分：完整实战Demo

### 一、个人助手Agent

```python
# 这里使用模拟的LLM来演示完整流程
class MockLLM:
    """模拟LLM（用于演示）"""
    
    def invoke(self, messages, tools=None):
        """模拟LLM响应"""
        
        user_message = messages[-1]['content']
        
        # 简单的规则匹配（实际使用真实LLM）
        if "天气" in user_message:
            # 模拟工具调用
            class MockResponse:
                def __init__(self):
                    self.tool_calls = [
                        type('obj', (object,), {
                            'id': 'call_1',
                            'function': type('obj', (object,), {
                                'name': 'get_weather',
                                'arguments': '{"city": "北京"}'
                            })()
                        })()
                    ]
                    self.message = {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": self.tool_calls
                    }
            
            return MockResponse()
        
        # 没有工具调用，返回最终答案
        class FinalResponse:
            def __init__(self, content):
                self.content = content
                self.tool_calls = None
        
        return FinalResponse("任务完成")

def demo_multi_tool_agent():
    """演示多工具Agent"""
    
    print("="*60)
    print("🤖 多工具Agent智能助手演示")
    print("="*60)
    
    # 创建Agent
    llm = MockLLM()
    agent = MultiToolAgent(llm)
    
    # 注册工具
    from datetime import datetime
    
    # 简单的工具实现
    class SimpleCalculator:
        def __init__(self):
            self.name = "calculator"
            self.description = "执行数学计算"
        
        def run(self, expression: str) -> str:
            try:
                result = eval(expression)
                return f"计算结果：{result}"
            except:
                return "计算错误"
        
        def to_dict(self):
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "数学表达式"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
    
    class SimpleWeather:
        def __init__(self):
            self.name = "get_weather"
            self.description = "获取城市天气"
        
        def run(self, city: str) -> str:
            # 模拟天气数据
            return f"{city}的天气：晴天，20-28℃"
        
        def to_dict(self):
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
    
    # 注册工具
    agent.register_tool(SimpleCalculator(), category="utility", priority=8)
    agent.register_tool(SimpleWeather(), category="api", priority=7)
    
    # 执行任务
    result = agent.run("查询北京的天气")
    print(f"\n最终结果：{result}")
    
    # 显示报告
    print(agent.get_execution_report())
    
    # 显示工具统计
    stats = agent.registry.get_statistics()
    print("\n" + "="*60)
    print("📈 工具统计")
    print("="*60)
    for tool_name, meta in stats.items():
        print(f"\n工具：{tool_name}")
        print(f"  使用次数：{meta['usage_count']}")
        print(f"  成功次数：{meta['success_count']}")
        print(f"  平均耗时：{meta['avg_execution_time']:.3f}秒")

demo_multi_tool_agent()
```

---

## 🎯 第三部分：生产级增强

### 一、错误处理与重试

```python
from functools import wraps
import traceback

def with_retry(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class RobustToolExecutor:
    """健壮的工具执行器"""
    
    def __init__(self, tool, max_retries=3):
        self.tool = tool
        self.max_retries = max_retries
        self.fallback_tools = []
    
    def add_fallback(self, fallback_tool):
        """添加备用工具"""
        self.fallback_tools.append(fallback_tool)
    
    def execute(self, **kwargs):
        """执行（带重试和备用）"""
        
        # 尝试主工具
        for attempt in range(self.max_retries):
            try:
                return self.tool.run(**kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    # 主工具失败，尝试备用
                    for fallback in self.fallback_tools:
                        try:
                            return fallback.run(**kwargs)
                        except:
                            continue
                    # 所有工具都失败
                    raise Exception(f"所有工具执行失败：{str(e)}")
                
                time.sleep(1 * (attempt + 1))
```

---

## 📝 课后练习

### 练习1：添加更多工具
集成邮件、日历、笔记等工具

### 练习2：智能规划
实现更智能的任务分解和规划

### 练习3：可视化Dashboard
创建工具使用和性能监控面板

---

## 🎓 知识总结

### 核心要点

1. **工具集成**
   - 统一注册
   - 分类管理
   - 统计监控

2. **任务执行**
   - ReAct框架
   - 工具调度
   - 结果整合

3. **错误处理**
   - 重试机制
   - 备用方案
   - 优雅降级

4. **生产特性**
   - 日志记录
   - 性能监控
   - 统计分析

---

## 🎉 第13章总结

### 完成的7节课

1. **第76课**：Tool Calling原理与标准
2. **第77课**：Function Calling深入
3. **第78课**：内置工具使用
4. **第79课**：API调用封装
5. **第80课**：数据库操作
6. **第81课**：文件系统操作
7. **第82课**：多工具Agent实战 ✅

### 掌握的核心能力

✅ Tool Calling协议标准  
✅ Function Calling高级用法  
✅ 并行调用优化  
✅ 5大内置工具  
✅ API封装技巧  
✅ 数据库安全操作  
✅ 文件系统沙箱  
✅ 多工具集成架构  

---

## 🚀 下一章预告

**第14章：Agent进阶开发（第83-90课）**

- Agent调试技巧
- 性能优化
- Multi-Agent协作
- Agent安全性
- 可观测性
- AutoGPT原理
- BabyAGI解析
- 【项目】智能办公助手

**进入Agent高级领域！** 🚀

---

**💪 恭喜！你已经掌握了Tool Calling的全部内容！**

**下一章见！** 🎉
