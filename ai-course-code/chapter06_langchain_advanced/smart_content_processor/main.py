"""
智能内容处理系统 - 演示入口
第6章第36课：综合实战项目

运行方式：python main.py
"""

import time
from src.system import SmartContentProcessorSystem


def demo_single_article():
    """演示1：单篇文章处理"""
    print("\n" + "=" * 60)
    print("📌 演示1：单篇文章处理")
    print("=" * 60 + "\n")

    system = SmartContentProcessorSystem(enable_cache=True)

    article = """
LangChain是一个强大的框架，用于开发由大语言模型驱动的应用程序。
它提供了一系列工具和抽象，使开发者能够轻松构建复杂的AI应用。
LangChain的核心概念包括Chains、Agents、Memory等，这些组件可以
灵活组合，创建出强大的AI系统。通过LangChain，开发者可以快速
构建聊天机器人、问答系统、文档分析工具等各种应用。
"""

    result = system.process_article(article)
    print(system.get_statistics())


def demo_batch_processing():
    """演示2：批量处理"""
    print("\n" + "=" * 60)
    print("📌 演示2：批量处理多篇文章")
    print("=" * 60 + "\n")

    system = SmartContentProcessorSystem(enable_cache=True)

    articles = [
        "Python 3.12 发布了许多新特性，包括性能改进和新的语法糖，让开发者的编码体验更加流畅。",
        "本地时间周一，美国科技公司宣布推出新一代AI芯片，性能提升50%，将于下季度量产。",
        "今天天气不错，适合出门散步，享受春日的阳光。公园里的樱花已经开了，美不胜收。",
    ]

    results = system.batch_process(articles)
    print(system.get_statistics())


def demo_cache_performance():
    """演示3：缓存性能对比"""
    print("\n" + "=" * 60)
    print("📌 演示3：缓存性能对比")
    print("=" * 60 + "\n")

    system = SmartContentProcessorSystem(enable_cache=True)

    article = "人工智能正在改变世界，从医疗到金融，AI的应用无处不在。"

    # 第一次
    print("第一次处理（无缓存命中）：")
    start = time.time()
    system.process_article(article, show_progress=False)
    time1 = time.time() - start
    print(f"  耗时：{time1:.2f}秒\n")

    # 第二次
    print("第二次处理（缓存命中）：")
    start = time.time()
    system.process_article(article, show_progress=False)
    time2 = time.time() - start
    print(f"  耗时：{time2:.2f}秒\n")

    if time2 > 0:
        print(f"  加速：{time1 / time2:.1f}倍\n")

    print(system.get_statistics())


def demo_interactive():
    """演示4：交互式处理"""
    print("\n" + "=" * 60)
    print("📌 演示4：交互式文章处理")
    print("=" * 60)
    print("输入文章内容，按两次回车提交，输入 'quit' 退出\n")

    system = SmartContentProcessorSystem(enable_cache=True)

    while True:
        print("请输入文章内容（输入空行提交，输入 quit 退出）：")
        lines = []
        while True:
            try:
                line = input()
            except (EOFError, KeyboardInterrupt):
                return
            if line.strip().lower() == "quit":
                print("\n再见！")
                print(system.get_statistics())
                return
            if line == "" and lines:
                break
            lines.append(line)

        article = "\n".join(lines).strip()
        if article:
            system.process_article(article)


def main():
    """主函数"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       智能内容处理系统 - 第6章综合实战项目                ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    print("选择演示模式：")
    print("  1. 单篇文章处理")
    print("  2. 批量处理")
    print("  3. 缓存性能对比")
    print("  4. 交互式处理")
    print("  5. 运行全部演示")
    print()

    try:
        choice = input("请选择（1-5，默认5）：").strip() or "5"
    except (EOFError, KeyboardInterrupt):
        choice = "5"

    if choice == "1":
        demo_single_article()
    elif choice == "2":
        demo_batch_processing()
    elif choice == "3":
        demo_cache_performance()
    elif choice == "4":
        demo_interactive()
    else:
        demo_single_article()
        demo_batch_processing()
        demo_cache_performance()

    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    print("\n💡 项目技术栈：")
    print("  ✓ RouterChain 智能路由")
    print("  ✓ SequentialChain 流程编排")
    print("  ✓ Memory 历史记录")
    print("  ✓ Callback 完整监控")
    print("  ✓ InMemoryCache 缓存优化")
    print("  ✓ 错误处理和降级机制")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
