"""
智能助手测试套件
对应课程：第28课-LangChain实战项目1

测试内容：基础对话、工具调用、上下文理解、错误处理
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.assistant import IntelligentAssistant
from src.tools import Tools
from src.conversation_manager import ConversationManager
from src.intent_classifier import IntentClassifier


def test_basic_chat():
    """测试1：基础对话"""
    print("\n" + "=" * 60)
    print("🧪 测试1：基础对话")
    print("=" * 60)

    assistant = IntelligentAssistant("test_chat")

    messages = [
        "你好",
        "你叫什么名字？",
        "你能做什么？",
    ]

    for msg in messages:
        result = assistant.chat(msg)
        print(f"\n用户：{msg}")
        print(f"助手：{result['response'][:100]}...")
        print(f"意图：{result.get('intent')}，置信度：{result.get('confidence', 0):.2f}")

    print("\n✅ 基础对话测试完成")


def test_tool_calls():
    """测试2：工具调用"""
    print("\n" + "=" * 60)
    print("🧪 测试2：工具调用")
    print("=" * 60)

    assistant = IntelligentAssistant("test_tools")

    tool_messages = [
        "现在几点了？",
        "北京的天气怎么样？",
        "帮我算一下 123 + 456",
    ]

    for msg in tool_messages:
        result = assistant.chat(msg)
        print(f"\n用户：{msg}")
        print(f"助手：{result['response'][:100]}...")
        if result.get("tool_used"):
            print(f"调用工具：{result['tool_used']}")

    print("\n✅ 工具调用测试完成")


def test_context():
    """测试3：上下文理解"""
    print("\n" + "=" * 60)
    print("🧪 测试3：上下文理解")
    print("=" * 60)

    assistant = IntelligentAssistant("test_context")

    conversation = [
        "我叫小明",
        "你还记得我叫什么吗？",
        "我喜欢Python编程",
        "你记得我喜欢什么吗？",
    ]

    for msg in conversation:
        result = assistant.chat(msg)
        print(f"\n用户：{msg}")
        print(f"助手：{result['response'][:100]}...")

    print("\n✅ 上下文理解测试完成")


def test_tools_standalone():
    """测试4：工具函数独立测试（不依赖LLM）"""
    print("\n" + "=" * 60)
    print("🧪 测试4：工具函数独立测试")
    print("=" * 60)

    tools = Tools()

    # 时间
    time_result = tools.get_current_time()
    print(f"\n当前时间：{time_result}")
    assert len(time_result) > 0, "时间结果不应为空"

    # 天气
    weather_result = tools.get_weather("北京")
    print(f"北京天气：{weather_result}")
    assert "北京" in weather_result, "天气结果应包含城市名"

    weather_unknown = tools.get_weather("火星")
    print(f"火星天气：{weather_unknown}")
    assert "无法获取" in weather_unknown, "未知城市应返回提示"

    # 计算器
    calc_result = tools.calculator("123 + 456")
    print(f"123+456：{calc_result}")
    assert "579" in calc_result, "计算结果应正确"

    calc_zero = tools.calculator("1/0")
    print(f"1/0：{calc_zero}")
    assert "零" in calc_zero or "错误" in calc_zero, "除零应报错"

    print("\n✅ 工具函数测试全部通过")


def test_conversation_manager():
    """测试5：对话管理器独立测试（不依赖LLM）"""
    print("\n" + "=" * 60)
    print("🧪 测试5：对话管理器测试")
    print("=" * 60)

    cm = ConversationManager(max_history=4)

    # 添加消息
    cm.add_message("s1", "user", "你好")
    cm.add_message("s1", "assistant", "你好！")
    cm.add_message("s1", "user", "天气如何")
    cm.add_message("s1", "assistant", "今天晴天")

    history = cm.get_history("s1")
    print(f"历史消息数：{len(history)}")
    assert len(history) == 4, "应有4条消息"

    # 测试裁剪
    cm.add_message("s1", "user", "第5条消息")
    history = cm.get_history("s1")
    print(f"裁剪后消息数：{len(history)}")
    assert len(history) == 4, "超出限制后应裁剪到4条"

    # 测试LLM格式
    llm_msgs = cm.get_messages_for_llm("s1")
    assert all("role" in m and "content" in m for m in llm_msgs)
    print(f"LLM格式消息数：{len(llm_msgs)}")

    # 测试摘要
    summary = cm.get_context_summary("s1")
    print(f"上下文摘要：{summary}")

    # 测试清除
    cm.clear_history("s1")
    assert len(cm.get_history("s1")) == 0
    print("清除后消息数：0")

    print("\n✅ 对话管理器测试全部通过")


def main():
    """运行所有测试"""
    print("🧪 智能助手测试套件")
    print("=" * 60)

    # 先运行不依赖LLM的测试
    test_tools_standalone()
    test_conversation_manager()

    # 再运行依赖LLM的测试（需要LM Studio运行）
    print("\n⚠️  以下测试需要LM Studio运行中...")
    try:
        test_basic_chat()
        test_tool_calls()
        test_context()
    except Exception as e:
        print(f"\n⚠️  LLM相关测试失败（可能LM Studio未启动）：{e}")
        print("工具函数和对话管理器测试已通过，LLM测试请启动LM Studio后重试。")

    print("\n" + "=" * 60)
    print("✅ 测试套件执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
