![RAG系统架构](./images/rag_flow.svg)
*图：RAG系统架构*

# 第60课：实战：构建生产级RAG系统

> **本课目标**：整合所有技术，构建完整的生产级RAG系统
> 
> **核心技能**：系统架构、性能优化、错误处理、监控部署
> 
> **实战案例**：企业级RAG完整实现
> 
> **学习时长**：90分钟

---

## 📖 口播文案（5分钟）
![Generation](./images/generation.svg)
*图：Generation*


### 🎯 前言

"我见过太多这样的场景：

小王花了一个月，学完了RAG的所有技术：
- ✅ 向量检索学会了
- ✅ 混合检索搞懂了
- ✅ Query优化也会了
- ✅ Rerank也实现了

然后信心满满地开始做项目，结果：

**第一天**：写了个demo，本地跑得挺好
**第二天**：加了几千个文档，查询速度变成10秒
**第三天**：出现一个错误，整个系统崩溃，不知道哪里出问题
**第四天**：老板问效果怎么样，他说'不知道，没监控'
**第五天**：想改个参数，发现代码太乱，不敢动

**为什么会这样？因为demo和生产系统差距太大了！**

我自己在做RAG项目时也踩过无数坑：

**性能坑**：
- 初版系统查询要15秒，用户完全无法接受
- 优化后降到2秒以内，才算能用

**稳定性坑**：
- 某个文档格式不对，整个系统就崩了
- 向量库偶尔连接失败，没有重试机制

**维护性坑**：
- 代码写得太随意，3个月后自己都看不懂
- 想加个新功能，发现要改一堆地方

**监控盲区**：
- 用户说"你这个系统不行啊"，我问哪里不行，他说不知道
- 查了半天日志，发现根本没记录关键信息

这些坑，花了我大半年时间才填完！

**今天这一课，我要把这些血泪教训全部分享给你！**

我们要构建的不是一个demo，而是一个：

✅ **高性能**的系统
   - 查询响应 < 2秒
   - 支持并发查询
   - 资源利用率高

✅ **高可靠**的系统
   - 完善的错误处理
   - 自动重试机制
   - 降级策略

✅ **可观测**的系统
   - 详细的日志记录
   - 实时性能监控
   - 问题快速定位

✅ **易维护**的系统
   - 代码结构清晰
   - 配置灵活可调
   - 文档完善

✅ **可扩展**的系统
   - 模块化设计
   - 插件化架构
   - 易于添加新功能

这一课我会教你：

**第一部分：完整架构设计**
- 分层架构的设计原则
- 各模块的职责划分
- 接口设计的最佳实践

**第二部分：核心代码实现**
- 配置管理系统
- 完整的RAG Pipeline
- 错误处理机制
- 缓存策略

**第三部分：性能优化**
- 查询性能优化
- 内存优化
- 批处理优化
- 异步处理

**第四部分：监控和日志**
- 结构化日志
- 性能指标采集
- 监控大盘
- 告警机制

**第五部分：部署方案**
- Docker容器化
- API服务部署
- 负载均衡
- 高可用方案

**这是你从入门到精通的最后一课，也是最重要的一课！**

学完这一课，你就能独立构建一个真正能上线的RAG系统！

准备好了吗？让我们开始！"

---

### 💡 课程核心价值

```
【Demo系统 vs 生产系统】

Demo系统：
• 功能能跑就行
• 性能慢点无所谓
• 出错了重启
• 代码随便写
• 没有监控

生产系统：
• 功能稳定可靠 ✅
• 性能达标 < 2秒 ✅
• 错误自动处理 ✅
• 代码规范易维护 ✅
• 监控告警完善 ✅

这一课教你如何从左边到右边！
```

---

## 📚 第一部分：系统架构设计

### 一、架构设计原则

```
【优秀架构的六大原则】

1. 单一职责原则
   每个模块只做一件事，做好一件事

2. 开闭原则
   对扩展开放，对修改封闭

3. 依赖倒置原则
   依赖抽象，不依赖具体实现

4. 接口隔离原则
   接口小而专，不要臃肿

5. 高内聚低耦合
   模块内部紧密，模块之间松散

6. 可测试性
   每个模块都可以独立测试
```

### 二、整体架构

