![向量数据库架构](./images/vector_db.svg)
*图：向量数据库架构*

# 第42课：Embedding技术深度解析 - RAG的核心引擎

> 📚 **课程信息**
> - 所属模块：第三模块 - 向量数据库与RAG系统  
> - 章节：第8章 - 向量数据库基础（第2/6课）
> - 学习目标：深入理解Embedding技术，掌握多种方案和最佳实践
> - 预计时间：100-120分钟
> - 前置知识：第41课

---

## 📢 课程导入

### 前言

上一课我们知道了：向量数据库存的是"向量"，通过相似度搜索来理解语义。但有个关键问题：**这些向量是怎么来的？**

"机器学习" → [0.2, -0.5, 0.8, ...]，这个转换过程是什么？为什么能表示语义？用什么模型？本地还是API？免费还是收费？

**这就是Embedding技术！**它是RAG系统的核心引擎：Embedding质量决定了搜索质量，搜索质量决定了RAG效果！**Embedding做不好，整个RAG系统都白搭！**

今天这课，我要彻底讲透Embedding：原理、模型选择、本地部署、质量评估、最佳实践！

---

### 核心价值点

**第一，Embedding质量直接决定RAG系统效果。**

看两个例子：

**差的Embedding**：
```
用户问："如何学习人工智能"
检索到："今天天气真好"、"Python基础语法"
→ 答案驴唇不对马嘴
```

**好的Embedding**：
```
用户问："如何学习人工智能"
检索到："AI学习路线图"、"机器学习入门教程"
→ 答案精准相关
```

**差距就在Embedding！**

90%的RAG效果问题，根源都是Embedding！掌握Embedding，RAG就成功了一半！

**第二，Embedding模型选择大有讲究。**

很多人随便选个模型就用，结果效果很差！

**关键考虑因素**：
1. **语言**：英文模型 vs 中文模型 vs 多语言模型
2. **质量**：大模型（慢但准）vs 小模型（快但可能不准）
3. **成本**：API付费 vs 开源免费
4. **部署**：云端API vs 本地部署
5. **领域**：通用模型 vs 领域专用模型

**选错模型，效果差10倍！**

**第三，本地Embedding是企业的核心需求。**

为什么要本地部署？

**API方案（OpenAI等）**：
- ❌ 每次调用都要钱（$0.0001/1K tokens）
- ❌ 数据发送到外部（隐私问题）
- ❌ 依赖网络（断网不能用）
- ❌ 被服务商控制（涨价、限流）

**本地方案**：
- ✅ 完全免费
- ✅ 数据不出本地
- ✅ 不依赖网络
- ✅ 自主可控

**企业级应用，必须会本地部署！**

**第四，这是从会用到精通的关键一课。**

- **初级**：只会用OpenAI Embedding（花钱）
- **中级**：会选择合适的开源模型
- **高级**：会本地部署、优化、评估

掌握这一课，你就是Embedding专家了！

---

### 行动号召

今天这一课会教你：
- Embedding原理深度解析
- 主流Embedding模型对比
- 本地部署完整方案
- Embedding质量评估
- 实战最佳实践

**这是RAG系统的核心技术！必须掌握！**

---

## 📖 知识讲解

![Embedding技术原理](./images/embedding.svg)
*图：Embedding技术原理*


### 1. Embedding原理

#### 1.1 什么是Embedding

```
Embedding = 将离散的符号转换为连续的向量

为什么需要？
- 计算机不理解文字，只理解数字
- 需要把"语义"转换成"数字"
- 而且要让相似的语义→相似的数字

示例：
"机器学习" → [0.2, 0.8, -0.3, 0.1, ...]  (768维)
"人工智能" → [0.3, 0.7, -0.2, 0.2, ...]  (很接近！)
"今天天气" → [-0.5, 0.1, 0.8, -0.6, ...] (很远！)

核心思想：
- 语义相似 → 向量相似
- 可以用数学方法计算相似度
```

#### 1.2 Embedding如何训练

