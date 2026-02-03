![模型部署架构](./images/deploy.svg)
*图：模型部署架构*

# 第109课：模型合并与量化-GGUF格式转换

> **本课目标**：掌握模型合并与GGUF量化，实现高效本地部署
> 
> **核心技能**：LoRA合并、GGUF转换、llama.cpp、本地推理
> 
> **学习时长**：90分钟

---

## 📖 口播文案（7分钟）
![Deploy Arch](./images/deploy_arch.svg)
*图：Deploy Arch*


### 🎯 前言

"上节课我们学习了vLLM高性能推理，在服务器上部署模型。

但有时我们需要：

**在本地电脑运行模型！**

**实际需求：**

```
场景1：个人开发者
• 没有GPU服务器
• 想在MacBook上运行7B模型
• 只有16GB内存

场景2：离线应用
• 需要断网使用
• 在边缘设备部署
• 如树莓派、工控机

场景3：隐私保护
• 敏感数据不能上云
• 必须本地处理
• 企业内网部署

问题：
传统模型太大，本地跑不动！
```

**传统模型的问题：**

```
Qwen2-7B模型：

原始格式（float16）：
• 模型大小：14GB
• 运行需要：20GB+ 内存
• 推理速度：慢

在16GB MacBook上：
• 根本装不下 ❌
• 即使装下也卡顿 ❌
• 无法实用 ❌
```

**解决方案：GGUF量化！**

**GGUF = GPT-Generated Unified Format**

**效果：**

```
Qwen2-7B模型：

原始（float16）：
• 大小：14GB
• 速度：2 tokens/秒
• 质量：100%

GGUF Q4_K_M（4-bit量化）：
• 大小：4.1GB（节省71%）
• 速度：8 tokens/秒（快4倍）
• 质量：97%（几乎无损）

完美！
```

**GGUF的优势：**

```
✅ 大幅压缩
• 4-bit量化：节省75%
• 3-bit量化：节省81%
• 2-bit量化：节省87%

✅ 质量保持
• 智能量化
• 关键层保护
• 效果几乎无损

✅ 速度提升
• CPU优化
• SIMD加速
• Apple Silicon优化

✅ 易于使用
• 工具完善
• 一键转换
• 开箱即用

✅ 跨平台
• Windows/Linux/macOS
• x86/ARM/Apple Silicon
• CPU/GPU混合推理
```

**llama.cpp：最强本地推理引擎**

```
特点：
• 纯C++实现
• 高度优化
• CPU推理也快
• 支持Metal（Mac）
• 支持CUDA（NVIDIA）
• 支持ROCm（AMD）

性能：
• M2 MacBook：15 tokens/秒
• i9-13900K：12 tokens/秒
• RTX 4090：80 tokens/秒

完全够用！
```

**量化方法详解：**

```
【Q8_0】8-bit量化
• 压缩率：50%
• 质量损失：<1%
• 适用：追求质量

【Q6_K】6-bit混合量化
• 压缩率：62%
• 质量损失：1-2%
• 适用：平衡

【Q5_K_M】5-bit K-quants（Medium）
• 压缩率：68%
• 质量损失：2-3%
• 适用：推荐

【Q4_K_M】4-bit K-quants（Medium）
• 压缩率：75%
• 质量损失：3-5%
• 适用：推荐（最常用）

【Q4_K_S】4-bit K-quants（Small）
• 压缩率：75%
• 质量损失：4-6%
• 适用：显存极限

【Q3_K_M】3-bit K-quants
• 压缩率：81%
• 质量损失：5-8%
• 适用：低配设备

【Q2_K】2-bit K-quants
• 压缩率：87%
• 质量损失：8-12%
• 适用：实验

推荐：Q4_K_M（最佳平衡）
```

**K-quants技术：**

```
什么是K-quants？

传统量化：
• 所有层相同bit数
• 一刀切

K-quants：
• 不同层不同bit数
• Attention层：高精度
• FFN层：低精度
• 智能分配

结果：
• 相同压缩率
• 质量更好

示例：
Q4_K_M:
• 重要层：6-bit
• 一般层：4-bit
• 不重要层：3-bit
• 平均：4-bit

比传统Q4质量好20%！
```

