"""
第4章-OpenAI API：Function Calling
对应课程：第17课-Function Calling入门

功能：让AI能够调用外部工具/函数
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()


def get_client():
    """获取AI客户端"""
    if os.getenv("OPENAI_API_KEY"):
        return OpenAI()
    else:
        return OpenAI(
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        )


def get_model():
    """获取模型名称"""
    if os.getenv("OPENAI_API_KEY"):
        return "gpt-3.5-turbo"
    else:
        return os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")


# ==================== 模拟的外部工具 ====================

def get_weather(location: str, unit: str = "celsius") -> dict:
    """模拟：获取天气信息"""
    # 实际项目中这里调用真实的天气API
    weather_data = {
        "北京": {"temperature": 15, "condition": "晴", "humidity": 45},
        "上海": {"temperature": 18, "condition": "多云", "humidity": 60},
        "广州": {"temperature": 25, "condition": "阴", "humidity": 75},
    }
    
    data = weather_data.get(location, {"temperature": 20, "condition": "未知", "humidity": 50})
    
    if unit == "fahrenheit":
        data["temperature"] = data["temperature"] * 9/5 + 32
    
    return {
        "location": location,
        "temperature": data["temperature"],
        "unit": unit,
        "condition": data["condition"],
        "humidity": data["humidity"]
    }


def calculator(expression: str) -> dict:
    """模拟：计算器"""
    try:
        # 注意：实际项目中要做安全检查，不能直接eval
        result = eval(expression)
        return {"expression": expression, "result": result, "success": True}
    except Exception as e:
        return {"expression": expression, "error": str(e), "success": False}


def search_products(query: str, max_results: int = 5) -> dict:
    """模拟：搜索商品"""
    # 模拟搜索结果
    products = [
        {"name": f"{query} 商品A", "price": 99.9, "rating": 4.5},
        {"name": f"{query} 商品B", "price": 199.9, "rating": 4.8},
        {"name": f"{query} 商品C", "price": 299.9, "rating": 4.2},
    ]
    return {"query": query, "results": products[:max_results]}


# ==================== 函数定义（Schema） ====================

TOOLS = [
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
                        "description": "城市名称，例如：北京、上海、广州"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，默认celsius"
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
            "description": "计算数学表达式，支持加减乘除",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，例如：2+3、10*5、100/4"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "搜索商品信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量，默认5"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 函数映射
FUNCTION_MAP = {
    "get_weather": get_weather,
    "calculator": calculator,
    "search_products": search_products
}


def call_with_tools(user_message: str):
    """完整的Function Calling流程"""
    client = get_client()
    model = get_model()
    
    messages = [{"role": "user", "content": user_message}]
    
    print(f"\n用户：{user_message}")
    
    # 第一次调用：让AI判断是否需要调用函数
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"  # auto让AI自己决定
    )
    
    assistant_message = response.choices[0].message
    
    # 检查是否有函数调用
    if assistant_message.tool_calls:
        print(f"\n[AI决定调用函数]")
        
        # 添加AI的回复到消息历史
        messages.append(assistant_message)
        
        # 执行每个函数调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"  函数：{function_name}")
            print(f"  参数：{function_args}")
            
            # 执行函数
            if function_name in FUNCTION_MAP:
                result = FUNCTION_MAP[function_name](**function_args)
                print(f"  结果：{result}")
            else:
                result = {"error": f"未知函数：{function_name}"}
            
            # 把函数结果添加到消息
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })
        
        # 第二次调用：让AI根据函数结果生成最终回复
        final_response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        final_answer = final_response.choices[0].message.content
        print(f"\nAI：{final_answer}")
        return final_answer
    else:
        # 不需要调用函数，直接返回AI的回复
        answer = assistant_message.content
        print(f"\nAI：{answer}")
        return answer


def demo_function_calling():
    """演示Function Calling"""
    print("=" * 60)
    print("Function Calling演示")
    print("=" * 60)
    print("""
Function Calling让AI能够：
1. 理解用户需要什么功能
2. 选择合适的函数
3. 提取参数
4. 你执行函数后，AI根据结果回答

本演示有3个函数：
- get_weather：查天气
- calculator：计算器
- search_products：搜索商品
""")
    
    # 测试不同场景
    test_cases = [
        "北京今天天气怎么样？",
        "帮我计算 123 乘以 456",
        "我想买一台笔记本电脑，有什么推荐？",
        "你好，介绍一下你自己"  # 不需要函数调用
    ]
    
    for case in test_cases:
        print("\n" + "-" * 60)
        call_with_tools(case)


if __name__ == "__main__":
    demo_function_calling()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\nFunction Calling核心流程：")
    print("  1. 定义函数Schema（JSON格式）")
    print("  2. 发送请求时带上tools参数")
    print("  3. AI返回tool_calls（函数名+参数）")
    print("  4. 你执行函数，获取结果")
    print("  5. 把结果发回给AI")
    print("  6. AI生成最终回复")

