![Callback回调系统](./images/callback.svg)
*图：Callback回调系统*

# 第33课：Callback系统与Chain监控 - 让执行透明可控

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第6章 - Chain高级应用（第4/7课）
> - 学习目标：掌握Callback机制，实现Chain的监控、日志和调试
> - 预计时间：80-90分钟
> - 前置知识：第23-32课

---

## 📢 课程导入

### 前言

你的LangChain应用上线了，突然用户反馈：**"AI回复很慢"** 或 **"有时候不回复"**。你一脸懵：到底哪个环节出问题了？Prompt生成慢？模型调用慢？还是Parser解析慢？

没有监控，你只能猜！但如果有个机制能记录Chain执行的每一步：**调用了什么、耗时多久、输入输出是什么**，那排查问题就太简单了！

**LangChain的Callback系统就是这样的监控神器！**今天这课，我要教你如何让Chain执行完全透明、可控、可监控！

---

### 核心价值点

**第一，Callback是生产环境的必备工具。**

没有Callback的系统是"黑盒"，出了问题你都不知道发生了什么：
- **性能问题**：哪个步骤慢？慢多久？
- **错误排查**：在哪一步失败的？错误信息是什么？
- **成本监控**：调用了多少次LLM？花了多少钱？
- **用户行为**：用户问了什么？AI答了什么？

Callback让这些问题都有答案！

**第二，Callback不只是日志那么简单。**

很多人以为Callback就是：
```python
print("Chain开始...")
result = chain.invoke(...)
print("Chain结束")
```

错！专业的Callback系统能做：
- **实时监控**：每个组件的执行状态
- **性能分析**：找出性能瓶颈
- **错误追踪**：完整的错误堆栈
- **自定义逻辑**：在特定时机执行代码
- **集成第三方**：发送到Sentry、DataDog等

这才是企业级的监控方案！

**第三，Callback让调试效率提升10倍。**

对比两种调试方式：
- **无Callback**：加print，改代码，重跑，猜测问题
- **有Callback**：看日志，精准定位，立即修复

特别是复杂Chain，没有Callback简直是噩梦！有了Callback，调试变得轻松愉快！

**第四，这是从开发到运维的关键能力。**

开发环境：Callback帮你调试
测试环境：Callback帮你验证
生产环境：Callback帮你监控

一套Callback系统，全场景适用！掌握Callback，你就具备了运维生产系统的能力！

---

### 行动号召

今天这一课会教你：
- Callback的完整机制
- 内置Callback的使用
- 自定义Callback
- 监控和日志最佳实践
- 生产环境的监控方案

**学完这课，你的Chain执行会完全透明！**

---

## 📖 知识讲解

### 1. Callback概述

#
![Monitoring](./images/monitoring.svg)
*图：Monitoring*

### 1.1 什么是Callback

```
Callback（回调）：
- 在Chain执行过程中触发的钩子函数
- 可以在特定时机执行自定义逻辑
- 用于监控、日志、调试、追踪

触发时机：
1. on_chain_start：Chain开始执行
2. on_chain_end：Chain执行完成
3. on_chain_error：Chain执行错误
4. on_llm_start：LLM开始调用
5. on_llm_end：LLM调用完成
6. on_llm_error：LLM调用错误
7. on_tool_start：工具开始执行
8. on_tool_end：工具执行完成
... 更多
```

#### 1.2 Callback的使用方式

```python
from langchain.callbacks import StdOutCallbackHandler

# 方式1：全局设置
from langchain.globals import set_verbose
set_verbose(True)

# 方式2：Chain级别
chain = prompt | llm | parser
result = chain.invoke(
    input_data,
    config={"callbacks": [StdOutCallbackHandler()]}
)

# 方式3：构造函数
conversation = ConversationChain(
    llm=llm,
    callbacks=[StdOutCallbackHandler()]
)
```

---

### 2. 内置Callback

#### 2.1 StdOutCallbackHandler（标准输出）

```python
from langchain.callbacks import StdOutCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

chain = (
    ChatPromptTemplate.from_template("解释{topic}")
    | llm
)

# 使用StdOutCallbackHandler
result = chain.invoke(
    {"topic": "量子计算"},
    config={"callbacks": [StdOutCallbackHandler()]}
)

# 会打印详细的执行信息
```

**输出示例：**
```
> Entering new LLMChain chain...
Prompt after formatting:
解释量子计算
> Finished chain.
```

---

#### 2.2 FileCallbackHandler（文件日志）