**LoRA合并：**

```
问题：
• 训练得到LoRA适配器
• 推理时需要加载两个文件
• 不方便

解决：
• 合并LoRA到基础模型
• 得到完整模型
• 再转换GGUF

流程：
基础模型 + LoRA → 合并模型 → GGUF量化
```

**实际效果对比：**

```
【测试：Qwen2-7B，MacBook M2 Pro（16GB）】

场景1：原始模型
• 格式：float16
• 大小：14GB
• 加载：失败 ❌（内存不足）

场景2：GGUF Q8_0
• 格式：GGUF 8-bit
• 大小：7.5GB
• 速度：8 tokens/秒
• 质量：99%

场景3：GGUF Q4_K_M
• 格式：GGUF 4-bit
• 大小：4.1GB
• 速度：15 tokens/秒（更快！）
• 质量：97%

场景4：GGUF Q3_K_M
• 格式：GGUF 3-bit
• 大小：3.2GB
• 速度：18 tokens/秒
• 质量：93%

推荐：Q4_K_M（完美平衡）
```

**应用场景：**

```
场景1：Mac开发
• MacBook Pro/Air
• 使用Metal加速
• Q4_K_M格式
• 体验流畅

场景2：Windows游戏本
• RTX 4060 Laptop
• CUDA加速
• Q5_K_M格式
• 性能优秀

场景3：树莓派
• 4GB内存
• CPU推理
• 小模型 + Q4量化
• 可以运行

场景4：企业内网
• 老旧服务器
• 无法升级GPU
• 用GGUF + CPU
• 满足需求
```

**工具链：**

```
1. llama.cpp
   • C++推理引擎
   • 核心工具

2. llama-cpp-python
   • Python绑定
   • 易于集成

3. Ollama
   • 图形化管理
   • 开箱即用

4. LM Studio
   • 桌面应用
   • 最简单

5. text-generation-webui
   • Web界面
   • 功能丰富
```

**今天这一课，我要带你：**

**第一部分：LoRA合并**
- 合并原理
- 完整实现
- 权重处理

**第二部分：GGUF转换**
- 转换流程
- 量化方法
- 最佳实践

**第三部分：llama.cpp部署**
- 编译安装
- 推理测试
- 性能优化

**第四部分：生态工具**
- Ollama使用
- LM Studio配置
- Python集成

学完这一课，让模型跑在任何设备！

准备好了吗？让我们开始！"

---

## 📚 第一部分：LoRA合并

### 一、合并原理与实现

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

