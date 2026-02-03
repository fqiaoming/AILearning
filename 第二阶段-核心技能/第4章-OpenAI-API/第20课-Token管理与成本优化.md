![Token成本](./images/token_cost.svg)
*图：Token计费原理和成本优化策略*

# 第20课：Token管理与成本优化 - 让AI应用既好用又省钱

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第4章 - API调用基础（第5/7课）
> - 学习目标：掌握Token计算和成本优化策略，打造高性价比AI应用
> - 预计时间：70-80分钟
> - 前置知识：第16-19课

---

## 📢 课程导入

### 前言

你知道吗？很多AI创业公司不是死在技术上，而是死在成本上！产品做出来了，用户量上去了，但每个月API费用几万、十几万，根本撑不住！最后只能关门大吉！

但真正聪明的团队，通过优化Token使用，把成本降低了80%甚至90%！同样的功能，别人花1万，你只花1千！这就是专业和业余的巨大差距！

今天这课，我要教你全套成本优化技巧，让你的AI应用既强大又省钱！

---

### 核心价值点

**第一，理解Token计算是控制成本的第一步。**

很多人不知道Token怎么算的，稀里糊涂地调API，最后账单来了吓一跳！其实Token计算有规律：
- 1 token ≈ 0.75个英文单词
- 1 token ≈ 0.5-1个中文字
- 输入和输出token分开计费
- 不同模型价格差异巨大

学会估算Token，你就能提前预知成本，不会被账单惊到！

**第二，Token优化的投入产出比极高。**

举个例子：
- 优化前：每次对话1000 tokens，每天1000次，月成本$1500
- 优化后：每次对话300 tokens，每天1000次，月成本$450

省了$1050！而你只需要：
- 精简提示词
- 加缓存
- 选对模型

这些优化几天就能完成，效果立竿见影！

**第三，成本优化不是降低质量，而是提升效率。**

很多人以为成本优化=降低质量，错！真正的优化是：
- 去掉冗余信息（不影响效果）
- 缓存重复请求（响应更快）
- 预处理简单任务（本地处理）
- 选择性价比高的模型（DeepSeek vs GPT-4）

结果是：**成本降低了，用户体验反而更好了！**

**第四，这是AI产品能否盈利的关键。**

看看成功的AI产品：
- ChatGPT：通过缓存、优化大幅降低成本
- Notion AI：混合使用不同模型
- GitHub Copilot：精准的上下文控制

它们都是成本优化的高手！如果不会优化，产品再好也赚不到钱！

---

### 行动号召

今天这一课会教你：
- Token的计算方法和估算技巧
- 提示词优化降低token使用
- 缓存策略的设计和实现
- 混合模型降低成本
- 成本监控和预警系统

**学完这课，你能把AI应用成本降低70%以上！**

---

## 📖 知识讲解

### 1. Token基础

#
![Api Architecture](./images/api_architecture.svg)
*图：Api Architecture*

### 1.1 什么是Token

```
Token：
- 是AI模型处理文本的基本单位
- 不是单词，也不是字符
- 是介于两者之间的概念

英文示例：
"Hello, how are you?" → ["Hello", ",", " how", " are", " you", "?"]
共6个tokens

中文示例：
"你好，今天天气真好" → ["你好", "，", "今天", "天气", "真好"]
共5个tokens

规律：
- 常见词：1词=1token（如"the"、"你好"）
- 罕见词：1词可能=2-3tokens
- 标点：通常单独1token
- 空格：计入前一个token
```

#### 1.2 Token计算规则

```
GPT系列（Tokenizer: cl100k_base）：

英文：
- 1 token ≈ 4个字符
- 1 token ≈ 0.75个单词
- "Hello world" ≈ 2 tokens

中文：
- 1个汉字 ≈ 1-2 tokens
- 常用字：1 token
- 生僻字：2-3 tokens
- "人工智能" ≈ 4 tokens

特殊字符：
- 换行符\n：1 token
- 制表符\t：1 token
- 代码缩进：算tokens
```

#### 1.3 使用tiktoken计算Token