```python
from langchain.callbacks import FileCallbackHandler
import logging

# 配置日志文件
logfile = "chain_execution.log"
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = FileCallbackHandler(logfile)

# 使用
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [handler]}
)

# 执行信息会保存到chain_execution.log
```

---

#### 2.3 StatsCallbackHandler（性能统计）

```python
from langchain.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

llm = ChatOpenAI()

# 统计OpenAI调用
with get_openai_callback() as cb:
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"input": "Hello"})
    
    # 查看统计
    print(f"总Token数: {cb.total_tokens}")
    print(f"提示Token数: {cb.prompt_tokens}")
    print(f"补全Token数: {cb.completion_tokens}")
    print(f"总成本: ${cb.total_cost}")
```

---

### 3. 自定义Callback

#### 3.1 基础自定义

```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List

class MyCallbackHandler(BaseCallbackHandler):
    """自定义Callback示例"""
    
    def on_chain_start(
        self, 
        serialized: Dict[str, Any], 
        inputs: Dict[str, Any],
        **kwargs
    ):
        """Chain开始时调用"""
        print(f"🔵 Chain开始")
        print(f"   输入: {inputs}")
    
    def on_chain_end(
        self, 
        outputs: Dict[str, Any],
        **kwargs
    ):
        """Chain结束时调用"""
        print(f"🟢 Chain完成")
        print(f"   输出: {outputs}")
    
    def on_chain_error(
        self, 
        error: Exception,
        **kwargs
    ):
        """Chain错误时调用"""
        print(f"🔴 Chain错误")
        print(f"   错误: {error}")
    
    def on_llm_start(
        self, 
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs
    ):
        """LLM开始调用时"""
        print(f"🔵 LLM调用开始")
        print(f"   Prompts: {prompts[0][:50]}...")
    
    def on_llm_end(
        self, 
        response: Any,
        **kwargs
    ):
        """LLM调用完成时"""
        print(f"🟢 LLM调用完成")
        # print(f"   Response: {response}")
    
    def on_llm_error(
        self, 
        error: Exception,
        **kwargs
    ):
        """LLM调用错误时"""
        print(f"🔴 LLM错误: {error}")


# 使用
callback = MyCallbackHandler()
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [callback]}
)
```

---

#### 3.2 性能监控Callback

```python
import time
from langchain.callbacks.base import BaseCallbackHandler

class PerformanceCallback(BaseCallbackHandler):
    """性能监控Callback"""
    
    def __init__(self):
        self.start_times = {}
        self.metrics = {
            "chain_calls": 0,
            "llm_calls": 0,
            "total_time": 0,
            "llm_time": 0
        }
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        """记录Chain开始时间"""
        run_id = kwargs.get("run_id")
        self.start_times[f"chain_{run_id}"] = time.time()
        self.metrics["chain_calls"] += 1
    
    def on_chain_end(self, outputs, **kwargs):
        """计算Chain执行时间"""
        run_id = kwargs.get("run_id")
        key = f"chain_{run_id}"
        if key in self.start_times:
            elapsed = time.time() - self.start_times[key]
            self.metrics["total_time"] += elapsed
            print(f"⏱️  Chain执行时间: {elapsed:.2f}秒")
            del self.start_times[key]
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        """记录LLM开始时间"""
        run_id = kwargs.get("run_id")
        self.start_times[f"llm_{run_id}"] = time.time()
        self.metrics["llm_calls"] += 1
    
    def on_llm_end(self, response, **kwargs):
        """计算LLM执行时间"""
        run_id = kwargs.get("run_id")
        key = f"llm_{run_id}"
        if key in self.start_times:
            elapsed = time.time() - self.start_times[key]
            self.metrics["llm_time"] += elapsed
            print(f"⏱️  LLM调用时间: {elapsed:.2f}秒")
            del self.start_times[key]
    
    def get_report(self):
        """生成性能报告"""
        return f"""
性能报告：
- Chain调用次数: {self.metrics['chain_calls']}
- LLM调用次数: {self.metrics['llm_calls']}
- 总执行时间: {self.metrics['total_time']:.2f}秒
- LLM总耗时: {self.metrics['llm_time']:.2f}秒
- 其他耗时: {self.metrics['total_time'] - self.metrics['llm_time']:.2f}秒
"""


# 使用
perf_callback = PerformanceCallback()
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [perf_callback]}
)

print(perf_callback.get_report())
```

---

#### 3.3 日志记录Callback

