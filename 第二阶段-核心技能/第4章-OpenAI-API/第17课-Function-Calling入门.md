![函数调用](./images/function_call.svg)
*图：Function Calling让AI能够调用外部工具*

# 第17课：Function Calling入门 - 让AI调用工具

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第4章 - API调用基础（第2/7课）
> - 学习目标：掌握Function Calling，让AI能够调用外部工具和API
> - 预计时间：70-80分钟
> - 前置知识：第16课

---

## 📢 课程导入

### 前言

想象一下，你问AI"北京今天天气怎么样"，它不是编造一个答案，而是真的去调用天气API查询，然后告诉你准确的天气！或者你说"帮我计算123乘456"，它真的去调用计算器函数，给你精确的答案！

这就是今天要学的Function Calling——OpenAI最强大的功能之一！它让AI从一个只会"说话"的聊天机器人，变成了一个能"做事"的智能助手！这是AI从对话到行动的关键技术！

---

### 核心价值点

**第一，Function Calling是AI应用开发的核心技术。**

为什么Function Calling这么重要？因为它解决了AI的根本局限：
- **不再编造**：以前AI不知道就会瞎编，现在可以调用工具获取真实数据
- **能力扩展**：AI不再只会聊天，可以查数据库、调API、操作系统
- **精确可控**：不是自由发挥，而是按你定义的规则执行
- **Agent基础**：这是构建Agent（智能体）的核心技术

可以说，没有Function Calling，就没有真正的AI应用！

**第二，Function Calling的工作原理非常优雅。**

你不需要训练模型，不需要微调，只需要：
1. 用JSON告诉AI有哪些函数可用
2. AI分析用户意图，决定调用哪个函数
3. 你的代码执行函数，获取结果
4. 把结果返回给AI，生成最终回复

整个过程优雅、可控、可扩展！这就是OpenAI设计的精妙之处！

**第三，Function Calling能解决海量实际问题。**

想想你可以用它做什么：
- **智能客服**：查订单、查物流、查库存
- **数据分析**：查询数据库、生成图表、导出报告
- **自动化**：发邮件、创建日程、操作文件
- **工具集成**：调用任何API、任何系统

几乎所有需要"AI+工具"的场景，都需要Function Calling！

**第四，这是Agent开发的第一步。**

后面我们会学Agent（智能体），它的核心就是Function Calling的延伸。如果你现在不学好Function Calling，后面学Agent会很吃力。

但如果你深入理解了Function Calling，Agent对你来说就是水到渠成！这就是循序渐进学习的重要性！

---

### 行动号召

今天这一课会教你：
- Function Calling的完整工作流程
- 如何定义函数schema（函数描述）
- 如何处理AI的函数调用请求
- 实战案例：天气查询、计算器、数据库查询
- 最佳实践和注意事项

**学完这课，你就能开发真正的智能助手了！**

---

## 📖 知识讲解

### 1. Function Calling概述

#
![Api Architecture](./images/api_architecture.svg)
*图：Api Architecture*

### 1.1 什么是Function Calling

```
Function Calling（函数调用）：
OpenAI提供的能力，让GPT模型能够：
1. 理解用户需要调用哪个函数
2. 提取函数所需的参数
3. 以结构化格式返回调用信息

注意：
⚠️ AI不会真正执行函数
⚠️ 它只是告诉你"应该调用哪个函数，用什么参数"
⚠️ 真正执行函数是你的代码的责任
```

#### 1.2 工作流程

```
完整流程：

步骤1：定义可用函数
你：我有这些函数可用（JSON schema）
    - get_weather(location)
    - calculator(expression)

步骤2：用户提问
用户："北京今天天气怎么样？"

步骤3：AI分析并返回函数调用
AI：{
  "name": "get_weather",
  "arguments": {"location": "北京"}
}

步骤4：你的代码执行函数
你的代码：调用天气API获取数据
结果：{"temperature": 15, "condition": "晴"}

步骤5：把结果返回给AI
你：这是get_weather的结果：{"temperature": 15, "condition": "晴"}

步骤6：AI生成最终回复
AI："北京今天天气晴朗，温度15度，适合外出。"
```

