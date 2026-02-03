![RAG高级检索流程](./images/rag_flow.svg)
*图：RAG高级检索流程*

# 第65课：实战-多策略RAG系统

> **本课目标**：整合所有高级RAG技术，构建智能的多策略RAG系统
> 
> **核心技能**：策略选择、自适应优化、完整实现
> 
> **实战案例**：企业级智能RAG系统
> 
> **学习时长**：90分钟

---

## 📖 口播文案（5分钟）
![Hyde](./images/hyde.svg)
*图：Hyde*


### 🎯 前言

"前面我们学了这么多高级RAG技术：
- ✅ HyDE：假设文档嵌入
- ✅ 自查询：智能Query解析
- ✅ 上下文压缩：成本优化
- ✅ Parent Document：精准+完整

但是！

**如何把这些技术整合到一起？**

很多同学学完后很困惑：
- 🤔 什么时候用HyDE？
- 🤔 什么时候用上下文压缩？
- 🤔 能不能同时用多种技术？
- 🤔 如何选择最优策略？

我在做企业级RAG项目时发现：

**不同的查询，需要不同的策略！**

举几个真实例子：

**场景1：简单事实查询**
```
用户："Python是什么？"

最优策略：
✅ 普通向量检索就够了
❌ 不需要HyDE（增加延迟）
❌ 不需要压缩（内容本来就少）
```

**场景2：复杂专业查询**
```
用户："分布式系统中的CAP定理在实际应用中如何权衡？"

最优策略：
✅ 使用HyDE生成假设答案（提升检索）
✅ Parent Document获取完整上下文
✅ 上下文压缩去除无关内容
❌ 不需要自查询（没有过滤条件）
```

**场景3：带过滤的查询**
```
用户："2023年关于React的高级教程"

最优策略：
✅ 自查询解析过滤条件
✅ 元数据过滤快速筛选
✅ 向量检索找相关内容
❌ 不需要HyDE（过滤已经很精准）
```

**场景4：长文档查询**
```
用户："这篇论文的核心贡献是什么？"

最优策略：
✅ Parent Document保证上下文完整
✅ 上下文压缩提取关键信息
✅ 关键句提取突出重点
❌ 不需要HyDE（已经很精准）
```

**看到了吗？不同场景需要不同策略！**

**如果能自动选择最优策略，那就完美了！**

这就是**多策略RAG系统**的核心思想！

**系统架构：**

```
用户Query
    ↓
【Query分析器】
  • 识别查询类型
  • 提取特征
  • 评估复杂度
    ↓
【策略选择器】
  • 根据Query特征
  • 选择最优策略组合
  • 动态配置参数
    ↓
【执行引擎】
  • HyDE模块
  • 自查询模块
  • 检索模块
  • 压缩模块
  • Parent Document模块
    ↓
【结果聚合】
  • 融合多个结果
  • 质量评分
  • 返回最优答案
```

**今天这一课，我要带你：**

**第一部分：策略分析**
- 各技术适用场景
- 组合策略设计
- 决策树构建

**第二部分：Query分析**
- 特征提取
- 类型识别
- 复杂度评估

**第三部分：策略选择**
- 基于规则的选择
- 基于模型的选择
- 自适应优化

**第四部分：完整实现**
- 多策略引擎
- 执行流程
- 监控优化

**第五部分：效果评估**
- A/B测试
- 性能对比
- 成本分析

这是RAG系统的终极形态！

学完这一课，你将掌握构建智能RAG系统的全部技能！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【单一策略 vs 多策略】

单一策略：
  所有Query用同一种方法
  → 简单但不够优化

多策略：
  不同Query用不同方法
  → 复杂但效果最优

【智能选择的价值】

正确选择策略可以：
✅ 提升效果 20-30%
✅ 降低成本 40-50%
✅ 提升速度 50-60%
✅ 改善体验 显著提升
```

---

## 📚 第一部分：策略分析与设计

### 一、技术适用场景矩阵

```python
from enum import Enum
from typing import List, Dict, Set
from dataclasses import dataclass

class QueryType(Enum):
    """查询类型"""
    SIMPLE_FACT = "简单事实"
    COMPLEX_REASONING = "复杂推理"
    WITH_FILTER = "带过滤条件"
    LONG_CONTEXT = "长文档"
    COMPARISON = "对比分析"