```python
import logging
from datetime import datetime

class LoggingCallback(BaseCallbackHandler):
    """详细日志Callback"""
    
    def __init__(self, log_file="chain.log"):
        self.logger = logging.getLogger("ChainLogger")
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        """记录Chain开始"""
        self.logger.info(f"Chain开始 | 输入: {inputs}")
    
    def on_chain_end(self, outputs, **kwargs):
        """记录Chain结束"""
        self.logger.info(f"Chain完成 | 输出: {outputs}")
    
    def on_chain_error(self, error, **kwargs):
        """记录Chain错误"""
        self.logger.error(f"Chain错误 | 错误: {error}")
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        """记录LLM开始"""
        self.logger.info(f"LLM开始 | Prompt: {prompts[0][:100]}...")
    
    def on_llm_end(self, response, **kwargs):
        """记录LLM结束"""
        self.logger.info(f"LLM完成 | Token使用: {response}")
```

---

#### 3.4 成本追踪Callback

```python
class CostTrackingCallback(BaseCallbackHandler):
    """成本追踪Callback"""
    
    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_cost = 0.0
        
        # 定价（示例）
        self.pricing = {
            "gpt-3.5-turbo": {
                "input": 0.0005 / 1000,
                "output": 0.0015 / 1000
            },
            "gpt-4": {
                "input": 0.03 / 1000,
                "output": 0.06 / 1000
            }
        }
    
    def on_llm_end(self, response, **kwargs):
        """统计token和成本"""
        if hasattr(response, 'llm_output'):
            token_usage = response.llm_output.get('token_usage', {})
            
            prompt_tokens = token_usage.get('prompt_tokens', 0)
            completion_tokens = token_usage.get('completion_tokens', 0)
            
            self.prompt_tokens += prompt_tokens
            self.completion_tokens += completion_tokens
            self.total_tokens += prompt_tokens + completion_tokens
            
            # 计算成本（假设gpt-3.5-turbo）
            model = "gpt-3.5-turbo"
            cost = (
                prompt_tokens * self.pricing[model]["input"] +
                completion_tokens * self.pricing[model]["output"]
            )
            self.total_cost += cost
    
    def get_summary(self):
        """获取成本摘要"""
        return {
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_cost": f"${self.total_cost:.4f}"
        }
```

---

### 4. 多个Callback组合

```python
# 同时使用多个Callback
callbacks = [
    MyCallbackHandler(),
    PerformanceCallback(),
    LoggingCallback("app.log"),
    CostTrackingCallback()
]

result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": callbacks}
)

# 所有Callback都会被调用
```

---

## 💻 Demo案例：Callback实战

创建`callback_demo.py`：

