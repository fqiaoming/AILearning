![调试与问题排查](./images/debugging.svg)
*图：调试与问题排查*

# 第34课：Chain调试技巧与问题排查 - 快速定位和解决问题

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第6章 - Chain高级应用（第5/7课）
> - 学习目标：掌握Chain调试技巧，快速定位和解决各种问题
> - 预计时间：80-90分钟
> - 前置知识：第23-33课

---

## 📢 课程导入

### 前言

你的LangChain应用运行时突然崩溃了，错误信息是一大堆堆栈追踪，看不懂！或者更糟糕的是：没有报错，但输出就是不对，你完全不知道哪里出问题了！

这种情况太常见了！复杂的Chain就像黑盒，出了问题根本不知道从哪下手。但如果你掌握了专业的调试技巧，**5分钟就能定位问题，10分钟就能修复！**

今天这课，我要教你所有LangChain调试的秘密武器和最佳实践！让你从"调试噩梦"变成"调试高手"！

---

### 核心价值点

**第一，调试能力直接决定开发效率。**

看看两个开发者的对比：
- **新手**：出bug就懵了，到处加print，改了又改，一个bug调3小时
- **高手**：看错误信息立即定位，用工具快速验证，10分钟搞定

差距就在调试能力！掌握调试技巧，开发效率能提升5-10倍！

**第二，LangChain的调试不同于普通代码。**

传统代码调试：
- 加断点，单步执行
- 看变量值
- 追踪函数调用

LangChain调试：
- Chain是声明式的，不能打断点
- 中间结果是异步的
- LLM输出不确定
- 多个组件组合，定位困难

需要全新的调试思路和工具！

**第三，常见问题都有固定的排查套路。**

LangChain开发中90%的问题都是：
- 变量名不匹配
- 输入格式错误
- Prompt设计不当
- Memory配置问题
- 模型选择不对

每种问题都有固定的排查方法！学会这些套路，遇到问题立即知道怎么查！

**第四，这是从能写代码到能解决问题的跨越。**

初级开发：能按教程写代码
中级开发：遇到问题能自己解决
高级开发：能预防问题发生

学会调试，你就是中级开发者了！这是找工作的核心竞争力！

---

### 行动号召

今天这一课会教你：
- LangChain常见错误和解决方案
- 系统化的调试流程
- 强大的调试工具
- 性能问题排查
- 预防性调试策略

**学完这课，调试对你来说就是小菜一碟！**

---

## 📖 知识讲解

### 1. 常见错误类型

#
![Monitoring](./images/monitoring.svg)
*图：Monitoring*

### 1.1 变量名不匹配

```python
# ❌ 错误示例
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "解释{topic}"  # 变量名是topic
)

chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)

# 错误！传入的是subject，不是topic
result = chain.invoke({"subject": "AI"})
# KeyError: 'topic'
```

**解决方法：**
```python
# 方法1：检查变量名
print(prompt.input_variables)  # ['topic']

# 方法2：使用正确的变量名
result = chain.invoke({"topic": "AI"})

# 方法3：修改Prompt模板
prompt = ChatPromptTemplate.from_template("解释{subject}")
```

---

#### 1.2 输入格式错误

```python
# ❌ 错误示例
from langchain.prompts import ChatPromptTemplate

# 期望dict输入
prompt = ChatPromptTemplate.from_template("分析{data}")

# 错误：传入了字符串
result = prompt.invoke("some data")
# TypeError: expected dict, got str
```

**解决方法：**
```python
# ✅ 正确做法
result = prompt.invoke({"data": "some data"})

# 或者使用format方法
result = prompt.format(data="some data")
```

---

#### 1.3 Chain组合错误

```python
# ❌ 错误示例
from langchain.schema.output_parser import StrOutputParser

# 第一个Chain返回dict，但第二个Chain期望字符串
chain1 = prompt1 | llm  # 返回AIMessage
chain2 = ChatPromptTemplate.from_template("处理{text}") | llm

# 错误：chain1的输出不匹配chain2的输入
full_chain = chain1 | chain2
# 运行时会报错
```

**解决方法：**
```python
# ✅ 添加中间转换
chain1 = prompt1 | llm | StrOutputParser()  # 转成字符串
chain2 = ChatPromptTemplate.from_template("处理{text}") | llm

# 或者使用正确的数据映射
full_chain = chain1 | {"text": RunnablePassthrough()} | chain2
```

