![Agent进阶架构](./images/agent.svg)
*图：Agent进阶架构*

# 第87课：Agent可观测性系统

> **本课目标**：构建完整的Agent可观测性系统，实现全方位监控和分析
> 
> **核心技能**：指标监控、链路追踪、日志分析、可视化Dashboard
> 
> **实战案例**：构建生产级Agent监控系统
> 
> **学习时长**：90分钟

---

## 📖 口播文案（6分钟）
![Agent Debug](./images/agent_debug.svg)
*图：Agent Debug*


### 🎯 前言

"上节课我们学习了Agent的安全性。

今天我们要学习另一个关键话题：**Agent可观测性！**

**什么是可观测性（Observability）？**

简单说：**让黑盒变透明！**

**没有可观测性的Agent：**
```
用户："为什么这么慢？"
你："不知道..."

用户："刚才为什么出错了？"
你："我看看...（翻日志半天）"

用户："性能怎么样？"
你："应该还行吧...（心虚）"

完全是个黑盒！😵
```

**有可观测性的Agent：**
```
用户："为什么这么慢？"
你："LLM调用占用了2.3秒，工具执行1.2秒"
    打开Dashboard，一目了然 ✨

用户："刚才为什么出错了？"
你："工具A在第3步调用失败，原因是参数格式错误"
    完整的调用链路，清晰可见 ✨

用户："性能怎么样？"
你："平均响应时间1.5秒，成功率99.2%，P95延迟2.8秒"
    实时数据，专业分析 ✨

一切尽在掌握！💪
```

**可观测性的3大支柱：**

**支柱1：Metrics（指标）**
```
What（发生了什么）

关键指标：
• 响应时间：平均、P50、P95、P99
• 吞吐量：QPS、RPS
• 成功率：成功/失败比例
• 资源使用：CPU、内存、网络

示例：
"最近1小时：
• 平均响应时间：1.2秒
• QPS：150
• 成功率：99.5%
• 内存使用：2.3GB"

一眼看出系统健康状态！
```

**支柱2：Logs（日志）**
```
Why（为什么发生）

详细记录：
• 用户输入
• Agent思考过程
• 工具调用
• 错误信息

示例：
[10:23:45] 用户输入: "查询天气"
[10:23:46] Agent思考: "需要调用天气API"
[10:23:46] 调用工具: get_weather(北京)
[10:23:47] 工具失败: API超时
[10:23:47] Agent重试: 第2次调用
[10:23:48] 调用成功: 晴天20℃

完整的故事线！
```

**支柱3：Traces（链路追踪）**
```
How（如何发生）

调用链路：
用户请求
  └─ Agent处理
      ├─ LLM调用1 (1.2s)
      ├─ 工具调用A (0.5s)
      │   └─ API请求 (0.4s)
      ├─ LLM调用2 (0.8s)
      └─ 返回结果

每一步都有：
• 开始时间
• 结束时间
• 耗时
• 状态

瓶颈一目了然！
```

**为什么需要可观测性？**

**原因1：快速定位问题**
```
场景：用户报告响应很慢

没有可观测性：
• 猜测可能的原因
• 逐个排查
• 浪费大量时间

有可观测性：
1. 打开Dashboard
2. 看到P95延迟突增
3. 追踪到具体请求
4. 发现是某个工具超时
5. 定位到根因

解决时间：5分钟 vs 2小时！
```

**原因2：性能优化**
```
问题：想优化性能，不知从何下手

可观测性告诉你：
• LLM调用：占60%时间
• 工具A：占25%时间
• 工具B：占10%时间
• 其他：占5%时间

结论：
优先优化LLM调用和工具A
性能提升最明显！

有数据支撑的优化！
```

**原因3：容量规划**
```
问题：需要扩容，但不知道扩多少

可观测性提供：
• 当前QPS：100
• 高峰QPS：500
• 资源使用趋势
• 增长预测

结论：
需要扩容到支持1000 QPS
提前准备，从容应对！
```

**原因4：用户体验优化**
```
数据显示：
• 80%请求在1秒内完成 ✅
• 15%请求在1-3秒完成 ⚠️
• 5%请求超过3秒 ❌

行动：
• 优化慢请求
• 提升用户体验
• 减少投诉

数据驱动的改进！
```

**可观测性系统的关键组件：**

**组件1：指标采集器**
```python
class MetricsCollector:
    """指标采集"""
    
    def record_request(
        self,
        duration: float,
        success: bool,
        user_id: str
    ):
        """记录请求"""
        
        # 响应时间
        self.response_times.append(duration)
        
        # 成功率
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        # QPS
        self.request_count += 1
```