```
训练目标：让语义相似的文本有相似的向量

方法1：Word2Vec（早期）
- 根据上下文预测单词
- "我喜欢___机器学习"
- 模型学会：机器学习、深度学习、AI相关

方法2：BERT-based（现代）
- 使用Transformer架构
- 双向理解上下文
- 在大量文本上预训练

方法3：Sentence Transformers
- 专门优化句子级Embedding
- 使用对比学习（Contrastive Learning）
- 相似句子拉近，不相似句子推远

训练数据：
- 数十亿文本对
- "问题-答案"对
- "同义文本"对
- "相关文本"对
```

---

### 2. Embedding模型对比

#### 2.1 OpenAI Embeddings

```python
# OpenAI的Embedding API

from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="机器学习是人工智能的核心"
)

embedding = response.data[0].embedding

print(f"维度：{len(embedding)}")  # 1536
print(f"前5维：{embedding[:5]}")

# 特点：
# ✓ 质量很好
# ✓ 支持多语言
# ✓ 1536维
# ❌ 付费：$0.0001/1K tokens
# ❌ 数据发送到OpenAI
# ❌ 需要网络
```

**成本估算**：
```
场景：10万篇文档，每篇300字
- 总字符数：3000万
- 估算tokens：约1000万
- 成本：$1 (一次性)

查询：每天1000次查询，每次50字
- 每天tokens：约17K
- 每天成本：$0.0017
- 每月成本：$0.05

总结：文档入库贵，查询便宜
```

---

#### 2.2 开源模型（HuggingFace）

```python
from sentence_transformers import SentenceTransformer

# 方案1：英文小模型（快）
model = SentenceTransformer('all-MiniLM-L6-v2')
# 维度：384
# 速度：很快
# 质量：中等
# 适合：英文，快速原型

# 方案2：英文大模型（质量好）
model = SentenceTransformer('all-mpnet-base-v2')
# 维度：768
# 速度：中等
# 质量：很好
# 适合：英文，生产环境

# 方案3：中文模型
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
# 维度：768
# 速度：中等
# 质量：好
# 适合：多语言

# 方案4：中文专用（推荐）
model = SentenceTransformer('moka-ai/m3e-base')
# 维度：768
# 速度：快
# 质量：很好
# 适合：中文

# 使用
text = "机器学习是人工智能的分支"
embedding = model.encode(text)

print(f"维度：{len(embedding)}")
print(f"前5维：{embedding[:5]}")

# 特点：
# ✓ 完全免费
# ✓ 本地运行
# ✓ 不需要网络
# ✓ 数据不出本地
# ❌ 首次下载模型（几百MB）
```

---

#### 2.3 BGE系列（中文最佳）

```python
from sentence_transformers import SentenceTransformer

# BGE = BAAI General Embedding（智源）
# 中文Embedding的SOTA模型

# BGE-small（快）
model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
# 维度：512
# 速度：很快
# 推荐：快速原型

# BGE-base（平衡）
model = SentenceTransformer('BAAI/bge-base-zh-v1.5')
# 维度：768
# 速度：快
# 推荐：生产环境 ⭐

# BGE-large（最强）
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
# 维度：1024
# 速度：慢
# 推荐：追求极致质量

# 使用
text = "深度学习在图像识别中的应用"
embedding = model.encode(text)

# 特点：
# ✓ 中文效果最好
# ✓ 完全开源免费
# ✓ 支持指令增强
```

**BGE指令增强**：
```python
# BGE支持通过指令提升效果

# 普通方式
embedding = model.encode("机器学习")

# 指令增强（检索场景）
query_instruction = "为这个句子生成表示以用于检索相关文章："
embedding = model.encode(query_instruction + "机器学习")

# 指令让模型更好地理解任务
```

---

#### 2.4 模型对比表