class RAGTechnique(Enum):
    """RAG技术"""
    BASIC_RETRIEVAL = "基础检索"
    HYDE = "HyDE"
    SELF_QUERY = "自查询"
    COMPRESSION = "上下文压缩"
    PARENT_DOC = "Parent Document"
    RERANK = "重排序"

@dataclass
class StrategyProfile:
    """策略画像"""
    techniques: List[RAGTechnique]
    priority: int  # 1-5，5最高
    cost: int  # 1-5，5最高
    latency: int  # 1-5，5最高
    effectiveness: int  # 1-5，5最高
    
class StrategyMatrix:
    """策略适用矩阵"""
    
    # 场景 -> 推荐策略
    SCENARIO_STRATEGIES = {
        QueryType.SIMPLE_FACT: StrategyProfile(
            techniques=[RAGTechnique.BASIC_RETRIEVAL],
            priority=5,
            cost=1,
            latency=1,
            effectiveness=4
        ),
        QueryType.COMPLEX_REASONING: StrategyProfile(
            techniques=[
                RAGTechnique.HYDE,
                RAGTechnique.PARENT_DOC,
                RAGTechnique.COMPRESSION,
                RAGTechnique.RERANK
            ],
            priority=5,
            cost=4,
            latency=4,
            effectiveness=5
        ),
        QueryType.WITH_FILTER: StrategyProfile(
            techniques=[
                RAGTechnique.SELF_QUERY,
                RAGTechnique.BASIC_RETRIEVAL
            ],
            priority=5,
            cost=2,
            latency=2,
            effectiveness=5
        ),
        QueryType.LONG_CONTEXT: StrategyProfile(
            techniques=[
                RAGTechnique.PARENT_DOC,
                RAGTechnique.COMPRESSION
            ],
            priority=4,
            cost=3,
            latency=3,
            effectiveness=5
        )
    }
    
    @classmethod
    def get_recommended_strategy(
        cls,
        query_type: QueryType
    ) -> StrategyProfile:
        """获取推荐策略"""
        return cls.SCENARIO_STRATEGIES.get(
            query_type,
            cls.SCENARIO_STRATEGIES[QueryType.SIMPLE_FACT]
        )

# 演示
def demo_strategy_matrix():
    """演示策略矩阵"""
    
    print("="*60)
    print("RAG策略适用矩阵")
    print("="*60)
    
    for query_type in QueryType:
        strategy = StrategyMatrix.get_recommended_strategy(query_type)
        
        print(f"\n【{query_type.value}】")
        print(f"  推荐技术: {[t.value for t in strategy.techniques]}")
        print(f"  优先级: {'⭐' * strategy.priority}")
        print(f"  成本: {'💰' * strategy.cost}")
        print(f"  延迟: {'⏱️' * strategy.latency}")
        print(f"  效果: {'✨' * strategy.effectiveness}")

demo_strategy_matrix()
```

---

## 💻 第二部分：Query分析器

### 一、Query特征提取

```python
import re
from typing import Dict, Any

class QueryAnalyzer:
    """Query分析器"""
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """
        分析Query特征
        
        返回：
        {
            'type': QueryType,
            'complexity': float,
            'has_filter': bool,
            'has_temporal': bool,
            'is_comparison': bool,
            'length': int,
            'keywords': List[str]
        }
        """
        features = {}
        
        # 1. 长度
        features['length'] = len(query)
        features['word_count'] = len(query.split())
        
        # 2. 是否包含过滤条件
        filter_patterns = [
            r'\d{4}年',  # 年份
            r'最近\d+',   # 最近N天/月
            r'关于.*的',  # 关于XX的
            r'(中文|英文|日文)',  # 语言
            r'(初级|中级|高级)',  # 级别
        ]
        features['has_filter'] = any(
            re.search(p, query) for p in filter_patterns
        )
        
        # 3. 是否包含时间条件
        temporal_patterns = [
            r'\d{4}年',
            r'最近',
            r'今年',
            r'去年',
            r'本月',
        ]
        features['has_temporal'] = any(
            re.search(p, query) for p in temporal_patterns
        )
        
        # 4. 是否是对比查询
        comparison_patterns = [
            r'对比',
            r'比较',
            r'区别',
            r'差异',
            r'vs',
            r'和.*的不同',
        ]
        features['is_comparison'] = any(
            re.search(p, query) for p in comparison_patterns
        )
        
        # 5. 是否是问句
        features['is_question'] = any(
            q in query for q in ['？', '?', '吗', '呢', '如何', '怎么', '为什么', '什么']
        )
        
        # 6. 复杂度评估
        complexity_score = 0
        
        # 长度因素
        if features['length'] > 50:
            complexity_score += 2
        elif features['length'] > 20:
            complexity_score += 1
        
        # 过滤条件
        if features['has_filter']:
            complexity_score += 2
        
        # 对比查询
        if features['is_comparison']:
            complexity_score += 3
        
        # 问句
        if features['is_question']:
            complexity_score += 1
        
        features['complexity'] = min(complexity_score / 10, 1.0)
        
        # 7. 判断类型
        features['type'] = self._determine_type(features)
        
        return features
    
    def _determine_type(self, features: Dict) -> QueryType:
        """判断查询类型"""
        # 带过滤条件
        if features['has_filter']:
            return QueryType.WITH_FILTER
        
        # 对比查询
        if features['is_comparison']:
            return QueryType.COMPARISON
        
        # 复杂推理
        if features['complexity'] > 0.6:
            return QueryType.COMPLEX_REASONING
        
        # 长查询
        if features['word_count'] > 15:
            return QueryType.LONG_CONTEXT
        
        # 简单查询
        return QueryType.SIMPLE_FACT