**组件2：链路追踪器**
```python
class Tracer:
    """链路追踪"""
    
    def start_span(self, name: str):
        """开始一个span"""
        span = Span(
            name=name,
            start_time=time.time()
        )
        return span
    
    def end_span(self, span: Span):
        """结束span"""
        span.end_time = time.time()
        span.duration = span.end_time - span.start_time
        self.spans.append(span)
```

**组件3：日志聚合器**
```python
class LogAggregator:
    """日志聚合"""
    
    def aggregate_logs(self):
        """聚合日志"""
        
        # 按错误类型分组
        error_types = {}
        for log in self.logs:
            if log.level == 'ERROR':
                error_type = log.error_type
                error_types[error_type] = \
                    error_types.get(error_type, 0) + 1
        
        return error_types
```

**组件4：可视化Dashboard**
```
实时展示：
• 请求数量曲线
• 响应时间分布
• 成功率趋势
• 错误统计
• 调用链路图

交互式分析：
• 时间范围选择
• 维度钻取
• 对比分析
```

**真实场景案例：**

**案例：性能突然下降**
```
【告警】
时间：14:23
问题：P95延迟从1.5s上升到8s

【快速定位】
1. 打开Dashboard
2. 查看响应时间趋势图
   → 14:20开始突增

3. 查看调用链路
   → 发现工具X的调用时间从0.5s增加到7s

4. 查看工具X的日志
   → API返回超时错误

5. 检查API服务
   → 外部API服务故障

【解决方案】
• 切换到备用API
• 问题解决，延迟恢复正常

总耗时：5分钟
没有可观测性：可能需要数小时！
```

**今天这一课，我要带你：**

**第一部分：指标系统**
- 指标定义
- 数据采集
- 统计分析

**第二部分：链路追踪**
- Span模型
- 分布式追踪
- 调用链可视化

**第三部分：日志系统**
- 结构化日志
- 日志聚合
- 搜索分析

**第四部分：可视化Dashboard**
- 实时监控
- 趋势分析
- 告警系统

**第五部分：完整实战**
- 可观测性平台
- 集成应用
- 最佳实践

学完这一课，你的Agent将完全透明可控！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【可观测性 = 系统的透明度】

黑盒系统：
• 不知道发生了什么
• 不知道为什么
• 不知道如何改进

透明系统：
• 知道每一步
• 了解每个细节
• 数据驱动优化

【监控 ≠ 可观测性】

监控：
• 预设的指标
• 已知的问题