---

#### 1.4 Memory配置错误

```python
# ❌ 错误示例
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 错误：memory_key和prompt中的变量不匹配
memory = ConversationBufferMemory(memory_key="history")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是助手"),
    MessagesPlaceholder(variable_name="chat_history"),  # 不匹配！
    ("human", "{input}")
])

chain = ConversationChain(memory=memory, prompt=prompt)
# 运行时找不到变量
```

**解决方法：**
```python
# ✅ 统一变量名
memory = ConversationBufferMemory(
    memory_key="chat_history",  # 和Prompt中一致
    return_messages=True
)
```

---

### 2. 系统化调试流程

#### 2.1 五步调试法

```
步骤1：复现问题
- 找到最小可复现案例
- 记录输入和预期输出

步骤2：定位位置
- 使用verbose=True
- 添加Callback
- 分段测试

步骤3：分析原因
- 检查输入输出
- 验证假设
- 查看日志

步骤4：修复问题
- 实施解决方案
- 验证修复

步骤5：预防复发
- 添加测试
- 更新文档
- 改进设计
```

---

#### 2.2 分段测试法

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# 复杂的Chain
prompt = ChatPromptTemplate.from_template("分析{topic}")
llm = ChatOpenAI()
parser = StrOutputParser()

full_chain = prompt | llm | parser

# 问题：输出不对

# ✅ 分段测试
print("=== 测试步骤1：Prompt ===")
step1 = prompt.invoke({"topic": "AI"})
print(step1)

print("\n=== 测试步骤2：LLM ===")
step2 = llm.invoke(step1)
print(step2)

print("\n=== 测试步骤3：Parser ===")
step3 = parser.invoke(step2)
print(step3)

# 找出哪一步出问题
```

---

#### 2.3 使用verbose模式

```python
from langchain.chains import LLMChain

# 启用详细日志
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True  # 关键！
)

result = chain.invoke({"topic": "AI"})

# 会打印：
# - Prompt模板
# - 格式化后的Prompt
# - LLM输出
# - 最终结果
```

---

### 3. 调试工具

#### 3.1 使用LangSmith（推荐）

```python
import os

# 配置LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# 正常运行Chain，自动追踪
chain = prompt | llm | parser
result = chain.invoke({"topic": "AI"})

# LangSmith会记录：
# - 完整的执行流程
# - 每步的输入输出
# - 耗时统计
# - 错误堆栈
```

**LangSmith的优势：**
```
✅ 可视化执行流程
✅ 时间线分析
✅ 输入输出追踪
✅ 错误定位
✅ 性能分析
✅ 团队协作
```

---

#### 3.2 自定义调试Callback

```python
from langchain.callbacks.base import BaseCallbackHandler

class DebugCallback(BaseCallbackHandler):
    """调试专用Callback"""
    
    def __init__(self):
        self.step = 0
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        self.step += 1
        print(f"\n{'='*60}")
        print(f"步骤 {self.step}: Chain开始")
        print(f"{'='*60}")
        print(f"输入: {inputs}")
    
    def on_chain_end(self, outputs, **kwargs):
        print(f"\n输出: {outputs}")
        print(f"{'='*60}\n")
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"\n🤖 LLM调用")
        print(f"Prompt: {prompts[0][:200]}...")
    
    def on_llm_end(self, response, **kwargs):
        if hasattr(response, 'generations'):
            text = response.generations[0][0].text
            print(f"回复: {text[:200]}...")
    
    def on_llm_error(self, error, **kwargs):
        print(f"\n❌ LLM错误: {error}")


# 使用
debug_callback = DebugCallback()
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [debug_callback]}
)
```

---

#### 3.3 打印中间结果

```python
from langchain.schema.runnable import RunnableLambda

def print_step(x):
    """打印中间步骤"""
    print(f"\n[中间结果] {type(x).__name__}: {str(x)[:100]}...")
    return x

# 在Chain中插入打印
chain = (
    prompt 
    | RunnableLambda(print_step)  # 打印Prompt输出
    | llm 
    | RunnableLambda(print_step)  # 打印LLM输出
    | parser
    | RunnableLambda(print_step)  # 打印Parser输出
)

