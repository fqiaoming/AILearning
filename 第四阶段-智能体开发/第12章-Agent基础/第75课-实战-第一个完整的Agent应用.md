![Agent架构设计](./images/agent.svg)
*图：Agent架构设计*

# 第75课：实战-第一个完整的Agent应用

> **本课目标**：构建一个生产级的完整Agent应用
> 
> **核心技能**：完整实现、错误处理、日志监控、用户交互
> 
> **实战案例**：智能个人助手Agent
> 
> **学习时长**：90分钟

---

## 📖 口播文案（5分钟）
![Action](./images/action.svg)
*图：Action*


### 🎯 前言

"前面四节课我们学习了Agent的理论和架构。

今天，我们要把所有知识整合起来，**使用LangChain 1.0构建第一个完整的生产级Agent应用！**

**LangChain 1.0的Agent开发优势：**

不到10行代码即可创建Agent：
```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})
```

**核心特性：**
- ✅ 基于LangGraph：持久化执行、流式输出、人机交互
- ✅ 简化的API：不再需要手动创建ReAct循环
- ✅ 标准化接口：统一的模型和工具调用方式
- ✅ 生产就绪：1.0稳定版本

**什么是完整的Agent？**

不是玩具Demo，而是：
- ✅ 功能完整
- ✅ 错误处理健壮
- ✅ 有日志监控
- ✅ 用户体验好
- ✅ 可以实际使用

**我们要构建什么？**

**智能个人助手Agent**

功能：
1. 📅 日程管理
2. 🌤️ 天气查询
3. 🔍 信息搜索
4. 🧮 计算器
5. 📝 笔记记录
6. 💰 汇率转换

**核心特性：**

**1. 多工具支持**
```
集成6个工具
可扩展
统一管理
```

**2. 智能对话**
```
理解自然语言
上下文记忆
多轮对话
```

**3. 错误处理**
```
工具调用失败→重试
参数错误→提示
超时→降级
```

**4. 日志监控**
```
记录每次调用
性能统计
错误追踪
```

**5. 用户体验**
```
清晰的反馈
进度提示
友好的错误信息
```

**实际使用场景：**

**场景1：日程+天气**
```
用户："明天早上9点我有个会议，
      帮我查一下明天的天气，
      如果下雨提醒我带伞"

Agent执行：
1. Thought: 需要添加日程并查天气
2. Action: add_calendar(明天9点, 会议)
3. Observation: 日程已添加
4. Thought: 现在查天气
5. Action: get_weather(明天)
6. Observation: 明天有雨
7. Answer: 
   "已为您添加明天9点的会议。
    明天会下雨，记得带伞哦！"

✅ 完美完成！
```

**场景2：搜索+笔记**
```
用户："帮我搜索Python装饰器的用法，
      然后把重点记录下来"

Agent执行：
1. 搜索装饰器用法
2. 总结重点
3. 保存到笔记
4. 返回总结

✅ 自动化学习助手！
```

**场景3：计算+汇率**
```
用户："我要买一个1000美元的东西，
      换算成人民币是多少？
      加上15%的税是多少？"

Agent执行：
1. 查询汇率
2. 计算换算
3. 计算税费
4. 返回结果

✅ 购物好帮手！
```

**今天要实现的完整系统架构：**

```
┌─────────────────────────────────────┐
│         用户交互层                   │
│  • CLI界面                          │
│  • 对话历史                         │
│  • 格式化输出                       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│         Agent核心层                  │
│  • ReAct循环                        │
│  • 对话管理                         │
│  • 状态管理                         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│         工具管理层                   │
│  • 工具注册                         │
│  • 工具调用                         │
│  • 错误处理                         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│         工具实现层                   │
│  • 天气API                          │
│  • 日程管理                         │
│  • 搜索引擎                         │
│  • 计算器                           │
│  • 笔记系统                         │
│  • 汇率查询                         │
└─────────────────────────────────────┘
```

**今天这一课，我要带你：**

