"""
工具集模块
对应课程：第28课-LangChain实战项目1

提供可供AI助手调用的工具函数：时间查询、天气查询、计算器、知识搜索
"""

from datetime import datetime
import math
import re


class Tools:
    """工具集合 - 提供各种实用工具供助手调用"""

    @staticmethod
    def get_current_time() -> str:
        """获取当前日期和时间"""
        now = datetime.now()
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday = weekdays[now.weekday()]
        return f"{now.strftime('%Y-%m-%d %H:%M:%S')} {weekday}"

    @staticmethod
    def get_weather(city: str) -> str:
        """
        获取天气信息（模拟数据）
        
        实际生产环境中应接入真实天气API（如和风天气、心知天气等）
        
        Args:
            city: 城市名称
        """
        # 模拟天气数据
        weather_data = {
            "北京": {"weather": "晴天", "temp": "15°C", "humidity": "35%", "wind": "北风3级"},
            "上海": {"weather": "多云", "temp": "20°C", "humidity": "65%", "wind": "东风2级"},
            "深圳": {"weather": "雷阵雨", "temp": "28°C", "humidity": "80%", "wind": "南风4级"},
            "广州": {"weather": "阴天", "temp": "25°C", "humidity": "70%", "wind": "东南风2级"},
            "杭州": {"weather": "小雨", "temp": "18°C", "humidity": "75%", "wind": "东风1级"},
            "成都": {"weather": "多云", "temp": "16°C", "humidity": "60%", "wind": "微风"},
        }

        if city in weather_data:
            d = weather_data[city]
            return (
                f"{city}天气：{d['weather']}，"
                f"温度{d['temp']}，湿度{d['humidity']}，{d['wind']}"
            )
        return f"{city}的天气数据暂时无法获取，请稍后再试"

    @staticmethod
    def calculator(expression: str) -> str:
        """
        安全计算器
        
        只允许数学运算，禁止执行任意代码
        
        Args:
            expression: 数学表达式，如 "123 + 456"
        """
        try:
            # 清理表达式，只保留数字和运算符
            cleaned = re.sub(r'[^\d+\-*/().%\s]', '', expression)
            if not cleaned.strip():
                return "无法识别的数学表达式"

            # 安全的eval：只允许数学相关的内置函数
            allowed_names = {
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "pow": pow,
            }
            result = eval(cleaned, {"__builtins__": {}}, allowed_names)
            return f"{cleaned.strip()} = {result}"
        except ZeroDivisionError:
            return "错误：除数不能为零"
        except Exception as e:
            return f"计算错误：{e}"

    @staticmethod
    def search_knowledge(query: str) -> str:
        """
        知识搜索（模拟）
        
        实际生产环境中应接入搜索API或RAG系统
        
        Args:
            query: 搜索关键词
        """
        # 模拟一些知识条目
        knowledge_base = {
            "python": "Python是一种高级编程语言，以简洁易读著称，广泛用于Web开发、数据科学、AI等领域。",
            "langchain": "LangChain是一个用于开发LLM应用的框架，提供了Prompt管理、Chain组合、Memory等核心功能。",
            "机器学习": "机器学习是人工智能的一个分支，通过数据和算法让计算机自动学习和改进，无需显式编程。",
            "深度学习": "深度学习是机器学习的子集，使用多层神经网络来学习数据的复杂模式和表示。",
        }

        query_lower = query.lower()
        for key, value in knowledge_base.items():
            if key in query_lower or query_lower in key:
                return value

        return f"关于'{query}'的信息暂未收录，建议查阅相关文档或搜索引擎。"


# 工具描述（用于AI理解每个工具的用途和参数）
TOOL_DESCRIPTIONS = {
    "get_current_time": {
        "name": "获取当前时间",
        "description": "获取当前日期和时间",
        "params": {},
    },
    "get_weather": {
        "name": "天气查询",
        "description": "查询指定城市的天气信息",
        "params": {"city": "城市名称，如：北京、上海"},
    },
    "calculator": {
        "name": "计算器",
        "description": "执行数学计算",
        "params": {"expression": "数学表达式，如：123 + 456"},
    },
    "search_knowledge": {
        "name": "知识搜索",
        "description": "搜索知识库中的信息",
        "params": {"query": "搜索关键词"},
    },
}
