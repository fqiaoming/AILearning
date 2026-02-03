![Tool Calling流程](./images/tool_calling.svg)
*图：Tool Calling流程*

# 第77课：Function Calling深入

> **本课目标**：深入掌握OpenAI Function Calling的高级用法
> 
> **核心技能**：多轮对话、参数提取、并行调用、错误处理
> 
> **实战案例**：复杂Function Calling场景实战
> 
> **学习时长**：85分钟

---

## 📖 口播文案（5分钟）
![Tool Chain](./images/tool_chain.svg)
*图：Tool Chain*


### 🎯 前言

"上节课我们学习了Tool Calling的原理和标准。

今天我们要深入学习：**OpenAI Function Calling的高级用法！**

**Function Calling vs 普通调用的区别？**

先看一个真实场景：

**任务：帮我查北京和上海的天气，然后对比一下**

**普通方式（需要多轮）：**
```
用户："帮我查北京和上海的天气"

Round 1:
Agent: 调用get_weather(北京)
结果: 北京晴天20-28℃

Round 2:
Agent: 调用get_weather(上海)
结果: 上海多云18-25℃

Round 3:
Agent: 生成对比
"北京比上海温度略高，北京晴天上海多云"

总耗时：3轮对话
```

**Function Calling并行方式：**
```
用户："帮我查北京和上海的天气"

LLM一次返回：
{
    "tool_calls": [
        {"function": {"name": "get_weather", "arguments": '{"city": "北京"}'}},
        {"function": {"name": "get_weather", "arguments": '{"city": "上海"}'}}
    ]
}

并行执行两个调用！

总耗时：1轮对话
速度提升3倍！✨
```

**看到了吗？这就是Function Calling的威力！**

**Function Calling的5大高级特性：**

**1. 并行调用（Parallel Function Calling）**
```
一次可以调用多个函数
极大提升效率

场景：
• 批量查询
• 多个独立任务
• 数据聚合
```

**2. 强制调用（Function Calling Enforcement）**
```python
# 可以强制LLM必须调用某个函数
chat.invoke(
    messages,
    tools=[weather_tool],
    tool_choice="required"  # 必须调用
)

# 或者指定调用特定函数
tool_choice={
    "type": "function",
    "function": {"name": "get_weather"}
}
```

**3. 多轮对话（Multi-turn Conversation）**
```
Round 1: User问 → LLM调用工具
Round 2: 工具结果 → LLM生成答案
Round 3: User追问 → LLM继续处理

上下文持续传递！
```

**4. 参数智能提取（Smart Parameter Extraction）**
```
用户："查一下明后两天北京的天气"

LLM自动理解：
• city = "北京"
• date = ["明天", "后天"]

生成两次调用！
```

**5. 错误处理与重试**
```
调用失败 → 错误信息 → LLM理解 → 调整参数 → 重试
```

**真实复杂场景：旅游规划**

```
用户："我下周要去北京玩3天，帮我规划一下"

LLM分析：
需要：
1. 查询下周北京天气
2. 搜索北京景点
3. 查找酒店
4. 推荐餐厅

并行调用4个函数：
{
    "tool_calls": [
        {"function": {"name": "get_weather", ...}},
        {"function": {"name": "search_attractions", ...}},
        {"function": {"name": "search_hotels", ...}},
        {"function": {"name": "search_restaurants", ...}}
    ]
}

一次性获取所有信息！
然后综合生成完整规划！

效率提升10倍！✨
```

**Function Calling的完整流程：**

```
【第1步】用户输入
"帮我查北京和上海明天的天气，然后对比"

【第2步】LLM理解并规划
分析：需要2次天气查询
生成：并行调用计划

【第3步】返回tool_calls
[
    {id: "call_1", function: {name: "get_weather", args: '{"city":"北京","date":"明天"}'}},
    {id: "call_2", function: {name: "get_weather", args: '{"city":"上海","date":"明天"}'}}
]

【第4步】并行执行
Result 1: 北京明天晴，20-28℃
Result 2: 上海明天多云，18-25℃

【第5步】结果返回LLM
messages.extend([
    {role: "tool", tool_call_id: "call_1", content: "北京..."},
    {role: "tool", tool_call_id: "call_2", content: "上海..."}
])

【第6步】LLM生成最终答案
"明天北京晴天20-28℃，上海多云18-25℃。
 北京比上海温度略高，天气更好，更适合户外活动。"

✅ 完美完成！
```