```
┌────────────────┬──────┬──────┬──────┬────────┬────────┐
│     模型       │ 维度 │ 语言 │ 质量 │  速度  │  成本  │
├────────────────┼──────┼──────┼──────┼────────┼────────┤
│ OpenAI ada-002 │ 1536 │ 多   │ 很好 │  快    │ 付费   │
│ all-MiniLM-L6  │  384 │ 英   │ 中等 │  很快  │ 免费   │
│ all-mpnet-base │  768 │ 英   │ 好   │  快    │ 免费   │
│ m3e-base       │  768 │ 中   │ 好   │  快    │ 免费   │
│ bge-small-zh   │  512 │ 中   │ 好   │  很快  │ 免费   │
│ bge-base-zh    │  768 │ 中   │ 很好 │  快    │ 免费⭐ │
│ bge-large-zh   │ 1024 │ 中   │ 最好 │  中等  │ 免费   │
└────────────────┴──────┴──────┴──────┴────────┴────────┘

选择建议：
- 英文项目：all-mpnet-base-v2
- 中文项目：bge-base-zh-v1.5 ⭐⭐⭐
- 追求速度：all-MiniLM-L6-v2 或 bge-small-zh
- 追求质量：bge-large-zh-v1.5 或 OpenAI
- 隐私敏感：必须用本地模型
```

---

### 3. 本地部署方案

#### 3.1 SentenceTransformer部署

```python
"""
方案1：直接使用SentenceTransformer
最简单的本地部署
"""

# 安装
# pip install sentence-transformers

from sentence_transformers import SentenceTransformer

# 加载模型（首次会下载）
model = SentenceTransformer('BAAI/bge-base-zh-v1.5')

# 设置缓存目录（可选）
import os
os.environ['SENTENCE_TRANSFORMERS_HOME'] = './models/'

# 使用
def embed_text(text):
    """文本向量化"""
    return model.encode(text)

# 批量处理（更快）
texts = ["文本1", "文本2", "文本3"]
embeddings = model.encode(texts, batch_size=32)

print(f"✓ 模型加载完成")
print(f"  维度：{model.get_sentence_embedding_dimension()}")
```

---

#### 3.2 性能优化

```python
"""
方案2：GPU加速（如果有GPU）
"""

import torch
from sentence_transformers import SentenceTransformer

# 检查GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用设备：{device}")

# 加载到GPU
model = SentenceTransformer('BAAI/bge-base-zh-v1.5', device=device)

# 使用（自动在GPU上计算）
embedding = model.encode("测试文本")

# 性能对比：
# CPU：~50 sentences/秒
# GPU：~500 sentences/秒（10倍加速）
```

---

#### 3.3 缓存优化

```python
"""
方案3：结果缓存
避免重复计算
"""

from functools import lru_cache
import hashlib

class CachedEmbedding:
    """带缓存的Embedding"""
    
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.cache = {}
    
    def encode(self, text):
        """带缓存的编码"""
        # 计算文本hash作为key
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        if text_hash not in self.cache:
            # 不在缓存，计算
            self.cache[text_hash] = self.model.encode(text)
        
        return self.cache[text_hash]
    
    def cache_size(self):
        """缓存大小"""
        return len(self.cache)


# 使用
embedder = CachedEmbedding('BAAI/bge-base-zh-v1.5')

# 第一次：计算
embedding1 = embedder.encode("测试文本")  # 慢

# 第二次：从缓存
embedding2 = embedder.encode("测试文本")  # 快！

print(f"缓存数量：{embedder.cache_size()}")
```

---

#### 3.4 批处理优化

```python
"""
方案4：批处理
同时处理多个文本，提升吞吐量
"""

# ❌ 不好的方式：逐个处理
embeddings = []
for text in texts:
    emb = model.encode(text)  # 每次单独调用
    embeddings.append(emb)

# ✅ 好的方式：批处理
embeddings = model.encode(
    texts,
    batch_size=32,  # 批大小
    show_progress_bar=True  # 显示进度
)

# 性能差异：
# 1000个文本：
# - 逐个：60秒
# - 批处理：10秒（6倍加速）
```

---

### 4. Embedding质量评估

#### 4.1 相似度测试

