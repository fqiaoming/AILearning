![路由链架构设计](./images/router_chain.svg)
*图：路由链架构设计*

# 第31课：RouterChain - 动态路由与智能分发

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第6章 - Chain高级应用（第2/7课）
> - 学习目标：掌握RouterChain，实现基于内容的智能路由和分发
> - 预计时间：70-80分钟
> - 前置知识：第23-30课

---

## 📢 课程导入

### 前言

你的AI助手收到用户消息：**"帮我翻译这段话"** vs **"解释什么是量子计算"** vs **"写一段代码"**。三种完全不同的任务，需要不同的处理方式：翻译用简单模型，解释用知识库，代码用专门的模型。

如果用if-else判断，代码会很乱。但如果有个智能路由器，能自动分析输入，把请求发送到最合适的Chain，那就完美了！

**RouterChain就是这样的智能路由器！**今天这课，我要教你如何用RouterChain构建智能分发系统！

---

### 核心价值点

**第一，RouterChain解决了"一个入口，多种处理"的问题。**

真实AI应用通常需要处理多种类型的请求：
- **客服系统**：咨询 vs 投诉 vs 建议 → 不同处理流程
- **内容平台**：文章 vs 视频 vs 图片 → 不同分析方式
- **智能助手**：闲聊 vs 工具调用 vs 知识问答 → 不同模型

如果都用一个Chain处理，效果不好；如果写一堆if-else，代码混乱。RouterChain提供优雅的解决方案！

**第二，RouterChain不是简单的if-else。**

很多人觉得RouterChain就是：
```python
if intent == "translate":
    return translate_chain
elif intent == "summarize":
    return summarize_chain
```

错！RouterChain提供的是：
- **智能分类**：用AI理解输入
- **动态路由**：运行时决定路径
- **降级处理**：找不到匹配时的默认方案
- **元数据路由**：基于上下文信息路由
- **性能优化**：缓存路由决策

这才是专业的路由系统！

**第三，RouterChain能显著提升系统性能和成本。**

看看优化效果：
- **性能提升**：简单任务用快速模型，响应快3倍
- **成本降低**：不是所有任务都用GPT-4，省70%
- **准确率提高**：专门的Chain处理特定任务，效果更好
- **可扩展性**：添加新类型只需加新Chain

合理使用RouterChain，系统会质的飞跃！

**第四，这是构建企业级AI系统的核心技术。**

大型AI系统都有路由层：
- **ChatGPT**：识别任务类型，分配不同策略
- **GitHub Copilot**：代码 vs 注释 vs 文档，不同处理
- **智能客服**：常见问题 vs 复杂问题，不同优先级

学会RouterChain，你就能构建这种专业系统！

---

### 行动号召

今天这一课会教你：
- RouterChain的设计原理
- LLMRouterChain智能路由
- 基于规则和基于AI的路由
- 多级路由策略
- 实战：构建智能分发系统

**学完这课，你的AI系统会更智能、更高效！**

---

## 📖 知识讲解

### 1. RouterChain概述

#
![Monitoring](./images/monitoring.svg)
*图：Monitoring*

### 1.1 什么是RouterChain

```
RouterChain：
- 根据输入内容动态选择处理路径
- 一个入口，多个出口
- 智能分发请求

工作流程：
用户输入 → Router分析 → 选择Chain → 执行 → 返回结果

场景示例：
输入："翻译：Hello"
Router：识别为翻译任务
选择：translation_chain
执行并返回
```

#### 1.2 RouterChain的类型

```
1. LLMRouterChain
   - 使用LLM判断路由
   - 灵活、智能
   - 适合复杂场景

2. EmbeddingRouterChain
   - 基于语义相似度
   - 快速、高效
   - 适合预定义类别

3. 规则路由
   - 基于关键词匹配
   - 简单、可控
   - 适合明确规则
```

---

### 2. LLMRouterChain（AI路由）

#### 2.1 基础用法

