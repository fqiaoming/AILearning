![RAG系统架构](./images/rag_flow.svg)
*图：RAG系统架构*

# 第58课：Query理解与改写

> **本课目标**：掌握Query理解和改写技术，提升RAG系统的检索准确率
> 
> **核心技能**：意图识别、Query扩展、同义词替换、查询优化
> 
> **实战案例**：构建智能Query优化系统
> 
> **学习时长**：75分钟

---

## 📖 口播文案（3分钟）

### 🎯 前言

"你有没有遇到过这种情况：

用户问：'怎么让电脑变聪明？'
RAG系统：找不到相关内容 ❌

为什么？因为知识库里都是'人工智能'、'机器学习'这些专业术语！

再比如：
用户问：'iPhone好用吗？'
系统只搜'iPhone'，错过了'苹果手机'、'iOS设备'这些相关内容！

**问题的核心：用户的问法千变万化，但知识库的表述是固定的！**

今天这一课，我会教你如何让RAG系统'读懂'用户的真实意图！

我们要学习：

✅ **意图识别**：用户到底想问什么？
✅ **Query扩展**：补充同义词、相关词
✅ **Query改写**：转换成更易检索的形式
✅ **拼写纠错**：容忍用户的输入错误
✅ **实体识别**：提取关键信息

学完这一课，你的RAG系统能理解：
- '怎么让电脑变聪明' = '人工智能入门'
- 'iPhone好用吗' → 搜索'iPhone'+'苹果手机'+'iOS'
- '机器学习'的错别字'机器血习' → 自动纠正

**这是RAG系统从'能用'到'好用'的关键一步！**

准备好了吗？让我们开始！"

---

### 💡 核心知识点

#### Query理解的重要性

```
原始Query → Query理解 → 优化后的Query → 检索

例子1：同义词问题
用户："AI是什么？"
知识库："人工智能（Artificial Intelligence）是..."
问题：直接搜"AI"可能搜不到
解决：扩展为 "AI" OR "人工智能" OR "Artificial Intelligence"

例子2：口语化表达
用户："怎么让电脑变聪明？"
意图：了解人工智能
改写："人工智能是什么" OR "如何开发AI"

例子3：拼写错误
用户："机器血习"
纠正："机器学习"

例子4：缩写和全称
用户："NLP技术"
扩展："NLP" OR "自然语言处理" OR "Natural Language Processing"
```

#### Query优化流程

```
┌─────────────────┐
│  原始Query       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  1. 预处理       │
│  • 去除特殊字符  │
│  • 统一大小写    │
│  • 分词          │
└────────┬────────┘
         ↓
┌─────────────────┐
│  2. 拼写纠错     │
│  • 检测错误      │
│  • 候选纠正      │
└────────┬────────┘
         ↓
┌─────────────────┐
│  3. 意图识别     │
│  • 问答型        │
│  • 检索型        │
│  • 对比型        │
└────────┬────────┘
         ↓
┌─────────────────┐
│  4. 实体识别     │
│  • 提取关键词    │
│  • 识别实体类型  │
└────────┬────────┘
         ↓
┌─────────────────┐
│  5. Query扩展    │
│  • 同义词        │
│  • 相关词        │
│  • 缩写展开      │
└────────┬────────┘
         ↓
┌─────────────────┐
│  优化后的Query   │
└─────────────────┘
```

---

## 📚 知识讲解

### 一、Query预处理

#
![Query理解](./images/retrieval.svg)
*图：Query理解*

### 1.1 基础预处理

