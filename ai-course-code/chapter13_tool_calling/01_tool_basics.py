"""
第13章-Tool Calling：工具定义基础
对应课程：第73课-工具定义

Tool = 名称 + 描述 + 参数 + 执行函数
让LLM知道有什么工具，怎么用
"""


def demo_tool_structure():
    """工具结构讲解"""
    print("=" * 60)
    print("工具定义结构")
    print("=" * 60)
    
    print("""
一个完整的工具定义包含：

1. 名称（name）
   - 简洁明了
   - 如：search、calculator、send_email

2. 描述（description）
   - 告诉LLM这个工具能干什么
   - 非常重要！LLM靠描述决定是否使用
   - 如："搜索互联网获取最新信息"

3. 参数（parameters）
   - JSON Schema格式
   - 定义输入参数的类型和说明
   - LLM会根据这个生成参数

4. 执行函数（function）
   - 实际执行工具的代码
""")


def demo_tool_definition():
    """工具定义示例"""
    print("\n" + "=" * 60)
    print("工具定义示例")
    print("=" * 60)
    
    # 工具定义
    tools = [
        {
            "name": "search",
            "description": "搜索互联网获取最新信息，适用于需要实时数据的问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "calculator",
            "description": "数学计算工具，支持加减乘除、幂运算等",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 2+3*4"
                    }
                },
                "required": ["expression"]
            }
        },
        {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    ]
    
    import json
    for tool in tools:
        print(f"\n工具：{tool['name']}")
        print(f"描述：{tool['description']}")
        print(f"参数：{json.dumps(tool['parameters'], ensure_ascii=False, indent=2)}")


def demo_tool_execution():
    """工具执行示例"""
    print("\n" + "=" * 60)
    print("工具执行流程")
    print("=" * 60)
    
    # 工具函数
    def search(query):
        """模拟搜索"""
        return f"关于'{query}'的搜索结果：找到100条相关信息"
    
    def calculator(expression):
        """计算器"""
        try:
            result = eval(expression)
            return f"计算结果：{expression} = {result}"
        except:
            return "计算错误"
    
    def get_weather(city):
        """模拟天气查询"""
        weather_data = {
            "北京": "晴天，25°C",
            "上海": "多云，28°C",
            "深圳": "阵雨，30°C"
        }
        return weather_data.get(city, "未找到该城市")
    
    # 工具注册表
    tools = {
        "search": search,
        "calculator": calculator,
        "get_weather": get_weather
    }
    
    # 模拟LLM返回的工具调用
    llm_response = {
        "tool": "get_weather",
        "parameters": {"city": "北京"}
    }
    
    print(f"\n模拟LLM决定调用工具：")
    print(f"  工具：{llm_response['tool']}")
    print(f"  参数：{llm_response['parameters']}")
    
    # 执行工具
    tool_name = llm_response["tool"]
    params = llm_response["parameters"]
    
    if tool_name in tools:
        result = tools[tool_name](**params)
        print(f"  结果：{result}")


def demo_good_vs_bad_description():
    """好描述vs坏描述"""
    print("\n" + "=" * 60)
    print("工具描述的重要性")
    print("=" * 60)
    
    print("""
描述决定LLM会不会正确使用工具！

【坏描述】❌
name: search
description: "搜索"
问题：太简单，LLM不知道什么时候该用

【好描述】✅
name: search
description: "搜索互联网获取最新信息，适用于：
- 查询实时新闻
- 获取最新股价
- 了解当前天气
- 查找最新发布的内容
不适用于历史知识性问题"

关键点：
1. 说清楚能干什么
2. 说清楚什么时候用
3. 最好说清楚什么时候不该用
""")


if __name__ == "__main__":
    demo_tool_structure()
    demo_tool_definition()
    demo_tool_execution()
    demo_good_vs_bad_description()
    
    print("\n" + "=" * 60)
    print("✅ 工具定义基础学习完成！")
    print("\n核心要点：")
    print("  • 工具 = 名称 + 描述 + 参数 + 函数")
    print("  • 描述要详细，告诉LLM什么时候用")
    print("  • 参数用JSON Schema定义")

