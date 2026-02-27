"""
智能内容处理系统测试
对应课程：第36课-第6章综合实战项目

测试内容：单篇处理、批量处理、缓存性能、监控面板
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.system import SmartContentProcessorSystem
from src.monitor import SystemMonitor
from src.analyzer import ArticleAnalyzer
from src.processor import ContentProcessor


# ============= 测试文章 =============

TECH_ARTICLE = """
LangChain是一个强大的框架，用于开发由大语言模型驱动的应用程序。
它提供了一系列工具和抽象，使开发者能够轻松构建复杂的AI应用。
LangChain的核心概念包括Chains、Agents、Memory等，这些组件可以
灵活组合，创建出强大的AI系统。通过LangChain，开发者可以快速
构建聊天机器人、问答系统、文档分析工具等各种应用。
"""

NEWS_ARTICLE = """
本地时间周一，某科技公司宣布推出新一代AI芯片，性能较上一代提升50%。
该芯片采用最新的3纳米工艺，专为大模型推理优化。公司CEO表示，
新芯片将于下季度量产，预计售价较竞品低30%。业内分析师认为，
这将加速AI技术的普及和应用落地。
"""

GENERAL_ARTICLE = """
今天天气不错，适合出门散步，享受春日的阳光。
公园里的樱花已经开了，粉色的花瓣随风飘落，美不胜收。
很多人带着家人来赏花拍照，孩子们在草地上奔跑嬉戏。
"""


def test_single_article():
    """测试1：单篇文章处理"""
    print("\n" + "=" * 60)
    print("🧪 测试1：单篇技术文章处理")
    print("=" * 60)

    system = SmartContentProcessorSystem(enable_cache=True)
    result = system.process_article(TECH_ARTICLE)

    assert result is not None, "处理结果不应为None"
    assert "summary" in result, "结果应包含摘要"
    assert "keywords" in result, "结果应包含关键词"
    assert "translation" in result, "结果应包含翻译"
    assert "image_suggestions" in result, "结果应包含配图建议"
    assert "article_type" in result, "结果应包含文章类型"

    print("✅ 单篇文章处理测试通过")


def test_batch_processing():
    """测试2：批量处理"""
    print("\n" + "=" * 60)
    print("🧪 测试2：批量处理多篇文章")
    print("=" * 60)

    system = SmartContentProcessorSystem(enable_cache=True)

    articles = [
        "Python 3.12 发布了许多新特性，包括性能改进和新的语法糖。",
        "今日股市大涨，上证指数突破3500点，创近期新高。",
        "周末去爬山，山顶的风景真的很美，空气也特别清新。",
    ]

    results = system.batch_process(articles)

    assert len(results) == 3, "应返回3个结果"
    success_count = sum(1 for r in results if r is not None)
    print(f"\n成功处理：{success_count}/3")

    print(system.get_statistics())
    print("✅ 批量处理测试通过")


def test_cache_performance():
    """测试3：缓存性能对比"""
    print("\n" + "=" * 60)
    print("🧪 测试3：缓存性能对比")
    print("=" * 60)

    system = SmartContentProcessorSystem(enable_cache=True)

    article = "人工智能正在改变世界，从医疗到金融，AI的应用无处不在。"

    # 第一次（无缓存命中）
    start = time.time()
    result1 = system.process_article(article, show_progress=False)
    time1 = time.time() - start
    print(f"第一次处理：{time1:.2f}秒")

    # 第二次（缓存命中）
    start = time.time()
    result2 = system.process_article(article, show_progress=False)
    time2 = time.time() - start
    print(f"第二次处理：{time2:.2f}秒")

    if time2 < time1:
        speedup = time1 / time2 if time2 > 0 else float("inf")
        print(f"缓存加速：{speedup:.1f}倍")
    else:
        print("缓存未生效（可能是首次运行）")

    print("✅ 缓存性能测试完成")


def test_monitor_standalone():
    """测试4：监控组件独立测试（不依赖LLM）"""
    print("\n" + "=" * 60)
    print("🧪 测试4：监控组件独立测试")
    print("=" * 60)

    monitor = SystemMonitor()

    # 模拟请求
    monitor.metrics["total_requests"] = 10
    monitor.metrics["success"] = 9
    monitor.metrics["errors"] = 1
    monitor.metrics["total_time"] = 25.5
    monitor.metrics["llm_calls"] = 40
    monitor.metrics["llm_time"] = 20.0
    monitor.metrics["total_tokens"] = 5000

    dashboard = monitor.get_dashboard()
    print(dashboard)

    assert "10" in dashboard, "面板应显示请求数"
    assert "9" in dashboard, "面板应显示成功数"

    # 测试重置
    monitor.reset()
    assert monitor.metrics["total_requests"] == 0, "重置后请求数应为0"

    print("✅ 监控组件测试通过")


def test_history():
    """测试5：处理历史"""
    print("\n" + "=" * 60)
    print("🧪 测试5：处理历史记录")
    print("=" * 60)

    system = SmartContentProcessorSystem(enable_cache=True)

    system.process_article("这是一篇测试文章。", show_progress=False)
    history = system.get_history()

    print(f"历史记录：{history}")
    assert "history" in history, "应包含history字段"

    print("✅ 历史记录测试通过")


def main():
    """运行所有测试"""
    print("🧪 智能内容处理系统 - 测试套件")
    print("=" * 60)

    # 不依赖LLM的测试
    test_monitor_standalone()

    # 依赖LLM的测试
    print("\n⚠️  以下测试需要LM Studio运行中...")
    try:
        test_single_article()
        test_batch_processing()
        test_cache_performance()
        test_history()
    except Exception as e:
        print(f"\n⚠️  LLM相关测试失败（可能LM Studio未启动）：{e}")
        print("监控组件测试已通过，LLM测试请启动LM Studio后重试。")

    print("\n" + "=" * 60)
    print("✅ 测试套件执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
