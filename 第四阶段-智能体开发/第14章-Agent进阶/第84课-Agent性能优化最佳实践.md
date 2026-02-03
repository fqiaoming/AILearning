![Agent进阶架构](./images/agent.svg)
*图：Agent进阶架构*

# 第84课：Agent性能优化最佳实践

> **本课目标**：掌握Agent性能优化的各种技巧，提升响应速度和吞吐量
> 
> **核心技能**：并发优化、缓存策略、提示词优化、资源管理
> 
> **实战案例**：将Agent响应速度提升10倍
> 
> **学习时长**：90分钟

---

## 📖 口播文案（6分钟)
![Agent Debug](./images/agent_debug.svg)
*图：Agent Debug*


### 🎯 前言

"上节课我们学习了Agent调试。

今天我们要解决一个更重要的问题：**性能优化！**

**你是否遇到过这些情况？**

**情况1：Agent响应太慢**
```
用户："查一下天气"
等待...
等待...
等待... (10秒后)
Agent："北京今天晴天"

用户心里：这也太慢了吧！💢
```

**情况2：高并发时崩溃**
```
1个用户：正常
10个用户：有点慢
100个用户：超时
1000个用户：服务器崩溃 💥
```

**情况3：成本太高**
```
每次请求：
• LLM调用: $0.02
• 日请求: 10000次
• 月成本: $6000

老板：能不能降低成本？💸
```

**今天我要教你：如何让Agent又快又省！**

**Agent性能的3大瓶颈：**

**瓶颈1：LLM调用慢**
```
一次LLM调用：
• GPT-4: 2-5秒
• GPT-3.5: 1-2秒
• 本地模型: 0.5-1秒

问题：占据了80%的响应时间！

解决方案：
✅ 使用Streaming（流式输出）
✅ 并行调用
✅ 缓存重复请求
✅ 优化Prompt长度
```

**瓶颈2：工具调用慢**
```
串行执行：
查天气(1s) → 查新闻(1s) → 查股票(1s)
总计: 3秒

并行执行：
同时查询 → 1秒完成
提升: 3倍！⚡
```

**瓶颈3：数据传输慢**
```
问题：
• 每次都重新查询数据库
• 每次都重新调用API
• 网络延迟累加

解决方案：
✅ 智能缓存
✅ 批量处理
✅ 连接复用
```

**性能优化的黄金法则：**

**法则1：测量优先**
```
错误做法：
"我觉得这里慢，优化一下"

正确做法：
1. 测量当前性能
2. 找到真正的瓶颈
3. 针对性优化
4. 再次测量验证

记住：没有测量，就没有优化！
```

**法则2：20/80原则**
```
80%的性能问题
来自20%的代码

策略：
• 找到那20%
• 集中火力优化
• 不要过度优化
```

**法则3：权衡取舍**
```
不可能三角：
• 速度
• 成本
• 质量

选择策略：
• 实时应用 → 优先速度
• 批量任务 → 优先成本
• 关键决策 → 优先质量
```

**实战优化案例：**

**案例1：Prompt优化（速度提升50%）**

```
优化前：
Prompt长度: 2000 tokens
LLM耗时: 4秒

优化后：
Prompt长度: 800 tokens
LLM耗时: 2秒

如何优化：
• 删除冗余的例子
• 简化指令描述
• 使用更精确的语言

提升: 50% ✨
```

**案例2：并行工具调用（速度提升5倍）**

```
优化前（串行）：
get_weather("北京") → 1s
get_news("科技") → 1s
get_stock("AAPL") → 1s
总计: 3s

优化后（并行）：
asyncio.gather(
    get_weather("北京"),
    get_news("科技"),
    get_stock("AAPL")
)
总计: 1s

提升: 3倍 ⚡
```

**案例3：智能缓存（成本降低80%）**

```
场景：天气查询

优化前：
每次查询都调用API
• 日调用: 10000次
• 月成本: $1000

优化后：
相同城市5分钟内使用缓存
• 命中率: 80%
• 实际调用: 2000次
• 月成本: $200

节省: $800/月 💰
```

**性能优化的5大技巧：**

**技巧1：Streaming流式输出**
```python
# 普通方式
response = llm.invoke(prompt)  # 等待完成
print(response)  # 一次性输出

# Streaming方式
for chunk in llm.stream(prompt):  # 逐块返回
    print(chunk, end='')  # 实时显示

用户体验：
普通: 等3秒 → 看到结果
Streaming: 立即开始看到内容

感觉快了3倍！✨
```

