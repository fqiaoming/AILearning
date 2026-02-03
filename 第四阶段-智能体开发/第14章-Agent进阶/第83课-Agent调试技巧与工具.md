![Agent进阶架构](./images/agent.svg)
*图：Agent进阶架构*

# 第83课：Agent调试技巧与工具

> **本课目标**：掌握Agent调试的各种技巧和工具，快速定位和解决问题
> 
> **核心技能**：日志调试、断点调试、可视化追踪、性能分析
> 
> **实战案例**：构建完整的Agent调试系统
> 
> **学习时长**：85分钟

---

## 📖 口播文案（6分钟）
![Agent Debug](./images/agent_debug.svg)
*图：Agent Debug*


### 🎯 前言

"前面我们学习了如何开发Agent和各种工具。

但开发过程中，你一定遇到过这些问题：

**问题1：Agent不按预期工作**
```
预期：查询天气 → 返回结果
实际：查询天气 → 调用了搜索工具 → 又调用了计算器 → 还是错的

问：到底哪里出错了？🤔
```

**问题2：Agent陷入死循环**
```
Agent一直在重复：
"我需要更多信息..."
"让我查询一下..."
"我需要更多信息..."
...（无限循环）

问：怎么找到循环的原因？🤔
```

**问题3：工具调用失败**
```
错误信息：
"工具执行失败"

问：是工具的问题？参数的问题？还是LLM的问题？🤔
```

**今天我要告诉你：Agent调试，其实很简单！**

只要掌握正确的技巧和工具！

**Agent调试的4大难点：**

**难点1：黑盒问题**
```
传统程序：
代码 → 输出
（逻辑清晰）

Agent：
输入 → LLM思考（黑盒）→ 工具调用 → LLM再思考 → 输出
（过程不透明）

怎么办？
→ 可视化追踪！
```

**难点2：不确定性**
```
同样的输入：
• 第1次：正确
• 第2次：错误
• 第3次：又对了

原因：LLM的随机性

怎么办？
→ 固定随机种子 + 多次测试
```

**难点3：错误链**
```
工具A失败 → Agent调整策略 → 工具B失败 → Agent放弃

到底是哪一步的问题？

怎么办？
→ 详细的执行日志
```

**难点4：性能问题**
```
Agent运行很慢，不知道瓶颈在哪：
• LLM调用慢？
• 工具执行慢？
• 网络延迟？

怎么办？
→ 性能分析工具
```

**Agent调试的5大利器：**

**利器1：详细日志**
```python
print(f"[{time}] 用户输入: {input}")
print(f"[{time}] LLM思考: {thought}")
print(f"[{time}] 选择工具: {tool}")
print(f"[{time}] 工具参数: {args}")
print(f"[{time}] 工具结果: {result}")
print(f"[{time}] 最终输出: {output}")

清晰可见！
```

**利器2：执行追踪**
```python
trace = {
    'steps': [
        {'action': 'think', 'content': '需要查天气'},
        {'action': 'tool_call', 'tool': 'weather', 'args': {...}},
        {'action': 'tool_result', 'result': '晴天'},
        {'action': 'answer', 'content': '今天晴天'}
    ],
    'total_time': 2.5,
    'tool_calls': 1
}

完整的执行链路！
```

**利器3：可视化面板**
```
Agent执行流程图：

用户输入
  ↓
[思考1] "需要查天气"
  ↓
[工具1] get_weather(北京)
  ↓
[结果1] "晴天20℃"
  ↓
[思考2] "天气不错"
  ↓
[输出] "今天北京晴天..."

一目了然！
```

**利器4：断点调试**
```python
# 在关键点设置断点
@breakpoint_before_tool_call
def execute_tool(tool, args):
    # 暂停执行，检查状态
    print(f"即将调用: {tool}")
    print(f"参数: {args}")
    input("按回车继续...")
    
    # 继续执行
    return tool.run(**args)
```

**利器5：性能分析**
```python
profiler = AgentProfiler()

with profiler:
    agent.run(task)

profiler.report()
# LLM调用: 2.1s (42%)
# 工具执行: 1.8s (36%)
# 其他: 1.1s (22%)

找到瓶颈！
```