```
┌─────────────────────────────────────────────────┐
│                  客户端层                        │
│  Web UI / API / 命令行                          │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│                  接口层                          │
│  • 请求验证                                      │
│  • 限流控制                                      │
│  • 结果缓存                                      │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│               核心处理层                         │
│  ┌───────────────────────────────────┐          │
│  │  1. Query优化模块                  │          │
│  │     • 预处理                       │          │
│  │     • 纠错                         │          │
│  │     • 扩展                         │          │
│  └────────────┬──────────────────────┘          │
│               ↓                                  │
│  ┌───────────────────────────────────┐          │
│  │  2. 检索模块                       │          │
│  │     • 向量检索                     │          │
│  │     • BM25检索                     │          │
│  │     • 元数据过滤                   │          │
│  │     • 结果融合                     │          │
│  └────────────┬──────────────────────┘          │
│               ↓                                  │
│  ┌───────────────────────────────────┐          │
│  │  3. 重排序模块                     │          │
│  │     • Cross-Encoder                │          │
│  └────────────┬──────────────────────┘          │
│               ↓                                  │
│  ┌───────────────────────────────────┐          │
│  │  4. 生成模块                       │          │
│  │     • Prompt构建                   │          │
│  │     • LLM调用                      │          │
│  │     • 答案后处理                   │          │
│  └───────────────────────────────────┘          │
└─────────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│                 数据层                           │
│  • 向量数据库 (Chroma)                          │
│  • 文档存储                                      │
│  • 缓存 (Redis)                                 │
│  • 日志存储                                      │
└─────────────────────────────────────────────────┘
```

---

## 💻 第二部分：核心代码实现

### 一、项目结构

```
production_rag/
├── config/
│   ├── __init__.py
│   ├── settings.py          # 配置管理
│   └── prompts.py           # Prompt模板
├── core/
│   ├── __init__.py
│   ├── query_optimizer.py   # Query优化
│   ├── retriever.py         # 检索器
│   ├── reranker.py          # 重排序
│   └── generator.py         # 答案生成
├── utils/
│   ├── __init__.py
│   ├── logger.py            # 日志工具
│   ├── cache.py             # 缓存工具
│   └── metrics.py           # 指标收集
├── api/
│   ├── __init__.py
│   ├── app.py               # FastAPI应用
│   └── models.py            # API模型
├── tests/
│   ├── test_retriever.py
│   ├── test_reranker.py
│   └── test_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 二、配置管理系统

```python
# config/settings.py
from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """系统配置（支持环境变量）"""
    
    # ========== 基础配置 ==========
    app_name: str = "Production RAG System"
    version: str = "1.0.0"
    debug: bool = False
    
    # ========== 模型配置 ==========
    embedding_model: str = "moka-ai/m3e-base"
    embedding_device: str = "cpu"
    embedding_batch_size: int = 32
    
    rerank_model: str = "BAAI/bge-reranker-base"
    rerank_enabled: bool = True
    rerank_batch_size: int = 16
    
    # ========== LLM配置 ==========
    llm_base_url: str = "http://localhost:1234/v1"
    llm_api_key: str = "lm-studio"
    llm_model: str = "local-model"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 500
    llm_timeout: int = 30
    
    # ========== 检索配置 ==========
    retrieval_k: int = 20
    retrieval_timeout: int = 10
    rerank_k: int = 5
    
    # ========== 向量库配置 ==========
    vector_db_path: str = "./data/chroma_db"
    vector_db_collection: str = "documents"
    
    # ========== 缓存配置 ==========
    cache_enabled: bool = True
    cache_ttl: int = 3600
    cache_max_size: int = 1000
    
    # ========== 性能配置 ==========
    max_concurrent_queries: int = 10
    query_timeout: int = 60
    
    # ========== 日志配置 ==========
    log_level: str = "INFO"
    log_file: str = "./logs/rag_system.log"
    log_rotation: str = "1 day"
    log_retention: str = "30 days"
    
    # ========== 监控配置 ==========
    metrics_enabled: bool = True
    metrics_port: int = 9090
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 全局配置实例
settings = Settings()

# config/prompts.py
class PromptTemplates:
    """Prompt模板管理"""
    
    QA_TEMPLATE = """请基于以下上下文回答问题。

上下文：
{context}

问题：{query}

要求：
1. 如果上下文中有相关信息，请基于上下文准确回答
2. 如果上下文中没有相关信息，请明确说"根据提供的信息，我无法回答这个问题"
3. 不要编造信息
4. 回答要简洁明了
5. 如果可能，请引用具体的上下文片段

答案："""
    
    SUMMARY_TEMPLATE = """请总结以下内容：

{content}

总结："""
    
    @staticmethod
    def format_qa_prompt(query: str, context: str) -> str:
        """格式化QA Prompt"""
        return PromptTemplates.QA_TEMPLATE.format(
            query=query,
            context=context
        )