```python
"""
评估方法1：相似度测试
检查语义相似的文本是否向量相似
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('BAAI/bge-base-zh-v1.5')

# 测试集
test_pairs = [
    {
        "text1": "机器学习是人工智能的分支",
        "text2": "AI的一个重要领域是机器学习",
        "expected": "高相似度"
    },
    {
        "text1": "今天天气很好",
        "text2": "机器学习算法",
        "expected": "低相似度"
    },
    {
        "text1": "如何学习Python编程",
        "text2": "Python编程入门教程",
        "expected": "高相似度"
    }
]

print("Embedding质量测试：\n")

for pair in test_pairs:
    emb1 = model.encode([pair["text1"]])
    emb2 = model.encode([pair["text2"]])
    
    similarity = cosine_similarity(emb1, emb2)[0][0]
    
    print(f"文本1：{pair['text1']}")
    print(f"文本2：{pair['text2']}")
    print(f"预期：{pair['expected']}")
    print(f"相似度：{similarity:.4f}")
    
    # 判断是否符合预期
    if pair['expected'] == "高相似度":
        status = "✓" if similarity > 0.5 else "❌"
    else:
        status = "✓" if similarity < 0.3 else "❌"
    
    print(f"结果：{status}\n")
```

---

#### 4.2 检索质量测试

```python
"""
评估方法2：检索质量测试
检查能否检索到正确的文档
"""

# 文档库
documents = [
    "Python是一种编程语言",
    "机器学习是AI的核心技术",
    "深度学习用于图像识别",
    "数据科学需要统计知识",
    "自然语言处理是AI的分支"
]

# 测试查询
test_queries = [
    {
        "query": "如何学习编程",
        "expected_doc": "Python是一种编程语言",
        "expected_rank": 1
    },
    {
        "query": "什么是人工智能",
        "expected_doc": "机器学习是AI的核心技术",
        "expected_rank": 1
    }
]

# 向量化
doc_embeddings = model.encode(documents)

# 测试
print("检索质量测试：\n")

for test in test_queries:
    # 查询向量化
    query_emb = model.encode([test["query"]])
    
    # 计算相似度
    similarities = cosine_similarity(query_emb, doc_embeddings)[0]
    
    # 排序
    ranked_indices = similarities.argsort()[::-1]
    
    # 检查结果
    print(f"查询：{test['query']}")
    print(f"预期：{test['expected_doc']}")
    print(f"结果：")
    
    for i, idx in enumerate(ranked_indices[:3], 1):
        print(f"  {i}. {documents[idx]} (相似度: {similarities[idx]:.4f})")
    
    # 验证
    top1_doc = documents[ranked_indices[0]]
    is_correct = top1_doc == test['expected_doc']
    
    print(f"是否正确：{'✓' if is_correct else '❌'}\n")
```

---

### 5. 最佳实践

#### 5.1 选择合适的模型

```python
"""
根据场景选择模型
"""

def choose_embedding_model(scenario):
    """选择Embedding模型"""
    
    recommendations = {
        "中文RAG系统": {
            "model": "BAAI/bge-base-zh-v1.5",
            "reason": "中文效果最好，速度快"
        },
        "英文RAG系统": {
            "model": "all-mpnet-base-v2",
            "reason": "英文质量好，广泛使用"
        },
        "多语言系统": {
            "model": "paraphrase-multilingual-mpnet-base-v2",
            "reason": "支持50+语言"
        },
        "快速原型": {
            "model": "all-MiniLM-L6-v2",
            "reason": "最快，适合快速迭代"
        },
        "追求质量": {
            "model": "BAAI/bge-large-zh-v1.5",
            "reason": "质量最高，适合生产"
        },
        "隐私敏感": {
            "model": "任何开源模型",
            "reason": "数据不出本地"
        }
    }
    
    return recommendations.get(scenario, {
        "model": "BAAI/bge-base-zh-v1.5",
        "reason": "通用推荐"
    })


# 使用
for scenario in ["中文RAG系统", "快速原型", "追求质量"]:
    rec = choose_embedding_model(scenario)
    print(f"{scenario}：")
    print(f"  推荐模型：{rec['model']}")
    print(f"  原因：{rec['reason']}\n")
```

---

#### 5.2 Normalize Embeddings