---

### 2. 函数定义（Schema）

#### 2.1 Schema格式

```json
{
  "name": "get_weather",
  "description": "获取指定城市的天气信息",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "城市名称，例如：北京、上海"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "温度单位"
      }
    },
    "required": ["location"]
  }
}
```

#### 2.2 Schema要素

```
必需字段：
1. name：函数名称
   - 使用小写字母和下划线
   - 见名知意
   - 例：get_weather、send_email

2. description：函数描述
   - 清晰描述函数的作用
   - 帮助AI理解何时调用
   - 例："获取指定城市的实时天气信息"

3. parameters：参数定义
   - type: "object"
   - properties: 各参数的定义
   - required: 必需参数列表

参数定义：
- type：数据类型（string、number、boolean、array、object）
- description：参数说明（AI靠这个理解参数含义）
- enum：可选值列表（限制取值范围）
- required：必需参数列表
```

#### 2.3 Schema最佳实践

```
✅ 好的Schema：
{
  "name": "search_products",
  "description": "搜索电商平台的商品信息",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "搜索关键词，例如：手机、笔记本电脑"
      },
      "category": {
        "type": "string",
        "enum": ["electronics", "clothing", "books"],
        "description": "商品分类"
      },
      "max_price": {
        "type": "number",
        "description": "最高价格（元）"
      }
    },
    "required": ["query"]
  }
}

特点：
✅ 描述清晰具体
✅ 有示例说明
✅ 使用enum限制选项
✅ 明确必需参数

❌ 不好的Schema：
{
  "name": "search",
  "description": "搜索",
  "parameters": {
    "type": "object",
    "properties": {
      "q": {
        "type": "string",
        "description": "关键词"
      }
    }
  }
}

问题：
❌ 描述太简单，AI不知道搜什么
❌ 参数名q不清晰
❌ 缺少示例和说明
```

---

### 3. 完整实现流程

#### 3.1 基础示例

```python
from openai import OpenAI
import json

client = OpenAI()

# 步骤1：定义函数
def get_weather(location: str, unit: str = "celsius"):
    """实际的天气查询函数"""
    # 模拟API调用
    return {
        "location": location,
        "temperature": 15,
        "unit": unit,
        "condition": "晴天"
    }

# 步骤2：定义函数schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# 步骤3：第一次API调用
messages = [{"role": "user", "content": "北京今天天气怎么样？"}]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"  # 让AI自动决定是否调用函数
)

response_message = response.choices[0].message

# 步骤4：检查是否需要调用函数
if response_message.tool_calls:
    # 步骤5：执行函数调用
    tool_call = response_message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    
    # 步骤6：调用实际函数
    function_response = get_weather(**function_args)
    
    # 步骤7：把结果返回给AI
    messages.append(response_message)  # AI的回复
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": function_name,
        "content": json.dumps(function_response)
    })
    
    # 步骤8：第二次API调用，生成最终回复
    final_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    print(final_response.choices[0].message.content)
else:
    # 不需要调用函数，直接输出回复
    print(response_message.content)
```

---

### 4. tool_choice参数

```python
tool_choice参数控制AI如何使用函数：

1. "auto"（默认）
   - AI自动决定是否调用函数
   - 如果不需要，直接回答
   - 推荐使用

2. "none"
   - 强制不调用函数
   - 即使定义了函数也不用
   - 适合：只想要文本回复

3. {"type": "function", "function": {"name": "get_weather"}}
   - 强制调用指定函数
   - 适合：确定要调用某个函数

示例：
# Auto模式
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "你好"}],
    tools=tools,
    tool_choice="auto"  # AI判断：这个不需要调用函数
)
# 输出："你好！有什么可以帮助你的吗？"

# 强制调用
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "北京"}],
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_weather"}}
)
# 强制调用get_weather，即使只说了"北京"
```

---

### 5. 多函数调用