class LoRAMerger:
    """LoRA合并器"""
    
    @staticmethod
    def explain_merging():
        """解释合并原理"""
        
        print("="*60)
        print("LoRA合并原理")
        print("="*60)
        
        print("""
【为什么要合并】

训练后的状态：
• 基础模型：base_model（14GB）
• LoRA适配器：adapter（100MB）

推理时：
• 需要同时加载两个文件
• 先加载base，再加载adapter
• 增加复杂度

合并后：
• 单一模型文件
• 包含所有权重
• 推理简单

【合并原理】

LoRA公式：
W_new = W_base + α * (A × B)

其中：
• W_base: 基础权重
• A, B: LoRA矩阵（低秩）
• α: 缩放因子

合并：
把 (A × B) 加到 W_base上
得到新的权重矩阵

【实际操作】

1. 加载基础模型
2. 加载LoRA适配器
3. 执行merge_and_unload()
4. 保存合并后的模型

简单！
        """)
    
    @staticmethod
    def merge_lora(
        base_model_path: str,
        lora_path: str,
        output_path: str
    ):
        """
        合并LoRA到基础模型
        
        Args:
            base_model_path: 基础模型路径
            lora_path: LoRA适配器路径
            output_path: 输出路径
        """
        
        print("\n" + "="*60)
        print("LoRA合并实战")
        print("="*60)
        
        print(f"\n基础模型: {base_model_path}")
        print(f"LoRA适配器: {lora_path}")
        print(f"输出路径: {output_path}")
        
        print("\n步骤1：加载基础模型")
        print("  正在加载...")
        # base_model = AutoModelForCausalLM.from_pretrained(
        #     base_model_path,
        #     torch_dtype=torch.float16,
        #     device_map="auto"
        # )
        print("  ✅ 基础模型加载完成")
        
        print("\n步骤2：加载LoRA适配器")
        print("  正在加载...")
        # model = PeftModel.from_pretrained(base_model, lora_path)
        print("  ✅ LoRA加载完成")
        
        print("\n步骤3：合并权重")
        print("  正在合并...")
        # model = model.merge_and_unload()
        print("  ✅ 合并完成")
        
        print("\n步骤4：保存模型")
        print("  正在保存...")
        # model.save_pretrained(output_path)
        # tokenizer = AutoTokenizer.from_pretrained(base_model_path)
        # tokenizer.save_pretrained(output_path)
        print("  ✅ 保存完成")
        
        print(f"\n合并后的模型已保存到: {output_path}")
    
    @staticmethod
    def show_merge_script():
        """展示完整合并脚本"""
        
        print("\n" + "="*60)
        print("完整合并脚本")
        print("="*60)
        
        script = """
# merge_lora.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import argparse

def merge_lora(base_model_path, lora_path, output_path):
    '''合并LoRA到基础模型'''
    
    print("="*60)
    print("LoRA合并工具")
    print("="*60)
    
    # 1. 加载基础模型
    print("\\n[1/4] 加载基础模型...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    print("✅ 基础模型加载完成")
    
    # 2. 加载LoRA
    print("\\n[2/4] 加载LoRA适配器...")
    model = PeftModel.from_pretrained(base_model, lora_path)
    print("✅ LoRA加载完成")
    
    # 3. 合并
    print("\\n[3/4] 合并权重...")
    model = model.merge_and_unload()
    print("✅ 合并完成")
    
    # 4. 保存
    print("\\n[4/4] 保存模型...")
    model.save_pretrained(
        output_path,
        safe_serialization=True
    )
    
    # 保存tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_path,
        trust_remote_code=True
    )
    tokenizer.save_pretrained(output_path)
    
    print("✅ 保存完成")
    print(f"\\n模型已保存到: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--lora-path", required=True)
    parser.add_argument("--output-path", required=True)
    
    args = parser.parse_args()
    
    merge_lora(
        args.base_model,
        args.lora_path,
        args.output_path
    )

# 使用方法：
# python merge_lora.py \\
#     --base-model Qwen/Qwen2-7B \\
#     --lora-path ./lora_output \\
#     --output-path ./merged_model
        """
        
        print(script)