```python
from langchain.chains.router import LLMRouterChain, MultiPromptChain
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

# 定义不同的目标Chain
physics_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "作为物理专家，解释：{input}"
    )
)

math_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "作为数学专家，解释：{input}"
    )
)

history_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "作为历史专家，解释：{input}"
    )
)

# 定义路由信息
prompt_infos = [
    {
        "name": "physics",
        "description": "适合回答物理相关问题，如力学、光学、量子物理等",
        "prompt_template": physics_chain.prompt
    },
    {
        "name": "math",
        "description": "适合回答数学问题，如代数、几何、微积分等",
        "prompt_template": math_chain.prompt
    },
    {
        "name": "history",
        "description": "适合回答历史问题，如古代史、近代史、世界历史等",
        "prompt_template": history_chain.prompt
    }
]

# 创建路由Chain
from langchain.chains.router.llm_router import RouterOutputParser

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

router_template = f"""给定用户输入，选择最合适的专家。

可选专家：
{destinations_str}

用户输入：{{input}}

返回格式：
{{"destination": "专家名称", "next_inputs": {{"input": "处理后的输入"}}}}
"""

router_prompt = ChatPromptTemplate.from_template(router_template)

router_chain = LLMRouterChain.from_llm(
    llm=llm,
    prompt=router_prompt
)

# 组合成MultiPromptChain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={
        "physics": physics_chain,
        "math": math_chain,
        "history": history_chain
    },
    default_chain=physics_chain,  # 默认Chain
    verbose=True
)

# 使用
result = chain.invoke("什么是牛顿第一定律？")
# 自动路由到physics_chain
```

---

#### 2.2 简化版本（使用LCEL）

```python
from langchain.schema.runnable import RunnableBranch
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

# 路由函数
def route_to_chain(inputs):
    """分析输入，返回目标chain名称"""
    text = inputs["text"].lower()
    
    # 简单规则（实际应该用LLM判断）
    if any(word in text for word in ["翻译", "translate"]):
        return "translate"
    elif any(word in text for word in ["总结", "摘要"]):
        return "summarize"
    elif any(word in text for word in ["代码", "编程"]):
        return "code"
    else:
        return "default"

# 定义目标Chains
translate_chain = (
    ChatPromptTemplate.from_template("翻译：{text}")
    | llm
)

summarize_chain = (
    ChatPromptTemplate.from_template("总结：{text}")
    | llm
)

code_chain = (
    ChatPromptTemplate.from_template("代码：{text}")
    | llm
)

default_chain = (
    ChatPromptTemplate.from_template("回答：{text}")
    | llm
)

# 创建路由
router = RunnableBranch(
    (lambda x: route_to_chain(x) == "translate", translate_chain),
    (lambda x: route_to_chain(x) == "summarize", summarize_chain),
    (lambda x: route_to_chain(x) == "code", code_chain),
    default_chain
)

# 使用
result = router.invoke({"text": "请翻译：Hello World"})
```

---

### 3. 基于规则的路由

#### 3.1 关键词匹配路由

```python
class KeywordRouter:
    """基于关键词的路由器"""
    
    def __init__(self):
        self.routes = {
            "translation": {
                "keywords": ["翻译", "translate", "英文", "中文"],
                "chain": translation_chain
            },
            "summary": {
                "keywords": ["总结", "摘要", "概括"],
                "chain": summary_chain
            },
            "code": {
                "keywords": ["代码", "编程", "函数", "python"],
                "chain": code_chain
            }
        }
        self.default_chain = default_chain
    
    def route(self, text: str):
        """路由到合适的chain"""
        text_lower = text.lower()
        
        # 匹配关键词
        for route_name, route_info in self.routes.items():
            for keyword in route_info["keywords"]:
                if keyword in text_lower:
                    print(f"[路由] {text[:30]}... → {route_name}")
                    return route_info["chain"]
        
        # 默认路由
        print(f"[路由] {text[:30]}... → default")
        return self.default_chain
    
    def invoke(self, text: str):
        """执行路由和调用"""
        chain = self.route(text)
        return chain.invoke({"text": text})


# 使用
router = KeywordRouter()
result = router.invoke("请翻译：Hello World")
```