result = chain.invoke({"topic": "AI"})
```

---

### 4. 常见问题排查

#### 4.1 "KeyError: 'xxx'"

```python
# 原因：变量名不匹配

# 排查步骤：
# 1. 检查Prompt的input_variables
print(prompt.input_variables)  # ['topic', 'style']

# 2. 检查传入的参数
inputs = {"topic": "AI"}  # 缺少'style'

# 3. 解决方法
# 方法A：添加缺少的变量
inputs = {"topic": "AI", "style": "简洁"}

# 方法B：使用partial
prompt = prompt.partial(style="简洁")
inputs = {"topic": "AI"}
```

---

#### 4.2 "输出格式不对"

```python
# 原因：Parser配置错误或输出不符合格式

# 排查步骤：
# 1. 检查Parser的格式说明
from langchain.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=MyModel)
print(parser.get_format_instructions())

# 2. 检查LLM实际输出
from langchain.schema.output_parser import StrOutputParser

temp_chain = prompt | llm | StrOutputParser()
raw_output = temp_chain.invoke({"topic": "AI"})
print(f"原始输出:\n{raw_output}")

# 3. 修改Prompt，加入格式说明
better_prompt = ChatPromptTemplate.from_template(
    """{format_instructions}

请分析：{topic}"""
).partial(format_instructions=parser.get_format_instructions())
```

---

#### 4.3 "响应很慢"

```python
# 排查步骤：
from langchain.callbacks.base import BaseCallbackHandler
import time

class TimingCallback(BaseCallbackHandler):
    """计时Callback"""
    
    def __init__(self):
        self.times = {}
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        run_id = kwargs.get("run_id")
        self.times[run_id] = time.time()
    
    def on_llm_end(self, response, **kwargs):
        run_id = kwargs.get("run_id")
        if run_id in self.times:
            elapsed = time.time() - self.times[run_id]
            print(f"⏱️  LLM耗时: {elapsed:.2f}秒")
            
            # 性能瓶颈判断
            if elapsed > 5:
                print("⚠️  LLM响应慢，可能原因：")
                print("  - 网络问题")
                print("  - 模型选择（GPT-4更慢）")
                print("  - Prompt太长")
                print("  - max_tokens设置过大")

# 使用
timer = TimingCallback()
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [timer]}
)

# 优化方案：
# 1. 使用更快的模型（GPT-4 → GPT-3.5）
# 2. 减少Prompt长度
# 3. 降低max_tokens
# 4. 使用流式输出
# 5. 添加缓存
```

---

#### 4.4 "Memory不工作"

```python
# 排查步骤：
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

# 1. 检查memory是否正确保存
memory.save_context({"input": "你好"}, {"output": "你好！"})
print(memory.load_memory_variables({}))

# 2. 检查变量名
print(f"Memory key: {memory.memory_key}")
# 确保和Prompt中的MessagesPlaceholder变量名一致

# 3. 检查return_messages
# 如果使用ChatPromptTemplate，需要return_messages=True
memory = ConversationBufferMemory(return_messages=True)

