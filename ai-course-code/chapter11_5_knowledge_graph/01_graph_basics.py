"""
第11.5章-知识图谱：基础概念
对应课程：第68课-知识图谱基础

知识图谱 = 实体 + 关系
比如：(马云, 创立, 阿里巴巴), (阿里巴巴, 总部位于, 杭州)
"""


def demo_knowledge_graph_concept():
    """知识图谱概念演示"""
    print("=" * 60)
    print("知识图谱基础概念")
    print("=" * 60)
    
    print("""
什么是知识图谱？

知识图谱是一种结构化的知识表示方式：
- 节点（Node）：实体，如人、公司、地点
- 边（Edge）：关系，如"创立"、"工作于"、"位于"

基本单位是三元组：(主体, 关系, 客体)

示例：
(马云, 创立, 阿里巴巴)
(阿里巴巴, 总部位于, 杭州)
(杭州, 是, 浙江省会)
""")

    # 简单的知识图谱表示
    knowledge_graph = [
        ("马云", "创立", "阿里巴巴"),
        ("阿里巴巴", "总部位于", "杭州"),
        ("阿里巴巴", "业务包括", "电商"),
        ("阿里巴巴", "业务包括", "云计算"),
        ("杭州", "属于", "浙江省"),
        ("马化腾", "创立", "腾讯"),
        ("腾讯", "总部位于", "深圳"),
    ]
    
    print("\n【示例知识图谱】")
    for s, p, o in knowledge_graph:
        print(f"  ({s}) --[{p}]--> ({o})")


def demo_graph_query():
    """图查询演示"""
    print("\n" + "=" * 60)
    print("知识图谱查询")
    print("=" * 60)
    
    # 简单的图结构
    graph = {
        "马云": {"创立": ["阿里巴巴"], "类型": ["人物"]},
        "阿里巴巴": {"总部位于": ["杭州"], "业务包括": ["电商", "云计算"], "类型": ["公司"]},
        "杭州": {"属于": ["浙江省"], "类型": ["城市"]},
    }
    
    def query_relation(entity, relation):
        """查询某实体的某种关系"""
        if entity in graph and relation in graph[entity]:
            return graph[entity][relation]
        return []
    
    def multi_hop_query(start, relations):
        """多跳查询"""
        current = [start]
        for relation in relations:
            next_entities = []
            for entity in current:
                next_entities.extend(query_relation(entity, relation))
            current = next_entities
        return current
    
    # 单跳查询
    print("\n【单跳查询】")
    print(f"马云创立了什么？{query_relation('马云', '创立')}")
    print(f"阿里巴巴的业务包括？{query_relation('阿里巴巴', '业务包括')}")
    
    # 多跳查询
    print("\n【多跳查询】")
    result = multi_hop_query("马云", ["创立", "总部位于"])
    print(f"马云创立的公司总部在哪？{result}")
    
    result = multi_hop_query("马云", ["创立", "总部位于", "属于"])
    print(f"马云创立的公司总部所在的省份？{result}")


def demo_graph_vs_vector():
    """图谱vs向量检索对比"""
    print("\n" + "=" * 60)
    print("知识图谱 vs 向量检索")
    print("=" * 60)
    
    print("""
场景：马云创立的公司总部在哪个省？

【向量检索】
1. 问题embedding → 检索相似文档
2. 可能检索到："马云创立阿里巴巴"、"杭州是浙江省会"
3. 需要LLM自己推理组合

【知识图谱】
1. 识别实体：马云
2. 图查询：马云 → 创立 → 阿里巴巴 → 总部位于 → 杭州 → 属于 → 浙江省
3. 直接得到答案：浙江省

对比：
- 向量检索：适合语义相似的问题
- 知识图谱：适合多跳推理的问题

最佳实践：两者结合使用！
""")


if __name__ == "__main__":
    demo_knowledge_graph_concept()
    demo_graph_query()
    demo_graph_vs_vector()
    
    print("\n" + "=" * 60)
    print("✅ 知识图谱基础学习完成！")
    print("\n核心要点：")
    print("  • 知识图谱 = 实体 + 关系")
    print("  • 基本单位：(主体, 关系, 客体)三元组")
    print("  • 优势：多跳推理")
    print("  • 实践：知识图谱 + 向量检索结合")

