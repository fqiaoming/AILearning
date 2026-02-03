![Tool Calling流程](./images/tool_calling.svg)
*图：Tool Calling流程*

# 第76课：Tool Calling原理与标准

> **本课目标**：深入理解Tool Calling的原理、标准和最佳实践
> 
> **核心技能**：Tool Calling协议、OpenAI标准、参数传递
> 
> **实战案例**：标准化的Tool Calling实现
> 
> **学习时长**：75分钟

---

## 📖 口播文案（5分钟）
![Tool Chain](./images/tool_chain.svg)
*图：Tool Chain*


### 🎯 前言

"恭喜你！完成了第12章Agent基础的学习！

今天我们开启第13章：**Tool Calling工具开发**！

**重要更新：本章内容已全面更新为LangChain 1.0标准！**

LangChain 1.0对工具调用进行了革命性简化：
- ✅ **直接使用Python函数**作为工具
- ✅ **自动推断工具schema**从函数签名和docstring
- ✅ **无需手动定义复杂的工具类**
- ✅ **统一的工具调用接口**

**什么是Tool Calling？**

简单说：**让AI能够调用外部工具的技术！**

**先看一个对比，感受标准化的重要性：**

**方式A：自己解析（不标准）**

```python
# Agent生成的文本
output = "我要调用天气查询工具，城市是北京"

# 你需要自己解析
if "天气查询" in output:
    if "北京" in output:
        result = get_weather("北京")
```

问题：
❌ 不可靠（依赖文本解析）
❌ 不通用（每个工具都要写解析）
❌ 容易出错（LLM输出不稳定）

**方式B：Tool Calling（标准化）**

```python
# LLM返回结构化数据
{
    "tool_calls": [
        {
            "id": "call_123",
            "type": "function",
            "function": {
                "name": "get_weather",
                "arguments": "{\"city\": \"北京\"}"
            }
        }
    ]
}

# 直接调用，安全可靠
result = tools[name](**json.loads(arguments))
```

优势：
✅ 结构化（JSON格式）
✅ 标准化（统一协议）
✅ 可靠（不依赖文本解析）
✅ 可扩展（易于添加新工具）

**Tool Calling的演进历史：**

**2023年6月：OpenAI发布Function Calling**
```
革命性功能！
• 模型原生支持工具调用
• 结构化输出
• 参数验证
```

**2023年底：成为行业标准**
```
各大模型厂商跟进：
• Claude
• Google Gemini
• 开源模型（Llama等）

统一协议！
```

**Tool Calling的核心机制：**

**第一步：工具定义（Tool Schema）**

```python
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如'北京'"
                },
                "date": {
                    "type": "string",
                    "description": "日期，如'今天'、'明天'"
                }
            },
            "required": ["city"]
        }
    }
}
```

关键要素：
• name：工具名称
• description：工具描述（LLM看）
• parameters：参数定义（JSON Schema）

**第二步：LLM理解工具**

```
用户："明天北京天气怎么样？"

LLM内部推理：
1. 用户想知道天气
2. 我有get_weather工具
3. 需要参数：city="北京", date="明天"
4. 生成tool_call
```

**第三步：结构化输出**

```json
{
    "tool_calls": [
        {
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "get_weather",
                "arguments": "{\"city\": \"北京\", \"date\": \"明天\"}"
            }
        }
    ]
}
```

**第四步：执行工具**

```python
# 解析
tool_call = response.tool_calls[0]
function_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

# 调用
result = tools[function_name](**arguments)
# 结果：明天北京多云，15-22℃
```

**第五步：返回结果**

```python
# 将结果告诉LLM
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": result
})

# LLM生成最终回答
"明天北京多云，温度15-22℃，适合出行。"
```

**Tool Calling vs 普通Prompt的区别：**

**普通Prompt方式：**
```
Prompt: "你有get_weather工具，请调用它"
LLM: "调用get_weather工具，参数city=北京"
你: 需要自己解析这段文本 😓
```

**Tool Calling方式：**
```
Tools: [weather_tool_schema]
LLM: {直接返回结构化的tool_call} ✅
你: 直接用，无需解析 😄
```

**为什么Tool Calling这么重要？**

**1. 可靠性**
```
结构化输出 → 不会解析错误
参数类型检查 → 减少错误
```

**2. 可扩展性**
```
标准协议 → 易于添加新工具
任何工具都用同样的方式调用
```

**3. 性能**
```
模型原生支持 → 更快
不需要复杂的Prompt → 省token
```

**4. 开发体验**
```
清晰的接口 → 易于开发
统一的标准 → 易于维护
```

**今天这一课，我要带你：**

**第一部分：Tool Calling协议**
- OpenAI标准
- 工具定义格式
- 参数Schema

**第二部分：Tool Calling流程**
- 工具注册
- LLM调用
- 结果处理

**第三部分：参数验证**
- JSON Schema
- 类型检查
- 错误处理

**第四部分：完整实现**
- 标准化工具类
- 调用管理器
- 最佳实践

**第五部分：高级特性**
- 多工具调用
- 并行调用
- 条件调用