# 4. 检查Chain配置
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # 看看memory是否被加载
)
```

---

## 💻 Demo案例：调试实战

创建`debugging_demo.py`：

```python
"""
Chain调试完整演示
常见问题和解决方案
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.callbacks.base import BaseCallbackHandler
import time


def demo_1_variable_mismatch():
    """示例1：变量名不匹配问题"""
    print("\n" + "="*60)
    print("示例1：变量名不匹配 - 问题演示与解决")
    print("="*60)
    
    # 问题代码
    prompt = ChatPromptTemplate.from_template(
        "解释{topic}，用{style}的方式"
    )
    
    print("Prompt需要的变量：", prompt.input_variables)
    
    # ❌ 错误：缺少style变量
    try:
        result = prompt.invoke({"topic": "AI"})
        print("结果：", result)
    except KeyError as e:
        print(f"❌ 错误：{e}")
        print("   原因：缺少required变量'style'")
    
    # ✅ 解决方案1：提供所有变量
    print("\n解决方案1：提供完整变量")
    result = prompt.invoke({"topic": "AI", "style": "简洁"})
    print(f"✓ 成功")
    
    # ✅ 解决方案2：使用partial
    print("\n解决方案2：使用partial固定变量")
    prompt_partial = prompt.partial(style="简洁")
    result = prompt_partial.invoke({"topic": "AI"})
    print(f"✓ 成功")


def demo_2_chain_debugging():
    """示例2：Chain逐步调试"""
    print("\n" + "="*60)
    print("示例2：Chain逐步调试")
    print("="*60)
    
    llm = ChatOpenAI()
    
    # 复杂Chain
    prompt = ChatPromptTemplate.from_template("用50字介绍{topic}")
    chain = prompt | llm | StrOutputParser()
    
    print("完整Chain测试：")
    topic = "机器学习"
    
    # 分步调试
    print("\n步骤1：测试Prompt")
    step1 = prompt.invoke({"topic": topic})
    print(f"  Prompt输出类型：{type(step1).__name__}")
    print(f"  内容：{step1.messages[0].content}")
    
    print("\n步骤2：测试LLM")
    step2 = llm.invoke(step1)
    print(f"  LLM输出类型：{type(step2).__name__}")
    print(f"  内容：{step2.content[:100]}...")
    
    print("\n步骤3：测试Parser")
    step3 = StrOutputParser().invoke(step2)
    print(f"  Parser输出类型：{type(step3).__name__}")
    print(f"  内容：{step3[:100]}...")
    
    print("\n完整Chain：")
    final = chain.invoke({"topic": topic})
    print(f"  最终结果：{final}")


def demo_3_performance_debugging():
    """示例3：性能问题排查"""
    print("\n" + "="*60)
    print("示例3：性能瓶颈分析")
    print("="*60)
    
    class PerformanceDebugger(BaseCallbackHandler):
        """性能调试器"""
        
        def __init__(self):
            self.times = {}
            self.counts = {"chain": 0, "llm": 0}
        
        def on_chain_start(self, serialized, inputs, **kwargs):
            run_id = kwargs.get("run_id")
            self.times[f"chain_{run_id}"] = time.time()
            self.counts["chain"] += 1
            print(f"▶️  Chain #{self.counts['chain']} 开始")
        
        def on_chain_end(self, outputs, **kwargs):
            run_id = kwargs.get("run_id")
            key = f"chain_{run_id}"
            if key in self.times:
                elapsed = time.time() - self.times[key]
                print(f"✓ Chain #{self.counts['chain']} 完成 ({elapsed:.2f}秒)")
                
                if elapsed > 3:
                    print(f"   ⚠️  耗时较长！可能的原因：")
                    print(f"      - LLM响应慢")
                    print(f"      - 网络问题")
                    print(f"      - Prompt太长")
        
        def on_llm_start(self, serialized, prompts, **kwargs):
            run_id = kwargs.get("run_id")
            self.times[f"llm_{run_id}"] = time.time()
            self.counts["llm"] += 1
            
            prompt_len = len(prompts[0])
            print(f"  🤖 LLM调用 (Prompt长度: {prompt_len}字符)")
            
            if prompt_len > 1000:
                print(f"     ⚠️  Prompt过长，可能影响性能")
        
        def on_llm_end(self, response, **kwargs):
            run_id = kwargs.get("run_id")
            key = f"llm_{run_id}"
            if key in self.times:
                elapsed = time.time() - self.times[key]
                print(f"  ✓ LLM响应 ({elapsed:.2f}秒)")
    
    debugger = PerformanceDebugger()
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template("详细分析{topic}")
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke(
        {"topic": "深度学习的发展历程"},
        config={"callbacks": [debugger]}
    )
    
    print(f"\n结果：{result[:100]}...")


def demo_4_error_handling():
    """示例4：错误处理和恢复"""
    print("\n" + "="*60)
    print("示例4：错误处理")
    print("="*60)
    
    class ErrorHandler(BaseCallbackHandler):
        """错误处理器"""
        
        def on_chain_error(self, error, **kwargs):
            print(f"❌ Chain错误捕获")
            print(f"   错误类型：{type(error).__name__}")
            print(f"   错误信息：{error}")
            print(f"   建议：检查输入格式和变量名")
        
        def on_llm_error(self, error, **kwargs):
            print(f"❌ LLM错误捕获")
            print(f"   错误类型：{type(error).__name__}")
            print(f"   错误信息：{error}")
            print(f"   建议：")
            print(f"   - 检查API密钥")
            print(f"   - 检查网络连接")
            print(f"   - 检查模型名称")
            print(f"   - 检查token限制")
    
    error_handler = ErrorHandler()
    
    # 故意制造错误
    prompt = ChatPromptTemplate.from_template("分析{topic}")
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    chain = prompt | llm | StrOutputParser()
    
    # 错误1：缺少变量
    print("测试1：变量缺失")
    try:
        result = chain.invoke(
            {},  # 空字典，缺少topic
            config={"callbacks": [error_handler]}
        )
    except Exception as e:
        print(f"捕获异常：{type(e).__name__}")
    
    # 错误2：无效模型
    print("\n测试2：无效模型名")
    try:
        bad_llm = ChatOpenAI(model="invalid-model-name")
        bad_chain = prompt | bad_llm | StrOutputParser()
        result = bad_chain.invoke(
            {"topic": "AI"},
            config={"callbacks": [error_handler]}
        )
    except Exception as e:
        print(f"捕获异常：{type(e).__name__}")


def demo_5_debugging_checklist():
    """示例5：调试检查清单"""
    print("\n" + "="*60)
    print("示例5：调试检查清单")
    print("="*60)
    
    checklist = """
