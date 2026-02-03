![向量数据库架构](./images/vector_db.svg)
*图：向量数据库架构*

# 第43课：本地Embedding模型部署 - 完全离线的向量生成

> 📚 **课程信息**
> - 所属模块：第三模块 - 向量数据库与RAG系统  
> - 章节：第8章 - 向量数据库基础（第3/6课）
> - 学习目标：掌握本地Embedding模型部署的多种方案
> - 预计时间：100-110分钟
> - 前置知识：第41-42课

---

## 📢 课程导入

### 前言

前两课我们学了向量数据库和Embedding技术，但有个问题：**每次生成向量都要调用OpenAI API，成本高、速度慢、还要联网！**

企业场景更麻烦：
- 敏感数据不能发到云端 ❌
- API调用费用太高（百万文档？破产！）❌
- 网络延迟影响用户体验 ❌

**本地部署Embedding模型**就能完美解决：
- ✅ 完全免费，无限次调用
- ✅ 数据不出本地，安全有保障
- ✅ 毫秒级响应，极速体验

今天这课，我要教你3种本地部署方案，让你的Embedding服务完全自主可控！

---

### 核心价值点

**第一，本地部署是企业级应用的必选项。**

看看成本对比：
```
OpenAI Embeddings（text-embedding-3-small）：
- 价格：$0.02 / 1M tokens
- 100万篇文档（平均500 tokens）：$10,000！
- 每月持续增长...

本地模型：
- 初始：免费下载（0元）
- 运行：只需GPU/CPU电费
- 100万文档：几乎免费！
```

**对于大规模应用，本地部署能省几十万！**

**第二，本地部署技术已经非常成熟。**

以前觉得部署困难？现在有多种简单方案：
- **Sentence-Transformers**：3行代码搞定
- **LM Studio**：图形界面，点点鼠标
- **Ollama**：一行命令部署
- **FastAPI包装**：10分钟上线API服务

**零基础也能快速上手！**

**第三，本地模型质量不输云端。**

误区：本地模型效果差？
真相：**开源模型质量已经非常接近商业模型！**

对比（中文检索任务）：
- OpenAI text-embedding-3-small：92%准确率
- BGE-base-zh-v1.5（本地）：90%准确率
- 差距很小，但完全免费！

**而且你可以针对自己的数据fine-tune，效果更好！**

**第四，这是构建私有化RAG系统的基础。**

企业私有化部署流程：
1. **本地Embedding服务**（本课）
2. 本地向量数据库
3. 本地大模型
4. 完整的私有化RAG系统

**第一步做好，后面就顺了！**

---

### 行动号召

今天这一课会教你：
- Sentence-Transformers本地部署
- LM Studio Embeddings使用
- Ollama Embeddings配置
- 性能优化技巧
- 部署API服务

**学完这课，你就能搭建自己的Embedding服务！**

---

## 📖 知识讲解

![本地Embedding模型](./images/embedding.svg)
*图：本地Embedding模型*


### 1. 部署方案对比

#### 1.1 主流方案

```
方案1：Sentence-Transformers（推荐）
  优点：最简单、最成熟、Python原生
  缺点：需要Python环境
  适合：开发环境、Python项目
  
方案2：LM Studio
  优点：图形界面、易用
  缺点：功能相对基础
  适合：初学者、快速原型
  
方案3：Ollama
  优点：命令行简单、性能好
  缺点：模型选择少（Embedding）
  适合：系统集成、轻量部署
  
方案4：自建API服务
  优点：灵活、可控、可扩展
  缺点：需要一定开发能力
  适合：生产环境、团队使用
```

---

### 2. Sentence-Transformers部署

#### 2.1 基础安装

```bash
# 1. 安装
pip install sentence-transformers

# 2. 可选：安装加速库
pip install torch  # GPU加速（如果有NVIDIA GPU）

# 3. 验证安装
python -c "from sentence_transformers import SentenceTransformer; print('安装成功')"
```

#### 2.2 基础使用

```python
from sentence_transformers import SentenceTransformer

# 第一次会自动下载模型（约1GB）
model = SentenceTransformer('all-MiniLM-L6-v2')

# 生成向量
texts = [
    "人工智能正在改变世界",
    "机器学习是AI的核心技术"
]

embeddings = model.encode(texts)

print(f"向量形状：{embeddings.shape}")  # (2, 384)
print(f"第一个向量：{embeddings[0][:5]}...")
```