```python
import re
from typing import List, Dict, Any

class QueryPreprocessor:
    """Query预处理器"""
    
    def __init__(self):
        # 停用词（可以扩展）
        self.stopwords = {
            '的', '了', '是', '在', '我', '有', '和', '就',
            '不', '人', '都', '一', '一个', '上', '也', '很',
            '到', '说', '要', '去', '你', '会', '着', '没有',
            '看', '好', '自己', '这', '那'
        }
    
    def clean(self, query: str) -> str:
        """清理Query"""
        # 1. 去除多余空格
        query = re.sub(r'\s+', ' ', query).strip()
        
        # 2. 去除特殊字符（保留中英文、数字、基本标点）
        query = re.sub(r'[^\w\s\u4e00-\u9fff?？！!。.]', '', query)
        
        # 3. 统一标点
        query = query.replace('？', '?').replace('！', '!')
        
        return query
    
    def normalize(self, query: str) -> str:
        """标准化Query"""
        # 1. 清理
        query = self.clean(query)
        
        # 2. 转小写（英文部分）
        # 保留中文，只转换英文
        result = []
        for char in query:
            if 'A' <= char <= 'Z':
                result.append(char.lower())
            else:
                result.append(char)
        
        return ''.join(result)
    
    def remove_stopwords(self, words: List[str]) -> List[str]:
        """去除停用词"""
        return [w for w in words if w not in self.stopwords]
    
    def tokenize(self, query: str) -> List[str]:
        """简单分词（仅用于演示）"""
        # 实际应用中建议使用jieba等专业分词工具
        
        # 分离中英文
        tokens = []
        current = []
        is_chinese = None
        
        for char in query:
            char_is_chinese = '\u4e00' <= char <= '\u9fff'
            
            if is_chinese is None:
                is_chinese = char_is_chinese
            
            if char_is_chinese != is_chinese or char.isspace():
                if current:
                    tokens.append(''.join(current))
                    current = []
                is_chinese = char_is_chinese
            
            if not char.isspace():
                current.append(char)
        
        if current:
            tokens.append(''.join(current))
        
        return tokens

# 使用示例
def demo_preprocessor():
    """演示预处理"""
    
    preprocessor = QueryPreprocessor()
    
    queries = [
        "  人工智能   是什么？？  ",
        "怎么学习Machine Learning???",
        "AI和ML有什么区别！！",
        "深度学习@#$%^框架对比",
    ]
    
    print("="*60)
    print("Query预处理演示")
    print("="*60)
    
    for query in queries:
        cleaned = preprocessor.clean(query)
        normalized = preprocessor.normalize(query)
        tokens = preprocessor.tokenize(normalized)
        
        print(f"\n原始: {query}")
        print(f"清理: {cleaned}")
        print(f"标准化: {normalized}")
        print(f"分词: {tokens}")

demo_preprocessor()
```

---

### 二、拼写纠错

#### 2.1 编辑距离算法