**Function Calling的常见问题：**

**问题1：参数格式错误**
```
错误：LLM生成了错误的JSON
解决：参数验证 + 错误提示 + 重试
```

**问题2：函数不存在**
```
错误：LLM调用了未注册的函数
解决：清晰的函数列表 + 描述优化
```

**问题3：并发冲突**
```
错误：并行调用相互冲突
解决：依赖分析 + 顺序执行
```

**今天这一课，我要带你：**

**第一部分：并行调用**
- 原理与实现
- 性能优化
- 场景应用

**第二部分：多轮对话**
- 上下文管理
- 状态追踪
- 复杂交互

**第三部分：参数处理**
- 智能提取
- 格式验证
- 错误纠正

**第四部分：高级特性**
- 强制调用
- 条件调用
- 动态工具

**第五部分：完整实战**
- 旅游规划助手
- 复杂场景处理
- 最佳实践

学完这一课，你将精通Function Calling！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【Function Calling = 智能工具调用】

普通调用：
• 你告诉它怎么做
• 需要精确指令

Function Calling：
• 它理解你的意图
• 自己决定怎么做
• 智能参数提取

【并行 vs 串行】

串行：A → B → C
时间：T1 + T2 + T3

并行：A、B、C同时
时间：max(T1, T2, T3)

性能提升巨大！
```

---

## 📚 第一部分：并行Function Calling

### 一、并行调用实现

```python
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