**第一部分：工具实现**
- 6个实用工具
- 统一接口
- 错误处理

**第二部分：Agent核心**
- ReAct实现
- 记忆管理
- 状态追踪

**第三部分：用户交互**
- CLI界面
- 对话流程
- 友好提示

**第四部分：日志监控**
- 调用日志
- 性能统计
- 错误追踪

**第五部分：完整集成**
- 系统组装
- 测试运行
- 优化改进

学完这一课，你将拥有一个可用的Agent应用！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【生产级vs玩具级】

玩具级：
• 核心功能能跑
• 没有错误处理
• 没有日志
• 用户体验差

生产级：
• 功能完善
• 健壮的错误处理
• 完整的日志
• 良好的用户体验

今天我们要做生产级！
```

---

## 📚 第一部分：工具实现

### 完整的工具集

```python
from typing import Dict, Any, Callable
from datetime import datetime, timedelta
import json
from dataclasses import dataclass

@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    result: Any = None
    error: str = None
    execution_time: float = 0

class Tool:
    """工具基类"""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Dict = None
    ):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}
    
    def run(self, **kwargs) -> ToolResult:
        """执行工具"""
        import time
        start_time = time.time()
        
        try:
            result = self.func(**kwargs)
            execution_time = time.time() - start_time
            
            return ToolResult(
                success=True,
                result=result,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            
            return ToolResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )

class PersonalAssistantTools:
    """个人助手工具集"""
    
    def __init__(self):
        # 模拟数据存储
        self.calendar = []
        self.notes = []
        
        # 注册所有工具
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Tool]:
        """注册所有工具"""
        
        tools = {}
        
        # 1. 天气查询
        tools['get_weather'] = Tool(
            name='get_weather',
            description='获取指定日期的天气信息，输入：日期(如"明天"、"2024-01-15")',
            func=self._get_weather
        )
        
        # 2. 日程管理
        tools['add_calendar'] = Tool(
            name='add_calendar',
            description='添加日程，输入：时间和事件描述',
            func=self._add_calendar
        )
        
        tools['list_calendar'] = Tool(
            name='list_calendar',
            description='查看日程列表',
            func=self._list_calendar
        )
        
        # 3. 搜索
        tools['search'] = Tool(
            name='search',
            description='搜索信息，输入：搜索关键词',
            func=self._search
        )
        
        # 4. 计算器
        tools['calculate'] = Tool(
            name='calculate',
            description='计算数学表达式，输入：数学表达式如"2+3*4"',
            func=self._calculate
        )
        
        # 5. 笔记
        tools['add_note'] = Tool(
            name='add_note',
            description='添加笔记，输入：笔记内容',
            func=self._add_note
        )
        
        tools['list_notes'] = Tool(
            name='list_notes',
            description='查看笔记列表',
            func=self._list_notes
        )
        
        # 6. 汇率转换
        tools['convert_currency'] = Tool(
            name='convert_currency',
            description='货币转换，输入：金额、源货币、目标货币',
            func=self._convert_currency
        )
        
        return tools
    
    # ===== 工具实现 =====
    
    def _get_weather(self, date: str = "今天") -> str:
        """获取天气（模拟）"""
        weather_data = {
            '今天': '晴，20-28℃',
            '明天': '多云转雨，18-25℃，降水概率70%',
            '后天': '雨，15-22℃'
        }
        return weather_data.get(date, '晴，20-25℃')
    
    def _add_calendar(self, time: str, event: str) -> str:
        """添加日程"""
        self.calendar.append({
            'time': time,
            'event': event,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return f"已添加日程：{time} - {event}"
    
    def _list_calendar(self) -> str:
        """查看日程"""
        if not self.calendar:
            return "暂无日程"
        
        result = "您的日程：\n"
        for i, item in enumerate(self.calendar, 1):
            result += f"{i}. {item['time']} - {item['event']}\n"
        return result
    
    def _search(self, query: str) -> str:
        """搜索（模拟）"""
        # 实际应用中这里会调用真实的搜索API
        return f"关于'{query}'的搜索结果：\n1. 相关文档1\n2. 相关文档2\n3. 相关文档3"
    
    def _calculate(self, expression: str) -> str:
        """计算器"""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            raise ValueError(f"计算错误：{str(e)}")
    
    def _add_note(self, content: str) -> str:
        """添加笔记"""
        self.notes.append({
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return f"已保存笔记：{content[:50]}..."
    
    def _list_notes(self) -> str:
        """查看笔记"""
        if not self.notes:
            return "暂无笔记"
        
        result = "您的笔记：\n"
        for i, note in enumerate(self.notes, 1):
            result += f"{i}. {note['content'][:50]}... ({note['created_at']})\n"
        return result
    
    def _convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> str:
        """汇率转换（模拟）"""
        # 模拟汇率
        rates = {
            'USD_CNY': 7.2,
            'CNY_USD': 1/7.2,
            'EUR_CNY': 7.8,
            'CNY_EUR': 1/7.8
        }
        
        rate_key = f"{from_currency}_{to_currency}"
        rate = rates.get(rate_key, 1.0)
        
        result = amount * rate
        return f"{amount} {from_currency} = {result:.2f} {to_currency}"
    
    def get_tools_description(self) -> str:
        """获取所有工具描述"""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)
```

---

## 💻 第二部分：完整Agent实现

```python
import logging
from typing import List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

class PersonalAssistantAgent:
    """个人助手Agent - 完整实现"""
    
    def __init__(
        self,
        llm,
        max_iterations: int = 10,
        enable_logging: bool = True
    ):
        self.llm = llm
        self.max_iterations = max_iterations
        self.enable_logging = enable_logging
        
        # 初始化工具
        self.tool_manager = PersonalAssistantTools()
        
        # 对话历史
        self.conversation_history = []
        
        # 统计信息
        self.stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'total_tool_calls': 0,
            'tool_call_stats': {}
        }
        
        # Logger
        self.logger = logging.getLogger(__name__)
        if enable_logging:
            self.logger.info("PersonalAssistantAgent initialized")
    
    def run(self, user_input: str, verbose: bool = True) -> str:
        """处理用户输入"""
        
        self.stats['total_queries'] += 1
        
        if verbose:
            print("\n" + "🤖"*30)
            print(f"用户: {user_input}")
            print("🤖"*30 + "\n")
        
        if self.enable_logging:
            self.logger.info(f"User query: {user_input}")
        
        # 添加到对话历史
        self.conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        
        try:
            # ReAct循环
            answer = self._react_loop(user_input, verbose)
            
            # 添加到对话历史
            self.conversation_history.append({
                'role': 'assistant',
                'content': answer
            })
            
            self.stats['successful_queries'] += 1
            
            if verbose:
                print(f"\n✅ Agent: {answer}\n")
            
            return answer
            
        except Exception as e:
            self.stats['failed_queries'] += 1
            
            error_msg = f"抱歉，处理您的请求时出错了：{str(e)}"
            
            if self.enable_logging:
                self.logger.error(f"Error processing query: {str(e)}", exc_info=True)
            
            if verbose:
                print(f"\n❌ {error_msg}\n")
            
            return error_msg
    
    def _react_loop(self, user_input: str, verbose: bool) -> str:
        """ReAct执行循环"""
        
        thought_action_history = []
        
        for iteration in range(self.max_iterations):
            if verbose:
                print(f"--- 迭代 {iteration + 1} ---")
            
            # 生成下一步
            next_step = self._generate_next_step(
                user_input,
                thought_action_history,
                verbose
            )
            
            # 检查是否完成
            if next_step['type'] == 'answer':
                return next_step['content']
            
            # 执行Action
            thought = next_step['thought']
            action = next_step['action']
            action_input = next_step['action_input']
            
            if verbose:
                print(f"💭 Thought: {thought}")
                print(f"🔧 Action: {action}({action_input})")
            
            # 调用工具
            observation = self._execute_tool(
                action,
                action_input,
                verbose
            )
            
            if verbose:
                print(f"👁️  Observation: {observation}\n")
            
            # 记录历史
            thought_action_history.append({
                'thought': thought,
                'action': action,
                'action_input': action_input,
                'observation': observation
            })
        
        # 超过最大迭代次数
        return "抱歉，任务太复杂了，我无法在限定步骤内完成。"
    
    def _generate_next_step(
        self,
        user_input: str,
        history: List[Dict],
        verbose: bool
    ) -> Dict:
        """生成下一步行动"""
        
        # 构建Prompt
        tools_desc = self.tool_manager.get_tools_description()
        
        # 格式化历史
        history_text = ""
        for item in history:
            history_text += f"Thought: {item['thought']}\n"
            history_text += f"Action: {item['action']}({item['action_input']})\n"
            history_text += f"Observation: {item['observation']}\n\n"
        
        # 获取对话历史（最近5轮）
        recent_conv = self.conversation_history[-10:]
        conv_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in recent_conv
        ])
        
        prompt = f"""你是一个智能个人助手，使用ReAct框架处理用户请求。

可用工具：
{tools_desc}

最近对话：
{conv_text}

当前任务：{user_input}

已执行步骤：
{history_text}

请继续：
1. 如果还没完成任务，输出：
   Thought: <你的思考>
   Action: <工具名称>
   Action Input: <工具输入>

2. 如果已完成任务，输出：
   Thought: <总结>
   Answer: <最终答案>

你的回复："""
        
        response = self.llm.invoke(prompt)
        
        # 解析输出
        return self._parse_output(response.content)
    
    def _parse_output(self, content: str) -> Dict:
        """解析LLM输出"""
        
        lines = content.strip().split('\n')
        result = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('Thought:'):
                result['thought'] = line.replace('Thought:', '').strip()
            elif line.startswith('Action:'):
                result['action'] = line.replace('Action:', '').strip()
            elif line.startswith('Action Input:'):
                result['action_input'] = line.replace('Action Input:', '').strip()
            elif line.startswith('Answer:'):
                result['type'] = 'answer'
                result['content'] = line.replace('Answer:', '').strip()
                return result
        
        result['type'] = 'action'
        return result
    
    def _execute_tool(
        self,
        tool_name: str,
        tool_input: str,
        verbose: bool
    ) -> str:
        """执行工具"""
        
        self.stats['total_tool_calls'] += 1
        self.stats['tool_call_stats'][tool_name] = \
            self.stats['tool_call_stats'].get(tool_name, 0) + 1
        
        if self.enable_logging:
            self.logger.info(f"Calling tool: {tool_name}({tool_input})")
        
        # 获取工具
        tool = self.tool_manager.tools.get(tool_name)
        
        if not tool:
            error = f"工具 {tool_name} 不存在"
            if self.enable_logging:
                self.logger.error(error)
            return error
        
        # 执行工具
        try:
            # 解析输入参数
            if ',' in tool_input:
                # 多个参数
                params = [p.strip() for p in tool_input.split(',')]
                result = tool.run(*params)
            else:
                # 单个参数
                result = tool.run(tool_input)
            
            if result.success:
                if self.enable_logging:
                    self.logger.info(f"Tool call successful: {tool_name}, time={result.execution_time:.2f}s")
                return str(result.result)
            else:
                if self.enable_logging:
                    self.logger.error(f"Tool call failed: {tool_name}, error={result.error}")
                return f"错误：{result.error}"
                
        except Exception as e:
            error = f"工具执行失败：{str(e)}"
            if self.enable_logging:
                self.logger.error(error, exc_info=True)
            return error
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*60)
        print("Agent统计信息")
        print("="*60)
        print(f"总查询数: {self.stats['total_queries']}")
        print(f"成功: {self.stats['successful_queries']}")
        print(f"失败: {self.stats['failed_queries']}")
        print(f"成功率: {self.stats['successful_queries']/self.stats['total_queries']:.1%}")
        print(f"\n工具调用统计:")
        print(f"总调用次数: {self.stats['total_tool_calls']}")
        for tool, count in self.stats['tool_call_stats'].items():
            print(f"  {tool}: {count}次")
        print("="*60)