```python
class SpellCorrector:
    """拼写纠错器"""
    
    def __init__(self):
        # 词典（实际应该从大量文本中构建）
        self.vocabulary = set()
        self.word_freq = {}
    
    def build_vocabulary(self, documents: List[str]):
        """构建词典"""
        print("📚 构建词典...")
        
        for doc in documents:
            # 简单分词
            words = re.findall(r'\w+', doc.lower())
            for word in words:
                self.vocabulary.add(word)
                self.word_freq[word] = self.word_freq.get(word, 0) + 1
        
        print(f"  ✅ 词汇量: {len(self.vocabulary)}")
    
    def edit_distance(self, word1: str, word2: str) -> int:
        """计算编辑距离（Levenshtein距离）"""
        m, n = len(word1), len(word2)
        
        # 初始化DP表
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # 初始化第一行和第一列
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # 动态规划
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + 1,    # 删除
                        dp[i][j-1] + 1,    # 插入
                        dp[i-1][j-1] + 1   # 替换
                    )
        
        return dp[m][n]
    
    def get_candidates(self, word: str, max_distance: int = 2) -> List[tuple]:
        """获取候选纠正词"""
        candidates = []
        
        for vocab_word in self.vocabulary:
            distance = self.edit_distance(word, vocab_word)
            if distance <= max_distance:
                # 使用词频作为权重
                freq = self.word_freq.get(vocab_word, 1)
                candidates.append((vocab_word, distance, freq))
        
        # 按距离和频率排序
        candidates.sort(key=lambda x: (x[1], -x[2]))
        
        return candidates
    
    def correct(self, word: str, threshold: int = 2) -> str:
        """纠正单词"""
        # 如果在词典中，直接返回
        if word.lower() in self.vocabulary:
            return word
        
        # 获取候选词
        candidates = self.get_candidates(word.lower(), max_distance=threshold)
        
        # 返回最佳候选
        if candidates:
            return candidates[0][0]
        
        return word
    
    def correct_query(self, query: str) -> str:
        """纠正整个Query"""
        words = re.findall(r'\w+', query)
        corrected_words = []
        
        for word in words:
            corrected = self.correct(word)
            corrected_words.append(corrected)
        
        # 重建Query
        result = query
        for original, corrected in zip(words, corrected_words):
            if original != corrected:
                result = result.replace(original, corrected)
        
        return result

# 使用示例
def demo_spell_corrector():
    """演示拼写纠错"""
    
    # 1. 构建词典
    documents = [
        "人工智能是计算机科学的重要分支",
        "机器学习是人工智能的核心技术",
        "深度学习使用神经网络",
        "自然语言处理研究人机交互",
        "计算机视觉处理图像和视频",
    ]
    
    corrector = SpellCorrector()
    corrector.build_vocabulary(documents)
    
    # 2. 测试纠错
    print("\n" + "="*60)
    print("拼写纠错演示")
    print("="*60)
    
    test_words = [
        "机器血习",  # 机器学习
        "人工只能",  # 人工智能
        "申度学习",  # 深度学习
        "计算鸡",    # 计算机
    ]
    
    for word in test_words:
        candidates = corrector.get_candidates(word, max_distance=2)
        corrected = corrector.correct(word)
        
        print(f"\n原词: {word}")
        print(f"纠正: {corrected}")
        print(f"候选: {candidates[:3]}")

demo_spell_corrector()
```

---

### 三、Query扩展

#### 3.1 同义词扩展

```python
class QueryExpander:
    """Query扩展器"""
    
    def __init__(self):
        # 同义词词典
        self.synonyms = {
            'ai': ['人工智能', 'artificial intelligence'],
            '人工智能': ['ai', 'artificial intelligence'],
            'ml': ['机器学习', 'machine learning'],
            '机器学习': ['ml', 'machine learning'],
            'dl': ['深度学习', 'deep learning'],
            '深度学习': ['dl', 'deep learning'],
            'nlp': ['自然语言处理', 'natural language processing'],
            '自然语言处理': ['nlp', 'natural language processing'],
            'cv': ['计算机视觉', 'computer vision'],
            '计算机视觉': ['cv', 'computer vision'],
        }
        
        # 相关词（语义相关但不同义）
        self.related_terms = {
            '人工智能': ['机器学习', '深度学习', '神经网络'],
            '机器学习': ['算法', '模型', '训练', '预测'],
            '深度学习': ['神经网络', 'cnn', 'rnn', 'transformer'],
            '自然语言处理': ['文本分析', '语义理解', 'bert', 'gpt'],
        }
        
        # 缩写展开
        self.abbreviations = {
            'ai': 'artificial intelligence',
            'ml': 'machine learning',
            'dl': 'deep learning',
            'nlp': 'natural language processing',
            'cv': 'computer vision',
            'rnn': 'recurrent neural network',
            'cnn': 'convolutional neural network',
        }
    
    def add_synonyms(self, word: str, synonyms: List[str]):
        """添加同义词"""
        self.synonyms[word.lower()] = synonyms
    
    def get_synonyms(self, word: str) -> List[str]:
        """获取同义词"""
        return self.synonyms.get(word.lower(), [])
    
    def get_related(self, word: str) -> List[str]:
        """获取相关词"""
        return self.related_terms.get(word, [])
    
    def expand_with_synonyms(self, query: str) -> List[str]:
        """用同义词扩展Query"""
        # 分词
        words = re.findall(r'\w+', query.lower())
        
        # 收集所有扩展
        expanded_queries = [query]
        
        for word in words:
            synonyms = self.get_synonyms(word)
            if synonyms:
                # 为每个同义词生成新query
                for syn in synonyms:
                    new_query = query.replace(word, syn)
                    if new_query not in expanded_queries:
                        expanded_queries.append(new_query)
        
        return expanded_queries
    
    def expand_with_related(self, query: str, max_related: int = 3) -> List[str]:
        """用相关词扩展Query"""
        # 分词
        words = re.findall(r'[\u4e00-\u9fff]+', query)
        
        expanded = [query]
        
        for word in words:
            related = self.get_related(word)
            if related:
                for rel in related[:max_related]:
                    expanded.append(f"{query} {rel}")
        
        return expanded
    
    def expand_abbreviations(self, query: str) -> str:
        """展开缩写"""
        result = query
        words = re.findall(r'\w+', query.lower())
        
        for word in words:
            if word in self.abbreviations:
                full_form = self.abbreviations[word]
                # 替换为 "缩写(全称)" 的形式
                result = re.sub(
                    rf'\b{word}\b',
                    f"{word} ({full_form})",
                    result,
                    flags=re.IGNORECASE
                )
        
        return result

# 使用示例
def demo_query_expander():
    """演示Query扩展"""
    
    expander = QueryExpander()
    
    print("="*60)
    print("Query扩展演示")
    print("="*60)
    
    # 1. 同义词扩展
    print("\n【1. 同义词扩展】")
    query = "AI技术是什么"
    expanded = expander.expand_with_synonyms(query)
    print(f"原始: {query}")
    print("扩展:")
    for i, exp in enumerate(expanded):
        print(f"  {i+1}. {exp}")
    
    # 2. 相关词扩展
    print("\n【2. 相关词扩展】")
    query = "机器学习"
    expanded = expander.expand_with_related(query)
    print(f"原始: {query}")
    print("扩展:")
    for i, exp in enumerate(expanded):
        print(f"  {i+1}. {exp}")
    
    # 3. 缩写展开
    print("\n【3. 缩写展开】")
    queries = ["NLP是什么", "CNN和RNN的区别"]
    for query in queries:
        expanded = expander.expand_abbreviations(query)
        print(f"原始: {query}")
        print(f"展开: {expanded}")

demo_query_expander()
```