```python
import tiktoken

# 获取编码器
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    """计算文本的token数"""
    tokens = encoding.encode(text)
    return len(tokens)

# 示例
text1 = "Hello, how are you?"
print(f"'{text1}' 的token数：{count_tokens(text1)}")

text2 = "你好，今天天气真好"
print(f"'{text2}' 的token数：{count_tokens(text2)}")

# 查看实际tokens
tokens = encoding.encode("Hello world")
print(f"Tokens: {tokens}")
print(f"解码: {[encoding.decode([t]) for t in tokens]}")
```

---

### 2. API成本计算

#### 2.1 定价模型（2024年参考）

```python
# GPT-3.5-Turbo
GPT35_INPUT_PRICE = 0.0005 / 1000   # $0.0005 per 1K tokens
GPT35_OUTPUT_PRICE = 0.0015 / 1000  # $0.0015 per 1K tokens

# GPT-4-Turbo
GPT4_INPUT_PRICE = 0.01 / 1000      # $0.01 per 1K tokens
GPT4_OUTPUT_PRICE = 0.03 / 1000     # $0.03 per 1K tokens

# GPT-4
GPT4_CLASSIC_INPUT_PRICE = 0.03 / 1000
GPT4_CLASSIC_OUTPUT_PRICE = 0.06 / 1000

def calculate_cost(input_tokens, output_tokens, model="gpt-3.5-turbo"):
    """计算单次调用成本"""
    if model == "gpt-3.5-turbo":
        input_cost = input_tokens * GPT35_INPUT_PRICE
        output_cost = output_tokens * GPT35_OUTPUT_PRICE
    elif model == "gpt-4-turbo":
        input_cost = input_tokens * GPT4_INPUT_PRICE
        output_cost = output_tokens * GPT4_OUTPUT_PRICE
    else:  # gpt-4
        input_cost = input_tokens * GPT4_CLASSIC_INPUT_PRICE
        output_cost = output_tokens * GPT4_CLASSIC_OUTPUT_PRICE
    
    return input_cost + output_cost

# 示例
print(f"1000次对话（每次500 input + 300 output tokens）")
print(f"GPT-3.5: ${calculate_cost(500, 300) * 1000:.2f}")
print(f"GPT-4-Turbo: ${calculate_cost(500, 300, 'gpt-4-turbo') * 1000:.2f}")
print(f"GPT-4: ${calculate_cost(500, 300, 'gpt-4') * 1000:.2f}")
```

#### 2.2 成本估算工具

```python
import tiktoken

class CostEstimator:
    """成本估算器"""
    
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        self.set_pricing(model)
    
    def set_pricing(self, model):
        """设置定价"""
        pricing = {
            "gpt-3.5-turbo": (0.0005/1000, 0.0015/1000),
            "gpt-4-turbo": (0.01/1000, 0.03/1000),
            "gpt-4": (0.03/1000, 0.06/1000)
        }
        self.input_price, self.output_price = pricing.get(
            model, (0.0005/1000, 0.0015/1000)
        )
    
    def estimate_message_cost(self, messages, expected_output_tokens=500):
        """估算消息成本"""
        # 计算输入tokens
        input_tokens = sum(
            len(self.encoding.encode(msg["content"]))
            for msg in messages
        )
        
        # 估算成本
        input_cost = input_tokens * self.input_price
        output_cost = expected_output_tokens * self.output_price
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": expected_output_tokens,
            "total_tokens": input_tokens + expected_output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    
    def estimate_monthly_cost(self, avg_input_tokens, avg_output_tokens, 
                             daily_requests):
        """估算月度成本"""
        daily_cost = (
            avg_input_tokens * self.input_price +
            avg_output_tokens * self.output_price
        ) * daily_requests
        
        monthly_cost = daily_cost * 30
        
        return {
            "daily_requests": daily_requests,
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost
        }


# 使用示例
estimator = CostEstimator("gpt-3.5-turbo")

messages = [
    {"role": "system", "content": "你是一个Python专家"},
    {"role": "user", "content": "解释一下什么是装饰器"}
]

cost = estimator.estimate_message_cost(messages)
print(f"预估成本：${cost['total_cost']:.6f}")

monthly = estimator.estimate_monthly_cost(
    avg_input_tokens=500,
    avg_output_tokens=300,
    daily_requests=1000
)
print(f"月度成本：${monthly['monthly_cost']:.2f}")
```