**真实调试案例：**

**案例：Agent重复调用同一工具**

```
症状：
Agent一直在调用 get_weather("北京")
调用了5次，还在继续...

【调试步骤1】查看日志
发现：每次结果都一样
问题：为什么不停止？

【调试步骤2】查看LLM输出
发现：LLM说"我需要确认天气"
问题：为什么需要确认？

【调试步骤3】查看Prompt
发现：Prompt中没有告诉LLM"工具结果已获得"
问题：LLM不知道已经有结果了！

【解决方案】
改进Prompt：
"工具返回结果：{result}
根据这个结果回答用户。"

✅ 问题解决！
```

**今天这一课，我要带你：**

**第一部分：日志系统**
- 结构化日志
- 日志级别
- 日志分析

**第二部分：执行追踪**
- 步骤记录
- 调用链追踪
- 可视化展示

**第三部分：断点调试**
- 条件断点
- 状态检查
- 交互式调试

**第四部分：性能分析**
- 时间分析
- 资源监控
- 瓶颈识别

**第五部分：调试工具箱**
- LangSmith集成
- 自定义调试器
- 最佳实践

学完这一课，Agent调试不再是难题！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【调试 = 让不透明变透明】

Agent是黑盒：
• 看不见思考过程
• 不知道为什么选这个工具
• 不清楚哪里出错

调试的目标：
• 可见化：看到每一步
• 可理解：知道为什么
• 可控制：能干预和修正

【好的调试系统 = 省时间】

没有调试系统：
• 盲目猜测
• 反复试错
• 浪费时间