可观测性：
• 任意维度分析
• 未知问题探索
```

---

## 📚 第一部分：指标系统

### 一、完整的指标采集器

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time
from collections import defaultdict, deque
import statistics

@dataclass
class MetricPoint:
    """指标数据点"""
    timestamp: float
    value: float
    tags: Dict[str, str] = field(default_factory=dict)

class MetricsCollector:
    """指标采集器"""
    
    def __init__(self, retention_seconds: int = 3600):
        """
        初始化
        
        Args:
            retention_seconds: 数据保留时间（秒）
        """
        self.retention_seconds = retention_seconds
        
        # 存储各类指标
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=10000)
        )
        self.timeseries: Dict[str, List[MetricPoint]] = defaultdict(list)
    
    def increment_counter(self, name: str, value: int = 1, tags: Dict = None):
        """递增计数器"""
        key = self._make_key(name, tags)
        self.counters[key] += value
        
        # 记录时间序列
        self._add_timeseries(name, value, tags)
    
    def set_gauge(self, name: str, value: float, tags: Dict = None):
        """设置仪表盘值"""
        key = self._make_key(name, tags)
        self.gauges[key] = value
        
        # 记录时间序列
        self._add_timeseries(name, value, tags)
    
    def record_histogram(self, name: str, value: float, tags: Dict = None):
        """记录直方图值"""
        key = self._make_key(name, tags)
        self.histograms[key].append(value)
        
        # 记录时间序列
        self._add_timeseries(name, value, tags)
    
    def _make_key(self, name: str, tags: Optional[Dict]) -> str:
        """生成指标键"""
        if not tags:
            return name
        
        tag_str = ','.join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}{{{tag_str}}}"
    
    def _add_timeseries(self, name: str, value: float, tags: Optional[Dict]):
        """添加时间序列数据"""
        key = self._make_key(name, tags)
        
        point = MetricPoint(
            timestamp=time.time(),
            value=value,
            tags=tags or {}
        )
        
        self.timeseries[key].append(point)
        
        # 清理过期数据
        self._cleanup_timeseries(key)
    
    def _cleanup_timeseries(self, key: str):
        """清理过期数据"""
        cutoff = time.time() - self.retention_seconds
        
        self.timeseries[key] = [
            point for point in self.timeseries[key]
            if point.timestamp >= cutoff
        ]
    
    def get_counter(self, name: str, tags: Dict = None) -> int:
        """获取计数器值"""
        key = self._make_key(name, tags)
        return self.counters.get(key, 0)
    
    def get_gauge(self, name: str, tags: Dict = None) -> Optional[float]:
        """获取仪表盘值"""
        key = self._make_key(name, tags)
        return self.gauges.get(key)
    
    def get_histogram_stats(
        self,
        name: str,
        tags: Dict = None
    ) -> Dict[str, float]:
        """获取直方图统计"""
        key = self._make_key(name, tags)
        values = list(self.histograms.get(key, []))
        
        if not values:
            return {}
        
        sorted_values = sorted(values)
        
        return {
            'count': len(values),
            'sum': sum(values),
            'avg': statistics.mean(values),
            'min': min(values),
            'max': max(values),
            'p50': self._percentile(sorted_values, 50),
            'p95': self._percentile(sorted_values, 95),
            'p99': self._percentile(sorted_values, 99),
        }
    
    def _percentile(self, sorted_values: List[float], p: int) -> float:
        """计算百分位数"""
        if not sorted_values:
            return 0.0
        
        k = (len(sorted_values) - 1) * p / 100
        f = int(k)
        c = f + 1
        
        if c >= len(sorted_values):
            return sorted_values[-1]
        
        return sorted_values[f] + (k - f) * (sorted_values[c] - sorted_values[f])

class AgentMetrics:
    """Agent指标"""
    
    def __init__(self):
        self.collector = MetricsCollector()
    
    def record_request(
        self,
        duration: float,
        success: bool,
        user_id: str,
        endpoint: str
    ):
        """记录请求"""
        
        # 请求计数
        self.collector.increment_counter(
            'agent.requests',
            tags={'endpoint': endpoint}
        )
        
        # 成功/失败计数
        status = 'success' if success else 'failure'
        self.collector.increment_counter(
            'agent.requests.status',
            tags={'status': status, 'endpoint': endpoint}
        )
        
        # 响应时间
        self.collector.record_histogram(
            'agent.response_time',
            duration,
            tags={'endpoint': endpoint}
        )
    
    def record_llm_call(self, duration: float, tokens: int):
        """记录LLM调用"""
        
        self.collector.increment_counter('agent.llm.calls')
        self.collector.record_histogram('agent.llm.duration', duration)
        self.collector.record_histogram('agent.llm.tokens', tokens)
    
    def record_tool_call(
        self,
        tool_name: str,
        duration: float,
        success: bool
    ):
        """记录工具调用"""
        
        self.collector.increment_counter(
            'agent.tools.calls',
            tags={'tool': tool_name}
        )
        
        status = 'success' if success else 'failure'
        self.collector.increment_counter(
            'agent.tools.status',
            tags={'tool': tool_name, 'status': status}
        )
        
        self.collector.record_histogram(
            'agent.tools.duration',
            duration,
            tags={'tool': tool_name}
        )
    
    def get_summary(self) -> Dict:
        """获取指标摘要"""
        
        total_requests = self.collector.get_counter('agent.requests')
        success_requests = self.collector.get_counter(
            'agent.requests.status',
            tags={'status': 'success'}
        )
        
        response_stats = self.collector.get_histogram_stats('agent.response_time')
        
        return {
            'total_requests': total_requests,
            'success_rate': success_requests / total_requests if total_requests > 0 else 0,
            'response_time': response_stats,
            'llm_calls': self.collector.get_counter('agent.llm.calls'),
            'tool_calls': self.collector.get_counter('agent.tools.calls'),
        }

# 演示
def demo_metrics():
    """演示指标系统"""
    
    print("="*60)
    print("指标系统演示")
    print("="*60)
    
    metrics = AgentMetrics()
    
    # 模拟请求
    print("\n模拟100个请求...")
    
    import random
    for i in range(100):
        duration = random.uniform(0.5, 3.0)
        success = random.random() > 0.05  # 95%成功率
        
        metrics.record_request(
            duration=duration,
            success=success,
            user_id=f"user_{i % 10}",
            endpoint="/chat"
        )
        
        # 模拟LLM调用
        if success:
            metrics.record_llm_call(
                duration=random.uniform(0.5, 2.0),
                tokens=random.randint(100, 1000)
            )
            
            # 模拟工具调用
            if random.random() > 0.5:
                metrics.record_tool_call(
                    tool_name="weather",
                    duration=random.uniform(0.1, 0.5),
                    success=random.random() > 0.1
                )
    
    # 显示摘要
    print("\n指标摘要:")
    print("-"*60)
    
    summary = metrics.get_summary()
    
    print(f"总请求数: {summary['total_requests']}")
    print(f"成功率: {summary['success_rate']*100:.1f}%")
    print(f"\n响应时间:")
    for key, value in summary['response_time'].items():
        print(f"  {key}: {value:.3f}s")
    print(f"\nLLM调用: {summary['llm_calls']}")
    print(f"工具调用: {summary['tool_calls']}")

demo_metrics()
```