---

#### 3.2 正则表达式路由

```python
import re

class RegexRouter:
    """基于正则的路由器"""
    
    def __init__(self):
        self.patterns = [
            {
                "pattern": r"翻译[:：]?\s*(.+)",
                "chain": translation_chain,
                "name": "translation"
            },
            {
                "pattern": r"总结[:：]?\s*(.+)",
                "chain": summary_chain,
                "name": "summary"
            },
            {
                "pattern": r"(计算|算)\s*(.+)",
                "chain": calculator_chain,
                "name": "calculator"
            }
        ]
        self.default_chain = default_chain
    
    def route(self, text: str):
        """路由"""
        for pattern_info in self.patterns:
            match = re.search(pattern_info["pattern"], text)
            if match:
                print(f"[路由] 匹配 {pattern_info['name']}")
                return pattern_info["chain"], match
        
        return self.default_chain, None
    
    def invoke(self, text: str):
        """执行"""
        chain, match = self.route(text)
        
        # 提取匹配的内容
        if match:
            extracted = match.group(1) if match.groups() else text
            return chain.invoke({"text": extracted})
        else:
            return chain.invoke({"text": text})
```

---

### 4. 多级路由

#### 4.1 两级路由示例

```python
class TwoLevelRouter:
    """两级路由系统"""
    
    def __init__(self):
        # 第一级：粗分类
        self.level1_router = {
            "content": content_router,  # 内容相关
            "tool": tool_router,        # 工具调用
            "chat": chat_chain          # 闲聊
        }
        
        # 第二级：细分类
        self.content_router = {
            "translate": translation_chain,
            "summarize": summary_chain,
            "analyze": analysis_chain
        }
        
        self.tool_router = {
            "weather": weather_tool,
            "calculator": calculator_tool,
            "search": search_tool
        }
    
    def route_level1(self, text: str) -> str:
        """第一级路由"""
        # 简化判断（实际用LLM）
        if any(word in text for word in ["翻译", "总结", "分析"]):
            return "content"
        elif any(word in text for word in ["天气", "计算", "搜索"]):
            return "tool"
        else:
            return "chat"
    
    def route_level2(self, category: str, text: str):
        """第二级路由"""
        if category == "content":
            if "翻译" in text:
                return self.content_router["translate"]
            elif "总结" in text:
                return self.content_router["summarize"]
            else:
                return self.content_router["analyze"]
        
        elif category == "tool":
            if "天气" in text:
                return self.tool_router["weather"]
            elif "计算" in text:
                return self.tool_router["calculator"]
            else:
                return self.tool_router["search"]
        
        else:
            return self.level1_router["chat"]
    
    def invoke(self, text: str):
        """执行两级路由"""
        # 第一级
        category = self.route_level1(text)
        print(f"[L1路由] → {category}")
        
        # 第二级
        chain = self.route_level2(category, text)
        print(f"[L2路由] → {chain}")
        
        # 执行
        return chain.invoke({"text": text})
```

---

## 💻 Demo案例：RouterChain实战

创建`router_chain_demo.py`：