```python
"""
最佳实践：向量归一化
"""

import numpy as np

def normalize_embeddings(embeddings):
    """归一化向量到单位长度"""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms

# 为什么归一化？
# 1. 余弦相似度 = 点积（归一化后）
# 2. 计算更快（不需要除以norm）
# 3. 统一scale，便于比较

# 使用
texts = ["文本1", "文本2", "文本3"]
embeddings = model.encode(texts)

# 归一化
normalized_emb = normalize_embeddings(embeddings)

# 验证：norm应该都是1
norms = np.linalg.norm(normalized_emb, axis=1)
print(f"归一化后的norm: {norms}")  # [1. 1. 1.]

# 很多向量数据库要求归一化的向量
```

---

## 💻 Demo案例：Embedding完整实战

创建`embedding_advanced_demo.py`：

```python
"""
Embedding技术完整演示
从模型选择到质量评估
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time


def demo_1_model_comparison():
    """演示1：不同模型对比"""
    
    print("\n" + "="*60)
    print("演示1：Embedding模型对比")
    print("="*60 + "\n")
    
    # 测试文本
    text = "机器学习是人工智能的重要分支"
    
    models = [
        ('all-MiniLM-L6-v2', '英文小模型'),
        ('BAAI/bge-small-zh-v1.5', '中文小模型'),
        ('BAAI/bge-base-zh-v1.5', '中文基础模型')
    ]
    
    for model_name, desc in models:
        print(f"测试：{desc} ({model_name})")
        
        # 加载模型
        start = time.time()
        model = SentenceTransformer(model_name)
        load_time = time.time() - start
        
        # 编码
        start = time.time()
        embedding = model.encode(text)
        encode_time = time.time() - start
        
        print(f"  加载时间：{load_time:.2f}秒")
        print(f"  编码时间：{encode_time:.4f}秒")
        print(f"  向量维度：{len(embedding)}")
        print(f"  向量前5维：{embedding[:5]}\n")


def demo_2_batch_processing():
    """演示2：批处理性能"""
    
    print("\n" + "="*60)
    print("演示2：批处理 vs 逐个处理")
    print("="*60 + "\n")
    
    model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
    
    # 准备100个文本
    texts = [f"这是第{i}个测试文本" for i in range(100)]
    
    # 方法1：逐个处理
    print("方法1：逐个处理")
    start = time.time()
    embeddings_single = []
    for text in texts:
        emb = model.encode(text)
        embeddings_single.append(emb)
    time_single = time.time() - start
    print(f"  耗时：{time_single:.2f}秒\n")
    
    # 方法2：批处理
    print("方法2：批处理")
    start = time.time()
    embeddings_batch = model.encode(texts, batch_size=32)
    time_batch = time.time() - start
    print(f"  耗时：{time_batch:.2f}秒\n")
    
    # 对比
    speedup = time_single / time_batch
    print(f"加速比：{speedup:.1f}x")


def demo_3_similarity_testing():
    """演示3：相似度质量测试"""
    
    print("\n" + "="*60)
    print("演示3：Embedding质量测试")
    print("="*60 + "\n")
    
    model = SentenceTransformer('BAAI/bge-base-zh-v1.5')
    
    # 测试用例
    test_cases = [
        ("机器学习", "深度学习", "高"),
        ("机器学习", "人工智能", "高"),
        ("机器学习", "今天天气", "低"),
        ("Python编程", "Python教程", "高"),
        ("Python编程", "Java开发", "中"),
    ]
    
    print("相似度测试：\n")
    
    for text1, text2, expected in test_cases:
        emb1 = model.encode([text1])
        emb2 = model.encode([text2])
        
        sim = cosine_similarity(emb1, emb2)[0][0]
        
        print(f"文本1：{text1}")
        print(f"文本2：{text2}")
        print(f"预期：{expected}相似度")
        print(f"实际：{sim:.4f}")
        
        # 判断
        if expected == "高" and sim > 0.5:
            status = "✓"
        elif expected == "中" and 0.3 < sim <= 0.5:
            status = "✓"
        elif expected == "低" and sim <= 0.3:
            status = "✓"
        else:
            status = "❌"
        
        print(f"结果：{status}\n")


def demo_4_retrieval_testing():
    """演示4：检索质量测试"""
    
    print("\n" + "="*60)
    print("演示4：检索质量测试")
    print("="*60 + "\n")
    
    model = SentenceTransformer('BAAI/bge-base-zh-v1.5')
    
    # 文档库
    documents = [
        "Python是一种高级编程语言，广泛用于数据科学和AI开发",
        "机器学习是人工智能的核心技术，包括监督学习和无监督学习",
        "深度学习使用神经网络，在图像识别和自然语言处理中表现出色",
        "数据科学结合统计学和编程，用于从数据中提取洞察",
        "云计算提供按需计算资源，支持弹性扩展",
        "区块链是一种分布式账本技术，保证数据不可篡改"
    ]
    
    # 向量化
    doc_embeddings = model.encode(documents)
    
    # 测试查询
    queries = [
        "如何学习编程",
        "什么是AI",
        "图像识别技术"
    ]
    
    for query in queries:
        print(f"查询：{query}\n")
        
        # 向量化查询
        query_emb = model.encode([query])
        
        # 计算相似度
        similarities = cosine_similarity(query_emb, doc_embeddings)[0]
        
        # 排序
        ranked_indices = similarities.argsort()[::-1]
        
        # 显示Top 3
        print("检索结果：")
        for i, idx in enumerate(ranked_indices[:3], 1):
            print(f"  {i}. [{similarities[idx]:.4f}] {documents[idx][:40]}...")
        
        print()


def demo_5_normalization():
    """演示5：向量归一化"""
    
    print("\n" + "="*60)
    print("演示5：向量归一化")
    print("="*60 + "\n")
    
    model = SentenceTransformer('BAAI/bge-base-zh-v1.5')
    
    texts = ["文本1", "文本2", "文本3"]
    embeddings = model.encode(texts)
    
    # 原始向量的norm
    original_norms = np.linalg.norm(embeddings, axis=1)
    print(f"原始向量norm：{original_norms}")
    
    # 归一化
    normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized_norms = np.linalg.norm(normalized, axis=1)
    print(f"归一化后norm：{normalized_norms}")
    
    print("\n✓ 归一化后所有向量norm都是1")
    print("  好处：")
    print("  - 余弦相似度 = 点积")
    print("  - 计算更快")
    print("  - 统一scale")


def main():
    """主函数"""
    
    print("\n" + "="*60)
    print("🎯 Embedding技术完整演示")
    print("="*60)
    
    demo_1_model_comparison()
    demo_2_batch_processing()
    demo_3_similarity_testing()
    demo_4_retrieval_testing()
    demo_5_normalization()
    
    print("\n" + "="*60)
    print("✅ 所有演示完成！")
    print("="*60)
    print("\n💡 核心要点：")
    print("  1. 中文推荐：bge-base-zh-v1.5")
    print("  2. 使用批处理提升性能")
    print("  3. 测试Embedding质量")
    print("  4. 向量归一化")
    print("  5. 本地部署完全免费")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
```

---

## 🎯 核心要点总结

### Embedding三大要素

```
1. 模型选择：
   - 中文：bge-base-zh-v1.5 ⭐⭐⭐
   - 英文：all-mpnet-base-v2
   - 多语言：paraphrase-multilingual

2. 性能优化：
   - 批处理（必须）
   - GPU加速（如果有）
   - 结果缓存

3. 质量保证：
   - 相似度测试
   - 检索质量测试
   - 向量归一化
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解Embedding原理
- [ ] 选择合适的Embedding模型
- [ ] 本地部署Embedding模型
- [ ] 评估Embedding质量
- [ ] 优化Embedding性能

---

## 📝 下一课预告

**第43课：本地Embedding模型部署（多种方案）**

下一课我们将学习：
- LM Studio部署Embedding模型
- Ollama Embedding方案
- FastEmbed高性能方案
- 自建Embedding服务
- 生产环境部署最佳实践

**掌握多种部署方案，灵活应对各种场景！**

---

**🎉 恭喜你完成第42课！**

**你已经掌握了Embedding的核心技术！**

**进度：42/165课（25.5%完成）** 🚀
