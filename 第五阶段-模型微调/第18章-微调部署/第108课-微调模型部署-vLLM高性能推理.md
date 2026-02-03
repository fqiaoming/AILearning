![模型部署架构](./images/deploy.svg)
*图：模型部署架构*

# 第108课：微调模型部署-vLLM高性能推理

> **本课目标**：掌握vLLM框架，实现高性能模型推理部署
> 
> **核心技能**：vLLM原理、PagedAttention、部署实战、性能优化
> 
> **学习时长**：95分钟

---

## 📖 口播文案（7分钟）
![Deploy Arch](./images/deploy_arch.svg)
*图：Deploy Arch*


### 🎯 前言

"前面我们学习了各种微调技术，训练出了优秀的模型。

但现在有个新问题：

**如何让模型跑得快？**

**实际痛点：**

```
你训练了一个7B模型：
• 训练：成功 ✅
• 效果：优秀 ✅

但部署后：
• 推理速度：每秒2个token ❌
• 用户体验：等半天才出结果 ❌
• 并发能力：10个用户就卡死 ❌
• GPU利用率：只有30% ❌

花了大价钱训练，结果不能用！
```

**传统部署方案的问题：**

```
【方案1：直接用Transformers】

from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("model")
output = model.generate(input_ids)

问题：
• 速度慢（每秒2-5 tokens）
• 显存浪费（大量碎片）
• 吞吐量低（并发能力差）
• GPU利用率低（<40%）

适用：
• 本地测试
• 小规模应用
不适合生产！

【方案2：TensorRT、ONNX】

优点：
• 速度快

缺点：
• 转换复杂
• 兼容性差
• 维护困难
• 对大模型支持不好
```

**今天要学习：vLLM**

**最强大的LLM推理框架！**

**vLLM的威力：**

```
【性能对比】

场景：Qwen2-7B，输入100 tokens，生成200 tokens

HuggingFace Transformers：
• 吞吐量：2.5 tokens/秒
• 批处理：1个请求
• 显存占用：16GB

vLLM：
• 吞吐量：65 tokens/秒（26倍！）
• 批处理：50个请求
• 显存占用：12GB（节省25%）

提升巨大！
```

**vLLM的核心技术：**

```
【技术1：PagedAttention】

传统Attention：
• 预先分配固定显存
• 大量显存碎片
• 浪费50%+显存

PagedAttention：
• 动态分配显存块
• 像操作系统的虚拟内存
• 显存利用率90%+

结果：
• 显存节省50%
• 批处理大小提升2-3倍
• 吞吐量提升10-20倍

【技术2：连续批处理】

传统批处理：
• 等所有请求完成
• 再处理下一批
• GPU经常空闲

连续批处理（Continuous Batching）：
• 请求完成立即移除
• 新请求立即加入
• GPU持续满载

结果：
• GPU利用率>90%
• 吞吐量提升3-5倍

【技术3：优化采样】

• Beam Search优化
• Top-K/Top-P加速
• 并行解码
• 减少CPU-GPU通信

结果：
• 采样速度提升2-3倍
```

**实际效果：**

```
【案例：企业客服系统】

需求：
• 支持1000并发用户
• 响应时间<2秒
• 使用Qwen2-7B

方案1：HuggingFace
• 需要GPU：20张A100 ❌
• 成本：$200,000/年
• 实际体验：卡顿

方案2：vLLM
• 需要GPU：4张A100 ✅
• 成本：$40,000/年
• 实际体验：流畅

节省成本80%！
```

**vLLM的优势：**

```
✅ 性能强大
• 吞吐量提升10-20倍
• 延迟降低50%+

✅ 易于使用
• API兼容OpenAI
• 简单几行代码部署

✅ 显存高效
• PagedAttention
• 节省50%显存

✅ 并发能力强
• 连续批处理
• 支持大并发

✅ 生态完善
• 支持主流模型
• 活跃社区
• 文档详细
```

**支持的模型：**

```
开源模型：
• LLaMA / LLaMA-2 / LLaMA-3 ✅
• Qwen / Qwen2 ✅
• Mistral / Mixtral ✅
• ChatGLM ✅
• Baichuan ✅

基本所有主流开源模型都支持！
```

**vLLM架构：**

```
用户请求
    ↓
API Server（FastAPI）
    ↓
Request Queue（请求队列）
    ↓
Scheduler（调度器）
    ↓
PagedAttention Engine
    ↓
GPU推理
    ↓
Response（流式输出）
```

**部署方式：**

