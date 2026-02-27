"""
第11章-RAG评估：评估指标详解
对应课程：第66课-RAG评估指标

RAG评估三个维度：
1. 检索质量 - 检索到的文档是否相关
2. 生成质量 - 生成的答案是否忠实于检索内容
3. 端到端 - 最终答案是否正确
"""


def demo_retrieval_metrics():
    """检索质量指标"""
    print("=" * 60)
    print("检索质量指标")
    print("=" * 60)
    
    print("""
1. Precision（精确率）
   - 检索到的文档中，有多少是相关的？
   - Precision = 相关文档数 / 检索到的文档数
   - 例：检索5篇，3篇相关 → Precision = 3/5 = 60%

2. Recall（召回率）
   - 所有相关文档中，检索到了多少？
   - Recall = 检索到的相关数 / 总相关数
   - 例：共10篇相关，检索到3篇 → Recall = 3/10 = 30%

3. MRR（平均倒数排名）
   - 第一个相关结果排在第几位？
   - 排名越靠前越好
   - MRR = 1/排名
   - 例：第一个相关结果在第2位 → MRR = 1/2 = 0.5
""")
    
    # 示例计算
    print("\n【示例计算】")
    retrieved = ["文档A", "文档B", "文档C", "文档D", "文档E"]
    relevant = ["文档A", "文档C"]  # 检索到的相关文档
    total_relevant = 4  # 总共有4篇相关文档
    
    precision = len(relevant) / len(retrieved)
    recall = len(relevant) / total_relevant
    
    # 第一个相关文档在第1位（文档A）
    first_relevant_rank = 1
    mrr = 1 / first_relevant_rank
    
    print(f"检索到：{len(retrieved)}篇")
    print(f"其中相关：{len(relevant)}篇")
    print(f"总相关文档：{total_relevant}篇")
    print(f"\nPrecision = {len(relevant)}/{len(retrieved)} = {precision:.1%}")
    print(f"Recall = {len(relevant)}/{total_relevant} = {recall:.1%}")
    print(f"MRR = 1/{first_relevant_rank} = {mrr:.2f}")


def demo_generation_metrics():
    """生成质量指标"""
    print("\n" + "=" * 60)
    print("生成质量指标")
    print("=" * 60)
    
    print("""
1. 忠实度（Faithfulness）
   - 生成的答案是否基于检索的内容？
   - 有没有"幻觉"（编造信息）？
   
   检查方法：答案中的每个声明，是否都能在检索内容中找到依据？
   
   示例：
   检索内容："Python由Guido于1991年创建"
   答案："Python由Guido于1989年创建" ← 不忠实！年份错了

2. 相关性（Relevance）
   - 答案是否回答了用户的问题？
   - 有没有答非所问？
   
   示例：
   问题："Python的优点是什么？"
   答案："Python是一种编程语言" ← 不相关！没回答优点
""")


def demo_e2e_metrics():
    """端到端指标"""
    print("\n" + "=" * 60)
    print("端到端评估指标")
    print("=" * 60)
    
    print("""
Answer Correctness（答案正确性）

这是最终指标：答案对不对？

评估方法：
1. 人工评估（最准但最贵）
2. LLM评估（让GPT-4打分）
3. 自动指标（BLEU、ROUGE等）

推荐：LLM评估 + 人工抽查
""")


def demo_evaluation_framework():
    """评估框架示例"""
    print("\n" + "=" * 60)
    print("简单评估框架")
    print("=" * 60)
    
    # 模拟评估数据
    test_cases = [
        {
            "question": "Python是什么时候创建的？",
            "expected": "1991年",
            "retrieved": ["Python由Guido于1991年创建"],
            "answer": "Python于1991年创建"
        },
        {
            "question": "Python的创始人是谁？",
            "expected": "Guido van Rossum",
            "retrieved": ["Python是一种流行的编程语言"],
            "answer": "Python的创始人是Guido"
        }
    ]
    
    print("评估结果：")
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试{i}：")
        print(f"  问题：{case['question']}")
        print(f"  期望：{case['expected']}")
        print(f"  答案：{case['answer']}")
        
        # 简单检查
        is_correct = case['expected'].lower() in case['answer'].lower()
        print(f"  正确：{'✅' if is_correct else '❌'}")


if __name__ == "__main__":
    demo_retrieval_metrics()
    demo_generation_metrics()
    demo_e2e_metrics()
    demo_evaluation_framework()
    
    print("\n" + "=" * 60)
    print("✅ RAG评估指标学习完成！")
    print("\n关键记忆点：")
    print("  • 检索：Precision（准不准）、Recall（全不全）")
    print("  • 生成：忠实度（有没有幻觉）、相关性（答没答对题）")
    print("  • 端到端：答案正确性")