---

## 💻 第二部分：链路追踪系统

### 一、分布式追踪实现

```python
import uuid
from typing import Optional, List
from contextlib import contextmanager

@dataclass
class Span:
    """追踪Span"""
    span_id: str
    trace_id: str
    parent_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict] = field(default_factory=list)
    error: Optional[str] = None

class Tracer:
    """链路追踪器"""
    
    def __init__(self):
        # 存储所有traces
        self.traces: Dict[str, List[Span]] = defaultdict(list)
        
        # 当前span栈（用于嵌套）
        self.span_stack: List[Span] = []
    
    @contextmanager
    def trace(self, name: str, tags: Dict = None):
        """
        追踪上下文管理器
        
        用法:
            with tracer.trace("llm_call"):
                result = llm.invoke(prompt)
        """
        span = self.start_span(name, tags)
        try:
            yield span
        except Exception as e:
            span.error = str(e)
            raise
        finally:
            self.end_span(span)
    
    def start_span(self, name: str, tags: Dict = None) -> Span:
        """开始一个span"""
        
        # 生成ID
        span_id = str(uuid.uuid4())
        
        # 确定trace_id和parent_id
        if self.span_stack:
            parent_span = self.span_stack[-1]
            trace_id = parent_span.trace_id
            parent_id = parent_span.span_id
        else:
            trace_id = str(uuid.uuid4())
            parent_id = None
        
        # 创建span
        span = Span(
            span_id=span_id,
            trace_id=trace_id,
            parent_id=parent_id,
            name=name,
            start_time=time.time(),
            tags=tags or {}
        )
        
        # 压栈
        self.span_stack.append(span)
        
        return span
    
    def end_span(self, span: Span):
        """结束span"""
        
        span.end_time = time.time()
        span.duration = span.end_time - span.start_time
        
        # 保存span
        self.traces[span.trace_id].append(span)
        
        # 出栈
        if self.span_stack and self.span_stack[-1].span_id == span.span_id:
            self.span_stack.pop()
    
    def add_log(self, message: str, level: str = "INFO"):
        """添加日志到当前span"""
        
        if not self.span_stack:
            return
        
        current_span = self.span_stack[-1]
        current_span.logs.append({
            'timestamp': time.time(),
            'level': level,
            'message': message
        })
    
    def get_trace(self, trace_id: str) -> List[Span]:
        """获取完整trace"""
        return self.traces.get(trace_id, [])
    
    def visualize_trace(self, trace_id: str) -> str:
        """可视化trace"""
        
        spans = self.get_trace(trace_id)
        
        if not spans:
            return "Trace not found"
        
        # 按开始时间排序
        spans = sorted(spans, key=lambda s: s.start_time)
        
        # 构建树形结构
        lines = []
        lines.append(f"\nTrace ID: {trace_id}")
        lines.append("="*60)
        
        # 找到根span
        root_spans = [s for s in spans if s.parent_id is None]
        
        for root in root_spans:
            self._visualize_span(root, spans, lines, depth=0)
        
        return "\n".join(lines)
    
    def _visualize_span(
        self,
        span: Span,
        all_spans: List[Span],
        lines: List[str],
        depth: int
    ):
        """递归可视化span"""
        
        indent = "  " * depth
        duration_ms = span.duration * 1000 if span.duration else 0
        
        # 状态图标
        icon = "❌" if span.error else "✅"
        
        line = f"{indent}├─ {icon} {span.name} ({duration_ms:.1f}ms)"
        
        if span.tags:
            line += f" {span.tags}"
        
        lines.append(line)
        
        # 错误信息
        if span.error:
            lines.append(f"{indent}│  Error: {span.error}")
        
        # 子spans
        children = [s for s in all_spans if s.parent_id == span.span_id]
        for child in children:
            self._visualize_span(child, all_spans, lines, depth + 1)

# 演示
def demo_tracing():
    """演示链路追踪"""
    
    print("="*60)
    print("链路追踪演示")
    print("="*60)
    
    tracer = Tracer()
    
    # 模拟Agent执行
    with tracer.trace("agent_execute") as root:
        tracer.add_log("开始处理用户请求")
        
        # LLM调用
        with tracer.trace("llm_call", tags={'model': 'gpt-4'}):
            time.sleep(0.1)  # 模拟LLM调用
            tracer.add_log("LLM返回结果")
        
        # 工具调用1
        with tracer.trace("tool_call", tags={'tool': 'weather'}):
            time.sleep(0.05)  # 模拟工具执行
        
        # 工具调用2
        with tracer.trace("tool_call", tags={'tool': 'news'}):
            time.sleep(0.08)
        
        # 第二次LLM调用
        with tracer.trace("llm_call", tags={'model': 'gpt-4'}):
            time.sleep(0.12)
            tracer.add_log("生成最终答案")
    
    # 可视化
    trace_id = root.trace_id
    print(tracer.visualize_trace(trace_id))

demo_tracing()
```