**技巧2：Prompt压缩**
```python
# 优化前
prompt = """
你是一个专业的助手。
你需要帮助用户回答问题。
用户的问题是：{question}
请仔细思考后回答。
回答要准确、详细、专业。
"""

# 优化后
prompt = "回答问题：{question}"

Token减少：80%
速度提升：50%
```

**技巧3：智能缓存**
```python
@cache(ttl=300)  # 缓存5分钟
def get_weather(city):
    return api.call(city)

# 相同请求直接返回缓存
get_weather("北京")  # 调用API: 1s
get_weather("北京")  # 使用缓存: 0.001s
```

**技巧4：批量处理**
```python
# 优化前：逐个处理
for item in items:
    process(item)  # 100次调用

# 优化后：批量处理
process_batch(items)  # 1次调用

速度提升：10倍+
```

**技巧5：异步并发**
```python
# 同步方式
results = []
for task in tasks:
    result = process(task)
    results.append(result)

# 异步方式
results = await asyncio.gather(*[
    process_async(task) for task in tasks
])

速度提升：任务数量倍
```

**今天这一课，我要带你：**

**第一部分：响应时间优化**
- Streaming实现
- Prompt优化
- 预测性加载

**第二部分：并发性能优化**
- 异步编程
- 并行工具调用
- 连接池管理

**第三部分：缓存策略**
- LRU缓存
- 分布式缓存
- 缓存失效策略

**第四部分：成本优化**
- Token使用优化
- 模型选择策略
- 批量折扣

**第五部分：监控与调优**
- 性能指标
- 瓶颈分析
- 持续优化

学完这一课，你的Agent将快如闪电！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【性能优化 = 找瓶颈 + 针对性改进】

不要：
• 盲目优化
• 过早优化
• 过度优化

要：
• 先测量
• 找瓶颈
• 再优化
• 验证效果

【快 ≠ 好，合适才是最好】

不同场景，不同策略：
• 实时聊天 → 追求速度
• 数据分析 → 追求准确
• 批量任务 → 追求成本
```

---

## 📚 第一部分：响应时间优化

### 一、Streaming流式输出

```python
from typing import Iterator, AsyncIterator
import asyncio
import time

class StreamingAgent:
    """支持流式输出的Agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def stream(self, user_input: str) -> Iterator[str]:
        """
        流式执行
        
        优点：
        • 用户立即看到响应
        • 感觉更快
        • 更好的用户体验
        """
        
        # 立即显示思考过程
        yield f"🤔 正在思考...\n"
        
        # 流式调用LLM
        for chunk in self.llm.stream(user_input):
            yield chunk
    
    async def astream(self, user_input: str) -> AsyncIterator[str]:
        """异步流式执行"""
        
        yield f"🤔 正在思考...\n"
        
        async for chunk in self.llm.astream(user_input):
            yield chunk

# 对比演示
def demo_streaming_vs_normal():
    """对比流式 vs 普通"""
    
    print("="*60)
    print("Streaming vs 普通模式对比")
    print("="*60)
    
    # 模拟LLM响应
    response_text = "这是一个很长的回答。" * 20
    chunks = [response_text[i:i+10] for i in range(0, len(response_text), 10)]
    
    # 普通模式
    print("\n【普通模式】")
    start = time.time()
    
    # 模拟等待完整响应
    time.sleep(2)
    print(f"等待{time.time()-start:.1f}秒...")
    print(response_text[:50] + "...")
    
    # Streaming模式
    print("\n【Streaming模式】")
    start = time.time()
    
    for i, chunk in enumerate(chunks[:5]):  # 只显示前5个chunk
        time.sleep(0.1)  # 模拟每个chunk的延迟
        print(chunk, end='', flush=True)
        if i == 0:
            print(f"  ← 立即开始显示（{time.time()-start:.1f}秒）")
    
    print("\n...")
    
    print("\n用户感知：")
    print("  普通模式：需要等2秒才能看到内容")
    print("  Streaming：0.1秒就开始看到内容")
    print("  感觉快了：20倍！✨")

demo_streaming_vs_normal()
```

---

## 💻 第二部分：Prompt优化

### 一、Prompt压缩技巧

```python
class PromptOptimizer:
    """Prompt优化器"""
    
    @staticmethod
    def compress_system_prompt(prompt: str) -> str:
        """
        压缩系统提示词
        
        策略：
        1. 删除冗余词语
        2. 使用简洁表达
        3. 合并相似指令
        """
        
        # 示例压缩规则
        compressions = [
            # 删除冗余的礼貌用语
            (r"请仔细", ""),
            (r"请认真", ""),
            
            # 简化常见表达
            (r"根据用户的问题，", ""),
            (r"你需要", ""),
            
            # 删除重复强调
            (r"一定要|务必", ""),
        ]
        
        result = prompt
        for pattern, replacement in compressions:
            import re
            result = re.sub(pattern, replacement, result)
        
        return result.strip()
    
    @staticmethod
    def optimize_examples(examples: list, max_examples: int = 3) -> list:
        """
        优化示例数量
        
        策略：
        • 保留最具代表性的例子
        • 删除相似的例子
        • 限制总数量
        """
        
        if len(examples) <= max_examples:
            return examples
        
        # 简单策略：取开头、中间、结尾
        indices = [0, len(examples)//2, len(examples)-1]
        return [examples[i] for i in indices[:max_examples]]
    
    @staticmethod
    def calculate_tokens(text: str) -> int:
        """
        估算Token数量
        
        粗略估算：英文1 token ≈ 4字符，中文1 token ≈ 1.5字符
        """
        
        # 统计中英文字符
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        other_chars = len(text) - chinese_chars
        
        # 估算tokens
        tokens = chinese_chars / 1.5 + other_chars / 4
        
        return int(tokens)

# 演示
def demo_prompt_optimization():
    """演示Prompt优化"""
    
    optimizer = PromptOptimizer()
    
    print("="*60)
    print("Prompt优化演示")
    print("="*60)
    
    # 原始Prompt
    original = """