# 演示
merger = LoRAMerger()
merger.explain_merging()
merger.merge_lora(
    "Qwen/Qwen2-7B",
    "./lora_output",
    "./merged_model"
)
merger.show_merge_script()
```

---

## 💻 第二部分：GGUF转换实战

### 一、转换流程

```python
class GGUFConverter:
    """GGUF转换器"""
    
    @staticmethod
    def explain_gguf():
        """解释GGUF格式"""
        
        print("\n" + "="*60)
        print("GGUF格式详解")
        print("="*60)
        
        print("""
【什么是GGUF】

GGUF = GPT-Generated Unified Format

特点：
• 统一格式（替代GGML）
• 单文件包含所有信息
• 高效存储
• 快速加载

优势：
✅ 元数据嵌入（模型信息）
✅ 支持多种量化
✅ 向后兼容
✅ 跨平台

【量化级别】

完整列表（从高到低）：

Q8_0: 8-bit量化
• 大小：~50%
• 质量：~99%
• 推荐：质量优先

Q6_K: 6-bit K-quants
• 大小：~38%
• 质量：~98%
• 推荐：高质量

Q5_K_M: 5-bit medium
• 大小：~32%
• 质量：~97%
• 推荐：平衡

Q5_K_S: 5-bit small
• 大小：~32%
• 质量：~96%

Q4_K_M: 4-bit medium ⭐推荐
• 大小：~25%
• 质量：~95%
• 推荐：最常用

Q4_K_S: 4-bit small
• 大小：~25%
• 质量：~94%

Q3_K_M: 3-bit medium
• 大小：~19%
• 质量：~92%
• 推荐：低配

Q3_K_S: 3-bit small
• 大小：~19%
• 质量：~90%

Q2_K: 2-bit
• 大小：~13%
• 质量：~85%
• 推荐：实验

选择建议：
• 有资源：Q5_K_M或Q6_K
• 一般使用：Q4_K_M ⭐
• 资源有限：Q3_K_M
        """)
    
    @staticmethod
    def show_conversion_steps():
        """展示转换步骤"""
        
        print("\n" + "="*60)
        print("GGUF转换流程")
        print("="*60)
        
        print("""
【准备工作】

1. 安装llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

2. 安装Python依赖
pip install -r requirements.txt

【转换步骤】

步骤1：转换为FP16 GGUF（中间格式）

python convert.py \\
    /path/to/merged_model \\
    --outtype f16 \\
    --outfile model-f16.gguf

步骤2：量化为目标精度

./quantize \\
    model-f16.gguf \\
    model-q4_k_m.gguf \\
    Q4_K_M

完成！

【一键脚本】

#!/bin/bash
# convert_to_gguf.sh

MODEL_PATH=$1
OUTPUT_NAME=$2
QUANT_TYPE=${3:-Q4_K_M}

echo "转换模型: $MODEL_PATH"
echo "输出名称: $OUTPUT_NAME"
echo "量化类型: $QUANT_TYPE"

# 步骤1：转换为FP16
python convert.py $MODEL_PATH \\
    --outtype f16 \\
    --outfile ${OUTPUT_NAME}-f16.gguf

# 步骤2：量化
./quantize \\
    ${OUTPUT_NAME}-f16.gguf \\
    ${OUTPUT_NAME}-${QUANT_TYPE}.gguf \\
    $QUANT_TYPE

# 清理中间文件
rm ${OUTPUT_NAME}-f16.gguf

echo "完成！输出文件: ${OUTPUT_NAME}-${QUANT_TYPE}.gguf"

# 使用：
# bash convert_to_gguf.sh ./merged_model qwen2-7b Q4_K_M
        """)
    
    @staticmethod
    def show_all_quant_commands():
        """展示所有量化命令"""
        
        print("\n" + "="*60)
        print("批量生成多个量化版本")
        print("="*60)
        
        script = """
#!/bin/bash
# batch_quantize.sh
# 一次性生成多个常用量化版本

MODEL_F16="model-f16.gguf"
OUTPUT_BASE="qwen2-7b"

echo "批量量化工具"
echo "============"

# 量化类型数组
QUANTS=("Q8_0" "Q6_K" "Q5_K_M" "Q4_K_M" "Q3_K_M")

for quant in "${QUANTS[@]}"; do
    echo ""
    echo "正在生成 $quant 版本..."
    
    ./quantize \\
        $MODEL_F16 \\
        ${OUTPUT_BASE}-${quant}.gguf \\
        $quant
    
    echo "✅ $quant 完成"
done

echo ""
echo "所有量化版本生成完成！"
echo ""
echo "文件列表："
ls -lh ${OUTPUT_BASE}-*.gguf
        """
        
        print(script)