---

### 3. Token优化策略

#### 3.1 提示词优化

```
策略1：去除冗余信息
❌ 不好：
"请你帮我用Python语言编写一个函数，这个函数的功能是计算两个数字的和，
函数应该接收两个参数，然后返回它们相加的结果。"
（约40 tokens）

✅ 好：
"Python函数：计算两数之和"
（约6 tokens）

节省：34 tokens (85%)

---

策略2：使用缩写和简洁表达
❌ 不好：
"Please provide a detailed explanation"

✅ 好：
"Explain briefly"

---

策略3：移除示例（如果不是必需）
❌ 不好：
Few-shot with 5个示例 = 500 tokens

✅ 好：
Few-shot with 2个示例 = 200 tokens
（如果准确率差不多）

---

策略4：精简system message
❌ 不好：
"You are a helpful assistant. You are knowledgeable, patient, 
and always try to provide accurate information..."
（约20 tokens）

✅ 好：
"You are a helpful Python expert."
（约7 tokens）
```

#### 3.2 上下文管理

```python
class ContextManager:
    """上下文管理器"""
    
    def __init__(self, max_tokens=2000):
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    def count_tokens(self, messages):
        """计算消息tokens"""
        return sum(
            len(self.encoding.encode(msg["content"]))
            for msg in messages
        )
    
    def truncate_history(self, messages, system_message=None):
        """截断历史消息"""
        # 保留system message
        if system_message:
            result = [system_message]
            remaining_tokens = self.max_tokens - \
                len(self.encoding.encode(system_message["content"]))
        else:
            result = []
            remaining_tokens = self.max_tokens
        
        # 从最新消息开始，向前添加
        for msg in reversed(messages):
            tokens = len(self.encoding.encode(msg["content"]))
            if remaining_tokens - tokens < 0:
                break
            result.insert(1 if system_message else 0, msg)
            remaining_tokens -= tokens
        
        return result
    
    def summarize_history(self, messages):
        """摘要历史（高级策略）"""
        # 可以调用AI生成摘要
        # 保留最近几轮完整对话 + 之前的摘要
        recent_count = 4  # 保留最近2轮对话
        recent_messages = messages[-recent_count:]
        old_messages = messages[:-recent_count]
        
        if old_messages:
            # 生成摘要（伪代码）
            summary = "（之前讨论了...）"
            return [{"role": "system", "content": summary}] + recent_messages
        
        return recent_messages


# 使用示例
manager = ContextManager(max_tokens=1000)

# 模拟长对话
long_conversation = [
    {"role": "user", "content": "什么是Python？"},
    {"role": "assistant", "content": "Python是..."},
    # ... 更多对话
]

# 截断到合适长度
truncated = manager.truncate_history(long_conversation)
print(f"原始：{len(long_conversation)}条消息")
print(f"截断后：{len(truncated)}条消息")
```

---

### 4. 缓存策略

#### 4.1 简单缓存

```python
from functools import lru_cache
import hashlib
import json

class SimpleCache:
    """简单的内存缓存"""
    
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get_key(self, message):
        """生成缓存key"""
        # 使用消息内容的hash作为key
        content = json.dumps(message, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, message):
        """获取缓存"""
        key = self.get_key(message)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, message, response):
        """设置缓存"""
        if len(self.cache) >= self.max_size:
            # 简单的LRU：删除最旧的
            self.cache.pop(next(iter(self.cache)))
        
        key = self.get_key(message)
        self.cache[key] = response
    
    def get_stats(self):
        """获取统计"""
        total = self.hits + self.misses
        hit_rate = self.hits / total * 100 if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%",
            "cache_size": len(self.cache)
        }


# 使用示例
cache = SimpleCache()

def chat_with_cache(message):
    # 检查缓存
    cached = cache.get(message)
    if cached:
        print("[缓存命中]")
        return cached
    
    # 调用API
    print("[调用API]")
    response = "..." # 实际API调用
    
    # 存入缓存
    cache.set(message, response)
    
    return response
```

#### 4.2 持久化缓存