```

### 三、核心系统类

```python
# core/rag_system.py
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@dataclass
class RAGConfig:
    """RAG系统配置"""
    # 向量模型
    embedding_model: str = "moka-ai/m3e-base"
    rerank_model: str = "BAAI/bge-reranker-base"
    
    # LLM配置
    llm_base_url: str = "http://localhost:1234/v1"
    llm_api_key: str = "lm-studio"
    llm_model: str = "local-model"
    llm_temperature: float = 0
    
    # 检索配置
    retrieval_k: int = 20
    rerank_k: int = 5
    
    # 性能配置
    enable_cache: bool = True
    enable_rerank: bool = True
    cache_ttl: int = 3600
    
    # 超时配置
    retrieval_timeout: int = 10
    generation_timeout: int = 30

@dataclass
class QueryResult:
    """查询结果"""
    query: str
    answer: str
    sources: List[Dict]
    metadata: Dict
    timing: Dict
    
    def to_dict(self):
        return asdict(self)

class ProductionRAGSystem:
    """生产级RAG系统"""
    
    def __init__(self, config: RAGConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self._init_components()
        
        # 性能指标
        self.metrics = {
            'total_queries': 0,
            'cache_hits': 0,
            'errors': 0
        }
    
    def _init_components(self):
        """初始化所有组件"""
        try:
            self.logger.info("初始化RAG系统组件...")
            
            # 1. Query优化器
            from query_optimizer import QueryOptimizer
            self.query_optimizer = QueryOptimizer()
            
            # 2. 检索器
            from hybrid_retriever import HybridRetriever
            self.retriever = HybridRetriever(
                embedding_model=self.config.embedding_model
            )
            
            # 3. 重排序器
            if self.config.enable_rerank:
                from reranker import CrossEncoderReranker
                self.reranker = CrossEncoderReranker(
                    model_name=self.config.rerank_model
                )
            
            # 4. LLM客户端
            from langchain.chat_models import ChatOpenAI
            self.llm = ChatOpenAI(
                base_url=self.config.llm_base_url,
                api_key=self.config.llm_api_key,
                model=self.config.llm_model,
                temperature=self.config.llm_temperature
            )
            
            # 5. 缓存
            if self.config.enable_cache:
                self.cache = {}
            
            self.logger.info("✅ 组件初始化完成")
            
        except Exception as e:
            self.logger.error(f"组件初始化失败: {e}")
            raise
    
    def query(
        self,
        query: str,
        metadata_filters: Optional[Dict] = None,
        verbose: bool = False
    ) -> QueryResult:
        """
        执行查询
        
        Args:
            query: 用户查询
            metadata_filters: 元数据过滤条件
            verbose: 是否输出详细日志
        """
        start_time = time.time()
        timing = {}
        
        try:
            self.metrics['total_queries'] += 1
            
            if verbose:
                self.logger.info(f"收到查询: {query}")
            
            # 1. 检查缓存
            if self.config.enable_cache:
                cache_key = self._get_cache_key(query, metadata_filters)
                cached = self._get_from_cache(cache_key)
                if cached:
                    self.metrics['cache_hits'] += 1
                    if verbose:
                        self.logger.info("✅ 缓存命中")
                    return cached
            
            # 2. Query优化
            t0 = time.time()
            optimized = self.query_optimizer.optimize(query, verbose=False)
            timing['query_optimization'] = time.time() - t0
            
            if verbose:
                self.logger.info(f"Query优化: {optimized['corrected']}")
            
            # 3. 检索
            t0 = time.time()
            retrieved = self.retriever.search(
                query=optimized['corrected'],
                k=self.config.retrieval_k,
                metadata_filters=metadata_filters
            )
            timing['retrieval'] = time.time() - t0
            
            if verbose:
                self.logger.info(f"检索到 {len(retrieved)} 个文档")
            
            # 4. 重排序
            if self.config.enable_rerank and retrieved:
                t0 = time.time()
                docs = [doc.content for doc, _ in retrieved]
                reranked = self.reranker.rerank(
                    query=optimized['corrected'],
                    documents=docs,
                    top_k=self.config.rerank_k
                )
                timing['rerank'] = time.time() - t0
                
                # 重新构建结果
                retrieved = [(docs[idx], score) for _, score, idx in reranked]
                
                if verbose:
                    self.logger.info(f"重排序完成，保留Top-{len(retrieved)}")
            
            # 5. 生成答案
            t0 = time.time()
            answer = self._generate_answer(
                query=query,
                context_docs=retrieved
            )
            timing['generation'] = time.time() - t0
            
            if verbose:
                self.logger.info("答案生成完成")
            
            # 6. 构建结果
            total_time = time.time() - start_time
            timing['total'] = total_time
            
            result = QueryResult(
                query=query,
                answer=answer,
                sources=[
                    {
                        'content': doc[:200] + '...',
                        'score': float(score)
                    }
                    for doc, score in retrieved[:5]
                ],
                metadata={
                    'optimized_query': optimized['corrected'],
                    'intent': optimized.get('intent', {}).get('value', 'unknown'),
                    'num_retrieved': len(retrieved)
                },
                timing=timing
            )
            
            # 7. 缓存结果
            if self.config.enable_cache:
                self._save_to_cache(cache_key, result)
            
            if verbose:
                self.logger.info(f"✅ 查询完成，总耗时: {total_time:.3f}秒")
            
            return result
            
        except Exception as e:
            self.metrics['errors'] += 1
            self.logger.error(f"查询失败: {e}", exc_info=True)
            
            # 返回错误结果
            return QueryResult(
                query=query,
                answer=f"抱歉，查询过程中出现错误: {str(e)}",
                sources=[],
                metadata={'error': str(e)},
                timing={'total': time.time() - start_time}
            )
    
    def _generate_answer(
        self,
        query: str,
        context_docs: List[tuple]
    ) -> str:
        """生成答案"""
        # 构建上下文
        context = "\n\n".join([
            f"【文档{i+1}】\n{doc}"
            for i, (doc, _) in enumerate(context_docs)
        ])
        
        # 构建Prompt
        prompt = f"""请基于以下上下文回答问题。

上下文：
{context}

问题：{query}

要求：
1. 如果上下文中有相关信息，请准确回答
2. 如果上下文中没有相关信息，请明确说明
3. 不要编造信息
4. 回答要简洁明了

答案："""
        
        # 调用LLM
        response = self.llm.invoke(prompt)
        return response.content
    
    def _get_cache_key(self, query: str, metadata_filters: Optional[Dict]) -> str:
        """生成缓存key"""
        import hashlib
        key_str = f"{query}_{json.dumps(metadata_filters, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_from_cache(self, key: str) -> Optional[QueryResult]:
        """从缓存获取"""
        return self.cache.get(key)
    
    def _save_to_cache(self, key: str, result: QueryResult):
        """保存到缓存"""
        self.cache[key] = result
    
    def get_metrics(self) -> Dict:
        """获取性能指标"""
        return {
            **self.metrics,
            'cache_hit_rate': (
                self.metrics['cache_hits'] / self.metrics['total_queries']
                if self.metrics['total_queries'] > 0 else 0
            )
        }
    
    def health_check(self) -> Dict:
        """健康检查"""
        return {
            'status': 'healthy',
            'components': {
                'retriever': 'ok',
                'reranker': 'ok' if self.config.enable_rerank else 'disabled',
                'llm': 'ok',
                'cache': 'ok' if self.config.enable_cache else 'disabled'
            },
            'metrics': self.get_metrics()
        }
```

---

---

## 🔧 第三部分：性能优化

### 一、查询性能优化

```python
# utils/performance.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable, Any

class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def parallel_execute(
        self,
        tasks: List[Callable],
        *args, **kwargs
    ) -> List[Any]:
        """并行执行多个任务"""
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(self.executor, task, *args, **kwargs)
            for task in tasks
        ]
        return await asyncio.gather(*futures)

