![Agent进阶架构](./images/agent.svg)
*图：Agent进阶架构*

# 第85课：Multi-Agent协作架构

> **本课目标**：掌握多Agent协作系统的设计与实现
> 
> **核心技能**：Agent通信、任务分配、协作模式、冲突解决
> 
> **实战案例**：构建Multi-Agent协作系统
> 
> **学习时长**：95分钟

---

## 📖 口播文案（6分钟）
![Agent Debug](./images/agent_debug.svg)
*图：Agent Debug*


### 🎯 前言

"前面两节课我们学习了Agent的调试和优化。

今天我们要学习更高级的话题：**Multi-Agent协作！**

**什么是Multi-Agent？**

**单Agent：**
```
一个Agent处理所有任务
就像：一个人做所有事情

优点：简单
缺点：能力有限、效率低
```

**Multi-Agent：**
```
多个Agent分工合作
就像：一个团队各司其职

优点：专业化、高效率、可扩展
缺点：需要协调
```

**为什么需要Multi-Agent？**

**原因1：复杂任务需要专业化**
```
任务："开发一个网站"

单Agent：
❌ 需要懂设计、开发、测试、运维...
   样样都会但样样不精

Multi-Agent：
✅ 设计Agent：专注UI/UX
✅ 开发Agent：专注编码
✅ 测试Agent：专注质量
✅ 运维Agent：专注部署

各司其职，专业高效！
```

**原因2：提升处理能力**
```
任务："处理1000个客户咨询"

单Agent：
• 串行处理
• 需要1000秒

Multi-Agent（10个）：
• 并行处理
• 只需100秒

效率提升10倍！⚡
```

**原因3：容错与备份**
```
单Agent：
Agent1挂了 → 系统停止 ❌

Multi-Agent：
Agent1挂了 → Agent2接管 ✅
高可用性！
```

**Multi-Agent的核心挑战：**

**挑战1：如何通信？**
```
问题：
Agent A要给Agent B传递信息
怎么传？用什么格式？

解决方案：
• 消息队列
• 统一消息格式
• 异步通信
```

**挑战2：如何分配任务？**
```
问题：
有10个任务，3个Agent
谁做什么？

策略：
• 负载均衡：平均分配
• 能力匹配：专长分配
• 优先级排序：重要的先做
```

**挑战3：如何协调冲突？**
```
问题：
Agent A说："用方案1"
Agent B说："用方案2"
听谁的？

解决方案：
• 投票机制
• 权威Agent决策
• 共识算法
```

**Multi-Agent的4种协作模式：**

**模式1：流水线模式（Pipeline）**
```
Agent A → Agent B → Agent C

就像工厂流水线：
• 数据收集Agent → 数据分析Agent → 报告生成Agent

优点：
• 职责清晰
• 易于理解

适用：
• 顺序处理任务
```

**模式2：分层模式（Hierarchical）**
```
       Manager Agent
      /       |       \
Agent A   Agent B   Agent C

就像公司组织架构：
• Manager分配任务
• Worker执行任务

优点：
• 集中管理
• 易于控制

适用：
• 复杂项目管理
```

**模式3：对等模式（Peer-to-Peer）**
```
Agent A ←→ Agent B
    ↓  ×    ↓
Agent C ←→ Agent D

所有Agent地位平等：
• 自主决策
• 相互协作

优点：
• 灵活
• 去中心化

适用：
• 分布式系统
```

**模式4：竞争模式（Competitive）**
```
Task → Agent A
    → Agent B
    → Agent C

多个Agent同时处理，选最好的结果

优点：
• 质量高
• 容错强

适用：
• 关键决策
• 创意生成
```

**真实Multi-Agent案例：**

**案例：智能客服系统**

```
【系统架构】

用户
 ↓
Router Agent（路由）
 ├→ 技术支持Agent
 ├→ 销售咨询Agent
 ├→ 售后服务Agent
 └→ 投诉处理Agent

【工作流程】

Step 1: 用户提问
"我的订单怎么还没到？"

Step 2: Router分析
类别：售后服务
→ 转给售后Agent

Step 3: 售后Agent处理
• 查询订单状态
• 联系物流
• 回复用户

Step 4: 如果需要升级
→ 转给Manager Agent

完美的分工协作！✨
```

**另一个案例：内容创作系统**

