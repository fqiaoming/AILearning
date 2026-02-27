"""
第14章-Agent进阶：Plan-and-Execute模式
对应课程：第76课-Plan-and-Execute Agent

与ReAct的区别：
- ReAct：边思考边执行
- Plan-and-Execute：先规划完，再逐步执行
"""


def demo_react_vs_plan_execute():
    """对比两种模式"""
    print("=" * 60)
    print("ReAct vs Plan-and-Execute")
    print("=" * 60)
    
    print("""
任务：帮我写一篇关于Python的文章并发布到博客

【ReAct模式】边想边做
Thought: 我先搜索Python的资料
Action: search("Python")
Observation: ...
Thought: 好，现在写文章
Action: write_article(...)
Thought: 接下来发布
Action: publish(...)

特点：
- 灵活，可以根据中间结果调整
- 但可能会"走偏"

【Plan-and-Execute模式】先规划后执行
Planning阶段：
1. 确定文章主题和大纲
2. 搜索相关资料
3. 撰写文章内容
4. 审核修改
5. 发布到博客

Execution阶段：
→ 执行步骤1...
→ 执行步骤2...
→ ...

特点：
- 有完整计划，不容易跑偏
- 适合复杂任务
""")


def demo_plan_execute_implementation():
    """Plan-and-Execute实现"""
    print("\n" + "=" * 60)
    print("Plan-and-Execute实现思路")
    print("=" * 60)
    
    class PlanExecuteAgent:
        def __init__(self, planner, executor):
            self.planner = planner
            self.executor = executor
        
        def run(self, task):
            # 阶段1：规划
            print(f"任务：{task}")
            print("\n【规划阶段】")
            plan = self.planner.plan(task)
            for i, step in enumerate(plan, 1):
                print(f"  步骤{i}：{step}")
            
            # 阶段2：执行
            print("\n【执行阶段】")
            results = []
            for i, step in enumerate(plan, 1):
                print(f"  执行步骤{i}：{step}")
                result = self.executor.execute(step)
                results.append(result)
                print(f"    结果：{result}")
            
            return results
    
    # 模拟Planner
    class MockPlanner:
        def plan(self, task):
            return [
                "搜索Python相关资料",
                "整理资料，列出大纲",
                "撰写文章",
                "检查并修改",
                "发布到博客"
            ]
    
    # 模拟Executor
    class MockExecutor:
        def execute(self, step):
            return f"完成：{step[:10]}..."
    
    # 运行
    agent = PlanExecuteAgent(MockPlanner(), MockExecutor())
    agent.run("帮我写一篇Python入门文章并发布")


def demo_when_to_use():
    """使用场景"""
    print("\n" + "=" * 60)
    print("何时使用Plan-and-Execute")
    print("=" * 60)
    
    print("""
✅ 适合使用Plan-and-Execute的场景：

1. 复杂多步骤任务
   - 撰写长文章
   - 项目开发流程
   - 数据分析报告

2. 需要有序执行
   - 订单处理流程
   - 审批流程

3. 任务分解明确
   - 旅行规划
   - 活动策划

❌ 不太适合的场景：

1. 需要灵活应变
   - 客服对话
   - 即时问答

2. 简单任务
   - 单一查询
   - 简单计算

3. 信息不完整
   - 需要探索的任务
   - 目标不明确的任务
""")


if __name__ == "__main__":
    demo_react_vs_plan_execute()
    demo_plan_execute_implementation()
    demo_when_to_use()
    
    print("\n" + "=" * 60)
    print("✅ Plan-and-Execute学习完成！")
    print("\n记住：")
    print("  • ReAct：边想边做，灵活")
    print("  • Plan-Execute：先规划后执行，有条理")
    print("  • 复杂任务用Plan-Execute更靠谱")