```
【方式1：Python API】

from vllm import LLM

llm = LLM(model="Qwen/Qwen2-7B")
output = llm.generate("你好")

适用：
• 本地开发
• 简单集成

【方式2：OpenAI兼容服务】

vllm serve Qwen/Qwen2-7B

# 客户端
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1")
response = client.chat.completions.create(...)

适用：
• 生产环境
• 替代OpenAI
• 多语言调用

【方式3：Docker部署】

docker run --gpus all \
  -p 8000:8000 \
  vllm/vllm-openai \
  --model Qwen/Qwen2-7B

适用：
• 容器化部署
• K8s集成
• 云原生
```

**性能调优：**

```
关键参数：

1. max_model_len
   • 最大序列长度
   • 影响显存占用
   • 建议：根据实际需求设置

2. tensor_parallel_size
   • 张量并行
   • 多卡推理
   • 适合大模型

3. gpu_memory_utilization
   • GPU显存利用率
   • 默认0.9
   • 可以设置0.95

4. max_num_seqs
   • 最大批处理大小
   • 影响吞吐量
   • 根据显存调整
```

**今天这一课，我要带你：**

**第一部分：vLLM原理**
- PagedAttention
- 连续批处理
- 架构设计

**第二部分：快速部署**
- Python API
- OpenAI服务
- Docker部署

**第三部分：性能优化**
- 参数调优
- 多卡推理
- 监控告警

**第四部分：生产实战**
- 完整部署方案
- 高可用架构
- 最佳实践

学完这一课，让你的模型飞起来！

准备好了吗？让我们开始！"

---

## 📚 第一部分：vLLM核心原理

### 一、PagedAttention详解

```python
class PagedAttentionExplainer:
    """PagedAttention原理解释"""
    
    @staticmethod
    def explain_traditional_attention():
        """解释传统Attention的问题"""
        
        print("="*60)
        print("传统Attention的显存问题")
        print("="*60)
        
        print("""
【传统方式】

预先分配固定显存：
• 假设最大序列长度：2048
• 为每个请求分配：2048 * hidden_size

问题：
1. 实际序列长度可能只有100
   → 浪费1948个位置的显存

2. 显存碎片化
   请求1: [已用 100][空闲 1948]
   请求2: [已用 500][空闲 1548]
   → 大量碎片，无法合并

3. 批处理受限
   • 只能处理少量请求
   • 显存很快耗尽

【实际数据】

模型：7B参数
序列长度：2048
批处理大小：8

需要显存：
• 模型参数：14GB
• KV Cache：8 * 2048 * hidden_size = 16GB
• 总计：30GB

但实际平均序列长度只有200：
• 实际需要：14GB + 1.6GB = 15.6GB
• 浪费：14.4GB（48%）

太浪费了！
        """)
    
    @staticmethod
    def explain_paged_attention():
        """解释PagedAttention"""
        
        print("\n" + "="*60)
        print("PagedAttention解决方案")
        print("="*60)
        
        print("""
【核心思想】

借鉴操作系统的虚拟内存：
• 将KV Cache分成固定大小的块（Page）
• 动态分配和回收
• 按需使用

【工作原理】

1. 分块存储
   • Page大小：例如16个token
   • KV Cache被分成多个Page
   • 类似操作系统的页表

2. 动态分配
   • 请求需要多少分配多少
   • 不预先分配所有空间

3. 灵活回收
   • 请求完成立即回收
   • 显存可以复用

4. 共享机制
   • Beam Search时共享前缀
   • 进一步节省显存

【示例】

请求："写一篇关于AI的文章"

传统方式：
• 预先分配：2048个位置
• 实际生成：300个token
• 浪费：1748个位置

PagedAttention：
• 初始分配：1个Page（16 tokens）
• 不够时：再分配1个Page
• 最终使用：19个Page（304 tokens）
• 浪费：只有4个token

效率提升巨大！

【显存节省】

场景：8个并发请求

传统：
• 8 * 2048 = 16384个位置
• 假设每个1KB = 16GB

PagedAttention：
• 实际平均长度200
• 8 * 200 = 1600个位置
• 1.6GB

节省：91%！

【性能提升】

显存节省 → 更大批处理 → 更高吞吐量

批处理大小：
• 传统：8个
• PagedAttention：50个

吞吐量：
• 传统：10 tokens/秒
• PagedAttention：120 tokens/秒

提升12倍！
        """)

# 演示
explainer = PagedAttentionExplainer()
explainer.explain_traditional_attention()
explainer.explain_paged_attention()
```

---

## 💻 第二部分：vLLM快速部署

### 一、安装配置