```python
import sqlite3
import json
from datetime import datetime, timedelta

class PersistentCache:
    """持久化缓存（使用SQLite）"""
    
    def __init__(self, db_path="cache.db", ttl_hours=24):
        self.db_path = db_path
        self.ttl = timedelta(hours=ttl_hours)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def get(self, message):
        """获取缓存"""
        key = hashlib.md5(json.dumps(message).encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 查询并检查是否过期
        cursor.execute('''
            SELECT value, created_at FROM cache WHERE key = ?
        ''', (key,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            value, created_at = result
            created_time = datetime.fromisoformat(created_at)
            if datetime.now() - created_time < self.ttl:
                return json.loads(value)
        
        return None
    
    def set(self, message, response):
        """设置缓存"""
        key = hashlib.md5(json.dumps(message).encode()).hexdigest()
        value = json.dumps(response)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO cache (key, value, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        
        conn.commit()
        conn.close()
    
    def clean_expired(self):
        """清理过期缓存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - self.ttl).isoformat()
        cursor.execute('''
            DELETE FROM cache WHERE created_at < ?
        ''', (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
```

---

### 5. 混合模型策略

```python
class HybridModelService:
    """混合模型服务"""
    
    def __init__(self):
        self.gpt4_client = OpenAI()  # GPT-4：贵但强
        self.gpt35_client = OpenAI()  # GPT-3.5：便宜
        self.local_client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"
        )  # 本地：免费
    
    def classify_complexity(self, message):
        """评估问题复杂度"""
        # 简单规则（实际可以更复杂）
        simple_keywords = ["什么是", "定义", "简介", "你好"]
        complex_keywords = ["设计", "架构", "优化", "详细分析"]
        
        if any(kw in message for kw in simple_keywords):
            return "simple"
        elif any(kw in message for kw in complex_keywords):
            return "complex"
        else:
            return "medium"
    
    def chat(self, message):
        """根据复杂度选择模型"""
        complexity = self.classify_complexity(message)
        
        if complexity == "simple":
            # 简单问题：本地模型（免费）
            print("[模型] 本地模型")
            client = self.local_client
            model = "qwen2.5-7b-instruct"
        
        elif complexity == "medium":
            # 中等问题：GPT-3.5（便宜）
            print("[模型] GPT-3.5-Turbo")
            client = self.gpt35_client
            model = "gpt-3.5-turbo"
        
        else:
            # 复杂问题：GPT-4（贵但强）
            print("[模型] GPT-4-Turbo")
            client = self.gpt4_client
            model = "gpt-4-turbo"
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
        
        return response.choices[0].message.content


# 成本对比
print("1000次请求成本对比：")
print("全用GPT-4：$30")
print("全用GPT-3.5：$0.80")
print("混合策略（30%简单+50%中等+20%复杂）：")
print("  简单（本地）：0 × 300 = $0")
print("  中等（GPT-3.5）：$0.0008 × 500 = $0.40")
print("  复杂（GPT-4）：$0.02 × 200 = $4")
print("  总计：$4.40")
print("节省：$25.60 (85%)")
```

---

## 💻 Demo案例：成本优化系统

创建`cost_optimization_system.py`：