🔍 LangChain调试检查清单

📋 基础检查：
  □ API密钥是否配置？
  □ 依赖包是否安装？
  □ 网络连接是否正常？

🔧 Prompt检查：
  □ input_variables是否正确？
  □ 所有变量是否都提供了值？
  □ 模板语法是否正确？

🔗 Chain检查：
  □ 组件类型是否匹配？
  □ 输入输出格式是否一致？
  □ Parser是否正确配置？

💾 Memory检查：
  □ memory_key是否匹配？
  □ return_messages是否正确？
  □ 是否正确保存和加载？

⚡ 性能检查：
  □ 是否启用了缓存？
  □ Prompt长度是否合理？
  □ 模型选择是否合适？
  □ 是否有不必要的重复调用？

📊 监控检查：
  □ 是否启用verbose？
  □ 是否添加Callback？
  □ 是否记录日志？
  □ 是否有错误告警？
"""
    
    print(checklist)


def main():
    """主函数"""
    print("🎯 Chain调试完整演示")
    print("="*60)
    
    demo_1_variable_mismatch()
    demo_2_chain_debugging()
    demo_3_performance_debugging()
    demo_4_error_handling()
    demo_5_debugging_checklist()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 调试技巧总结：")
    print("1. 使用verbose=True查看执行流程")
    print("2. 分步测试，逐个排查")
    print("3. 检查变量名匹配")
    print("4. 使用Callback监控性能")
    print("5. 善用LangSmith可视化工具")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 调试最佳实践

### 调试工具箱

```python
# 工具1：快速检查
def quick_check(chain):
    """快速检查Chain配置"""
    print("Chain类型：", type(chain).__name__)
    if hasattr(chain, 'input_variables'):
        print("输入变量：", chain.input_variables)
    if hasattr(chain, 'output_keys'):
        print("输出键：", chain.output_keys)

# 工具2：输入验证
def validate_input(chain, inputs):
    """验证输入是否完整"""
    if hasattr(chain, 'input_variables'):
        required = set(chain.input_variables)
        provided = set(inputs.keys())
        missing = required - provided
        if missing:
            print(f"❌ 缺少变量：{missing}")
            return False
    return True

# 工具3：安全执行
def safe_invoke(chain, inputs, **kwargs):
    """安全执行，捕获错误"""
    try:
        if not validate_input(chain, inputs):
            return None
        return chain.invoke(inputs, **kwargs)
    except Exception as e:
        print(f"❌ 执行错误：{type(e).__name__}: {e}")
        return None
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 识别和解决常见错误
- [ ] 使用系统化方法调试
- [ ] 运用各种调试工具
- [ ] 快速定位性能瓶颈
- [ ] 预防常见问题

---

## 📝 下一课预告

**第35课：Chain性能优化与最佳实践**

下一课我们将学习：
- Chain性能优化技巧
- 缓存策略
- 并发处理
- 成本优化
- 生产环境最佳实践

**让你的Chain又快又省！**

---

**🎉 恭喜你完成第34课！**

你现在是调试高手了！

**进度：34/165课（20.6%完成）** 🚀
