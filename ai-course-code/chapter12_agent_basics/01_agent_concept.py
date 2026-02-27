"""
第12章-Agent基础：Agent概念
对应课程：第70课-什么是Agent

Agent = LLM + 工具 + 规划能力
让AI不只是"说"，还能"做"
"""


def demo_llm_vs_agent():
    """LLM vs Agent对比"""
    print("=" * 60)
    print("LLM vs Agent")
    print("=" * 60)
    
    print("""
【普通LLM】
用户："今天北京天气怎么样？"
LLM："我没有实时信息，无法告诉你今天的天气。"

【Agent】
用户："今天北京天气怎么样？"
Agent思考："我需要查询天气信息..."
Agent行动：调用天气API
Agent观察：返回结果"北京今天晴，25°C"
Agent回答："北京今天晴天，气温25°C，适合户外活动。"

区别：
- LLM只能基于训练数据回答
- Agent可以调用工具获取实时信息
""")


def demo_agent_components():
    """Agent组成部分"""
    print("\n" + "=" * 60)
    print("Agent组成部分")
    print("=" * 60)
    
    print("""
Agent三要素：

1. 大脑（LLM）
   - 理解用户意图
   - 决定下一步行动
   - 生成最终回答

2. 工具（Tools）
   - 搜索引擎
   - 计算器
   - 数据库查询
   - API调用
   - 代码执行
   - ...任何可调用的功能

3. 规划能力（Planning）
   - 分析问题
   - 制定计划
   - 选择合适的工具
   - 根据结果调整
""")


def demo_react_pattern():
    """ReAct模式详解"""
    print("\n" + "=" * 60)
    print("ReAct模式")
    print("=" * 60)
    
    print("""
ReAct = Reasoning + Acting（推理+行动）

循环过程：
思考(Thought) → 行动(Action) → 观察(Observation) → 思考...

示例：用户问"苹果公司市值多少？"

第1轮：
Thought: 我需要查询苹果公司的股票信息
Action: search("Apple stock market cap")
Observation: Apple Inc. market cap is $2.8 trillion

第2轮：
Thought: 我得到了市值信息，可以回答了
Action: finish("苹果公司市值约2.8万亿美元")
""")
    
    # 模拟ReAct流程
    print("\n【模拟ReAct流程】")
    
    class SimpleAgent:
        def __init__(self):
            self.tools = {
                "search": lambda q: f"搜索结果：{q}的答案是42",
                "calculate": lambda expr: f"计算结果：{eval(expr)}",
            }
        
        def think(self, question, observation=None):
            """模拟思考过程"""
            if observation:
                return f"观察到：{observation}，我可以回答了"
            return f"我需要搜索关于'{question}'的信息"
        
        def act(self, thought):
            """模拟行动"""
            if "搜索" in thought:
                return "search", "相关问题"
            return "finish", None
        
        def run(self, question):
            print(f"问题：{question}")
            
            # 第1轮
            thought1 = self.think(question)
            print(f"Thought: {thought1}")
            
            action, param = self.act(thought1)
            print(f"Action: {action}({param})")
            
            if action in self.tools:
                obs = self.tools[action](param)
                print(f"Observation: {obs}")
                
                # 第2轮
                thought2 = self.think(question, obs)
                print(f"Thought: {thought2}")
                print("Action: finish(回答用户)")
    
    agent = SimpleAgent()
    agent.run("宇宙的终极答案是什么？")


def demo_agent_types():
    """Agent类型"""
    print("\n" + "=" * 60)
    print("常见Agent类型")
    print("=" * 60)
    
    print("""
1. ReAct Agent
   - 思考-行动-观察循环
   - 最经典的Agent模式

2. Plan-and-Execute Agent
   - 先规划完整计划
   - 再逐步执行
   - 适合复杂任务

3. Self-Ask Agent
   - 把问题分解成子问题
   - 逐个解决子问题
   - 适合多跳推理

4. Multi-Agent
   - 多个Agent协作
   - 各司其职
   - 适合复杂系统
""")


if __name__ == "__main__":
    demo_llm_vs_agent()
    demo_agent_components()
    demo_react_pattern()
    demo_agent_types()
    
    print("\n" + "=" * 60)
    print("✅ Agent概念学习完成！")
    print("\n核心记忆：")
    print("  • Agent = LLM + 工具 + 规划")
    print("  • ReAct = 思考 → 行动 → 观察 → 循环")
    print("  • 让AI从'只会说'变成'能做事'")