#### 2.3 模型下载和管理

```python
# 方式1：自动下载（默认）
model = SentenceTransformer('all-MiniLM-L6-v2')

# 方式2：指定缓存目录
model = SentenceTransformer(
    'all-MiniLM-L6-v2',
    cache_folder='/path/to/models'
)

# 方式3：从本地加载
# 1. 先下载到本地
# 2. 然后加载
model = SentenceTransformer('/path/to/local/model')

# 查看模型信息
print(f"最大序列长度：{model.max_seq_length}")
print(f"向量维度：{model.get_sentence_embedding_dimension()}")
```

#### 2.4 批量处理优化

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# 大量文本
texts = ["文本" + str(i) for i in range(10000)]

# ✅ 批量处理（快）
embeddings = model.encode(
    texts,
    batch_size=32,  # 批次大小
    show_progress_bar=True,  # 显示进度
    convert_to_numpy=True  # 转numpy数组
)

# ❌ 逐条处理（慢）
# embeddings = [model.encode([t])[0] for t in texts]

print(f"生成了 {len(embeddings)} 个向量")
```

---

### 3. LM Studio Embeddings

#### 3.1 配置步骤

```
1. 打开LM Studio

2. 下载Embedding模型：
   - 搜索："nomic-embed-text"
   - 下载：nomic-ai/nomic-embed-text-v1.5-GGUF
   
3. 加载模型（Local Server选项卡）

4. 使用OpenAI兼容API
```

#### 3.2 Python调用

```python
from openai import OpenAI

# LM Studio本地服务
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # 随意，LM Studio不验证
)

def get_local_embedding(text):
    """使用LM Studio获取向量"""
    response = client.embeddings.create(
        input=text,
        model="nomic-embed-text"  # 模型名称
    )
    return response.data[0].embedding

# 使用
text = "人工智能正在改变世界"
embedding = get_local_embedding(text)

print(f"维度：{len(embedding)}")
print(f"前5个值：{embedding[:5]}")
```

#### 3.3 LangChain集成

```python
from langchain.embeddings import OpenAIEmbeddings

# 配置本地Embeddings
embeddings = OpenAIEmbeddings(
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
    model="nomic-embed-text"
)

# 使用
text = "测试文本"
vector = embeddings.embed_query(text)

print(f"向量维度：{len(vector)}")

# 批量
texts = ["文本1", "文本2", "文本3"]
vectors = embeddings.embed_documents(texts)
print(f"生成了 {len(vectors)} 个向量")
```

---

### 4. Ollama Embeddings

#### 4.1 安装和配置

```bash
# 1. 安装Ollama（macOS/Linux）
curl -fsSL https://ollama.com/install.sh | sh

# Windows：下载安装包
# https://ollama.com/download

# 2. 拉取Embedding模型
ollama pull nomic-embed-text

# 3. 测试
ollama run nomic-embed-text "测试文本"
```

#### 4.2 Python调用

```python
import requests
import json

def get_ollama_embedding(text):
    """使用Ollama获取向量"""
    
    url = "http://localhost:11434/api/embeddings"
    
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    return data["embedding"]

# 使用
text = "人工智能正在改变世界"
embedding = get_ollama_embedding(text)

print(f"维度：{len(embedding)}")
print(f"前5个值：{embedding[:5]}")
```

#### 4.3 LangChain集成

```python
from langchain.embeddings import OllamaEmbeddings

# 初始化
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# 单个文本
text = "测试文本"
vector = embeddings.embed_query(text)
print(f"维度：{len(vector)}")

# 批量
texts = ["文本1", "文本2", "文本3"]
vectors = embeddings.embed_documents(texts)
print(f"生成 {len(vectors)} 个向量")
```

---

### 5. 自建Embedding API服务

#### 5.1 FastAPI实现

```python
# embedding_service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List
import uvicorn

# 初始化
app = FastAPI(title="Local Embedding Service")

# 加载模型（启动时加载一次）
print("加载Embedding模型...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("模型加载完成！")


# 请求模型
class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "all-MiniLM-L6-v2"


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: str
    dimensions: int


# API端点
@app.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """生成向量"""
    
    try:
        # 生成向量
        embeddings = model.encode(
            request.texts,
            batch_size=32,
            convert_to_numpy=True
        )
        
        # 转为列表
        embeddings_list = embeddings.tolist()
        
        return EmbeddingResponse(
            embeddings=embeddings_list,
            model=request.model,
            dimensions=len(embeddings_list[0])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "model": "all-MiniLM-L6-v2"}


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "Local Embedding Service",
        "version": "1.0",
        "model": "all-MiniLM-L6-v2",
        "dimensions": model.get_sentence_embedding_dimension()
    }


