"""
工具单元测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools import PersonalAssistantTools, Tool, ToolResult


def test_weather():
    """测试天气查询"""
    tools = PersonalAssistantTools()
    result = tools.tools["get_weather"].run(date="今天")
    assert result.success
    assert "晴" in result.result
    print(f"✅ 天气查询: {result.result}")


def test_calendar():
    """测试日程管理"""
    tools = PersonalAssistantTools()

    # 添加日程
    result = tools.tools["add_calendar"].run(time="明天下午3点", event="团队会议")
    assert result.success
    assert "已添加" in result.result
    print(f"✅ 添加日程: {result.result}")

    # 查看日程
    result = tools.tools["list_calendar"].run()
    assert result.success
    assert "团队会议" in result.result
    print(f"✅ 查看日程: {result.result}")


def test_calculator():
    """测试计算器"""
    tools = PersonalAssistantTools()
    result = tools.tools["calculate"].run(expression="(123+456)*2")
    assert result.success
    assert "1158" in result.result
    print(f"✅ 计算器: {result.result}")

    # 测试非法表达式
    result = tools.tools["calculate"].run(expression="import os")
    assert not result.success
    print(f"✅ 非法表达式拦截: {result.error}")


def test_search():
    """测试搜索"""
    tools = PersonalAssistantTools()
    result = tools.tools["search"].run(query="Python装饰器")
    assert result.success
    assert "装饰器" in result.result
    print(f"✅ 搜索: {result.result[:60]}...")


def test_notes():
    """测试笔记"""
    tools = PersonalAssistantTools()

    result = tools.tools["add_note"].run(content="今天学习了Agent开发")
    assert result.success
    print(f"✅ 添加笔记: {result.result}")

    result = tools.tools["list_notes"].run()
    assert result.success
    assert "Agent" in result.result
    print(f"✅ 查看笔记: {result.result}")


def test_currency():
    """测试汇率转换"""
    tools = PersonalAssistantTools()
    result = tools.tools["convert_currency"].run(amount="100", from_currency="USD", to_currency="CNY")
    assert result.success
    assert "724" in result.result
    print(f"✅ 汇率转换: {result.result}")


def test_tool_result():
    """测试ToolResult数据类"""
    r = ToolResult(success=True, result="ok", execution_time=0.1)
    assert r.success
    assert r.error is None
    print("✅ ToolResult数据类正常")


if __name__ == "__main__":
    test_weather()
    test_calendar()
    test_calculator()
    test_search()
    test_notes()
    test_currency()
    test_tool_result()
    print("\n🎉 所有工具测试通过！")