# 在RAG系统中使用
class OptimizedRAGSystem(ProductionRAGSystem):
    """性能优化版RAG系统"""
    
    async def query_async(
        self,
        query: str,
        **kwargs
    ) -> QueryResult:
        """异步查询（提升并发性能）"""
        
        # 1. Query优化（可并行）
        optimized_task = asyncio.create_task(
            self._optimize_query_async(query)
        )
        
        # 2. 等待优化完成
        optimized = await optimized_task
        
        # 3. 检索（可能需要多个源）
        retrieval_tasks = [
            self._vector_search_async(optimized['corrected']),
            self._bm25_search_async(optimized['corrected'])
        ]
        
        results = await asyncio.gather(*retrieval_tasks)
        
        # 4. 融合和重排序
        fused = self._fuse_results(results)
        
        if self.config.enable_rerank:
            reranked = await self._rerank_async(query, fused)
        else:
            reranked = fused
        
        # 5. 生成答案
        answer = await self._generate_async(query, reranked)
        
        return self._build_result(query, answer, reranked)
```

### 二、缓存策略

```python
# utils/cache.py
from functools import lru_cache
import hashlib
import time
from typing import Optional, Any
import redis

class SmartCache:
    """智能缓存系统"""
    
    def __init__(
        self,
        use_redis: bool = False,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        ttl: int = 3600,
        max_size: int = 1000
    ):
        self.ttl = ttl
        self.use_redis = use_redis
        
        if use_redis:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True
            )
        else:
            # 使用内存缓存
            self.memory_cache = {}
            self.cache_times = {}
            self.max_size = max_size
    
    def _get_key(self, query: str, **kwargs) -> str:
        """生成缓存key"""
        key_str = f"{query}_{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, query: str, **kwargs) -> Optional[Any]:
        """获取缓存"""
        key = self._get_key(query, **kwargs)
        
        if self.use_redis:
            return self._get_from_redis(key)
        else:
            return self._get_from_memory(key)
    
    def set(self, query: str, value: Any, **kwargs):
        """设置缓存"""
        key = self._get_key(query, **kwargs)
        
        if self.use_redis:
            self._set_to_redis(key, value)
        else:
            self._set_to_memory(key, value)
    
    def _get_from_memory(self, key: str) -> Optional[Any]:
        """从内存获取"""
        if key not in self.memory_cache:
            return None
        
        # 检查是否过期
        if time.time() - self.cache_times[key] > self.ttl:
            del self.memory_cache[key]
            del self.cache_times[key]
            return None
        
        return self.memory_cache[key]
    
    def _set_to_memory(self, key: str, value: Any):
        """设置到内存"""
        # LRU淘汰
        if len(self.memory_cache) >= self.max_size:
            oldest_key = min(self.cache_times, key=self.cache_times.get)
            del self.memory_cache[oldest_key]
            del self.cache_times[oldest_key]
        
        self.memory_cache[key] = value
        self.cache_times[key] = time.time()
    
    def _get_from_redis(self, key: str) -> Optional[Any]:
        """从Redis获取"""
        import json
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    def _set_to_redis(self, key: str, value: Any):
        """设置到Redis"""
        import json
        self.redis_client.setex(
            key,
            self.ttl,
            json.dumps(value)
        )