if __name__ == "__main__":
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 5.2 客户端调用

```python
# client.py

import requests
import json

def get_embeddings(texts, api_url="http://localhost:8000"):
    """调用本地Embedding服务"""
    
    response = requests.post(
        f"{api_url}/embeddings",
        json={"texts": texts}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data["embeddings"]
    else:
        raise Exception(f"API错误：{response.text}")


# 使用
texts = [
    "人工智能正在改变世界",
    "机器学习是AI的核心技术"
]

embeddings = get_embeddings(texts)

print(f"生成了 {len(embeddings)} 个向量")
print(f"维度：{len(embeddings[0])}")
```

#### 5.3 启动和使用

```bash
# 1. 安装依赖
pip install fastapi uvicorn sentence-transformers

# 2. 启动服务
python embedding_service.py

# 服务运行在 http://localhost:8000

# 3. 测试
curl http://localhost:8000/health

# 4. 调用API
python client.py
```

---

### 6. 性能优化

#### 6.1 GPU加速

```python
from sentence_transformers import SentenceTransformer
import torch

# 检查GPU
if torch.cuda.is_available():
    device = 'cuda'
    print(f"使用GPU：{torch.cuda.get_device_name(0)}")
else:
    device = 'cpu'
    print("使用CPU")

# 加载到GPU
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# 使用（自动在GPU上运行）
texts = ["文本" + str(i) for i in range(1000)]
embeddings = model.encode(texts, batch_size=64)

print("完成！")
```

#### 6.2 多进程加速

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = ["文本" + str(i) for i in range(10000)]

# 使用多进程池
embeddings = model.encode_multi_process(
    texts,
    pool_size=4,  # 进程数
    batch_size=32
)

print(f"生成 {len(embeddings)} 个向量")
```

#### 6.3 量化模型

```python
# 使用量化模型（减小体积、提升速度）

from sentence_transformers import SentenceTransformer
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

# 动态量化
model = torch.quantization.quantize_dynamic(
    model, 
    {torch.nn.Linear}, 
    dtype=torch.qint8
)

# 使用（速度更快，精度略降）
texts = ["测试文本"]
embeddings = model.encode(texts)
```

---

## 💻 Demo案例：完整部署方案

创建`local_embedding_deployment_demo.py`：

```python
"""
本地Embedding部署完整演示
对比不同方案的性能和使用体验
"""

from sentence_transformers import SentenceTransformer
import time
import numpy as np


# ============= 方案1：Sentence-Transformers =============

def demo_1_sentence_transformers():
    """方案1：Sentence-Transformers"""
    
    print("\n" + "="*60)
    print("方案1：Sentence-Transformers")
    print("="*60 + "\n")
    
    print("1. 加载模型...")
    start = time.time()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    load_time = time.time() - start
    print(f"   加载耗时：{load_time:.2f}秒\n")
    
    print("2. 生成向量...")
    texts = [
        "人工智能正在改变世界",
        "机器学习是AI的核心技术",
        "深度学习基于神经网络"
    ]
    
    start = time.time()
    embeddings = model.encode(texts)
    encode_time = time.time() - start
    
    print(f"   生成3个向量耗时：{encode_time:.3f}秒")
    print(f"   向量维度：{embeddings.shape}\n")
    
    print("3. 批量处理性能测试...")
    large_texts = ["测试文本" + str(i) for i in range(1000)]
    
    start = time.time()
    large_embeddings = model.encode(large_texts, batch_size=32, show_progress_bar=False)
    batch_time = time.time() - start
    
    print(f"   生成1000个向量耗时：{batch_time:.2f}秒")
    print(f"   速度：{len(large_texts)/batch_time:.0f} docs/sec\n")
    
    return {
        "方案": "Sentence-Transformers",
        "加载时间": f"{load_time:.2f}s",
        "单次速度": f"{encode_time:.3f}s",
        "批量速度": f"{len(large_texts)/batch_time:.0f} docs/s",
        "维度": embeddings.shape[1]
    }


# ============= 方案2：模拟LM Studio =============

