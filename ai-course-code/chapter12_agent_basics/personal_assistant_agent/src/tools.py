"""
工具实现层
包含6个实用工具：天气查询、日程管理、信息搜索、计算器、笔记记录、汇率转换
"""
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0


class Tool:
    """工具基类 - 统一接口"""

    def __init__(self, name: str, description: str, func: Callable, parameters: Dict = None):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}

    def run(self, **kwargs) -> ToolResult:
        """执行工具，自动计时和错误捕获"""
        start_time = time.time()
        try:
            result = self.func(**kwargs)
            return ToolResult(
                success=True,
                result=result,
                execution_time=time.time() - start_time,
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
            )


class PersonalAssistantTools:
    """个人助手工具集 - 集成6个工具"""

    def __init__(self):
        # 模拟数据存储
        self.calendar: list = []
        self.notes: list = []
        # 注册所有工具
        self.tools: Dict[str, Tool] = self._register_tools()

    def _register_tools(self) -> Dict[str, Tool]:
        """注册所有工具"""
        tools = {}

        # 1. 天气查询
        tools["get_weather"] = Tool(
            name="get_weather",
            description='获取指定日期的天气信息，参数：date（如"今天"、"明天"、"后天"）',
            func=self._get_weather,
        )
        # 2. 添加日程
        tools["add_calendar"] = Tool(
            name="add_calendar",
            description="添加日程，参数：time（时间）、event（事件描述）",
            func=self._add_calendar,
        )
        # 3. 查看日程
        tools["list_calendar"] = Tool(
            name="list_calendar",
            description="查看日程列表，无需参数",
            func=self._list_calendar,
        )
        # 4. 搜索
        tools["search"] = Tool(
            name="search",
            description="搜索信息，参数：query（搜索关键词）",
            func=self._search,
        )
        # 5. 计算器
        tools["calculate"] = Tool(
            name="calculate",
            description='计算数学表达式，参数：expression（如"2+3*4"）',
            func=self._calculate,
        )
        # 6. 添加笔记
        tools["add_note"] = Tool(
            name="add_note",
            description="添加笔记，参数：content（笔记内容）",
            func=self._add_note,
        )
        # 7. 查看笔记
        tools["list_notes"] = Tool(
            name="list_notes",
            description="查看笔记列表，无需参数",
            func=self._list_notes,
        )
        # 8. 汇率转换
        tools["convert_currency"] = Tool(
            name="convert_currency",
            description="货币转换，参数：amount（金额）、from_currency（源货币如USD）、to_currency（目标货币如CNY）",
            func=self._convert_currency,
        )
        return tools

    # ===== 工具实现 =====

    def _get_weather(self, date: str = "今天") -> str:
        """获取天气（模拟数据）"""
        weather_data = {
            "今天": "☀️ 晴，20-28℃，空气质量良好",
            "明天": "🌧️ 多云转雨，18-25℃，降水概率70%，建议带伞",
            "后天": "🌧️ 小雨，15-22℃，降水概率85%",
        }
        return weather_data.get(date, f"📅 {date}：晴，20-25℃（预测数据）")

    def _add_calendar(self, time: str, event: str) -> str:
        """添加日程"""
        if not time or not event:
            raise ValueError("时间和事件描述不能为空")
        self.calendar.append({
            "time": time,
            "event": event,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        return f"✅ 已添加日程：{time} - {event}"

    def _list_calendar(self) -> str:
        """查看日程"""
        if not self.calendar:
            return "📅 暂无日程安排"
        lines = ["📅 您的日程："]
        for i, item in enumerate(self.calendar, 1):
            lines.append(f"  {i}. {item['time']} - {item['event']}")
        return "\n".join(lines)

    def _search(self, query: str) -> str:
        """搜索信息（模拟）"""
        if not query:
            raise ValueError("搜索关键词不能为空")
        # 模拟搜索结果
        results = {
            "Python装饰器": "Python装饰器是一种设计模式，用@语法糖实现。\n1. 函数装饰器：用于增强函数功能\n2. 类装饰器：用于修改类行为\n3. 常见内置装饰器：@property, @staticmethod, @classmethod",
            "机器学习": "机器学习是AI的子领域，主要分为：\n1. 监督学习：分类、回归\n2. 无监督学习：聚类、降维\n3. 强化学习：策略优化",
        }
        if query in results:
            return f"🔍 关于'{query}'的搜索结果：\n{results[query]}"
        return f"🔍 关于'{query}'的搜索结果：\n1. {query}相关文档1\n2. {query}相关文档2\n3. {query}相关文档3"

    def _calculate(self, expression: str) -> str:
        """安全计算器"""
        if not expression:
            raise ValueError("表达式不能为空")
        # 只允许数字和基本运算符
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            raise ValueError(f"不安全的表达式：{expression}")
        try:
            result = eval(expression)
            return f"🧮 {expression} = {result}"
        except Exception as e:
            raise ValueError(f"计算错误：{str(e)}")

    def _add_note(self, content: str) -> str:
        """添加笔记"""
        if not content:
            raise ValueError("笔记内容不能为空")
        self.notes.append({
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        preview = content[:50] + "..." if len(content) > 50 else content
        return f"📝 已保存笔记：{preview}"

    def _list_notes(self) -> str:
        """查看笔记"""
        if not self.notes:
            return "📝 暂无笔记"
        lines = ["📝 您的笔记："]
        for i, note in enumerate(self.notes, 1):
            preview = note["content"][:50] + "..." if len(note["content"]) > 50 else note["content"]
            lines.append(f"  {i}. {preview} ({note['created_at']})")
        return "\n".join(lines)

    def _convert_currency(self, amount: str, from_currency: str, to_currency: str) -> str:
        """汇率转换（模拟汇率）"""
        try:
            amount_float = float(amount)
        except (ValueError, TypeError):
            raise ValueError(f"无效金额：{amount}")

        rates = {
            "USD_CNY": 7.24, "CNY_USD": 0.138,
            "EUR_CNY": 7.85, "CNY_EUR": 0.127,
            "USD_EUR": 0.92, "EUR_USD": 1.09,
            "GBP_CNY": 9.15, "CNY_GBP": 0.109,
            "JPY_CNY": 0.048, "CNY_JPY": 20.83,
        }
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        rate_key = f"{from_currency}_{to_currency}"
        rate = rates.get(rate_key)
        if rate is None:
            raise ValueError(f"不支持的货币对：{from_currency} → {to_currency}")
        result = amount_float * rate
        return f"💰 {amount_float:.2f} {from_currency} = {result:.2f} {to_currency}（汇率：{rate}）"

    def get_tools_description(self) -> str:
        """获取所有工具描述（供Agent使用）"""
        lines = []
        for name, tool in self.tools.items():
            lines.append(f"- {name}: {tool.description}")
        return "\n".join(lines)