```python
# 定义多个函数
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气信息",
            "parameters": {...}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：123 + 456"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "搜索数据库",
            "parameters": {...}
        }
    }
]

# AI会根据用户问题自动选择合适的函数
# "北京天气" → get_weather
# "123 + 456" → calculator
# "查询用户信息" → search_database
```

---

## 💻 Demo案例：Function Calling实战

### 案例说明

实现一个多功能智能助手，支持天气查询、计算器、数据库查询。

### 代码实现

创建`function_calling_assistant.py`：

```python
"""
Function Calling智能助手
支持多种工具调用
"""

from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class FunctionCallingAssistant:
    """Function Calling助手"""
    
    def __init__(self):
        """初始化"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = self._define_tools()
        self.available_functions = {
            "get_weather": self.get_weather,
            "calculator": self.calculator,
            "get_current_time": self.get_current_time,
            "search_user": self.search_user
        }
    
    def _define_tools(self):
        """定义可用工具"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的实时天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市名称，例如：北京、上海、深圳"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "执行数学计算，支持加减乘除和基本运算",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "数学表达式，例如：123 + 456、10 * 20"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "获取当前时间",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_user",
                    "description": "根据用户ID查询用户信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "用户ID"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            }
        ]
    
    # ===== 实际工具函数 =====
    
    def get_weather(self, location: str) -> dict:
        """获取天气（模拟）"""
        # 实际应用中，这里调用真实的天气API
        weather_data = {
            "北京": {"temperature": 15, "condition": "晴天", "humidity": "45%"},
            "上海": {"temperature": 20, "condition": "多云", "humidity": "60%"},
            "深圳": {"temperature": 28, "condition": "雷阵雨", "humidity": "80%"}
        }
        
        return weather_data.get(location, {
            "temperature": 20,
            "condition": "未知",
            "humidity": "50%",
            "note": f"暂无{location}的数据"
        })
    
    def calculator(self, expression: str) -> dict:
        """计算器"""
        try:
            # 注意：eval有安全风险，生产环境应该使用安全的计算库
            result = eval(expression)
            return {
                "expression": expression,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "expression": expression,
                "error": str(e),
                "success": False
            }
    
    def get_current_time(self) -> dict:
        """获取当前时间"""
        now = datetime.now()
        return {
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "weekday": now.strftime("%A")
        }
    
    def search_user(self, user_id: str) -> dict:
        """查询用户（模拟数据库）"""
        # 模拟数据库查询
        users = {
            "001": {"name": "张三", "age": 25, "email": "zhangsan@example.com"},
            "002": {"name": "李四", "age": 30, "email": "lisi@example.com"},
            "003": {"name": "王五", "age": 28, "email": "wangwu@example.com"}
        }
        
        if user_id in users:
            return {"user_id": user_id, **users[user_id], "found": True}
        else:
            return {"user_id": user_id, "found": False, "message": "用户不存在"}
    
    # ===== 核心逻辑 =====
    
    def chat(self, user_message: str) -> str:
        """处理用户消息"""
        messages = [{"role": "user", "content": user_message}]
        
        # 第一次API调用
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # 检查是否需要调用函数
        if response_message.tool_calls:
            print(f"\n🔧 AI决定调用工具...")
            
            # 处理所有工具调用（可能多个）
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"   调用：{function_name}({function_args})")
                
                # 执行函数
                function_response = self.available_functions[function_name](**function_args)
                
                print(f"   结果：{function_response}")
                
                # 添加函数结果到消息
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_response, ensure_ascii=False)
                })
            
            # 第二次API调用，生成最终回复
            print(f"\n💬 AI生成最终回复...")
            final_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            return final_response.choices[0].message.content
        else:
            # 不需要调用函数
            return response_message.content


def main():
    """主函数：交互式测试"""
    print("="*60)
    print("Function Calling智能助手")
    print("="*60)
    print("\n支持的功能：")
    print("  1. 天气查询：'北京今天天气怎么样？'")
    print("  2. 数学计算：'帮我算一下 123 * 456'")
    print("  3. 时间查询：'现在几点了？'")
    print("  4. 用户查询：'查询用户001的信息'")
    print("\n输入 'quit' 退出\n")
    
    assistant = FunctionCallingAssistant()
    
    # 预设测试案例
    test_cases = [
        "北京今天天气怎么样？",
        "帮我计算 1234 + 5678",
        "现在几点了？",
        "查询用户001的信息",
        "你好"  # 不需要调用函数的情况
    ]
    
    print("【自动测试模式】\n")
    for i, question in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}/{len(test_cases)}")
        print(f"{'='*60}")
        print(f"用户：{question}")
        
        try:
            response = assistant.chat(question)
            print(f"助手：{response}")
        except Exception as e:
            print(f"错误：{e}")
    
    print(f"\n{'='*60}")
    print("【交互模式】")
    print(f"{'='*60}\n")
    
    # 交互模式
    while True:
        user_input = input("用户：").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("再见！")
            break
        
        try:
            response = assistant.chat(user_input)
            print(f"助手：{response}\n")
        except Exception as e:
            print(f"错误：{e}\n")


if __name__ == "__main__":
    main()
```