你是一个专业的AI助手。
请仔细阅读用户的问题。
你需要认真思考后回答。
回答一定要准确、详细、专业。
请根据用户的问题提供帮助。
务必确保回答的质量。
"""
    
    # 优化后
    optimized = optimizer.compress_system_prompt(original)
    optimized = "AI助手，准确回答用户问题。"
    
    print("\n原始Prompt:")
    print(original)
    print(f"Token数: {optimizer.calculate_tokens(original)}")
    
    print("\n优化后:")
    print(optimized)
    print(f"Token数: {optimizer.calculate_tokens(optimized)}")
    
    reduction = (1 - optimizer.calculate_tokens(optimized) / 
                 optimizer.calculate_tokens(original)) * 100
    
    print(f"\n压缩率: {reduction:.1f}%")
    print(f"速度提升: 预计{reduction * 0.5:.1f}%")  # 粗略估算

demo_prompt_optimization()
```

---

## 🎯 第三部分：并发优化

### 一、异步Agent实现

```python
import asyncio
from typing import List, Dict, Any

class AsyncAgent:
    """异步Agent（支持并发）"""
    
    def __init__(self, llm, tools: Dict):
        self.llm = llm
        self.tools = tools
    
    async def execute_tools_parallel(
        self,
        tool_calls: List[Dict]
    ) -> List[Dict]:
        """
        并行执行多个工具
        
        性能提升：N倍（N=工具数量）
        """
        
        # 创建异步任务
        tasks = [
            self._execute_tool_async(call)
            for call in tool_calls
        ]
        
        # 并行执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def _execute_tool_async(self, tool_call: Dict) -> Dict:
        """异步执行单个工具"""
        
        tool_name = tool_call['name']
        arguments = tool_call['arguments']
        
        try:
            tool = self.tools[tool_name]
            
            # 如果工具支持异步
            if hasattr(tool, 'arun'):
                result = await tool.arun(**arguments)
            else:
                # 在线程池中执行同步工具
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: tool.run(**arguments)
                )
            
            return {
                'success': True,
                'result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# 性能对比
async def demo_parallel_performance():
    """演示并行性能提升"""
    
    print("="*60)
    print("并行执行性能对比")
    print("="*60)
    
    # 模拟工具（每个耗时1秒）
    async def slow_tool(name: str):
        await asyncio.sleep(1)
        return f"{name}完成"
    
    tools = [
        {"name": "tool1"},
        {"name": "tool2"},
        {"name": "tool3"},
        {"name": "tool4"},
        {"name": "tool5"}
    ]
    
    # 串行执行
    print("\n【串行执行】")
    start = time.time()
    results = []
    for tool in tools:
        result = await slow_tool(tool['name'])
        results.append(result)
    serial_time = time.time() - start
    print(f"耗时: {serial_time:.2f}秒")
    
    # 并行执行
    print("\n【并行执行】")
    start = time.time()
    results = await asyncio.gather(*[
        slow_tool(tool['name']) for tool in tools
    ])
    parallel_time = time.time() - start
    print(f"耗时: {parallel_time:.2f}秒")
    
    # 对比
    print(f"\n性能提升: {serial_time / parallel_time:.1f}倍 ⚡")

# 运行演示
asyncio.run(demo_parallel_performance())
```

---

## ⚡ 第四部分：智能缓存

### 一、多级缓存系统

```python
from functools import lru_cache, wraps
import hashlib
import json
import time
from typing import Optional, Any

class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        # 内存缓存（快速但有限）
        self.memory_cache = {}
        
        # 缓存统计
        self.stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0
        }
    
    def get_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """生成缓存键"""
        
        # 将参数序列化
        key_data = {
            'function': func_name,
            'args': args,
            'kwargs': kwargs
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        
        self.stats['total_requests'] += 1
        
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            
            # 检查是否过期
            if time.time() - entry['timestamp'] < entry['ttl']:
                self.stats['hits'] += 1
                return entry['value']
            else:
                # 删除过期缓存
                del self.memory_cache[key]
        
        self.stats['misses'] += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """设置缓存"""
        
        self.memory_cache[key] = {
            'value': value,
            'timestamp': time.time(),
            'ttl': ttl
        }
    
    def get_hit_rate(self) -> float:
        """获取命中率"""
        
        if self.stats['total_requests'] == 0:
            return 0.0
        
        return self.stats['hits'] / self.stats['total_requests']
    
    def clear(self):
        """清空缓存"""
        self.memory_cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'total_requests': 0}

# 缓存装饰器
def cached(ttl: int = 300):
    """缓存装饰器"""
    
    cache_manager = CacheManager()
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = cache_manager.get_cache_key(
                func.__name__,
                args,
                kwargs
            )
            
            # 尝试从缓存获取
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 保存到缓存
            cache_manager.set(cache_key, result, ttl)
            
            return result
        
        # 添加缓存管理方法
        wrapper.cache_stats = lambda: cache_manager.get_hit_rate()
        wrapper.clear_cache = cache_manager.clear
        
        return wrapper
    
    return decorator

# 演示
@cached(ttl=10)
def slow_function(city: str) -> str:
    """模拟慢速函数（如API调用）"""
    time.sleep(1)  # 模拟1秒延迟
    return f"{city}的天气是晴天"

def demo_caching():
    """演示缓存效果"""
    
    print("="*60)
    print("缓存系统演示")
    print("="*60)
    
    # 第一次调用（无缓存）
    print("\n第1次调用（无缓存）:")
    start = time.time()
    result = slow_function("北京")
    time1 = time.time() - start
    print(f"  结果: {result}")
    print(f"  耗时: {time1:.3f}秒")
    
    # 第二次调用（使用缓存）
    print("\n第2次调用（使用缓存）:")
    start = time.time()
    result = slow_function("北京")
    time2 = time.time() - start
    print(f"  结果: {result}")
    print(f"  耗时: {time2:.3f}秒")
    
    # 性能提升
    print(f"\n性能提升: {time1/time2:.0f}倍 ⚡")
    print(f"缓存命中率: {slow_function.cache_stats()*100:.1f}%")

demo_caching()
```

---

## 📝 课后练习

### 练习1：实现分布式缓存
使用Redis实现分布式缓存

### 练习2：智能批处理
实现请求的自动批处理

### 练习3：性能监控Dashboard
创建实时性能监控面板

---

## 🎓 知识总结

### 核心要点

1. **响应时间优化**
   - Streaming流式输出
   - Prompt压缩
   - 预测性加载

2. **并发优化**
   - 异步编程
   - 并行工具调用
   - 连接池

3. **缓存策略**
   - 多级缓存
   - TTL管理
   - 缓存失效

4. **成本优化**
   - Token优化
   - 批量处理
   - 模型选择

---

## 🚀 下节预告

下一课：**第85课：Multi-Agent协作架构**

- Agent间通信
- 任务分配
- 协作模式
- 冲突解决

**多个Agent一起工作！** 🤝

---

**💪 记住：性能优化要测量先行，针对瓶颈优化！**

**下一课见！** 🎉