有调试系统：
• 快速定位
• 精准修复
• 高效开发
```

---

## 📚 第一部分：结构化日志系统

### 一、完整的日志框架

```python
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json
from pathlib import Path
from enum import Enum

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AgentLogger:
    """Agent专用日志器"""
    
    def __init__(
        self,
        name: str = "agent",
        log_dir: str = "./logs",
        console_output: bool = True,
        file_output: bool = True
    ):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 清除已有的handlers
        self.logger.handlers.clear()
        
        # 添加handlers
        if console_output:
            self._add_console_handler()
        
        if file_output:
            self._add_file_handler()
        
        # 结构化日志存储
        self.structured_logs = []
    
    def _add_console_handler(self):
        """添加控制台输出"""
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 彩色输出格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self):
        """添加文件输出"""
        
        # 按日期创建日志文件
        today = datetime.now().strftime('%Y%m%d')
        log_file = self.log_dir / f"{self.name}_{today}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def log_user_input(self, user_input: str):
        """记录用户输入"""
        self.logger.info(f"👤 用户输入: {user_input}")
        self._add_structured_log("user_input", {"content": user_input})
    
    def log_agent_thought(self, thought: str):
        """记录Agent思考"""
        self.logger.info(f"🤔 Agent思考: {thought}")
        self._add_structured_log("agent_thought", {"content": thought})
    
    def log_tool_call(
        self,
        tool_name: str,
        arguments: Dict,
        call_id: Optional[str] = None
    ):
        """记录工具调用"""
        self.logger.info(f"🔧 调用工具: {tool_name}")
        self.logger.debug(f"   参数: {json.dumps(arguments, ensure_ascii=False)}")
        
        self._add_structured_log("tool_call", {
            "tool": tool_name,
            "arguments": arguments,
            "call_id": call_id
        })
    
    def log_tool_result(
        self,
        tool_name: str,
        result: Any,
        success: bool = True,
        execution_time: float = 0.0,
        call_id: Optional[str] = None
    ):
        """记录工具结果"""
        
        status = "✅" if success else "❌"
        self.logger.info(
            f"{status} 工具结果: {tool_name} "
            f"({execution_time:.2f}s)"
        )
        self.logger.debug(f"   结果: {str(result)[:200]}")
        
        self._add_structured_log("tool_result", {
            "tool": tool_name,
            "result": str(result),
            "success": success,
            "execution_time": execution_time,
            "call_id": call_id
        })
    
    def log_agent_response(self, response: str):
        """记录Agent响应"""
        self.logger.info(f"💬 Agent响应: {response[:100]}...")
        self._add_structured_log("agent_response", {"content": response})
    
    def log_error(self, error: Exception, context: str = ""):
        """记录错误"""
        self.logger.error(
            f"❌ 错误 [{context}]: {str(error)}",
            exc_info=True
        )
        
        self._add_structured_log("error", {
            "error": str(error),
            "context": context,
            "type": type(error).__name__
        })
    
    def _add_structured_log(self, event_type: str, data: Dict):
        """添加结构化日志"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        self.structured_logs.append(log_entry)
    
    def export_structured_logs(self, output_file: Optional[str] = None) -> str:
        """导出结构化日志"""
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.log_dir / f"structured_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.structured_logs, f, ensure_ascii=False, indent=2)
        
        return str(output_file)
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        
        stats = {
            "total_events": len(self.structured_logs),
            "event_types": {},
            "tool_calls": [],
            "errors": []
        }
        
        for log in self.structured_logs:
            event_type = log["event_type"]
            stats["event_types"][event_type] = \
                stats["event_types"].get(event_type, 0) + 1
            
            if event_type == "tool_call":
                stats["tool_calls"].append(log["data"]["tool"])
            elif event_type == "error":
                stats["errors"].append(log["data"]["error"])
        
        return stats

# 演示
def demo_agent_logger():
    """演示日志系统"""
    
    logger = AgentLogger("demo_agent")
    
    print("="*60)
    print("Agent日志系统演示")
    print("="*60)
    
    # 模拟Agent执行流程
    logger.log_user_input("查询北京的天气")
    
    logger.log_agent_thought("用户想知道北京的天气，我需要调用天气查询工具")
    
    logger.log_tool_call(
        "get_weather",
        {"city": "北京"},
        call_id="call_1"
    )
    
    logger.log_tool_result(
        "get_weather",
        "北京今天晴天，20-28℃",
        success=True,
        execution_time=0.5,
        call_id="call_1"
    )
    
    logger.log_agent_thought("已获得天气信息，可以回答用户了")
    
    logger.log_agent_response("北京今天天气很好，晴天，温度在20到28度之间。")
    
    # 模拟错误
    try:
        raise ValueError("测试错误")
    except Exception as e:
        logger.log_error(e, context="工具执行")
    
    # 导出日志
    log_file = logger.export_structured_logs()
    print(f"\n结构化日志已导出: {log_file}")
    
    # 显示统计
    stats = logger.get_statistics()
    print("\n统计信息:")
    print(f"  总事件数: {stats['total_events']}")
    print(f"  事件类型: {stats['event_types']}")
    print(f"  工具调用: {stats['tool_calls']}")

demo_agent_logger()
```

---

## 💻 第二部分：执行追踪系统

### 一、完整的追踪器

```python
from dataclasses import dataclass, field
from typing import List, Optional
import time

@dataclass
class TraceStep:
    """追踪步骤"""
    step_id: int
    step_type: str  # think, tool_call, tool_result, answer
    timestamp: float
    duration: Optional[float] = None
    
    # 内容
    content: Optional[str] = None
    tool_name: Optional[str] = None
    tool_args: Optional[Dict] = None
    tool_result: Optional[str] = None
    success: bool = True
    error: Optional[str] = None

class AgentTracer:
    """Agent执行追踪器"""
    
    def __init__(self):
        self.steps: List[TraceStep] = []
        self.current_step_id = 0
        self.start_time = None
        self.end_time = None
    
    def start_trace(self):
        """开始追踪"""
        self.steps = []
        self.current_step_id = 0
        self.start_time = time.time()
    
    def end_trace(self):
        """结束追踪"""
        self.end_time = time.time()
    
    def add_step(
        self,
        step_type: str,
        **kwargs
    ) -> int:
        """添加步骤"""
        
        step = TraceStep(
            step_id=self.current_step_id,
            step_type=step_type,
            timestamp=time.time(),
            **kwargs
        )
        
        self.steps.append(step)
        self.current_step_id += 1
        
        return step.step_id
    
    def update_step_duration(self, step_id: int, duration: float):
        """更新步骤耗时"""
        
        for step in self.steps:
            if step.step_id == step_id:
                step.duration = duration
                break
    
    def get_trace_summary(self) -> Dict:
        """获取追踪摘要"""
        
        summary = {
            "total_steps": len(self.steps),
            "total_time": self.end_time - self.start_time if self.end_time else 0,
            "step_types": {},
            "tool_calls": {},
            "errors": []
        }
        
        for step in self.steps:
            # 统计步骤类型
            step_type = step.step_type
            summary["step_types"][step_type] = \
                summary["step_types"].get(step_type, 0) + 1
            
            # 统计工具调用
            if step.step_type == "tool_call" and step.tool_name:
                tool = step.tool_name
                if tool not in summary["tool_calls"]:
                    summary["tool_calls"][tool] = {
                        "count": 0,
                        "total_time": 0
                    }
                summary["tool_calls"][tool]["count"] += 1
                if step.duration:
                    summary["tool_calls"][tool]["total_time"] += step.duration
            
            # 收集错误
            if not step.success and step.error:
                summary["errors"].append({
                    "step_id": step.step_id,
                    "error": step.error
                })
        
        return summary
    
    def visualize(self) -> str:
        """可视化追踪结果"""
        
        lines = []
        lines.append("\n" + "="*60)
        lines.append("🔍 执行追踪")
        lines.append("="*60)
        
        for step in self.steps:
            # 时间偏移
            offset = step.timestamp - self.start_time
            
            # 步骤图标
            icons = {
                "think": "🤔",
                "tool_call": "🔧",
                "tool_result": "📝",
                "answer": "💬"
            }
            icon = icons.get(step.step_type, "•")
            
            # 构建行
            line = f"\n[{offset:6.2f}s] {icon} "
            
            if step.step_type == "think":
                line += f"思考: {step.content}"
            elif step.step_type == "tool_call":
                line += f"调用: {step.tool_name}({step.tool_args})"
            elif step.step_type == "tool_result":
                status = "✅" if step.success else "❌"
                duration_str = f"{step.duration:.2f}s" if step.duration else "?"
                line += f"结果: {status} ({duration_str})"
                if step.tool_result:
                    line += f"\n         {step.tool_result[:80]}..."
            elif step.step_type == "answer":
                line += f"回答: {step.content[:80]}..."
            
            lines.append(line)
        
        # 添加摘要
        summary = self.get_trace_summary()
        lines.append("\n" + "-"*60)
        lines.append("📊 摘要:")
        lines.append(f"  总步骤: {summary['total_steps']}")
        lines.append(f"  总耗时: {summary['total_time']:.2f}s")
        lines.append(f"  工具调用: {summary['tool_calls']}")
        
        if summary['errors']:
            lines.append(f"  错误: {len(summary['errors'])}个")
        
        return "\n".join(lines)

# 演示
def demo_agent_tracer():
    """演示追踪系统"""
    
    tracer = AgentTracer()
    
    print("="*60)
    print("Agent追踪系统演示")
    print("="*60)
    
    # 开始追踪
    tracer.start_trace()
    
    # 模拟执行流程
    tracer.add_step(
        "think",
        content="用户想知道北京的天气"
    )
    
    time.sleep(0.1)
    
    step_id = tracer.add_step(
        "tool_call",
        tool_name="get_weather",
        tool_args={"city": "北京"}
    )
    
    time.sleep(0.5)  # 模拟工具执行
    
    tracer.add_step(
        "tool_result",
        tool_name="get_weather",
        tool_result="北京今天晴天，20-28℃",
        success=True,
        duration=0.5
    )
    
    time.sleep(0.1)
    
    tracer.add_step(
        "think",
        content="已获得天气信息"
    )
    
    time.sleep(0.1)
    
    tracer.add_step(
        "answer",
        content="北京今天天气很好，晴天，温度在20到28度之间。"
    )
    
    # 结束追踪
    tracer.end_trace()
    
    # 显示追踪
    print(tracer.visualize())

demo_agent_tracer()
```

---

## 🎯 第三部分：断点调试系统

### 一、交互式调试器

```python
class AgentDebugger:
    """Agent调试器"""
    
    def __init__(self):
        self.breakpoints = {
            "before_tool_call": False,
            "after_tool_call": False,
            "on_error": True,
            "on_loop": True
        }
        
        self.loop_detection = {
            "enabled": True,
            "max_same_action": 3,
            "action_history": []
        }
    
    def set_breakpoint(self, breakpoint_type: str, enabled: bool = True):
        """设置断点"""
        if breakpoint_type in self.breakpoints:
            self.breakpoints[breakpoint_type] = enabled
    
    def check_breakpoint(
        self,
        breakpoint_type: str,
        context: Dict = None
    ) -> bool:
        """检查是否命中断点"""
        
        if not self.breakpoints.get(breakpoint_type, False):
            return False
        
        # 命中断点，进入交互
        self._enter_debug_mode(breakpoint_type, context)
        return True
    
    def _enter_debug_mode(self, breakpoint_type: str, context: Dict):
        """进入调试模式"""
        
        print("\n" + "🔴"*30)
        print(f"断点命中: {breakpoint_type}")
        print("🔴"*30)
        
        if context:
            print("\n上下文:")
            for key, value in context.items():
                print(f"  {key}: {value}")
        
        while True:
            print("\n命令:")
            print("  c - 继续执行")
            print("  s - 跳过此步骤")
            print("  i - 查看详细信息")
            print("  q - 退出程序")
            
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'c':
                break
            elif cmd == 's':
                context['skip'] = True
                break
            elif cmd == 'i':
                self._show_details(context)
            elif cmd == 'q':
                raise KeyboardInterrupt("用户终止")
    
    def _show_details(self, context: Dict):
        """显示详细信息"""
        import json
        print("\n详细信息:")
        print(json.dumps(context, ensure_ascii=False, indent=2))
    
    def detect_loop(self, action: str) -> bool:
        """检测循环"""
        
        if not self.loop_detection["enabled"]:
            return False
        
        # 添加到历史
        self.loop_detection["action_history"].append(action)
        
        # 只保留最近的记录
        max_len = self.loop_detection["max_same_action"] * 2
        if len(self.loop_detection["action_history"]) > max_len:
            self.loop_detection["action_history"] = \
                self.loop_detection["action_history"][-max_len:]
        
        # 检测重复
        recent = self.loop_detection["action_history"][-self.loop_detection["max_same_action"]:]
        
        if len(recent) == self.loop_detection["max_same_action"]:
            if len(set(recent)) == 1:
                # 检测到循环
                print(f"\n⚠️  检测到循环: 连续{self.loop_detection['max_same_action']}次执行相同动作")
                print(f"   动作: {action}")
                
                if self.breakpoints["on_loop"]:
                    self._enter_debug_mode("loop_detected", {
                        "action": action,
                        "count": self.loop_detection["max_same_action"]
                    })
                
                return True
        
        return False
```

---

## 📝 课后练习

### 练习1：日志查询工具
实现日志搜索和过滤功能

### 练习2：性能火焰图
生成Agent执行的火焰图

### 练习3：自动化测试
创建Agent的自动化测试框架

---

## 🎓 知识总结

### 核心要点

1. **日志系统**
   - 结构化日志
   - 多级别输出
   - 统计分析

2. **执行追踪**
   - 步骤记录
   - 可视化展示
   - 性能分析

3. **断点调试**
   - 条件断点
   - 交互式调试
   - 循环检测

4. **最佳实践**
   - 合理的日志级别
   - 详细的上下文
   - 清晰的可视化

---

## 🚀 下节预告

下一课：**第84课：Agent性能优化最佳实践**

- 响应时间优化
- 并发处理
- 缓存策略
- 资源管理

**让Agent更快更强！** ⚡

---

**💪 记住：好的调试系统是高效开发的关键！**

**下一课见！** 🎉