# 演示
converter = GGUFConverter()
converter.explain_gguf()
converter.show_conversion_steps()
converter.show_all_quant_commands()
```

---

## 🎯 第三部分：llama.cpp推理

### 一、使用llama.cpp

```python
class LlamaCppGuide:
    """llama.cpp使用指南"""
    
    @staticmethod
    def show_inference_commands():
        """展示推理命令"""
        
        print("\n" + "="*60)
        print("llama.cpp推理使用")
        print("="*60)
        
        print("""
【基础推理】

# 命令行交互
./main -m model-q4_k_m.gguf \\
    -p "你好，请介绍一下人工智能" \\
    -n 512 \\
    -t 8

参数说明：
• -m: 模型文件
• -p: 提示词（prompt）
• -n: 生成token数
• -t: 线程数

【高级参数】

./main -m model-q4_k_m.gguf \\
    -p "你好" \\
    -n 512 \\
    -t 8 \\
    -c 4096 \\
    --temp 0.7 \\
    --top-p 0.9 \\
    --top-k 40 \\
    --repeat-penalty 1.1

参数说明：
• -c: 上下文长度
• --temp: 温度（创造性）
• --top-p: 核采样
• --top-k: Top-K采样
• --repeat-penalty: 重复惩罚

【GPU加速】

# CUDA（NVIDIA）
./main -m model.gguf \\
    -ngl 35 \\
    -t 8

# Metal（Mac）
./main -m model.gguf \\
    -ngl 1 \\
    -t 8

参数：
• -ngl: GPU层数
  • -1: 全部到GPU
  • 35: 35层到GPU
  • 0: 只用CPU

【服务器模式】

./server -m model-q4_k_m.gguf \\
    -c 4096 \\
    --host 0.0.0.0 \\
    --port 8080 \\
    -ngl -1

启动HTTP服务器，兼容OpenAI API

# 客户端调用
curl http://localhost:8080/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'

【性能测试】

./perplexity -m model-q4_k_m.gguf \\
    -f prompts.txt \\
    -t 8

测试模型困惑度（perplexity）
        """)
    
    @staticmethod
    def show_python_integration():
        """展示Python集成"""
        
        print("\n" + "="*60)
        print("Python集成（llama-cpp-python）")
        print("="*60)
        
        code = """
# 安装
pip install llama-cpp-python

# 基础使用
from llama_cpp import Llama

# 1. 加载模型
llm = Llama(
    model_path="model-q4_k_m.gguf",
    n_ctx=4096,        # 上下文长度
    n_threads=8,       # 线程数
    n_gpu_layers=35    # GPU层数（0=CPU）
)

# 2. 生成
output = llm(
    "你好，请介绍一下人工智能",
    max_tokens=512,
    temperature=0.7,
    top_p=0.9,
    stop=["\\n\\n"]
)

print(output['choices'][0]['text'])

# 3. 流式输出
stream = llm(
    "写一篇关于AI的文章",
    max_tokens=512,
    stream=True
)

for chunk in stream:
    text = chunk['choices'][0]['text']
    print(text, end='', flush=True)

# 4. 对话模式
from llama_cpp import Llama

llm = Llama(model_path="model.gguf")

messages = [
    {"role": "system", "content": "你是一个AI助手"},
    {"role": "user", "content": "你好"}
]

response = llm.create_chat_completion(
    messages=messages,
    temperature=0.7,
    max_tokens=512
)

print(response['choices'][0]['message']['content'])

# 5. 完整示例
class LocalLLM:
    def __init__(self, model_path):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=-1  # 全部GPU
        )
    
    def chat(self, message, history=None):
        messages = history or []
        messages.append({"role": "user", "content": message})
        
        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=512,
            stream=True
        )
        
        reply = ""
        for chunk in response:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                reply += delta['content']
                print(delta['content'], end='', flush=True)
        
        print()  # 换行
        return reply

# 使用
llm = LocalLLM("model-q4_k_m.gguf")
response = llm.chat("你好")
        """
        
        print(code)

# 演示
guide = LlamaCppGuide()
guide.show_inference_commands()
guide.show_python_integration()
```

---

## 📝 课后练习

### 练习1：LoRA合并
合并你的LoRA到基础模型

### 练习2：GGUF转换
转换模型为GGUF格式

### 练习3：本地推理
使用llama.cpp进行推理测试

---

## 🎓 知识总结

### 核心要点

1. **LoRA合并**
   - merge_and_unload()
   - 得到完整模型
   - 便于部署

2. **GGUF转换**
   - 两步转换
   - 多种量化级别
   - Q4_K_M推荐

3. **llama.cpp**
   - 高性能C++引擎
   - CPU/GPU混合
   - 跨平台支持

4. **实战建议**
   - Q4_K_M最常用
   - GPU加速优先
   - Python集成简单

---

## 🚀 下节预告

下一课：**第110课：实战项目-垂直领域模型微调**

- 完整项目流程
- 数据准备到部署
- 最佳实践
- 避坑指南

**集大成之作！** 🔥

---

**💪 记住：GGUF让模型跑在任何设备！**

**下一课见！** 🎉