```
【架构】

Topic Generator Agent（选题）
      ↓
Research Agent（调研）
      ↓
Writing Agent（写作）
      ↓
Editor Agent（编辑）
      ↓
SEO Agent（优化）

【优势】

每个Agent专注自己擅长的：
• 选题Agent：懂热点
• 调研Agent：会搜索
• 写作Agent：文笔好
• 编辑Agent：抓错误
• SEO Agent：懂优化

结果：高质量内容！
```

**Multi-Agent通信协议：**

```json
{
  "message_id": "msg_001",
  "from": "agent_a",
  "to": "agent_b",
  "type": "request",
  "content": {
    "task": "analyze_data",
    "data": {...}
  },
  "timestamp": "2024-11-15T10:00:00"
}
```

**今天这一课，我要带你：**

**第一部分：Multi-Agent架构**
- 系统设计
- 通信机制
- 消息协议

**第二部分：任务分配策略**
- 负载均衡
- 能力匹配
- 优先级调度

**第三部分：协作模式实现**
- Pipeline模式
- Hierarchical模式
- P2P模式

**第四部分：冲突解决**
- 投票机制
- 共识算法
- 仲裁系统

**第五部分：完整实战**
- 智能客服系统
- 协作框架
- 最佳实践

学完这一课，你将能构建Multi-Agent系统！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【Multi-Agent = 团队协作】

不是：
• 多个独立的Agent
• 各自为战

而是：
• 有共同目标
• 相互配合
• 协调一致

【好的Multi-Agent系统特征】

1. 清晰的职责分工
2. 高效的通信机制
3. 智能的任务分配
4. 完善的冲突解决
```

---

## 📚 第一部分：Multi-Agent基础架构

### 一、Agent基类和消息系统

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime
import asyncio
from queue import Queue
import json

class MessageType(Enum):
    """消息类型"""
    REQUEST = "request"      # 请求
    RESPONSE = "response"    # 响应
    NOTIFICATION = "notification"  # 通知
    BROADCAST = "broadcast"  # 广播

@dataclass
class Message:
    """Agent间消息"""
    
    message_id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime
    reply_to: Optional[str] = None
    
    @classmethod
    def create(
        cls,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        content: Dict
    ):
        """创建消息"""
        return cls(
            message_id=str(uuid.uuid4()),
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            timestamp=datetime.now()
        )
    
    def to_dict(self) -> Dict:
        """转为字典"""
        return {
            "message_id": self.message_id,
            "from": self.from_agent,
            "to": self.to_agent,
            "type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "reply_to": self.reply_to
        }

class MessageBus:
    """消息总线（Agent通信中心）"""
    
    def __init__(self):
        # Agent的消息队列
        self.agent_queues: Dict[str, Queue] = {}
        
        # 消息历史
        self.message_history: List[Message] = []
        
        # 订阅关系
        self.subscriptions: Dict[str, List[str]] = {}
    
    def register_agent(self, agent_id: str):
        """注册Agent"""
        if agent_id not in self.agent_queues:
            self.agent_queues[agent_id] = Queue()
    
    def send_message(self, message: Message):
        """发送消息"""
        
        # 记录历史
        self.message_history.append(message)
        
        # 广播消息
        if message.message_type == MessageType.BROADCAST:
            for agent_id in self.agent_queues:
                if agent_id != message.from_agent:
                    self.agent_queues[agent_id].put(message)
        
        # 单播消息
        elif message.to_agent in self.agent_queues:
            self.agent_queues[message.to_agent].put(message)
        else:
            print(f"警告：Agent {message.to_agent} 不存在")
    
    def receive_message(self, agent_id: str, timeout: float = 1.0) -> Optional[Message]:
        """接收消息"""
        
        if agent_id not in self.agent_queues:
            return None
        
        try:
            queue = self.agent_queues[agent_id]
            message = queue.get(timeout=timeout)
            return message
        except:
            return None
    
    def get_message_history(self, agent_id: Optional[str] = None) -> List[Message]:
        """获取消息历史"""
        
        if agent_id is None:
            return self.message_history
        
        return [
            msg for msg in self.message_history
            if msg.from_agent == agent_id or msg.to_agent == agent_id
        ]

class BaseAgent:
    """Agent基类"""
    
    def __init__(
        self,
        agent_id: str,
        message_bus: MessageBus,
        capabilities: List[str] = None
    ):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.capabilities = capabilities or []
        
        # 注册到消息总线
        self.message_bus.register_agent(agent_id)
        
        # 运行状态
        self.running = False
    
    def send_request(
        self,
        to_agent: str,
        task: str,
        data: Dict = None
    ) -> str:
        """发送请求"""
        
        message = Message.create(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=MessageType.REQUEST,
            content={
                "task": task,
                "data": data or {}
            }
        )
        
        self.message_bus.send_message(message)
        return message.message_id
    
    def send_response(
        self,
        to_agent: str,
        result: Any,
        reply_to: str
    ):
        """发送响应"""
        
        message = Message.create(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=MessageType.RESPONSE,
            content={"result": result}
        )
        message.reply_to = reply_to
        
        self.message_bus.send_message(message)
    
    def broadcast(self, content: Dict):
        """广播消息"""
        
        message = Message.create(
            from_agent=self.agent_id,
            to_agent="all",
            message_type=MessageType.BROADCAST,
            content=content
        )
        
        self.message_bus.send_message(message)
    
    def handle_message(self, message: Message):
        """处理消息（子类实现）"""
        pass
    
    async def run(self):
        """运行Agent"""
        
        self.running = True
        
        while self.running:
            # 接收消息
            message = self.message_bus.receive_message(self.agent_id)
            
            if message:
                try:
                    self.handle_message(message)
                except Exception as e:
                    print(f"Agent {self.agent_id} 处理消息失败: {e}")
            
            await asyncio.sleep(0.1)
    
    def stop(self):
        """停止Agent"""
        self.running = False
```