```python
"""
Callback系统完整演示
从基础到生产级监控
"""

from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import time
import logging
from datetime import datetime


def demo_1_builtin_callbacks():
    """示例1：内置Callbacks"""
    print("\n" + "="*60)
    print("示例1：内置Callbacks")
    print("="*60)
    
    from langchain.callbacks import StdOutCallbackHandler
    
    llm = ChatOpenAI()
    chain = (
        ChatPromptTemplate.from_template("用一句话解释{topic}")
        | llm
        | StrOutputParser()
    )
    
    print("\n使用StdOutCallbackHandler：")
    result = chain.invoke(
        {"topic": "区块链"},
        config={"callbacks": [StdOutCallbackHandler()]}
    )
    
    print(f"\n结果：{result}")


def demo_2_custom_callback():
    """示例2：自定义Callback"""
    print("\n" + "="*60)
    print("示例2：自定义Callback")
    print("="*60)
    
    class SimpleCallback(BaseCallbackHandler):
        """简单的自定义Callback"""
        
        def on_chain_start(self, serialized, inputs, **kwargs):
            print(f"▶️  Chain开始")
            print(f"   输入: {inputs}")
        
        def on_chain_end(self, outputs, **kwargs):
            print(f"✅ Chain完成")
            print(f"   输出类型: {type(outputs)}")
        
        def on_llm_start(self, serialized, prompts, **kwargs):
            print(f"🔵 LLM调用开始")
        
        def on_llm_end(self, response, **kwargs):
            print(f"🟢 LLM调用完成")
    
    llm = ChatOpenAI()
    chain = (
        ChatPromptTemplate.from_template("解释{topic}")
        | llm
        | StrOutputParser()
    )
    
    callback = SimpleCallback()
    result = chain.invoke(
        {"topic": "量子计算"},
        config={"callbacks": [callback]}
    )
    
    print(f"\n最终结果：{result[:100]}...")


def demo_3_performance_monitoring():
    """示例3：性能监控"""
    print("\n" + "="*60)
    print("示例3：性能监控Callback")
    print("="*60)
    
    class PerformanceMonitor(BaseCallbackHandler):
        """性能监控"""
        
        def __init__(self):
            self.start_time = None
            self.llm_start = None
            self.chain_time = 0
            self.llm_time = 0
        
        def on_chain_start(self, serialized, inputs, **kwargs):
            self.start_time = time.time()
            print(f"⏱️  Chain开始...")
        
        def on_chain_end(self, outputs, **kwargs):
            self.chain_time = time.time() - self.start_time
            print(f"⏱️  Chain完成 - 总耗时: {self.chain_time:.2f}秒")
        
        def on_llm_start(self, serialized, prompts, **kwargs):
            self.llm_start = time.time()
        
        def on_llm_end(self, response, **kwargs):
            self.llm_time = time.time() - self.llm_start
            print(f"⏱️  LLM耗时: {self.llm_time:.2f}秒")
        
        def get_summary(self):
            other_time = self.chain_time - self.llm_time
            return f"""
性能摘要：
- 总耗时: {self.chain_time:.2f}秒
- LLM耗时: {self.llm_time:.2f}秒 ({self.llm_time/self.chain_time*100:.1f}%)
- 其他耗时: {other_time:.2f}秒 ({other_time/self.chain_time*100:.1f}%)
"""
    
    monitor = PerformanceMonitor()
    
    llm = ChatOpenAI()
    chain = (
        ChatPromptTemplate.from_template("详细解释{topic}")
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke(
        {"topic": "深度学习"},
        config={"callbacks": [monitor]}
    )
    
    print(monitor.get_summary())


def demo_4_logging_callback():
    """示例4：日志记录"""
    print("\n" + "="*60)
    print("示例4：日志记录Callback")
    print("="*60)
    
    class DetailedLogger(BaseCallbackHandler):
        """详细日志记录"""
        
        def __init__(self):
            self.request_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.events = []
        
        def on_chain_start(self, serialized, inputs, **kwargs):
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": "chain_start",
                "inputs": inputs
            }
            self.events.append(event)
            print(f"[{self.request_id}] Chain开始 | 输入: {inputs}")
        
        def on_chain_end(self, outputs, **kwargs):
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": "chain_end",
                "outputs": str(outputs)[:100]
            }
            self.events.append(event)
            print(f"[{self.request_id}] Chain完成")
        
        def on_chain_error(self, error, **kwargs):
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": "chain_error",
                "error": str(error)
            }
            self.events.append(event)
            print(f"[{self.request_id}] Chain错误: {error}")
        
        def get_log_summary(self):
            """获取日志摘要"""
            return {
                "request_id": self.request_id,
                "total_events": len(self.events),
                "events": self.events
            }
    
    logger = DetailedLogger()
    
    llm = ChatOpenAI()
    chain = (
        ChatPromptTemplate.from_template("总结{topic}")
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke(
        {"topic": "人工智能的发展历程"},
        config={"callbacks": [logger]}
    )
    
    print(f"\n日志记录了 {len(logger.events)} 个事件")


def demo_5_multiple_callbacks():
    """示例5：多个Callbacks组合"""
    print("\n" + "="*60)
    print("示例5：多个Callbacks组合使用")
    print("="*60)
    
    class EventCounter(BaseCallbackHandler):
        """事件计数器"""
        def __init__(self):
            self.counts = {
                "chain_start": 0,
                "chain_end": 0,
                "llm_start": 0,
                "llm_end": 0
            }
        
        def on_chain_start(self, *args, **kwargs):
            self.counts["chain_start"] += 1
        
        def on_chain_end(self, *args, **kwargs):
            self.counts["chain_end"] += 1
        
        def on_llm_start(self, *args, **kwargs):
            self.counts["llm_start"] += 1
        
        def on_llm_end(self, *args, **kwargs):
            self.counts["llm_end"] += 1
    
    class ProgressPrinter(BaseCallbackHandler):
        """进度打印"""
        def on_chain_start(self, *args, **kwargs):
            print("🔵 开始处理...")
        
        def on_llm_start(self, *args, **kwargs):
            print("   🤖 调用AI中...")
        
        def on_llm_end(self, *args, **kwargs):
            print("   ✅ AI回复完成")
        
        def on_chain_end(self, *args, **kwargs):
            print("🟢 全部完成！")
    
    # 组合使用
    counter = EventCounter()
    progress = ProgressPrinter()
    
    llm = ChatOpenAI()
    chain = (
        ChatPromptTemplate.from_template("介绍{topic}")
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke(
        {"topic": "机器学习"},
        config={"callbacks": [counter, progress]}
    )
    
    print(f"\n事件统计：{counter.counts}")


def demo_6_production_monitoring():
    """示例6：生产级监控"""
    print("\n" + "="*60)
    print("示例6：生产级监控系统")
    print("="*60)
    
    class ProductionMonitor(BaseCallbackHandler):
        """生产级监控"""
        
        def __init__(self):
            self.metrics = {
                "request_count": 0,
                "success_count": 0,
                "error_count": 0,
                "total_time": 0,
                "avg_time": 0
            }
            self.current_start = None
        
        def on_chain_start(self, serialized, inputs, **kwargs):
            self.metrics["request_count"] += 1
            self.current_start = time.time()
        
        def on_chain_end(self, outputs, **kwargs):
            self.metrics["success_count"] += 1
            elapsed = time.time() - self.current_start
            self.metrics["total_time"] += elapsed
            self.metrics["avg_time"] = (
                self.metrics["total_time"] / 
                self.metrics["request_count"]
            )
        
        def on_chain_error(self, error, **kwargs):
            self.metrics["error_count"] += 1
            print(f"❌ 错误: {error}")
        
        def get_dashboard(self):
            """生成监控面板"""
            success_rate = (
                self.metrics["success_count"] / 
                self.metrics["request_count"] * 100
                if self.metrics["request_count"] > 0 else 0
            )
            
            return f"""
📊 监控面板
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
请求总数：{self.metrics["request_count"]}
成功：{self.metrics["success_count"]}
失败：{self.metrics["error_count"]}
成功率：{success_rate:.1f}%
平均耗时：{self.metrics["avg_time"]:.2f}秒
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    monitor = ProductionMonitor()
    
    llm = ChatOpenAI()
    chain = (
        ChatPromptTemplate.from_template("回答{question}")
        | llm
        | StrOutputParser()
    )
    
    # 模拟多个请求
    questions = [
        "什么是AI？",
        "什么是ML？",
        "什么是DL？"
    ]
    
    for q in questions:
        result = chain.invoke(
            {"question": q},
            config={"callbacks": [monitor]}
        )
        print(f"Q: {q}")
        print(f"A: {result[:50]}...\n")
    
    print(monitor.get_dashboard())


def main():
    """主函数"""
    print("🎯 Callback系统完整演示")
    print("="*60)
    
    demo_1_builtin_callbacks()
    demo_2_custom_callback()
    demo_3_performance_monitoring()
    demo_4_logging_callback()
    demo_5_multiple_callbacks()
    demo_6_production_monitoring()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 核心要点：")
    print("1. Callback在Chain执行时触发")
    print("2. 可以监控性能、记录日志、追踪成本")
    print("3. 多个Callback可以组合使用")
    print("4. 生产环境必备监控工具")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 最佳实践

### Callback使用建议

```
开发环境：
✅ StdOutCallbackHandler（调试）
✅ PerformanceMonitor（性能分析）