---

### 四、意图识别

#### 4.1 基于规则的意图识别

```python
from enum import Enum
from typing import Optional

class QueryIntent(Enum):
    """Query意图类型"""
    QUESTION = "问答"          # 什么是、如何、为什么
    SEARCH = "检索"            # 查找、搜索
    COMPARISON = "对比"        # 对比、区别、vs
    INSTRUCTION = "指令"       # 帮我、请、生成
    DEFINITION = "定义"        # 定义、概念、解释
    EXAMPLE = "示例"           # 例子、案例
    UNKNOWN = "未知"

class IntentClassifier:
    """意图分类器"""
    
    def __init__(self):
        # 意图关键词模式
        self.patterns = {
            QueryIntent.QUESTION: [
                r'什么是', r'如何', r'怎么', r'怎样', r'为什么',
                r'why', r'how', r'what', r'\?', r'？'
            ],
            QueryIntent.COMPARISON: [
                r'对比', r'比较', r'区别', r'差异', r'vs', r'和.*的区别'
            ],
            QueryIntent.DEFINITION: [
                r'定义', r'概念', r'解释', r'含义', r'是指'
            ],
            QueryIntent.EXAMPLE: [
                r'例子', r'案例', r'示例', r'实例', r'举例'
            ],
            QueryIntent.INSTRUCTION: [
                r'帮我', r'请', r'生成', r'创建', r'写一个'
            ],
            QueryIntent.SEARCH: [
                r'查找', r'搜索', r'找', r'有哪些', r'列出'
            ],
        }
    
    def classify(self, query: str) -> QueryIntent:
        """分类Query意图"""
        query_lower = query.lower()
        
        # 检查每种意图的模式
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        return QueryIntent.UNKNOWN
    
    def classify_with_confidence(self, query: str) -> tuple:
        """分类并返回置信度"""
        query_lower = query.lower()
        
        # 计算每种意图的匹配得分
        scores = {}
        for intent, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    score += 1
            scores[intent] = score
        
        # 找到最高分
        if not scores or max(scores.values()) == 0:
            return QueryIntent.UNKNOWN, 0.0
        
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent] / len(self.patterns[best_intent])
        
        return best_intent, confidence

# 使用示例
def demo_intent_classifier():
    """演示意图识别"""
    
    classifier = IntentClassifier()
    
    queries = [
        "什么是人工智能？",
        "如何学习机器学习",
        "深度学习和机器学习的区别",
        "帮我生成一个Python脚本",
        "举个神经网络的例子",
        "查找关于NLP的资料",
        "人工智能的定义是什么",
    ]
    
    print("="*60)
    print("意图识别演示")
    print("="*60)
    
    for query in queries:
        intent, confidence = classifier.classify_with_confidence(query)
        print(f"\nQuery: {query}")
        print(f"意图: {intent.value}")
        print(f"置信度: {confidence:.2%}")

demo_intent_classifier()
```