# 演示
def demo_query_analyzer():
    """演示Query分析"""
    
    analyzer = QueryAnalyzer()
    
    test_queries = [
        "Python是什么？",
        "2023年关于机器学习的中文高级教程",
        "深度学习和传统机器学习的区别是什么？",
        "如何在分布式系统中实现CAP定理的权衡，特别是在高并发场景下？"
    ]
    
    print("="*60)
    print("Query分析演示")
    print("="*60)
    
    for query in test_queries:
        features = analyzer.analyze(query)
        
        print(f"\nQuery: {query}")
        print(f"  类型: {features['type'].value}")
        print(f"  复杂度: {features['complexity']:.2f}")
        print(f"  长度: {features['length']}字")
        print(f"  有过滤: {features['has_filter']}")
        print(f"  对比查询: {features['is_comparison']}")

demo_query_analyzer()
```

---

## 🎯 第三部分：策略选择器

### 一、基于规则的策略选择

```python
class RuleBasedStrategySelector:
    """基于规则的策略选择器"""
    
    def __init__(self):
        self.analyzer = QueryAnalyzer()
    
    def select_strategy(
        self,
        query: str,
        verbose: bool = False
    ) -> StrategyProfile:
        """选择策略"""
        
        # 1. 分析Query
        features = self.analyzer.analyze(query)
        
        if verbose:
            print("="*60)
            print("策略选择")
            print("="*60)
            print(f"Query: {query}")
            print(f"\n特征分析:")
            print(f"  类型: {features['type'].value}")
            print(f"  复杂度: {features['complexity']:.2f}")
        
        # 2. 获取推荐策略
        strategy = StrategyMatrix.get_recommended_strategy(
            features['type']
        )
        
        # 3. 根据具体特征微调
        techniques = list(strategy.techniques)
        
        # 如果很简单，去掉复杂技术
        if features['complexity'] < 0.3:
            techniques = [RAGTechnique.BASIC_RETRIEVAL]
        
        # 如果有过滤条件，确保使用自查询
        if features['has_filter'] and RAGTechnique.SELF_QUERY not in techniques:
            techniques.insert(0, RAGTechnique.SELF_QUERY)
        
        # 如果很复杂，添加HyDE
        if features['complexity'] > 0.7 and RAGTechnique.HYDE not in techniques:
            techniques.append(RAGTechnique.HYDE)
        
        # 创建最终策略
        final_strategy = StrategyProfile(
            techniques=techniques,
            priority=strategy.priority,
            cost=strategy.cost,
            latency=strategy.latency,
            effectiveness=strategy.effectiveness
        )
        
        if verbose:
            print(f"\n选择的策略:")
            print(f"  技术: {[t.value for t in final_strategy.techniques]}")
            print(f"  预期成本: {'💰' * final_strategy.cost}")
            print(f"  预期延迟: {'⏱️' * final_strategy.latency}")
            print(f"  预期效果: {'✨' * final_strategy.effectiveness}")
        
        return final_strategy