```python
"""
完整的成本优化系统
集成Token计算、缓存、混合模型
"""

import tiktoken
from openai import OpenAI
import hashlib
import json
from datetime import datetime


class CostOptimizedService:
    """成本优化的AI服务"""
    
    def __init__(self):
        self.client = OpenAI()
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.cache = {}
        
        # 统计
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0.0
        }
    
    def _count_tokens(self, text):
        """计算tokens"""
        return len(self.encoding.encode(text))
    
    def _calculate_cost(self, input_tokens, output_tokens):
        """计算成本"""
        return (
            input_tokens * 0.0005 / 1000 +
            output_tokens * 0.0015 / 1000
        )
    
    def _get_cache_key(self, message):
        """生成缓存key"""
        return hashlib.md5(message.encode()).hexdigest()
    
    def chat(self, message):
        """优化的聊天接口"""
        self.stats["total_requests"] += 1
        
        # 1. 检查缓存
        cache_key = self._get_cache_key(message)
        if cache_key in self.cache:
            self.stats["cache_hits"] += 1
            print("[✓] 缓存命中，成本：$0")
            return self.cache[cache_key]
        
        # 2. 优化提示词（移除冗余）
        optimized_message = message.strip()
        
        # 3. 计算预期成本
        input_tokens = self._count_tokens(optimized_message)
        expected_output_tokens = 300  # 估算
        expected_cost = self._calculate_cost(
            input_tokens, expected_output_tokens
        )
        
        print(f"[预估] 输入: {input_tokens} tokens, "
              f"预期成本: ${expected_cost:.6f}")
        
        # 4. 调用API
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": optimized_message}],
            max_tokens=500  # 限制输出长度
        )
        
        # 5. 计算实际成本
        usage = response.usage
        actual_cost = self._calculate_cost(
            usage.prompt_tokens,
            usage.completion_tokens
        )
        
        # 6. 更新统计
        self.stats["total_input_tokens"] += usage.prompt_tokens
        self.stats["total_output_tokens"] += usage.completion_tokens
        self.stats["total_cost"] += actual_cost
        
        print(f"[实际] 输入: {usage.prompt_tokens} tokens, "
              f"输出: {usage.completion_tokens} tokens, "
              f"成本: ${actual_cost:.6f}")
        
        # 7. 缓存结果
        result = response.choices[0].message.content
        self.cache[cache_key] = result
        
        return result
    
    def get_stats(self):
        """获取统计信息"""
        cache_hit_rate = 0
        if self.stats["total_requests"] > 0:
            cache_hit_rate = (self.stats["cache_hits"] / 
                            self.stats["total_requests"] * 100)
        
        avg_cost = 0
        if self.stats["total_requests"] > 0:
            avg_cost = self.stats["total_cost"] / self.stats["total_requests"]
        
        saved_cost = (self.stats["cache_hits"] * avg_cost 
                     if self.stats["cache_hits"] > 0 else 0)
        
        return {
            **self.stats,
            "cache_hit_rate": f"{cache_hit_rate:.2f}%",
            "avg_cost_per_request": f"${avg_cost:.6f}",
            "saved_by_cache": f"${saved_cost:.4f}"
        }


def demo():
    """演示"""
    print("🎯 成本优化系统演示\n")
    
    service = CostOptimizedService()
    
    test_cases = [
        "什么是Python？",
        "什么是Python？",  # 重复，测试缓存
        "Python有哪些特点？",
        "什么是Python？",  # 再次重复
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"请求 {i}/{len(test_cases)}")
        print(f"{'='*60}")
        print(f"问题：{question}")
        
        response = service.chat(question)
        print(f"回复：{response[:100]}...")
    
    # 显示统计
    print(f"\n{'='*60}")
    print("成本统计")
    print(f"{'='*60}")
    stats = service.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print(f"\n💡 优化效果：")
    print(f"  缓存命中率：{stats['cache_hit_rate']}")
    print(f"  节省成本：{stats['saved_by_cache']}")


if __name__ == "__main__":
    demo()
```

---

## 🎯 最佳实践总结

### 成本优化清单

```
✅ Token优化
  - 精简提示词
  - 移除冗余信息
  - 限制输出长度（max_tokens）

✅ 缓存策略
  - 缓存常见问题
  - 设置合理TTL
  - 定期清理

✅ 模型选择
  - 简单任务用本地/GPT-3.5
  - 复杂任务才用GPT-4
  - 考虑DeepSeek等性价比模型

✅ 上下文管理
  - 截断历史记录
  - 摘要长对话
  - 只保留必要上下文

✅ 批量处理
  - 合并相似请求
  - 异步并发处理

✅ 监控告警
  - 实时成本监控
  - 异常消耗告警
  - 定期成本报告
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 计算和估算Token使用
- [ ] 优化提示词减少Token
- [ ] 实现缓存降低成本
- [ ] 设计混合模型策略
- [ ] 监控和控制API成本

---

## 📝 下一课预告

**第21课：API安全最佳实践**

API密钥泄露、滥用、恶意攻击...下一课我们将学习：
- API密钥的安全管理
- 访问控制和权限管理
- 防止滥用的策略
- 审计和监控
- 合规性要求

**让你的AI应用既强大又安全！**

---

**🎉 恭喜你完成第20课！**

你现在能打造高性价比的AI应用了！

**进度：20/165课（12.1%完成）** 🚀

**下一步：** 学习API安全最佳实践！