```python
"""
RouterChain完整演示
从简单到复杂的路由策略
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableBranch
from langchain.schema.output_parser import StrOutputParser


def demo_1_simple_routing():
    """示例1：简单关键词路由"""
    print("\n" + "="*60)
    print("示例1：简单关键词路由")
    print("="*60)
    
    llm = ChatOpenAI()
    
    # 定义不同的Chains
    translate_chain = (
        ChatPromptTemplate.from_template("翻译成英文：{text}")
        | llm
        | StrOutputParser()
    )
    
    summarize_chain = (
        ChatPromptTemplate.from_template("用20字总结：{text}")
        | llm
        | StrOutputParser()
    )
    
    explain_chain = (
        ChatPromptTemplate.from_template("详细解释：{text}")
        | llm
        | StrOutputParser()
    )
    
    # 路由函数
    def classify_intent(inputs):
        text = inputs["text"].lower()
        if "翻译" in text:
            return "translate"
        elif "总结" in text:
            return "summarize"
        else:
            return "explain"
    
    # 创建路由
    router = RunnableBranch(
        (lambda x: classify_intent(x) == "translate", translate_chain),
        (lambda x: classify_intent(x) == "summarize", summarize_chain),
        explain_chain  # 默认
    )
    
    # 测试
    test_cases = [
        "请翻译：人工智能正在改变世界",
        "总结这段话：Python是一种高级编程语言...",
        "什么是机器学习？"
    ]
    
    for text in test_cases:
        result = router.invoke({"text": text})
        print(f"\n输入：{text}")
        print(f"输出：{result}")


def demo_2_ai_powered_routing():
    """示例2：AI驱动的路由"""
    print("\n" + "="*60)
    print("示例2：AI驱动的智能路由")
    print("="*60)
    
    llm = ChatOpenAI()
    
    # 路由分类器
    router_prompt = ChatPromptTemplate.from_template(
        """分析用户请求的类别。

类别：
- translate: 翻译任务
- code: 代码相关
- explain: 解释说明
- chat: 闲聊

用户请求：{text}

只返回类别名称（translate/code/explain/chat）"""
    )
    
    router_chain = router_prompt | llm | StrOutputParser()
    
    # 目标Chains
    chains = {
        "translate": (
            ChatPromptTemplate.from_template("翻译：{text}")
            | llm
            | StrOutputParser()
        ),
        "code": (
            ChatPromptTemplate.from_template("生成代码：{text}")
            | llm
            | StrOutputParser()
        ),
        "explain": (
            ChatPromptTemplate.from_template("详细解释：{text}")
            | llm
            | StrOutputParser()
        ),
        "chat": (
            ChatPromptTemplate.from_template("友好回复：{text}")
            | llm
            | StrOutputParser()
        )
    }
    
    # 路由逻辑
    def route_and_execute(inputs):
        text = inputs["text"]
        
        # AI判断类别
        category = router_chain.invoke({"text": text}).strip().lower()
        print(f"[AI路由] {text[:30]}... → {category}")
        
        # 选择Chain
        chain = chains.get(category, chains["chat"])
        
        # 执行
        return chain.invoke({"text": text})
    
    # 测试
    test_cases = [
        "把'你好'翻译成英文",
        "写一个Python函数计算斐波那契数列",
        "解释什么是区块链",
        "今天天气真好"
    ]
    
    for text in test_cases:
        result = route_and_execute({"text": text})
        print(f"输出：{result[:100]}...\n")


def demo_3_multi_level_routing():
    """示例3：多级路由"""
    print("\n" + "="*60)
    print("示例3：两级路由系统")
    print("="*60)
    
    llm = ChatOpenAI()
    
    class MultiLevelRouter:
        def __init__(self):
            # 一级路由：大类
            self.level1_categories = ["content", "tool", "chat"]
            
            # 二级路由：细分
            self.content_chains = {
                "translate": ChatPromptTemplate.from_template("翻译：{text}") | llm,
                "summarize": ChatPromptTemplate.from_template("总结：{text}") | llm
            }
            
            self.tool_chains = {
                "weather": ChatPromptTemplate.from_template("天气：{text}") | llm,
                "calculator": ChatPromptTemplate.from_template("计算：{text}") | llm
            }
            
            self.chat_chain = ChatPromptTemplate.from_template("聊天：{text}") | llm
        
        def route_level1(self, text: str) -> str:
            """一级路由"""
            if any(w in text for w in ["翻译", "总结"]):
                return "content"
            elif any(w in text for w in ["天气", "计算"]):
                return "tool"
            else:
                return "chat"
        
        def route_level2(self, category: str, text: str):
            """二级路由"""
            if category == "content":
                if "翻译" in text:
                    return self.content_chains["translate"]
                else:
                    return self.content_chains["summarize"]
            elif category == "tool":
                if "天气" in text:
                    return self.tool_chains["weather"]
                else:
                    return self.tool_chains["calculator"]
            else:
                return self.chat_chain
        
        def invoke(self, text: str):
            # 一级路由
            category = self.route_level1(text)
            print(f"[L1] {text[:30]}... → {category}")
            
            # 二级路由
            chain = self.route_level2(category, text)
            print(f"[L2] → {type(chain).__name__}")
            
            # 执行
            result = chain.invoke({"text": text})
            return result.content if hasattr(result, 'content') else result
    
    # 测试
    router = MultiLevelRouter()
    
    test_cases = [
        "翻译：Hello World",
        "总结这篇文章...",
        "北京今天天气怎么样？",
        "计算 123 + 456",
        "你好呀"
    ]
    
    for text in test_cases:
        result = router.invoke(text)
        print(f"输出：{result[:80]}...\n")


def demo_4_smart_router_with_context():
    """示例4：带上下文的智能路由"""
    print("\n" + "="*60)
    print("示例4：上下文感知路由")
    print("="*60)
    
    llm = ChatOpenAI()
    
    class ContextAwareRouter:
        def __init__(self):
            self.history = []
            self.user_preferences = {}
        
        def route(self, text: str, user_id: str = "default"):
            """根据输入和上下文路由"""
            # 考虑用户历史
            recent_topics = [h["topic"] for h in self.history[-3:]]
            
            # 考虑用户偏好
            preferred_style = self.user_preferences.get(
                user_id, {"style": "详细"}
            )
            
            # 智能路由（简化）
            if "翻译" in text:
                chain_type = "translate"
            elif len(recent_topics) > 0 and "继续" in text:
                chain_type = "continue"  # 继续之前的话题
            else:
                chain_type = "general"
            
            print(f"[路由] 话题历史: {recent_topics}")
            print(f"[路由] 用户偏好: {preferred_style}")
            print(f"[路由] 选择: {chain_type}")
            
            return chain_type
        
        def invoke(self, text: str, user_id: str = "default"):
            chain_type = self.route(text, user_id)
            
            # 记录历史
            self.history.append({"text": text, "topic": chain_type})
            
            # 执行（简化）
            return f"[{chain_type}] 处理: {text}"
    
    # 测试
    router = ContextAwareRouter()
    
    # 模拟对话
    print(router.invoke("什么是AI？"))
    print(router.invoke("继续讲"))  # 上下文相关
    print(router.invoke("翻译：Hello"))


def main():
    """主函数"""
    print("🎯 RouterChain完整演示")
    print("="*60)
    
    demo_1_simple_routing()
    demo_2_ai_powered_routing()
    demo_3_multi_level_routing()
    demo_4_smart_router_with_context()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("\n💡 核心要点：")
    print("1. 关键词路由：简单快速")
    print("2. AI路由：灵活智能")
    print("3. 多级路由：处理复杂场景")
    print("4. 上下文路由：考虑历史和偏好")
    print("="*60)


if __name__ == "__main__":
    main()
```

---

## 🎯 最佳实践

### 路由策略选择

```
简单场景（<5个分类）：
→ 关键词匹配

中等场景（5-20个分类）：
→ AI路由 + 规则兜底

复杂场景（>20个分类）：
→ 多级路由

动态场景（分类经常变化）：
→ AI路由 + 配置文件
```

### 性能优化

```python
# 1. 缓存路由决策
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_route(text: str) -> str:
    return router.classify(text)

# 2. 批量路由
texts = ["text1", "text2", "text3"]
routes = router.batch_classify(texts)

# 3. 异步路由
async def async_route(text: str):
    return await router.aclassify(text)
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 理解RouterChain的设计原理
- [ ] 实现基于关键词的路由
- [ ] 使用AI进行智能路由
- [ ] 设计多级路由系统
- [ ] 优化路由性能

---

## 📝 下一课预告

**第32课：Memory与对话管理深入**

下一课我们将深入学习：
- ConversationBufferMemory详解
- ConversationWindowMemory
- ConversationSummaryMemory
- 自定义Memory
- Memory性能优化

**让AI真正"记住"对话！**

---

**🎉 恭喜你完成第31课！**

你的AI系统现在能智能路由了！

**进度：31/165课（18.8%完成）** 🚀