```python
class VLLMQuickStart:
    """vLLM快速入门"""
    
    @staticmethod
    def show_installation():
        """展示安装步骤"""
        
        print("="*60)
        print("vLLM安装")
        print("="*60)
        
        print("""
【环境要求】

• Python: 3.8+
• CUDA: 11.8+
• GPU: 16GB+ VRAM（推荐A100/A6000/RTX 4090）

【安装命令】

# 使用pip安装
pip install vllm

# 或从源码安装（最新版）
pip install git+https://github.com/vllm-project/vllm.git

【验证安装】

python -c "import vllm; print(vllm.__version__)"

看到版本号即安装成功！

【常见问题】

问题1：CUDA版本不匹配
解决：重新安装对应CUDA版本的PyTorch

问题2：显存不足
解决：使用更小的模型或量化版本

问题3：编译错误
解决：确保安装了build-essential和CUDA toolkit
        """)
    
    @staticmethod
    def demo_python_api():
        """演示Python API"""
        
        print("\n" + "="*60)
        print("方式1：Python API（推荐开发测试）")
        print("="*60)
        
        print("""
【基础使用】

from vllm import LLM, SamplingParams

# 1. 加载模型
llm = LLM(
    model="Qwen/Qwen2-7B-Instruct",
    trust_remote_code=True,
    tensor_parallel_size=1  # 单卡
)

# 2. 设置采样参数
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512
)

# 3. 生成
prompts = ["你好，请介绍一下人工智能"]
outputs = llm.generate(prompts, sampling_params)

# 4. 获取结果
for output in outputs:
    text = output.outputs[0].text
    print(text)

【批量推理】

# 多个请求一起处理
prompts = [
    "什么是机器学习？",
    "解释深度学习",
    "AI的应用有哪些？"
]

outputs = llm.generate(prompts, sampling_params)

# vLLM自动优化批处理！

【流式输出】

# 对于长文本生成，使用流式
from vllm import LLM

llm = LLM(model="Qwen/Qwen2-7B-Instruct")

# 注意：Python API不直接支持流式
# 需要使用OpenAI兼容服务器

【性能对比】

HuggingFace:
import time
start = time.time()
# generate...
print(f"耗时: {time.time() - start:.2f}秒")
# 输出：耗时: 25.3秒

vLLM:
start = time.time()
# generate...
print(f"耗时: {time.time() - start:.2f}秒")
# 输出：耗时: 1.8秒

快14倍！
        """)
    
    @staticmethod
    def demo_openai_server():
        """演示OpenAI兼容服务器"""
        
        print("\n" + "="*60)
        print("方式2：OpenAI兼容服务器（推荐生产）")
        print("="*60)
        
        print("""
【启动服务器】

# 命令行启动
vllm serve Qwen/Qwen2-7B-Instruct \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --trust-remote-code

# 高级配置
vllm serve Qwen/Qwen2-7B-Instruct \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --tensor-parallel-size 1 \\
    --gpu-memory-utilization 0.95 \\
    --max-model-len 4096 \\
    --trust-remote-code

参数说明：
• tensor-parallel-size: 多卡并行数
• gpu-memory-utilization: GPU显存利用率
• max-model-len: 最大序列长度

【客户端调用】

# Python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",  # vLLM不需要key
    base_url="http://localhost:8000/v1"
)

# 对话
response = client.chat.completions.create(
    model="Qwen/Qwen2-7B-Instruct",
    messages=[
        {"role": "user", "content": "你好"}
    ],
    temperature=0.7,
    max_tokens=512
)

print(response.choices[0].message.content)

# 流式输出（推荐）
stream = client.chat.completions.create(
    model="Qwen/Qwen2-7B-Instruct",
    messages=[
        {"role": "user", "content": "写一篇AI文章"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

【JavaScript调用】

// Node.js
const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: 'EMPTY',
  baseURL: 'http://localhost:8000/v1'
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'Qwen/Qwen2-7B-Instruct',
    messages: [
      { role: 'user', content: '你好' }
    ]
  });
  
  console.log(response.choices[0].message.content);
}

【cURL测试】

curl http://localhost:8000/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "Qwen/Qwen2-7B-Instruct",
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'

【优势】

✅ 完全兼容OpenAI API
✅ 多语言支持
✅ 易于集成现有项目
✅ 支持流式输出
✅ 生产级稳定性
        """)

# 演示
quickstart = VLLMQuickStart()
quickstart.show_installation()
quickstart.demo_python_api()
quickstart.demo_openai_server()
```

---

## 🎯 第三部分：性能优化实战

### 一、参数调优