def demo_2_lm_studio_style():
    """方案2：LM Studio风格（模拟）"""
    
    print("\n" + "="*60)
    print("方案2：LM Studio API风格")
    print("="*60 + "\n")
    
    print("说明：LM Studio提供OpenAI兼容API")
    print("配置：")
    print("  base_url: http://localhost:1234/v1")
    print("  api_key: lm-studio")
    print("  model: nomic-embed-text\n")
    
    print("示例代码：")
    code = """
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

response = client.embeddings.create(
    input="你的文本",
    model="nomic-embed-text"
)

embedding = response.data[0].embedding
"""
    print(code)
    
    print("优点：")
    print("  ✓ 图形界面，易用")
    print("  ✓ OpenAI兼容API")
    print("  ✓ 适合快速原型\n")


# ============= 方案3：模拟Ollama =============

def demo_3_ollama_style():
    """方案3：Ollama风格（模拟）"""
    
    print("\n" + "="*60)
    print("方案3：Ollama")
    print("="*60 + "\n")
    
    print("安装和使用：")
    commands = """
# 安装
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull nomic-embed-text

# Python调用
import requests

url = "http://localhost:11434/api/embeddings"
response = requests.post(url, json={
    "model": "nomic-embed-text",
    "prompt": "你的文本"
})

embedding = response.json()["embedding"]
"""
    print(commands)
    
    print("优点：")
    print("  ✓ 命令行简单")
    print("  ✓ 轻量级")
    print("  ✓ 易于集成\n")


# ============= 方案对比 =============

def print_comparison():
    """打印方案对比"""
    
    print("\n" + "="*60)
    print("方案对比总结")
    print("="*60 + "\n")
    
    comparison = """
┌────────────────┬────────────────────┬────────────────────┬────────────────────┐
│  特性          │  Sentence-Trans    │  LM Studio         │  Ollama            │
├────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ 易用性         │  ★★★★☆           │  ★★★★★           │  ★★★★☆           │
│ 性能           │  ★★★★★           │  ★★★☆☆           │  ★★★★☆           │
│ 模型选择       │  ★★★★★（最多）   │  ★★☆☆☆           │  ★★★☆☆           │
│ 自定义能力     │  ★★★★★           │  ★★☆☆☆           │  ★★★☆☆           │
│ API支持        │  ★★★☆☆           │  ★★★★★（OpenAI）│  ★★★★☆           │
│ 适合场景       │  开发、生产        │  快速原型          │  系统集成          │
└────────────────┴────────────────────┴────────────────────┴────────────────────┘

推荐选择：
1. Python项目：Sentence-Transformers（最灵活）
2. 快速开始：LM Studio（最简单）
3. 系统集成：Ollama（最轻量）
4. 生产环境：自建API服务（最可控）
"""
    
    print(comparison)


# ============= 主函数 =============

def main():
    """主函数"""
    
    print("\n" + "="*60)
    print("🎯 本地Embedding部署方案演示")
    print("="*60)
    
    # 运行演示
    result = demo_1_sentence_transformers()
    demo_2_lm_studio_style()
    demo_3_ollama_style()
    print_comparison()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("="*60)
    print("\n💡 核心要点：")
    print("  1. 本地部署完全免费，无限次调用")
    print("  2. 数据不出本地，安全有保障")
    print("  3. 多种方案可选，根据场景选择")
    print("  4. 性能和质量都不输云端API")
    print("\n🚀 下一课：Chroma向量数据库精通")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
```

---

## 🎯 最佳实践

### 部署建议

```
开发阶段：
✓ 使用Sentence-Transformers
✓ 快速迭代和测试
✓ 灵活切换模型

测试阶段：
✓ 搭建API服务
✓ 负载测试
✓ 性能调优

生产阶段：
✓ Docker容器化
✓ 负载均衡
✓ 监控告警
✓ 定期更新模型
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 使用Sentence-Transformers部署模型
- [ ] 配置LM Studio Embeddings
- [ ] 使用Ollama生成向量
- [ ] 搭建自定义API服务
- [ ] 优化Embedding性能

---

## 📝 下一课预告

**第44课：Chroma向量数据库精通**

下一课我们将学习：
- Chroma数据库完整教程
- 集合管理和配置
- 高级检索技巧
- 持久化和备份
- 与LangChain集成

**开始构建完整的向量检索系统！**

---

**🎉 恭喜你完成第43课！**

**你已经掌握了本地Embedding部署！**

**进度：43/165课（26.1%完成）** 🚀