学完这一课，你将掌握Tool Calling的完整原理！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【标准化的力量】

没有标准：
• 每个工具不同实现
• 难以维护
• 容易出错

有了标准：
• 统一协议
• 易于扩展
• 可靠稳定

Tool Calling = 工具调用的HTTP协议
```

---

## 📚 第一部分：Tool Calling协议详解

### 一、OpenAI Function Calling标准

```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json

@dataclass
class FunctionParameter:
    """函数参数定义"""
    type: str  # string, number, boolean, object, array
    description: str
    enum: Optional[List] = None  # 枚举值

@dataclass
class FunctionDefinition:
    """函数定义（Tool Schema）"""
    name: str
    description: str
    parameters: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """转为字典"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

class ToolSchemaBuilder:
    """工具Schema构建器"""
    
    @staticmethod
    def build_schema(
        name: str,
        description: str,
        parameters: Dict[str, Dict],
        required: List[str] = None
    ) -> FunctionDefinition:
        """
        构建工具Schema
        
        参数格式：
        {
            "param_name": {
                "type": "string",
                "description": "参数描述",
                "enum": ["选项1", "选项2"]  # 可选
            }
        }
        """
        
        # 构建JSON Schema格式的parameters
        param_schema = {
            "type": "object",
            "properties": {},
            "required": required or []
        }
        
        for param_name, param_def in parameters.items():
            param_schema["properties"][param_name] = {
                "type": param_def["type"],
                "description": param_def["description"]
            }
            
            if "enum" in param_def:
                param_schema["properties"][param_name]["enum"] = param_def["enum"]
        
        return FunctionDefinition(
            name=name,
            description=description,
            parameters=param_schema
        )

# 示例：定义工具
def demo_tool_schema():
    """演示工具Schema定义"""
    
    print("="*60)
    print("工具Schema示例")
    print("="*60 + "\n")
    
    # 1. 天气查询工具
    weather_schema = ToolSchemaBuilder.build_schema(
        name="get_weather",
        description="获取指定城市的天气信息",
        parameters={
            "city": {
                "type": "string",
                "description": "城市名称，如'北京'、'上海'"
            },
            "date": {
                "type": "string",
                "description": "日期，如'今天'、'明天'、'后天'",
                "enum": ["今天", "明天", "后天"]
            }
        },
        required=["city"]
    )
    
    print("【天气查询工具】")
    print(json.dumps(weather_schema.to_dict(), indent=2, ensure_ascii=False))
    
    # 2. 计算器工具
    print("\n" + "-"*60 + "\n")
    
    calculator_schema = ToolSchemaBuilder.build_schema(
        name="calculate",
        description="计算数学表达式",
        parameters={
            "expression": {
                "type": "string",
                "description": "数学表达式，如'2+3*4'"
            }
        },
        required=["expression"]
    )
    
    print("【计算器工具】")
    print(json.dumps(calculator_schema.to_dict(), indent=2, ensure_ascii=False))
    
    # 3. 搜索工具
    print("\n" + "-"*60 + "\n")
    
    search_schema = ToolSchemaBuilder.build_schema(
        name="search",
        description="在网络上搜索信息",
        parameters={
            "query": {
                "type": "string",
                "description": "搜索关键词"
            },
            "num_results": {
                "type": "number",
                "description": "返回结果数量",
            }
        },
        required=["query"]
    )
    
    print("【搜索工具】")
    print(json.dumps(search_schema.to_dict(), indent=2, ensure_ascii=False))

demo_tool_schema()
```

---

## 💻 第二部分：Tool Calling完整流程

### 一、Tool Calling管理器

```python
from typing import Callable
import inspect

@dataclass
class ToolCall:
    """工具调用信息"""
    id: str
    function_name: str
    arguments: Dict[str, Any]

@dataclass
class ToolResult:
    """工具执行结果"""
    tool_call_id: str
    success: bool
    result: Any = None
    error: str = None

class ToolCallingManager:
    """Tool Calling管理器"""
    
    def __init__(self, llm):
        self.llm = llm
        self.tools: Dict[str, Dict] = {}
        self.tool_functions: Dict[str, Callable] = {}
    
    def register_tool(
        self,
        func: Callable,
        name: str = None,
        description: str = None,
        parameters: Dict = None
    ):
        """
        注册工具
        
        可以自动从函数提取Schema，也可以手动指定
        """
        # 使用函数名作为工具名
        tool_name = name or func.__name__
        
        # 如果没有提供description，从docstring提取
        if description is None:
            description = func.__doc__ or f"调用{tool_name}"
        
        # 如果没有提供parameters，从函数签名提取
        if parameters is None:
            parameters = self._extract_parameters_from_function(func)
        
        # 构建Schema
        schema = ToolSchemaBuilder.build_schema(
            name=tool_name,
            description=description,
            parameters=parameters,
            required=list(parameters.keys())
        )
        
        # 注册
        self.tools[tool_name] = schema.to_dict()
        self.tool_functions[tool_name] = func
        
        print(f"✅ 注册工具: {tool_name}")
    
    def _extract_parameters_from_function(self, func: Callable) -> Dict:
        """从函数签名自动提取参数"""
        
        sig = inspect.signature(func)
        parameters = {}
        
        for param_name, param in sig.parameters.items():
            # 获取类型
            param_type = "string"  # 默认
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int or param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
            
            parameters[param_name] = {
                "type": param_type,
                "description": f"参数{param_name}"
            }
        
        return parameters
    
    def call_llm_with_tools(
        self,
        messages: List[Dict],
        verbose: bool = True
    ) -> Dict:
        """
        调用LLM（带工具）
        
        返回：LLM响应，可能包含tool_calls
        """
        if verbose:
            print("\n" + "="*60)
            print("调用LLM（带工具）")
            print("="*60)
        
        # 将tools添加到LLM调用中
        response = self.llm.invoke(
            messages,
            tools=list(self.tools.values())
        )
        
        if verbose:
            if hasattr(response, 'tool_calls') and response.tool_calls:
                print(f"\nLLM选择调用 {len(response.tool_calls)} 个工具:")
                for tc in response.tool_calls:
                    print(f"  • {tc.function.name}({tc.function.arguments})")
            else:
                print(f"\nLLM直接回复:")
                print(f"  {response.content[:100]}...")
        
        return response
    
    def execute_tool_calls(
        self,
        tool_calls: List,
        verbose: bool = True
    ) -> List[ToolResult]:
        """执行工具调用"""
        
        if verbose:
            print("\n" + "="*60)
            print("执行工具调用")
            print("="*60)
        
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if verbose:
                print(f"\n执行: {function_name}({arguments})")
            
            # 获取函数
            func = self.tool_functions.get(function_name)
            
            if not func:
                result = ToolResult(
                    tool_call_id=tool_call.id,
                    success=False,
                    error=f"工具{function_name}不存在"
                )
            else:
                try:
                    # 调用函数
                    output = func(**arguments)
                    
                    result = ToolResult(
                        tool_call_id=tool_call.id,
                        success=True,
                        result=output
                    )
                    
                    if verbose:
                        print(f"  ✅ 成功: {output}")
                except Exception as e:
                    result = ToolResult(
                        tool_call_id=tool_call.id,
                        success=False,
                        error=str(e)
                    )
                    
                    if verbose:
                        print(f"  ❌ 失败: {str(e)}")
            
            results.append(result)
        
        return results
    
    def format_tool_results_for_llm(
        self,
        tool_results: List[ToolResult]
    ) -> List[Dict]:
        """格式化工具结果为LLM消息"""
        
        messages = []
        
        for result in tool_results:
            messages.append({
                "role": "tool",
                "tool_call_id": result.tool_call_id,
                "content": str(result.result) if result.success else f"错误：{result.error}"
            })
        
        return messages

# 完整演示
def demo_tool_calling_manager():
    """演示Tool Calling Manager"""
    
    from langchain.chat_models import ChatOpenAI
    
    # 初始化
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    manager = ToolCallingManager(llm)
    
    # 注册工具
    def get_weather(city: str, date: str = "今天") -> str:
        """获取天气"""
        return f"{city}{date}的天气是晴天，20-28℃"
    
    def calculate(expression: str) -> str:
        """计算数学表达式"""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except:
            return "计算错误"
    
    manager.register_tool(get_weather, description="获取指定城市的天气")
    manager.register_tool(calculate, description="计算数学表达式")
    
    # 测试对话
    print("\n" + "🤖"*30)
    print("测试Tool Calling")
    print("🤖"*30)
    
    messages = [
        {"role": "user", "content": "明天北京的天气怎么样？"}
    ]
    
    # 第一轮：LLM可能返回tool_calls
    response = manager.call_llm_with_tools(messages, verbose=True)
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        # 执行工具
        tool_results = manager.execute_tool_calls(response.tool_calls, verbose=True)
        
        # 将结果返回给LLM
        messages.append(response.message)
        messages.extend(manager.format_tool_results_for_llm(tool_results))
        
        # 第二轮：LLM生成最终回答
        final_response = manager.call_llm_with_tools(messages, verbose=True)
        print(f"\n最终回答: {final_response.content}")

# demo_tool_calling_manager()
```

---

## 📝 课后练习

### 练习1：参数验证
实现完整的JSON Schema验证

### 练习2：错误重试
工具调用失败时自动重试

### 练习3：工具文档
自动生成工具使用文档

---

## 🎓 知识总结

### 核心要点

1. **Tool Calling标准**
   - 结构化输出
   - JSON Schema
   - 统一协议

2. **核心流程**
   - 工具定义
   - LLM调用
   - 工具执行
   - 结果返回

3. **关键组件**
   - Tool Schema
   - Tool Call
   - Tool Result

4. **最佳实践**
   - 清晰的描述
   - 完整的参数定义
   - 良好的错误处理

---

## 🚀 下节预告

下一课：**第77课：Function Calling深入**

- OpenAI Function Calling
- 参数提取
- 多轮对话
- 复杂场景

**深入Function Calling！** 🔧

---

**💪 记住：Tool Calling让AI更强大！**

**下一课见！** 🎉