```python
class VLLMOptimization:
    """vLLM性能优化"""
    
    @staticmethod
    def explain_key_parameters():
        """解释关键参数"""
        
        print("\n" + "="*60)
        print("vLLM关键参数调优")
        print("="*60)
        
        print("""
【参数1：tensor_parallel_size】

作用：张量并行，多卡推理

设置：
• 单卡：1
• 双卡：2
• 四卡：4

示例：
vllm serve model --tensor-parallel-size 2

适用：
• 模型太大，单卡装不下
• 提升吞吐量

注意：
• 卡数必须是2的幂次
• 通信开销随卡数增加

【参数2：gpu_memory_utilization】

作用：控制GPU显存使用比例

设置：
• 保守：0.85
• 默认：0.90
• 激进：0.95

示例：
vllm serve model --gpu-memory-utilization 0.95

适用：
• 显存充足：0.95
• 显存紧张：0.85

注意：
• 过高可能OOM
• 过低浪费显存

【参数3：max_model_len】

作用：最大序列长度

设置：
• 根据实际需求
• 不要设置太大

示例：
vllm serve model --max-model-len 2048

影响：
• 越大越占显存
• 影响批处理大小

建议：
• 短对话：1024
• 长文本：4096
• 超长：8192+

【参数4：max_num_seqs】

作用：最大批处理大小

设置：
• 自动：不设置
• 手动：根据显存

示例：
vllm serve model --max-num-seqs 256

影响：
• 越大吞吐量越高
• 受显存限制

建议：
• 让vLLM自动管理
• 除非有特殊需求

【参数5：dtype】

作用：数据类型

选项：
• float16: 默认，速度快
• bfloat16: 数值稳定（推荐A100）
• float32: 精度高，慢

示例：
vllm serve model --dtype bfloat16

建议：
• A100/H100: bfloat16
• 其他GPU: float16

【参数6：quantization】

作用：量化加速

选项：
• awq: 4-bit量化
• gptq: 4-bit量化
• squeezellm: 压缩

示例：
vllm serve model --quantization awq

效果：
• 显存节省75%
• 速度略降
• 效果略降

适用：
• 显存不足
• 追求高并发
        """)
    
    @staticmethod
    def show_optimization_examples():
        """展示优化示例"""
        
        print("\n" + "="*60)
        print("实战优化配置")
        print("="*60)
        
        configs = {
            "开发测试": {
                "描述": "本地开发，单卡",
                "命令": """
vllm serve Qwen/Qwen2-7B-Instruct \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --gpu-memory-utilization 0.85 \\
    --max-model-len 2048
                """,
                "特点": [
                    "保守配置",
                    "稳定性优先",
                    "适合开发调试"
                ]
            },
            "生产环境-单卡": {
                "描述": "生产环境，A100单卡",
                "命令": """
vllm serve Qwen/Qwen2-7B-Instruct \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --dtype bfloat16 \\
    --gpu-memory-utilization 0.95 \\
    --max-model-len 4096 \\
    --trust-remote-code
                """,
                "特点": [
                    "高性能配置",
                    "充分利用显存",
                    "支持长文本"
                ]
            },
            "生产环境-多卡": {
                "描述": "大模型，双卡推理",
                "命令": """
vllm serve Qwen/Qwen2-72B-Instruct \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --tensor-parallel-size 2 \\
    --dtype bfloat16 \\
    --gpu-memory-utilization 0.95 \\
    --max-model-len 4096
                """,
                "特点": [
                    "支持大模型",
                    "双卡并行",
                    "高吞吐量"
                ]
            },
            "高并发场景": {
                "描述": "高并发，量化加速",
                "命令": """
vllm serve Qwen/Qwen2-7B-Instruct-AWQ \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --quantization awq \\
    --gpu-memory-utilization 0.95 \\
    --max-model-len 2048
                """,
                "特点": [
                    "4-bit量化",
                    "显存占用少",
                    "支持超高并发"
                ]
            }
        }
        
        for scenario, config in configs.items():
            print(f"\n【{scenario}】")
            print(f"描述：{config['描述']}")
            print(f"\n命令：{config['命令']}")
            print(f"\n特点：")
            for feature in config['特点']:
                print(f"  • {feature}")

# 演示
optimizer = VLLMOptimization()
optimizer.explain_key_parameters()
optimizer.show_optimization_examples()
```

---

## 📝 课后练习

### 练习1：部署测试
使用vLLM部署一个7B模型

### 练习2：性能对比
对比vLLM和HuggingFace性能

### 练习3：参数调优
测试不同参数对性能的影响

---

## 🎓 知识总结

### 核心要点

1. **vLLM优势**
   - 吞吐量提升10-20倍
   - 显存节省50%
   - 并发能力强

2. **核心技术**
   - PagedAttention
   - 连续批处理
   - 优化采样

3. **部署方式**
   - Python API
   - OpenAI服务
   - Docker容器

4. **性能调优**
   - 合理设置显存利用率
   - 根据需求调整max_len
   - 考虑量化加速

---

## 🚀 下节预告

下一课：**第109课：模型合并与量化-GGUF格式转换**

- 模型合并
- GGUF格式
- llama.cpp
- 本地部署

**让模型跑在任何设备！** 🔥

---

**💪 记住：vLLM是生产部署的最佳选择！**

**下一课见！** 🎉