---

### 五、完整的Query优化系统

#### 5.1 整合所有组件

```python
class QueryOptimizer:
    """完整的Query优化系统"""
    
    def __init__(self):
        self.preprocessor = QueryPreprocessor()
        self.spell_corrector = SpellCorrector()
        self.expander = QueryExpander()
        self.intent_classifier = IntentClassifier()
    
    def initialize(self, documents: List[str]):
        """初始化（构建词典等）"""
        print("🚀 初始化Query优化器...")
        self.spell_corrector.build_vocabulary(documents)
        print("✅ 初始化完成\n")
    
    def optimize(
        self,
        query: str,
        enable_spell_check: bool = True,
        enable_expansion: bool = True,
        expansion_type: str = "synonyms",  # synonyms, related, both
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        优化Query
        
        Returns:
            {
                'original': 原始query,
                'normalized': 标准化后的query,
                'corrected': 纠错后的query,
                'expanded': 扩展后的queries,
                'intent': 意图,
                'tokens': 分词结果
            }
        """
        if verbose:
            print("="*60)
            print("🔍 Query优化")
            print("="*60)
            print(f"原始Query: {query}\n")
        
        result = {'original': query}
        
        # 1. 预处理
        if verbose:
            print("【步骤1】预处理")
        
        normalized = self.preprocessor.normalize(query)
        result['normalized'] = normalized
        
        if verbose:
            print(f"  标准化: {normalized}")
        
        # 2. 拼写纠错
        if enable_spell_check:
            if verbose:
                print("\n【步骤2】拼写纠错")
            
            corrected = self.spell_corrector.correct_query(normalized)
            result['corrected'] = corrected
            
            if corrected != normalized:
                if verbose:
                    print(f"  ⚠️  发现错误: {normalized}")
                    print(f"  ✅ 纠正为: {corrected}")
            else:
                if verbose:
                    print(f"  ✅ 无需纠正")
        else:
            result['corrected'] = normalized
        
        # 3. 意图识别
        if verbose:
            print("\n【步骤3】意图识别")
        
        intent, confidence = self.intent_classifier.classify_with_confidence(
            result['corrected']
        )
        result['intent'] = intent
        result['intent_confidence'] = confidence
        
        if verbose:
            print(f"  意图: {intent.value}")
            print(f"  置信度: {confidence:.2%}")
        
        # 4. Query扩展
        result['expanded'] = [result['corrected']]
        
        if enable_expansion:
            if verbose:
                print("\n【步骤4】Query扩展")
            
            if expansion_type in ['synonyms', 'both']:
                expanded_syn = self.expander.expand_with_synonyms(result['corrected'])
                result['expanded'].extend(expanded_syn)
                
                if verbose and len(expanded_syn) > 1:
                    print(f"  同义词扩展: +{len(expanded_syn)-1}个变体")
            
            if expansion_type in ['related', 'both']:
                expanded_rel = self.expander.expand_with_related(result['corrected'])
                result['expanded'].extend(expanded_rel)
                
                if verbose and len(expanded_rel) > 1:
                    print(f"  相关词扩展: +{len(expanded_rel)-1}个变体")
            
            # 去重
            result['expanded'] = list(set(result['expanded']))
            
            if verbose:
                print(f"  ✅ 总共生成 {len(result['expanded'])} 个查询变体")
        
        # 5. 分词
        tokens = self.preprocessor.tokenize(result['corrected'])
        result['tokens'] = tokens
        
        if verbose:
            print("\n【步骤5】分词")
            print(f"  分词: {tokens}")
        
        if verbose:
            print("\n" + "="*60)
            print("✅ 优化完成")
            print("="*60)
        
        return result
    
    def optimize_for_retrieval(
        self,
        query: str,
        top_k: int = 3
    ) -> List[str]:
        """
        为检索优化Query，返回最佳的k个查询变体
        """
        result = self.optimize(
            query,
            enable_spell_check=True,
            enable_expansion=True,
            expansion_type='both',
            verbose=False
        )
        
        # 返回top-k个变体
        # 策略：原始纠正后的 + 同义词扩展优先
        queries = []
        
        # 1. 纠正后的query
        queries.append(result['corrected'])
        
        # 2. 扩展的queries
        for exp in result['expanded']:
            if exp != result['corrected'] and exp not in queries:
                queries.append(exp)
        
        return queries[:top_k]

# 完整示例
def full_demo():
    """完整演示"""
    
    # 1. 准备文档（用于构建词典）
    documents = [
        "人工智能是计算机科学的重要分支",
        "机器学习是人工智能的核心技术",
        "深度学习使用神经网络进行学习",
        "自然语言处理研究人机交互",
        "计算机视觉处理图像识别任务",
        "Python是人工智能开发的主流语言",
    ]
    
    # 2. 创建优化器
    optimizer = QueryOptimizer()
    optimizer.initialize(documents)
    
    # 3. 测试不同类型的Query
    test_queries = [
        "什么是AI技术？",
        "机器血习和深度学习的区别",
        "nlp应用案例",
        "怎么学习人工智能",
    ]
    
    for query in test_queries:
        result = optimizer.optimize(query)
        
        print("\n📋 优化结果汇总:")
        print(f"  原始: {result['original']}")
        print(f"  纠正: {result['corrected']}")
        print(f"  意图: {result['intent'].value}")
        print(f"  扩展查询数: {len(result['expanded'])}")
        
        print("\n🔎 推荐用于检索的查询:")
        retrieval_queries = optimizer.optimize_for_retrieval(query, top_k=3)
        for i, q in enumerate(retrieval_queries):
            print(f"  {i+1}. {q}")
        
        print("\n" + "="*80 + "\n")

full_demo()
```

---

## 📝 课后练习

### 练习1：使用LLM改写Query

用LLM实现更智能的Query改写

### 练习2：构建领域词典

为特定领域构建专业术语词典

### 练习3：多语言支持

扩展系统支持中英文混合查询

---

## 🎓 知识总结

### 核心要点

1. **Query理解的重要性**
   - 用户表达千变万化
   - 需要理解真实意图
   - 扩展查询提高召回

2. **五大核心技术**
   - 预处理：标准化
   - 纠错：容错性
   - 扩展：同义词、相关词
   - 意图识别：理解目的
   - 优化：生成最佳查询

3. **应用策略**
   - FAQ：重点纠错
   - 搜索：重点扩展
   - 对话：重点意图

### 最佳实践

✅ 始终做预处理
✅ 拼写纠错提高容错
✅ 同义词扩展提高召回
✅ 意图识别指导后续处理
✅ 生成多个查询变体

---

## 🚀 下节预告

下一课：**第59课：Rerank重排序技术**

- 为什么需要重排序
- Cross-Encoder原理
- 重排序策略
- 实战：提升检索精准度

**让最相关的结果排在最前面！** 🎯

---

**💪 记住：理解Query是提升RAG效果的关键！**

**下一课见！** 🎉
