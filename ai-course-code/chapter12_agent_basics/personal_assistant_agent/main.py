"""
第75课：智能个人助手Agent - 主程序入口

功能：
- 交互模式：CLI对话界面
- 演示模式：自动运行测试场景

使用方法：
    python main.py          # 交互模式
    python main.py --demo   # 演示模式
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent import PersonalAssistantAgent


def interactive_mode():
    """交互模式 - CLI对话界面"""
    agent = PersonalAssistantAgent()

    print("=" * 60)
    print("🤖 智能个人助手Agent v1.0")
    print("=" * 60)
    print("\n可用功能:")
    print("  • 🌤️  天气查询    例：明天天气怎么样？")
    print("  • 📅 日程管理    例：帮我添加明天下午3点的会议")
    print("  • 🔍 信息搜索    例：搜索Python装饰器的用法")
    print("  • 🧮 计算器      例：计算 (123+456)*2")
    print("  • 📝 笔记记录    例：记录一下今天的学习要点")
    print("  • 💰 汇率转换    例：100美元等于多少人民币？")
    print("\n输入 'quit' 或 'exit' 退出")
    print("输入 'stats' 查看统计信息")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("你: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "退出"):
                print("\n再见！👋")
                agent.print_stats()
                break
            if user_input.lower() == "stats":
                agent.print_stats()
                continue

            agent.run(user_input, verbose=True)

        except KeyboardInterrupt:
            print("\n\n再见！👋")
            agent.print_stats()
            break
        except Exception as e:
            print(f"\n错误：{str(e)}\n")


def demo_mode():
    """演示模式 - 自动运行测试场景"""
    agent = PersonalAssistantAgent()

    print("=" * 60)
    print("🤖 智能个人助手Agent - 演示模式")
    print("=" * 60)

    scenarios = [
        "明天的天气怎么样？",
        "帮我添加一个明天下午3点的会议",
        "100美元等于多少人民币？",
        "计算 (123 + 456) * 2",
        "帮我搜索Python装饰器的用法",
        "查看我的日程",
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'=' * 60}")
        print(f"📋 场景 {i}/{len(scenarios)}")
        print(f"{'=' * 60}")
        agent.run(scenario, verbose=True)

    agent.print_stats()


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo_mode()
    else:
        interactive_mode()