class ParallelFunctionCaller:
    """并行函数调用器"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def execute_parallel(
        self,
        tool_calls: List[Dict],
        tool_functions: Dict[str, callable],
        verbose: bool = True
    ) -> List[Dict]:
        """
        并行执行多个函数调用
        
        Args:
            tool_calls: LLM返回的tool_calls列表
            tool_functions: 函数映射字典
            verbose: 是否打印详细信息
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"并行执行 {len(tool_calls)} 个函数调用")
            print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # 准备任务
        futures = []
        for tool_call in tool_calls:
            future = self.executor.submit(
                self._execute_single,
                tool_call,
                tool_functions,
                verbose
            )
            futures.append((tool_call, future))
        
        # 等待所有任务完成
        results = []
        for tool_call, future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    "tool_call_id": tool_call.id,
                    "success": False,
                    "error": str(e)
                })
        
        total_time = time.time() - start_time
        
        if verbose:
            print(f"\n所有调用完成，总耗时: {total_time:.2f}秒")
            print(f"平均每个: {total_time/len(tool_calls):.2f}秒")
        
        return results
    
    def _execute_single(
        self,
        tool_call: Dict,
        tool_functions: Dict[str, callable],
        verbose: bool
    ) -> Dict:
        """执行单个函数调用"""
        
        import json
        
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if verbose:
            print(f"执行: {function_name}({arguments})")
        
        start_time = time.time()
        
        try:
            func = tool_functions[function_name]
            result = func(**arguments)
            
            execution_time = time.time() - start_time
            
            if verbose:
                print(f"  ✅ 成功 ({execution_time:.2f}s): {str(result)[:50]}...")
            
            return {
                "tool_call_id": tool_call.id,
                "success": True,
                "result": result,
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            if verbose:
                print(f"  ❌ 失败 ({execution_time:.2f}s): {str(e)}")
            
            return {
                "tool_call_id": tool_call.id,
                "success": False,
                "error": str(e),
                "execution_time": execution_time
            }

# 演示
def demo_parallel_calling():
    """演示并行调用"""
    
    import time
    
    # 模拟工具函数（有延迟）
    def get_weather(city: str) -> str:
        time.sleep(1)  # 模拟API延迟
        return f"{city}的天气是晴天"
    
    def search_hotels(city: str) -> str:
        time.sleep(1)
        return f"{city}的酒店推荐：酒店A、酒店B"
    
    def search_attractions(city: str) -> str:
        time.sleep(1)
        return f"{city}的景点推荐：景点A、景点B"
    
    # 模拟tool_calls（通常由LLM返回）
    class MockToolCall:
        def __init__(self, id, name, args):
            self.id = id
            self.function = type('obj', (object,), {
                'name': name,
                'arguments': args
            })()
    
    tool_calls = [
        MockToolCall("call_1", "get_weather", '{"city": "北京"}'),
        MockToolCall("call_2", "search_hotels", '{"city": "北京"}'),
        MockToolCall("call_3", "search_attractions", '{"city": "北京"}')
    ]
    
    tool_functions = {
        "get_weather": get_weather,
        "search_hotels": search_hotels,
        "search_attractions": search_attractions
    }
    
    # 测试并行执行
    print("="*60)
    print("对比：串行 vs 并行")
    print("="*60)
    
    # 串行执行
    print("\n【串行执行】")
    start = time.time()
    for call in tool_calls:
        import json
        func = tool_functions[call.function.name]
        args = json.loads(call.function.arguments)
        func(**args)
    serial_time = time.time() - start
    print(f"总耗时: {serial_time:.2f}秒")
    
    # 并行执行
    print("\n【并行执行】")
    caller = ParallelFunctionCaller(max_workers=3)
    results = caller.execute_parallel(tool_calls, tool_functions, verbose=True)
    
    print(f"\n性能对比:")
    print(f"  串行: {serial_time:.2f}秒")
    print(f"  并行: {results[0]['execution_time']:.2f}秒")
    print(f"  提升: {serial_time / results[0]['execution_time']:.1f}倍")

demo_parallel_calling()
```

---

## 💻 第二部分：多轮对话管理

### 一、对话状态管理器

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class ConversationTurn:
    """单轮对话"""
    turn_id: int
    user_message: str
    assistant_message: Optional[str] = None
    tool_calls: List[Dict] = field(default_factory=list)
    tool_results: List[Dict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

class MultiTurnFunctionCalling:
    """多轮Function Calling管理器"""
    
    def __init__(self, llm, tools, max_turns: int = 10):
        self.llm = llm
        self.tools = tools
        self.max_turns = max_turns
        
        # 对话历史
        self.conversation_history = []
        self.current_turn = 0
        
        # 消息列表（用于LLM）
        self.messages = []
    
    def start_conversation(self, user_input: str, verbose: bool = True):
        """开始对话"""
        
        if verbose:
            print("\n" + "🤖"*30)
            print(f"用户: {user_input}")
            print("🤖"*30)
        
        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 创建新的对话轮次
        turn = ConversationTurn(
            turn_id=self.current_turn,
            user_message=user_input
        )
        
        # 多轮循环
        for iteration in range(self.max_turns):
            if verbose:
                print(f"\n--- 第 {iteration + 1} 轮 ---")
            
            # 调用LLM
            response = self.llm.invoke(
                self.messages,
                tools=[t.to_dict() for t in self.tools.values()]
            )
            
            # 检查是否有tool_calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # 有工具调用
                if verbose:
                    print(f"LLM选择调用 {len(response.tool_calls)} 个工具")
                
                turn.tool_calls.extend(response.tool_calls)
                
                # 添加assistant消息
                self.messages.append(response.message)
                
                # 执行工具
                tool_results = self._execute_tools(
                    response.tool_calls,
                    verbose
                )
                turn.tool_results.extend(tool_results)
                
                # 添加工具结果到消息
                for result in tool_results:
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": result["tool_call_id"],
                        "content": result["content"]
                    })
                
                # 继续下一轮（让LLM看到工具结果）
                continue
            else:
                # 没有工具调用，得到最终答案
                turn.assistant_message = response.content
                
                # 添加assistant消息
                self.messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                if verbose:
                    print(f"\nAssistant: {response.content}")
                
                break
        
        # 保存对话轮次
        self.conversation_history.append(turn)
        self.current_turn += 1
        
        return turn.assistant_message
    
    def _execute_tools(
        self,
        tool_calls: List,
        verbose: bool
    ) -> List[Dict]:
        """执行工具调用"""
        
        results = []
        
        for tool_call in tool_calls:
            import json
            
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if verbose:
                print(f"  执行: {function_name}({arguments})")
            
            # 获取工具
            tool = self.tools.get(function_name)
            
            if not tool:
                result_content = f"错误：工具{function_name}不存在"
                success = False
            else:
                try:
                    result = tool.func(**arguments)
                    result_content = str(result)
                    success = True
                    
                    if verbose:
                        print(f"    ✅ {result_content[:50]}...")
                except Exception as e:
                    result_content = f"错误：{str(e)}"
                    success = False
                    
                    if verbose:
                        print(f"    ❌ {result_content}")
            
            results.append({
                "tool_call_id": tool_call.id,
                "content": result_content,
                "success": success
            })
        
        return results
    
    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        
        summary = []
        summary.append("对话历史:")
        summary.append("="*60)
        
        for turn in self.conversation_history:
            summary.append(f"\n轮次 {turn.turn_id + 1}:")
            summary.append(f"  用户: {turn.user_message}")
            
            if turn.tool_calls:
                summary.append(f"  工具调用: {len(turn.tool_calls)}次")
                for tc in turn.tool_calls:
                    summary.append(f"    • {tc.function.name}")
            
            if turn.assistant_message:
                summary.append(f"  Assistant: {turn.assistant_message[:100]}...")
        
        return "\n".join(summary)
```

---

## 🎯 第三部分：智能参数处理

### 一、参数验证器

```python
import json
from jsonschema import validate, ValidationError

class ParameterValidator:
    """参数验证器"""
    
    @staticmethod
    def validate_arguments(
        arguments_json: str,
        parameters_schema: Dict,
        verbose: bool = True
    ) -> tuple[bool, str, Dict]:
        """
        验证参数
        
        Returns:
            (is_valid, error_message, parsed_args)
        """
        if verbose:
            print("\n【参数验证】")
        
        # 1. JSON解析
        try:
            arguments = json.loads(arguments_json)
        except json.JSONDecodeError as e:
            error = f"JSON解析错误: {str(e)}"
            if verbose:
                print(f"  ❌ {error}")
            return False, error, None
        
        # 2. Schema验证
        try:
            validate(instance=arguments, schema=parameters_schema)
        except ValidationError as e:
            error = f"参数验证失败: {e.message}"
            if verbose:
                print(f"  ❌ {error}")
            return False, error, None
        
        if verbose:
            print(f"  ✅ 验证通过")
        
        return True, "", arguments
    
    @staticmethod
    def fix_common_errors(arguments_json: str) -> str:
        """修复常见错误"""
        
        # 修复单引号
        arguments_json = arguments_json.replace("'", '"')
        
        # 修复多余的逗号
        arguments_json = arguments_json.replace(',}', '}')
        arguments_json = arguments_json.replace(',]', ']')
        
        # 修复布尔值
        arguments_json = arguments_json.replace('True', 'true')
        arguments_json = arguments_json.replace('False', 'false')
        
        return arguments_json

# 演示
def demo_parameter_validation():
    """演示参数验证"""
    
    # 定义参数Schema
    schema = {
        "type": "object",
        "properties": {
            "city": {
                "type": "string"
            },
            "date": {
                "type": "string",
                "enum": ["今天", "明天", "后天"]
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["city"]
    }
    
    validator = ParameterValidator()
    
    # 测试用例
    test_cases = [
        ('{"city": "北京", "date": "明天"}', "正常情况"),
        ('{"city": "北京"}', "缺少可选参数"),
        ('{}', "缺少必需参数"),
        ('{"city": "北京", "date": "下周"}', "枚举值错误"),
        ("{'city': '北京'}", "单引号（可修复）"),
    ]
    
    print("="*60)
    print("参数验证测试")
    print("="*60)
    
    for args_json, description in test_cases:
        print(f"\n测试: {description}")
        print(f"输入: {args_json}")
        
        # 尝试修复
        fixed = validator.fix_common_errors(args_json)
        if fixed != args_json:
            print(f"修复后: {fixed}")
        
        # 验证
        is_valid, error, parsed = validator.validate_arguments(
            fixed,
            schema,
            verbose=True
        )

demo_parameter_validation()
```

---

## 📝 课后练习

### 练习1：智能重试
实现参数错误自动修正和重试

### 练习2：依赖分析
分析工具调用之间的依赖关系

### 练习3：性能监控
实现详细的性能统计和分析

---

## 🎓 知识总结

### 核心要点

1. **并行调用**
   - 提升性能3-10倍
   - 适合独立任务
   - 注意并发控制

2. **多轮对话**
   - 状态管理
   - 上下文传递
   - 循环控制

3. **参数处理**
   - JSON Schema验证
   - 错误自动修复
   - 类型检查

4. **最佳实践**
   - 清晰的函数描述
   - 完整的参数定义
   - 健壮的错误处理

---

## 🚀 下节预告

下一课：**第78课：内置工具使用**

- Calculator工具
- Search工具
- DateTime工具
- 文件工具

**掌握常用内置工具！** 🛠️

---

**💪 记住：Function Calling让Agent更智能更高效！**

**下一课见！** 🎉