---

## 💻 第二部分：任务分配策略

### 一、智能任务分配器

```python
from typing import List, Tuple
import heapq

class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Task:
    """任务"""
    task_id: str
    task_type: str
    priority: TaskPriority
    data: Dict
    created_at: datetime
    
    def __lt__(self, other):
        # 用于优先队列排序
        return self.priority.value > other.priority.value

class TaskDispatcher:
    """任务分配器"""
    
    def __init__(self):
        # 任务队列（优先队列）
        self.task_queue: List[Task] = []
        
        # Agent能力表
        self.agent_capabilities: Dict[str, List[str]] = {}
        
        # Agent负载
        self.agent_loads: Dict[str, int] = {}
    
    def register_agent(self, agent_id: str, capabilities: List[str]):
        """注册Agent及其能力"""
        self.agent_capabilities[agent_id] = capabilities
        self.agent_loads[agent_id] = 0
    
    def add_task(self, task: Task):
        """添加任务"""
        heapq.heappush(self.task_queue, task)
    
    def assign_task(self) -> Optional[Tuple[str, Task]]:
        """
        分配任务
        
        策略：
        1. 能力匹配：选择有相应能力的Agent
        2. 负载均衡：选择负载最低的Agent
        3. 优先级：高优先级任务优先
        
        Returns:
            (agent_id, task) 或 None
        """
        
        if not self.task_queue:
            return None
        
        # 获取最高优先级任务
        task = heapq.heappop(self.task_queue)
        
        # 找到有能力处理的Agent
        capable_agents = [
            agent_id
            for agent_id, capabilities in self.agent_capabilities.items()
            if task.task_type in capabilities
        ]
        
        if not capable_agents:
            print(f"警告：没有Agent能处理任务 {task.task_type}")
            return None
        
        # 选择负载最低的Agent
        selected_agent = min(
            capable_agents,
            key=lambda a: self.agent_loads[a]
        )
        
        # 更新负载
        self.agent_loads[selected_agent] += 1
        
        return (selected_agent, task)
    
    def complete_task(self, agent_id: str):
        """任务完成，减少负载"""
        if agent_id in self.agent_loads:
            self.agent_loads[agent_id] = max(0, self.agent_loads[agent_id] - 1)
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "pending_tasks": len(self.task_queue),
            "agent_loads": self.agent_loads.copy(),
            "total_agents": len(self.agent_capabilities)
        }

# 演示
def demo_task_dispatcher():
    """演示任务分配"""
    
    print("="*60)
    print("任务分配器演示")
    print("="*60)
    
    dispatcher = TaskDispatcher()
    
    # 注册Agent
    dispatcher.register_agent("agent_1", ["search", "analyze"])
    dispatcher.register_agent("agent_2", ["search", "write"])
    dispatcher.register_agent("agent_3", ["analyze", "visualize"])
    
    # 添加任务
    tasks = [
        Task("t1", "search", TaskPriority.HIGH, {}, datetime.now()),
        Task("t2", "analyze", TaskPriority.URGENT, {}, datetime.now()),
        Task("t3", "search", TaskPriority.MEDIUM, {}, datetime.now()),
        Task("t4", "write", TaskPriority.LOW, {}, datetime.now()),
        Task("t5", "analyze", TaskPriority.HIGH, {}, datetime.now()),
    ]
    
    for task in tasks:
        dispatcher.add_task(task)
    
    print("\n任务分配结果：")
    print("-"*60)
    
    # 分配所有任务
    assignments = []
    while True:
        assignment = dispatcher.assign_task()
        if assignment is None:
            break
        
        agent_id, task = assignment
        assignments.append((agent_id, task))
        
        print(f"任务 {task.task_id} ({task.task_type}, {task.priority.name})")
        print(f"  → 分配给 {agent_id}")
    
    # 显示统计
    print("\n" + "-"*60)
    print("统计信息：")
    stats = dispatcher.get_statistics()
    print(f"  待处理任务: {stats['pending_tasks']}")
    print(f"  Agent负载: {stats['agent_loads']}")

demo_task_dispatcher()
```