测试环境：
✅ LoggingCallback（详细日志）
✅ CostTrackingCallback（成本控制）

生产环境：
✅ 集成APM（Sentry、DataDog）
✅ 监控面板（Grafana）
✅ 告警系统（PagerDuty）
```

### 性能考虑

```python
# ✅ 好的做法：异步日志
class AsyncLogger(BaseCallbackHandler):
    def on_chain_end(self, outputs, **kwargs):
        # 异步写入，不阻塞主流程
        asyncio.create_task(self.log_async(outputs))

# ❌ 不好的做法：同步阻塞
class BadLogger(BaseCallbackHandler):
    def on_chain_end(self, outputs, **kwargs):
        # 同步写入，可能很慢
        with open("log.txt", "a") as f:
            f.write(str(outputs))  # 阻塞！
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解Callback的触发机制
- [ ] 使用内置Callbacks
- [ ] 自定义Callback组件
- [ ] 实现性能监控
- [ ] 搭建生产级监控系统

---

## 📝 下一课预告

**第34课：Chain调试技巧与问题排查**

下一课我们将学习：
- Chain调试的常见问题
- 使用LangSmith调试
- 错误追踪和定位
- 性能瓶颈分析
- 调试工具集

**让调试变得简单高效！**

---

**🎉 恭喜你完成第33课！**

你的Chain执行现在完全透明可控了！

**进度：33/165课（20.0%完成）** 🎊

**里程碑：完成20%进度！**