```

### 三、批处理优化

```python
class BatchProcessor:
    """批处理优化器"""
    
    def __init__(self, batch_size: int = 32):
        self.batch_size = batch_size
    
    def batch_embed(
        self,
        texts: List[str],
        model
    ) -> np.ndarray:
        """批量向量化（减少模型调用次数）"""
        embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_emb = model.encode(batch)
            embeddings.append(batch_emb)
        
        return np.vstack(embeddings)
    
    def batch_rerank(
        self,
        query: str,
        documents: List[str],
        model,
        batch_size: int = 16
    ) -> List[float]:
        """批量重排序"""
        scores = []
        
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            pairs = [[query, doc] for doc in batch_docs]
            batch_scores = model.predict(pairs)
            scores.extend(batch_scores)
        
        return scores
```

---

## 📊 第四部分：监控和日志

### 一、结构化日志

```python
# utils/logger.py
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class StructuredLogger:
    """结构化日志器"""
    
    def __init__(
        self,
        name: str,
        log_file: str = "./logs/rag_system.log",
        level: str = "INFO"
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        
        # 确保日志目录存在
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # 文件处理器
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(getattr(logging, level))
        
        # 控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, level))
        
        # 格式化
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_query(
        self,
        query: str,
        result: QueryResult,
        user_id: Optional[str] = None,
        **extra
    ):
        """记录查询日志"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'event': 'query',
            'user_id': user_id,
            'query': query,
            'query_length': len(query),
            'answer_length': len(result.answer),
            'num_sources': len(result.sources),
            'timing': result.timing,
            'metadata': result.metadata,
            **extra
        }
        
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
    
    def log_error(
        self,
        error: Exception,
        context: Dict[str, Any]
    ):
        """记录错误日志"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'event': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context
        }
        
        self.logger.error(json.dumps(log_data, ensure_ascii=False))
    
    def log_performance(
        self,
        operation: str,
        duration: float,
        **metrics
    ):
        """记录性能日志"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'event': 'performance',
            'operation': operation,
            'duration': duration,
            **metrics
        }
        
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
```

### 二、性能指标采集

```python
# utils/metrics.py
from dataclasses import dataclass, field
from typing import Dict, List
import time
from collections import defaultdict
import numpy as np

@dataclass
class MetricsCollector:
    """性能指标收集器"""
    
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    query_times: List[float] = field(default_factory=list)
    retrieval_times: List[float] = field(default_factory=list)
    rerank_times: List[float] = field(default_factory=list)
    generation_times: List[float] = field(default_factory=list)
    
    error_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    def record_query(
        self,
        success: bool,
        timing: Dict[str, float],
        cache_hit: bool = False
    ):
        """记录查询指标"""
        self.total_queries += 1
        
        if success:
            self.successful_queries += 1
        else:
            self.failed_queries += 1
        
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        # 记录时间
        if 'total' in timing:
            self.query_times.append(timing['total'])
        if 'retrieval' in timing:
            self.retrieval_times.append(timing['retrieval'])
        if 'rerank' in timing:
            self.rerank_times.append(timing['rerank'])
        if 'generation' in timing:
            self.generation_times.append(timing['generation'])
    
    def record_error(self, error_type: str):
        """记录错误"""
        self.error_counts[error_type] += 1
    
    def get_summary(self) -> Dict:
        """获取指标摘要"""
        return {
            'total_queries': self.total_queries,
            'successful_queries': self.successful_queries,
            'failed_queries': self.failed_queries,
            'success_rate': (
                self.successful_queries / self.total_queries
                if self.total_queries > 0 else 0
            ),
            'cache_hit_rate': (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0 else 0
            ),
            'avg_query_time': np.mean(self.query_times) if self.query_times else 0,
            'p50_query_time': np.percentile(self.query_times, 50) if self.query_times else 0,
            'p95_query_time': np.percentile(self.query_times, 95) if self.query_times else 0,
            'p99_query_time': np.percentile(self.query_times, 99) if self.query_times else 0,
            'avg_retrieval_time': np.mean(self.retrieval_times) if self.retrieval_times else 0,
            'avg_rerank_time': np.mean(self.rerank_times) if self.rerank_times else 0,
            'avg_generation_time': np.mean(self.generation_times) if self.generation_times else 0,
            'error_counts': dict(self.error_counts)
        }
```

---

## 🚀 第五部分：API服务与部署

### 一、FastAPI完整实现

```python
# api/app.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import time

app = FastAPI(
    title="Production RAG API",
    version="1.0.0",
    description="企业级RAG系统API"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化RAG系统（单例模式）
rag_system = None

def get_rag_system():
    """获取RAG系统实例"""
    global rag_system
    if rag_system is None:
        from config.settings import settings
        rag_system = ProductionRAGSystem(settings)
    return rag_system

# API模型定义
class QueryRequest(BaseModel):
    query: str
    metadata_filters: Optional[Dict] = None
    user_id: Optional[str] = None
    verbose: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "query": "什么是人工智能？",
                "metadata_filters": {"category": "技术"},
                "user_id": "user123",
                "verbose": False
            }
        }

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[Dict]
    metadata: Dict
    timing: Dict
    request_id: str

class HealthResponse(BaseModel):
    status: str
    version: str
    components: Dict
    timestamp: str

@app.post("/v1/query", response_model=QueryResponse, tags=["Query"])
async def query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    rag: ProductionRAGSystem = Depends(get_rag_system)
):
    """
    查询接口
    
    - **query**: 用户查询文本
    - **metadata_filters**: 元数据过滤条件（可选）
    - **user_id**: 用户ID（可选，用于日志）
    - **verbose**: 是否返回详细信息
    """
    import uuid
    request_id = str(uuid.uuid4())
    
    try:
        start_time = time.time()
        
        result = rag.query(
            query=request.query,
            metadata_filters=request.metadata_filters,
            verbose=request.verbose
        )
        
        # 后台任务：记录日志
        background_tasks.add_task(
            rag.logger.log_query,
            query=request.query,
            result=result,
            user_id=request.user_id,
            request_id=request_id
        )
        
        response = result.to_dict()
        response['request_id'] = request_id
        
        return response
        
    except Exception as e:
        rag.logger.log_error(e, {
            'query': request.query,
            'request_id': request_id
        })
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health(rag: ProductionRAGSystem = Depends(get_rag_system)):
    """健康检查"""
    from datetime import datetime
    
    health_status = rag.health_check()
    health_status['timestamp'] = datetime.now().isoformat()
    
    return health_status

@app.get("/metrics", tags=["System"])
async def metrics(rag: ProductionRAGSystem = Depends(get_rag_system)):
    """性能指标"""
    return rag.metrics_collector.get_summary()

@app.post("/v1/index", tags=["Management"])
async def index_documents(
    documents: List[str],
    rag: ProductionRAGSystem = Depends(get_rag_system)
):
    """索引文档"""
    try:
        rag.index_documents(documents)
        return {"status": "success", "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### 二、Docker部署

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p logs data

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=true
      - RERANK_ENABLED=true
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### 三、部署脚本

```bash
# deploy.sh
#!/bin/bash

echo "🚀 开始部署RAG系统..."

# 1. 构建Docker镜像
echo "📦 构建Docker镜像..."
docker-compose build

# 2. 启动服务
echo "🔄 启动服务..."
docker-compose up -d

# 3. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 4. 健康检查
echo "🏥 健康检查..."
curl -f http://localhost:8000/health || exit 1

echo "✅ 部署完成！"
echo "📍 API地址: http://localhost:8000"
echo "📖 API文档: http://localhost:8000/docs"
```

---

## 🎯 第六部分：测试与质量保证

### 一、单元测试

```python
# tests/test_retriever.py
import pytest
from core.retriever import HybridRetriever

class TestRetriever:
    """测试检索器"""
    
    @pytest.fixture
    def retriever(self):
        """测试夹具"""
        return HybridRetriever()
    
    @pytest.fixture
    def sample_documents(self):
        """示例文档"""
        return [
            "人工智能是计算机科学的分支",
            "机器学习是AI的核心技术",
            "深度学习使用神经网络"
        ]
    
    def test_index_documents(self, retriever, sample_documents):
        """测试文档索引"""
        retriever.index_documents(sample_documents)
        assert len(retriever.documents) == 3
    
    def test_search(self, retriever, sample_documents):
        """测试检索功能"""
        retriever.index_documents(sample_documents)
        results = retriever.search("什么是AI", k=2)
        assert len(results) <= 2
        assert all(isinstance(r, tuple) for r in results)
    
    def test_empty_query(self, retriever, sample_documents):
        """测试空查询"""
        retriever.index_documents(sample_documents)
        results = retriever.search("", k=5)
        assert len(results) == 0

# tests/test_api.py
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_query():
    """测试查询接口"""
    response = client.post(
        "/v1/query",
        json={"query": "什么是人工智能？"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
```

### 二、性能测试

```python
# tests/performance_test.py
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

def performance_test(rag_system, num_queries: int = 100):
    """性能测试"""
    
    test_queries = [
        "什么是人工智能？",
        "机器学习的应用场景",
        "深度学习vs传统机器学习"
    ] * (num_queries // 3)
    
    print(f"🧪 开始性能测试 ({num_queries}次查询)...")
    
    # 单线程测试
    print("\n【单线程测试】")
    single_times = []
    start = time.time()
    
    for query in test_queries:
        t0 = time.time()
        rag_system.query(query, verbose=False)
        single_times.append(time.time() - t0)
    
    single_total = time.time() - start
    
    print(f"总耗时: {single_total:.2f}秒")
    print(f"平均耗时: {statistics.mean(single_times):.3f}秒")
    print(f"QPS: {num_queries / single_total:.2f}")
    
    # 并发测试
    print("\n【并发测试】(10线程)")
    concurrent_times = []
    
    def query_task(query):
        t0 = time.time()
        rag_system.query(query, verbose=False)
        return time.time() - t0
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        concurrent_times = list(executor.map(query_task, test_queries))
    
    concurrent_total = time.time() - start
    
    print(f"总耗时: {concurrent_total:.2f}秒")
    print(f"平均耗时: {statistics.mean(concurrent_times):.3f}秒")
    print(f"QPS: {num_queries / concurrent_total:.2f}")
    
    # 性能分析
    print("\n【性能分析】")
    print(f"P50: {statistics.median(single_times):.3f}秒")
    print(f"P95: {sorted(single_times)[int(0.95*len(single_times))]:.3f}秒")
    print(f"P99: {sorted(single_times)[int(0.99*len(single_times))]:.3f}秒")
```

---

## 📋 第七部分：最佳实践与经验总结

### 一、性能优化清单

```
✅ 【必做】缓存热门查询
   → 可提升30-50%响应速度

✅ 【必做】批量处理embedding
   → 减少模型调用次数，提升2-3倍速度

✅ 【必做】异步处理非关键任务
   → 日志记录、指标上报等

✅ 【推荐】使用连接池
   → 数据库、Redis连接复用

✅ 【推荐】限制检索候选数
   → retrieval_k=20-50即可，不要太大

✅ 【推荐】开启重排序
   → 显著提升准确性，成本可控

✅ 【可选】使用GPU加速
   → embedding和rerank可以GPU加速
```

### 二、稳定性保障清单

```
✅ 【必做】完善的错误处理
   • try-catch包裹所有外部调用
   • 返回友好的错误信息
   • 记录详细的错误日志

✅ 【必做】超时控制
   • 设置合理的超时时间
   • 避免长时间阻塞

✅ 【必做】重试机制
   • 网络请求失败自动重试
   • 指数退避策略

✅ 【必做】降级策略
   • 向量检索失败→降级到BM25
   • Rerank失败→返回原始检索结果
   • LLM失败→返回检索到的原文

✅ 【推荐】熔断机制
   • 连续失败达到阈值→暂停调用
   • 自动恢复机制

✅ 【推荐】限流保护
   • API限流：防止过载
   • 用户限流：防止滥用
```

### 三、可观测性清单

```
✅ 【必做】结构化日志
   • JSON格式
   • 包含关键信息（query、timing、结果等）
   • 便于查询和分析

✅ 【必做】性能指标
   • 查询耗时（P50、P95、P99）
   • QPS（每秒查询数）
   • 错误率
   • 缓存命中率

✅ 【必做】健康检查
   • /health 接口
   • 检查各组件状态
   • 用于负载均衡探活

✅ 【推荐】分布式追踪
   • 使用Trace ID串联请求
   • 查看完整调用链

✅ 【推荐】告警机制
   • 错误率超阈值→告警
   • 响应时间超阈值→告警
   • 服务不可用→告警
```

### 四、安全性清单

```
✅ 【必做】输入验证
   • Query长度限制
   • 特殊字符过滤
   • SQL注入防护

✅ 【必做】API认证
   • API Key验证
   • Token机制
   • 权限控制

✅ 【必做】数据脱敏
   • 日志中敏感信息脱敏
   • PII数据保护

✅ 【推荐】HTTPS
   • 生产环境使用HTTPS
   • 证书管理

✅ 【推荐】审计日志
   • 记录敏感操作
   • 数据访问审计
```

---

## 📝 课后练习

### 练习1：添加流式输出
为API添加流式输出功能，让用户可以实时看到答案生成过程

### 练习2：实现多租户
支持多个租户共用一个系统，每个租户有独立的数据和配置

### 练习3：添加反馈机制
让用户可以对答案点赞/点踩，用于持续优化

### 练习4：实现A/B测试
支持同时运行多个版本的模型，对比效果

---

## 🎓 知识总结

### 核心要点回顾

1. **架构设计**
   - 分层架构：接口层、核心层、数据层
   - 模块化：每个模块职责单一
   - 可扩展：易于添加新功能

2. **性能优化**
   - 缓存：减少重复计算
   - 批处理：提升吞吐量
   - 异步：提高并发性能

3. **监控日志**
   - 结构化日志：便于分析
   - 性能指标：及时发现问题
   - 告警机制：快速响应

4. **质量保证**
   - 单元测试：保证功能正确
   - 性能测试：验证性能指标
   - 错误处理：提升稳定性

### 生产级系统的核心特征

```
Demo系统                  生产系统
├─ 功能能跑       →      ├─ 功能稳定可靠
├─ 性能不关注     →      ├─ 性能优化到位
├─ 错误就崩溃     →      ├─ 错误优雅处理
├─ 代码随意写     →      ├─ 代码规范清晰
└─ 没有监控       →      └─ 监控告警完善
```

### 关键指标

```
性能指标：
• 查询响应时间 < 2秒 (P95)
• QPS > 10 (单机)
• 缓存命中率 > 30%

质量指标：
• 错误率 < 1%
• 可用性 > 99.9%
• 准确率 > 85%
```

---

## 🚀 下节预告

**第10章完成！恭喜你完成RAG系统的完整学习！**

下一章：**第四模块：Agent智能体开发**

- Agent架构设计
- 工具调用机制
- ReAct模式实现
- 多Agent协作

**从RAG到Agent，开启新的篇章！** 🎯

---

## 💪 最后的话

"从第41课到第60课，我们完整学习了RAG系统的方方面面：

- 从向量数据库的基础原理
- 到文档处理的工程化实践
- 从基础检索到混合检索
- 从Query优化到Rerank重排序
- 最后到完整的生产级系统

这20课的内容，是我在实际项目中踩过无数坑、花了大量时间总结出来的精华！

如果你能完整学完并实践这些内容，你已经具备了：
✅ 构建企业级RAG系统的能力
✅ 解决实际问题的能力
✅ 持续优化系统的能力

记住：
- 好的系统不是一蹴而就的，需要持续迭代
- 监控和日志是你最好的朋友
- 用户反馈比任何指标都重要

接下来，继续学习Agent智能体开发，让你的AI应用更加智能！

加油！💪"

---

**🎉 RAG系统完整章节学习完成！**

**👏 为自己鼓掌！你已经掌握了RAG的全部核心技术！**