---

## 🎯 第三部分：协作模式实现

### 一、Pipeline流水线模式

```python
class PipelineAgent(BaseAgent):
    """流水线Agent"""
    
    def __init__(
        self,
        agent_id: str,
        message_bus: MessageBus,
        next_agent: Optional[str] = None,
        process_func: callable = None
    ):
        super().__init__(agent_id, message_bus)
        self.next_agent = next_agent
        self.process_func = process_func or self.default_process
    
    def default_process(self, data: Dict) -> Dict:
        """默认处理函数"""
        return data
    
    def handle_message(self, message: Message):
        """处理消息"""
        
        if message.message_type == MessageType.REQUEST:
            # 处理数据
            data = message.content.get("data", {})
            
            print(f"[{self.agent_id}] 处理数据...")
            processed_data = self.process_func(data)
            
            # 传递给下一个Agent
            if self.next_agent:
                self.send_request(
                    to_agent=self.next_agent,
                    task="process",
                    data=processed_data
                )
            else:
                # 最后一个Agent，发送最终结果
                print(f"[{self.agent_id}] 流水线完成")
                print(f"最终结果: {processed_data}")

# 演示Pipeline模式
def demo_pipeline():
    """演示流水线模式"""
    
    print("\n" + "="*60)
    print("Pipeline流水线模式演示")
    print("="*60)
    
    message_bus = MessageBus()
    
    # 创建流水线：数据收集 → 数据清洗 → 数据分析
    
    def collect_data(data):
        data['collected'] = True
        return data
    
    def clean_data(data):
        data['cleaned'] = True
        return data
    
    def analyze_data(data):
        data['analyzed'] = True
        return data
    
    # 创建Agent
    collector = PipelineAgent(
        "collector",
        message_bus,
        next_agent="cleaner",
        process_func=collect_data
    )
    
    cleaner = PipelineAgent(
        "cleaner",
        message_bus,
        next_agent="analyzer",
        process_func=clean_data
    )
    
    analyzer = PipelineAgent(
        "analyzer",
        message_bus,
        next_agent=None,  # 最后一个
        process_func=analyze_data
    )
    
    # 启动流水线
    print("\n启动流水线...")
    collector.send_request(
        to_agent="collector",
        task="process",
        data={"source": "sensor_1"}
    )
    
    # 模拟消息处理
    for _ in range(3):
        for agent in [collector, cleaner, analyzer]:
            msg = message_bus.receive_message(agent.agent_id, timeout=0.1)
            if msg:
                agent.handle_message(msg)

demo_pipeline()
```

---

## 📝 课后练习

### 练习1：实现Hierarchical模式
创建Manager-Worker层级结构

### 练习2：实现共识算法
多Agent投票决策机制

### 练习3：分布式Multi-Agent
跨服务器的Multi-Agent系统

---

## 🎓 知识总结

### 核心要点

1. **Multi-Agent架构**
   - 消息总线
   - Agent基类
   - 通信协议

2. **任务分配**
   - 能力匹配
   - 负载均衡
   - 优先级调度

3. **协作模式**
   - Pipeline流水线
   - Hierarchical层级
   - P2P对等
   - Competitive竞争

4. **关键挑战**
   - Agent通信
   - 任务协调
   - 冲突解决
   - 性能优化

---

## 🚀 下节预告

下一课：**第86课：Agent安全性与权限控制**

- 权限系统
- 访问控制
- 安全审计
- 防护机制

**保障Agent系统安全！** 🔒

---

**💪 记住：Multi-Agent的关键是协作，不是竞争！**

**下一课见！** 🎉