```

---

## 🎯 第三部分：完整运行Demo

```python
def main():
    """主程序"""
    
    from langchain.chat_models import ChatOpenAI
    
    # 初始化LLM
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    # 创建Agent
    agent = PersonalAssistantAgent(llm, enable_logging=True)
    
    print("="*60)
    print("智能个人助手Agent v1.0")
    print("="*60)
    print("\n可用功能:")
    print("  • 天气查询")
    print("  • 日程管理")
    print("  • 信息搜索")
    print("  • 计算器")
    print("  • 笔记记录")
    print("  • 汇率转换")
    print("\n输入 'quit' 或 'exit' 退出")
    print("输入 'stats' 查看统计信息")
    print("="*60 + "\n")
    
    # 交互循环
    while True:
        try:
            user_input = input("你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n再见！👋")
                agent.print_stats()
                break
            
            if user_input.lower() == 'stats':
                agent.print_stats()
                continue
            
            # 处理请求
            response = agent.run(user_input, verbose=True)
            
        except KeyboardInterrupt:
            print("\n\n再见！👋")
            agent.print_stats()
            break
        except Exception as e:
            print(f"\n错误：{str(e)}\n")

# 测试场景
def demo_scenarios():
    """演示不同场景"""
    
    from langchain.chat_models import ChatOpenAI
    
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0
    )
    
    agent = PersonalAssistantAgent(llm)
    
    # 测试场景
    scenarios = [
        "明天的天气怎么样？",
        "帮我添加一个明天下午3点的会议",
        "100美元等于多少人民币？",
        "计算 (123 + 456) * 2",
        "帮我搜索Python装饰器的用法，然后记录到笔记"
    ]
    
    for scenario in scenarios:
        print("\n" + "="*70)
        response = agent.run(scenario, verbose=True)
        print("="*70)
    
    # 显示统计
    agent.print_stats()