---

## 🎯 第三部分：可视化Dashboard

### 一、简单的文本Dashboard

```python
class SimpleDashboard:
    """简单的文本Dashboard"""
    
    def __init__(self, metrics: AgentMetrics):
        self.metrics = metrics
    
    def render(self) -> str:
        """渲染Dashboard"""
        
        summary = self.metrics.get_summary()
        
        lines = []
        lines.append("\n" + "="*60)
        lines.append("Agent监控Dashboard")
        lines.append("="*60)
        
        # 总览
        lines.append("\n【总览】")
        lines.append(f"  总请求数: {summary['total_requests']}")
        lines.append(f"  成功率: {summary['success_rate']*100:.1f}%")
        lines.append(f"  LLM调用: {summary['llm_calls']}")
        lines.append(f"  工具调用: {summary['tool_calls']}")
        
        # 响应时间
        response_time = summary['response_time']
        if response_time:
            lines.append("\n【响应时间】")
            lines.append(f"  平均: {response_time.get('avg', 0):.3f}s")
            lines.append(f"  P50: {response_time.get('p50', 0):.3f}s")
            lines.append(f"  P95: {response_time.get('p95', 0):.3f}s")
            lines.append(f"  P99: {response_time.get('p99', 0):.3f}s")
            
            # ASCII图表
            lines.append("\n  响应时间分布:")
            lines.append(self._render_histogram(response_time))
        
        return "\n".join(lines)
    
    def _render_histogram(self, stats: Dict) -> str:
        """渲染直方图"""
        
        values = {
            'P50': stats.get('p50', 0),
            'P95': stats.get('p95', 0),
            'P99': stats.get('p99', 0),
            'Max': stats.get('max', 0),
        }
        
        max_value = max(values.values())
        width = 40
        
        lines = []
        for label, value in values.items():
            bar_len = int((value / max_value) * width) if max_value > 0 else 0
            bar = "█" * bar_len
            lines.append(f"  {label:4s} │{bar} {value:.3f}s")
        
        return "\n".join(lines)

# 演示
def demo_dashboard():
    """演示Dashboard"""
    
    # 创建指标并生成数据
    metrics = AgentMetrics()
    
    import random
    for i in range(100):
        metrics.record_request(
            duration=random.uniform(0.5, 3.0),
            success=random.random() > 0.05,
            user_id=f"user_{i}",
            endpoint="/chat"
        )
    
    # 渲染Dashboard
    dashboard = SimpleDashboard(metrics)
    print(dashboard.render())

demo_dashboard()
```

---

## 📝 课后练习

### 练习1：集成Prometheus
将指标导出到Prometheus

### 练习2：集成Grafana
创建可视化Dashboard

### 练习3：实现告警系统
异常自动告警

---

## 🎓 知识总结

### 核心要点

1. **指标系统**
   - Counter、Gauge、Histogram
   - 百分位数计算
   - 时间序列数据

2. **链路追踪**
   - Span模型
   - 分布式追踪
   - 调用链可视化

3. **可观测性**
   - Metrics + Logs + Traces
   - 多维度分析
   - 数据驱动决策

4. **最佳实践**
   - 合理的指标
   - 详细的追踪
   - 清晰的可视化

---

## 🚀 下节预告

下一课：**第88课：AutoGPT原理深度解析**

- AutoGPT架构
- 自主规划
- 长期记忆
- 实现原理

**探索自主Agent！** 🤖

---

**💪 记住：可观测性让Agent从黑盒变透明！**

**下一课见！** 🎉