```

---

## ⚡ 第四部分：多策略执行引擎

### 完整的多策略RAG系统

```python
class MultiStrategyRAGSystem:
    """多策略RAG系统"""
    
    def __init__(
        self,
        llm,
        embedding_model,
        vectorstore,
        enable_auto_strategy: bool = True
    ):
        self.llm = llm
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
        self.enable_auto_strategy = enable_auto_strategy
        
        # 初始化各个模块
        self.strategy_selector = RuleBasedStrategySelector()
        
        # 技术模块（按需初始化）
        self.modules = {}
        self._init_modules()
        
        # 指标
        self.metrics = {
            'total_queries': 0,
            'strategy_distribution': {},
            'avg_latency': 0,
            'avg_cost': 0
        }
    
    def _init_modules(self):
        """初始化技术模块"""
        # 这里import各个技术模块
        # 实际项目中这些应该是前面课程实现的类
        
        from hyde import HyDERetriever
        from self_query import SelfQueryRetriever
        from compression import ContextualCompressor
        from parent_doc import ParentDocumentRetriever
        
        self.modules[RAGTechnique.HYDE] = HyDERetriever(
            self.llm,
            self.embedding_model,
            self.vectorstore
        )
        
        self.modules[RAGTechnique.SELF_QUERY] = SelfQueryRetriever(
            self.llm,
            self.vectorstore
        )
        
        self.modules[RAGTechnique.COMPRESSION] = ContextualCompressor(
            self.llm,
            self.embedding_model
        )
        
        self.modules[RAGTechnique.PARENT_DOC] = ParentDocumentRetriever(
            self.embedding_model
        )
    
    def query(
        self,
        query: str,
        k: int = 5,
        force_strategy: Optional[StrategyProfile] = None,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        执行查询
        
        流程：
        1. 选择策略
        2. 执行检索
        3. 后处理
        4. 生成答案
        """
        import time
        start_time = time.time()
        
        self.metrics['total_queries'] += 1
        
        if verbose:
            print("\n" + "🚀"*30)
            print("多策略RAG系统")
            print("🚀"*30)
        
        # 1. 选择策略
        if force_strategy:
            strategy = force_strategy
        elif self.enable_auto_strategy:
            strategy = self.strategy_selector.select_strategy(
                query,
                verbose=verbose
            )
        else:
            # 默认策略
            strategy = StrategyProfile(
                techniques=[RAGTechnique.BASIC_RETRIEVAL],
                priority=3,
                cost=1,
                latency=1,
                effectiveness=3
            )
        
        # 记录策略使用
        strategy_key = str([t.value for t in strategy.techniques])
        self.metrics['strategy_distribution'][strategy_key] = \
            self.metrics['strategy_distribution'].get(strategy_key, 0) + 1
        
        # 2. 执行检索
        if verbose:
            print(f"\n【执行检索】")
        
        documents = self._execute_retrieval(
            query,
            strategy,
            k,
            verbose
        )
        
        # 3. 生成答案
        if verbose:
            print(f"\n【生成答案】")
        
        answer = self._generate_answer(query, documents)
        
        # 4. 构建结果
        total_time = time.time() - start_time
        
        result = {
            'query': query,
            'answer': answer,
            'strategy': {
                'techniques': [t.value for t in strategy.techniques],
                'cost_level': strategy.cost,
                'latency_level': strategy.latency
            },
            'num_documents': len(documents),
            'timing': {
                'total': total_time
            }
        }
        
        # 更新指标
        self.metrics['avg_latency'] = (
            self.metrics['avg_latency'] * (self.metrics['total_queries'] - 1) +
            total_time
        ) / self.metrics['total_queries']
        
        if verbose:
            print(f"\n【完成】")
            print(f"  总耗时: {total_time:.2f}秒")
            print(f"  使用策略: {[t.value for t in strategy.techniques]}")
        
        return result
    
    def _execute_retrieval(
        self,
        query: str,
        strategy: StrategyProfile,
        k: int,
        verbose: bool
    ) -> List[str]:
        """执行检索"""
        
        documents = []
        
        # 按策略中的技术顺序执行
        for technique in strategy.techniques:
            if verbose:
                print(f"  执行: {technique.value}")
            
            if technique == RAGTechnique.BASIC_RETRIEVAL:
                # 基础向量检索
                docs = self.vectorstore.similarity_search(query, k=k)
                documents.extend([doc.page_content for doc in docs])
            
            elif technique == RAGTechnique.HYDE:
                # HyDE检索
                docs = self.modules[RAGTechnique.HYDE].retrieve(query, k=k)
                documents.extend([doc for doc, _ in docs])
            
            elif technique == RAGTechnique.SELF_QUERY:
                # 自查询
                docs = self.modules[RAGTechnique.SELF_QUERY].retrieve(query, k=k)
                documents.extend([doc.page_content for doc in docs])
            
            elif technique == RAGTechnique.PARENT_DOC:
                # Parent Document
                docs = self.modules[RAGTechnique.PARENT_DOC].retrieve(query, k=k)
                documents.extend([doc.content for doc in docs])
            
            elif technique == RAGTechnique.COMPRESSION:
                # 上下文压缩（应用于已有documents）
                if documents:
                    compressed = self.modules[RAGTechnique.COMPRESSION].compress(
                        query,
                        documents
                    )
                    documents = compressed
        
        # 去重
        unique_docs = []
        seen = set()
        for doc in documents:
            if doc not in seen:
                unique_docs.append(doc)
                seen.add(doc)
        
        return unique_docs[:k]
    
    def _generate_answer(
        self,
        query: str,
        documents: List[str]
    ) -> str:
        """生成答案"""
        
        # 构建上下文
        context = "\n\n".join([
            f"【文档{i+1}】\n{doc}"
            for i, doc in enumerate(documents)
        ])
        
        # 构建Prompt
        prompt = f"""请基于以下上下文回答问题。

上下文：
{context}

问题：{query}

要求：
1. 基于上下文准确回答
2. 简洁明了
3. 如果上下文中没有相关信息，明确说明

答案："""
        
        # 调用LLM
        response = self.llm.invoke(prompt)
        return response.content
    
    def get_metrics(self) -> Dict:
        """获取性能指标"""
        return {
            **self.metrics,
            'strategy_distribution': {
                k: f"{v}/{self.metrics['total_queries']} ({v/self.metrics['total_queries']:.1%})"
                for k, v in self.metrics['strategy_distribution'].items()
            }
        }

# 完整演示
def demo_multi_strategy_rag():
    """演示多策略RAG系统"""
    
    from langchain.chat_models import ChatOpenAI
    
    # 初始化
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )
    
    # 创建多策略系统
    rag_system = MultiStrategyRAGSystem(
        llm=llm,
        embedding_model="moka-ai/m3e-base",
        vectorstore=None,  # 实际应用中需要初始化
        enable_auto_strategy=True
    )
    
    # 测试不同类型的查询
    test_queries = [
        "Python是什么？",  # 简单查询
        "2023年关于深度学习的中文教程",  # 带过滤
        "深度学习和机器学习的区别",  # 对比
        "如何在生产环境中部署大规模机器学习模型？"  # 复杂
    ]
    
    for query in test_queries:
        result = rag_system.query(query, verbose=True)
        print("\n" + "="*60 + "\n")
    
    # 显示整体指标
    print("\n" + "📊"*30)
    print("系统性能指标")
    print("📊"*30)
    
    metrics = rag_system.get_metrics()
    print(f"\n总查询数: {metrics['total_queries']}")
    print(f"平均延迟: {metrics['avg_latency']:.2f}秒")
    print(f"\n策略分布:")
    for strategy, count in metrics['strategy_distribution'].items():
        print(f"  {strategy}: {count}")

# demo_multi_strategy_rag()
```

---

## 📝 课后练习

### 练习1：机器学习选择器
用机器学习模型代替规则做策略选择

### 练习2：在线学习
根据用户反馈持续优化策略选择

### 练习3：成本控制
在保证效果前提下最小化成本

---

## 🎓 知识总结

### 第11章完整回顾

通过5节课，我们学习了：

1. **HyDE** - 假设文档嵌入
   - 解决表述差异
   - 提升检索准确性

2. **自查询** - 智能Query解析
   - 分离语义和过滤
   - 结构化查询

3. **上下文压缩** - 成本优化
   - 降低成本70%
   - 提升效果

4. **Parent Document** - 精准+完整
   - 小块检索
   - 大块返回

5. **多策略整合** - 智能选择
   - 自适应优化
   - 最优效果

### 最佳实践

✅ 简单查询用简单方法
✅ 复杂查询用组合策略
✅ 监控各策略效果
✅ 持续优化调整
✅ 平衡成本和效果

---

## 🚀 下一章预告

**第12章：RAG评估与优化**

- 评估指标体系
- 检索质量评估
- 生成质量评估
- 端到端评估
- 实战评估报告

**从技术实现到效果评估！** 📊

---

**💪 恭喜！第11章完成！你已掌握所有高级RAG技术！**

**下一章见！** 🎉