# 运行演示
# demo_scenarios()

if __name__ == "__main__":
    # main()  # 交互模式
    demo_scenarios()  # 演示模式
```

---

## 📝 课后练习

### 练习1：添加更多工具
实现邮件发送、文件操作等工具

### 练习2：Web界面
使用Flask/FastAPI构建Web界面

### 练习3：语音交互
集成语音识别和TTS

---

## 🎓 知识总结

### 第12章完整回顾

通过5节课，我们完整学习了Agent基础：

1. **第71课：Agent概念**
   - 从对话到行动
   - Agent vs ChatBot
   - 应用场景

2. **第72课：核心组件**
   - Planning规划
   - Memory记忆
   - Tools工具
   - Action执行

3. **第73课：ReAct框架**
   - 思考-行动循环
   - 执行轨迹
   - 完整实现

4. **第74课：架构模式**
   - ReAct
   - Plan-and-Execute
   - ReWOO
   - Reflexion

5. **第75课：完整应用**
   - 生产级实现
   - 工具集成
   - 日志监控

### 核心能力

✅ 理解Agent本质
✅ 掌握核心组件
✅ 熟练ReAct框架
✅ 了解多种架构
✅ 构建完整应用

---

## 🎉 第12章完成！

恭喜！你已经掌握了Agent开发的基础知识！

---

## 🚀 下一章预告

**第13章：Tool Calling工具开发（7课）**

- Tool Calling原理
- Function Calling深入
- 内置工具使用
- 自定义工具开发
- API调用封装
- 数据库操作
- 多工具Agent实战

**深入工具开发！** 🛠️

---

**💪 恭喜完成第12章！你已经可以构建Agent应用了！**

**下一章见！** 🎉