### 运行演示

```bash
# 确保OPENAI_API_KEY已配置
python function_calling_assistant.py
```

---

## 🎯 高级技巧

### 1. 并行函数调用

```python
# GPT-4-turbo支持一次调用多个函数
# 例如："北京和上海的天气分别是什么？"
# AI可能会返回两个tool_calls：
# 1. get_weather(location="北京")
# 2. get_weather(location="上海")

# 处理并行调用
for tool_call in response_message.tool_calls:
    # 执行每个函数
    function_response = execute_function(tool_call)
    # 收集结果
```

### 2. 函数链式调用

```python
# 有时需要多次往返
# 例如："查询用户001，然后发邮件给他"
# 第一次：调用search_user
# 第二次：根据查询结果，调用send_email

# 实现循环处理
while response_message.tool_calls:
    # 执行函数调用
    # 再次请求AI
    # 直到不再需要调用函数
```

### 3. 错误处理

```python
try:
    function_response = execute_function(...)
except Exception as e:
    # 把错误信息返回给AI
    function_response = {
        "error": str(e),
        "message": "函数执行失败"
    }

# AI会根据错误信息调整回复
# 例如："抱歉，查询天气时出现了错误..."
```

---

## 📊 最佳实践

### 1. Schema设计

```
✅ 描述要详细
✅ 参数说明要清楚
✅ 使用enum限制选项
✅ 提供示例
✅ 明确required参数

❌ 避免：
❌ 描述过于简单
❌ 参数名不清晰
❌ 缺少类型约束
```

### 2. 函数实现

```
✅ 函数要健壮（处理异常）
✅ 返回结构化数据（dict/JSON）
✅ 包含执行状态（success/error）
✅ 记录日志
✅ 设置超时

❌ 避免：
❌ 函数可能卡死
❌ 返回格式不统一
❌ 缺少错误处理
```

### 3. 安全性

```
⚠️ 重要：
- 验证函数参数（防止注入）
- 限制函数权限（最小权限原则）
- 不要用eval执行用户输入
- 敏感操作要二次确认
- 记录所有函数调用

示例：
def delete_user(user_id: str):
    # ❌ 危险
    # 直接删除，没有验证
    
    # ✅ 安全
    if not is_admin(current_user):
        return {"error": "权限不足"}
    if not confirm_delete():
        return {"error": "需要确认"}
    # 执行删除
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解Function Calling的工作原理
- [ ] 编写函数schema定义
- [ ] 处理AI的函数调用请求
- [ ] 实现完整的函数调用流程
- [ ] 处理多函数和错误情况
- [ ] 理解安全性注意事项

---

## 📝 下一课预告

**第18课：Streaming与异步处理**

下一课我们将学习：
- 如何在Function Calling中使用流式响应
- 异步API调用
- 提升用户体验的技巧
- 处理长时间运行的任务

**让你的AI应用更加流畅和高效！**

---

**🎉 恭喜你完成第17课！**

你已经掌握了Function Calling，AI从此能"做事"而不只是"说话"！

**下一步：** 继续学习更高级的API特性！

