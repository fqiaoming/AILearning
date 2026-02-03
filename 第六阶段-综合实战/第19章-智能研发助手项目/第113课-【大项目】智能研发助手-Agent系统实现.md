![智能研发助手架构](./images/project.svg)
*图：智能研发助手架构*

# 第113课：【大项目】智能研发助手-Agent系统实现

> **本课目标**：实现企业级智能Agent任务执行系统  
> 
> **核心技能**：Agent架构、工具开发、任务规划、完整实现
> 
> **学习时长**：120分钟

---

## 📖 口播文案（9分钟）
![Agent Impl](./images/agent_impl.svg)
*图：Agent Impl*


### 🎯 前言

"上节课我们实现了RAG文档知识库。

今天实现另一个核心：**Agent智能任务执行系统！**

**为什么需要Agent？**

```
RAG能回答问题，但不能执行任务！

场景1：查看Git日志
用户："最近3天有哪些提交？"
• RAG：告诉你Git命令怎么用 ❌
• Agent：直接执行git log并返回结果 ✅

场景2：数据库查询
用户："统计昨天的订单数量"
• RAG：告诉你SQL怎么写 ❌
• Agent：执行SQL查询并返回数据 ✅

场景3：代码分析
用户："UserService类有多少行代码？"
• RAG：提示你如何统计 ❌
• Agent：读取文件并统计返回 ✅

场景4：自动化任务
用户："帮我创建一个新分支feature/login"
• RAG：告诉你命令 ❌
• Agent：自动执行git checkout -b ✅

Agent能执行任务！这是核心区别！
```

**Agent的强大之处：**

```
1. 自主规划
   • 理解复杂任务
   • 分解成子任务
   • 按顺序执行

2. 工具调用
   • Git操作
   • 数据库查询
   • API调用
   • 文件操作
   • 代码分析

3. 多步骤执行
   • 步骤1：查询数据
   • 步骤2：分析结果
   • 步骤3：生成报告
   • 步骤4：发送通知

4. 错误处理
   • 执行失败自动重试
   • 切换备选方案
   • 报告详细错误

5. 安全控制
   • 权限检查
   • 危险操作确认
   • 操作审计日志
```

**今天要实现的Agent系统：**

```
┌─────────────────────────────────────────┐
│            Agent核心引擎                 │
├────────────┬────────────────────────────┤
│ Planning   │ 任务理解与规划              │
│ Memory     │ 上下文记忆                  │
│ Tools      │ 工具集管理                  │
│ Execution  │ 执行控制                    │
│ Safety     │ 安全检查                    │
└────────────┴────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│            工具集（Tools）               │
├───────────┬─────────────┬───────────────┤
│ Git工具   │ 数据库工具   │ 文件工具      │
│ ├─log    │ ├─query    │ ├─read        │
│ ├─status │ ├─insert   │ ├─write       │
│ ├─branch │ ├─update   │ ├─search      │
│ └─commit │ └─analyze  │ └─analyze     │
├───────────┼─────────────┼───────────────┤
│ API工具   │ 分析工具     │ 通知工具      │
│ ├─get    │ ├─代码统计  │ ├─email       │
│ ├─post   │ ├─依赖分析  │ ├─slack       │
│ └─auth   │ └─性能分析  │ └─webhook     │
└───────────┴─────────────┴───────────────┘
```

**Agent工作流程示例：**

```
【复杂任务】
用户："分析UserService类的代码质量并生成报告"

Step 1: 任务理解
• 需要找到UserService.java文件
• 需要分析代码质量
• 需要生成报告

Step 2: 规划
Plan:
1. 搜索UserService.java文件
2. 读取文件内容
3. 统计代码行数
4. 分析代码复杂度
5. 检查代码规范
6. 生成质量报告
7. 保存报告到文件

Step 3: 执行
Action 1: 使用FileSearchTool
• 输入：{"filename": "UserService.java"}
• 输出："/src/main/java/com/example/service/UserService.java"
• 状态：✓ 成功

Action 2: 使用FileReadTool
• 输入：{"path": "/src/.../UserService.java"}
• 输出：文件内容（450行）
• 状态：✓ 成功

Action 3: 使用CodeAnalysisTool
• 输入：{"code": "...", "metrics": ["loc", "complexity"]}
• 输出：{
    "total_lines": 450,
    "code_lines": 320,
    "comment_lines": 80,
    "blank_lines": 50,
    "complexity": 15,
    "methods": 18
  }
• 状态：✓ 成功

Action 4: 使用LLM分析
• 根据指标分析质量
• 生成改进建议

Action 5: 生成报告
• 结构化报告
• 保存为Markdown

Step 4: 返回结果
```
UserService类代码质量报告
==========================

基本信息：
• 文件路径：/src/main/java/com/example/service/UserService.java
• 总行数：450行
• 代码行：320行（71%）
• 注释行：80行（18%）
• 空白行：50行（11%）

质量指标：
• 代码复杂度：15（中等）
• 方法数量：18个
• 平均方法长度：18行
• 注释覆盖率：18%

评分：78/100（良好）

优点：
✓ 代码结构清晰
✓ 方法职责单一
✓ 命名规范

待改进：
• 建议增加注释（目标25%）
• 部分方法过长（>30行）
• 可以拆分复杂逻辑

改进建议：
1. 为公共方法添加JavaDoc
2. 拆分login()方法（42行）
3. 提取重复的验证逻辑
4. 增加单元测试覆盖

报告已保存：./reports/UserService_quality_report.md
```

执行完成！
```

**Agent架构设计：**

```
【ReAct架构】

Reason（推理）→ Act（行动）→ Observe（观察）→ Reason...

示例：
Thought 1: 我需要先找到UserService文件
Action 1: file_search("UserService.java")
Observation 1: 找到文件在/src/.../UserService.java

Thought 2: 现在读取文件内容
Action 2: file_read("/src/.../UserService.java")
Observation 2: 文件内容已读取，共450行

Thought 3: 使用代码分析工具分析
Action 3: code_analysis(content, metrics)
Observation 3: 分析完成，获得各项指标

Thought 4: 现在可以生成报告了
Action 4: generate_report(analysis_result)
Observation 4: 报告生成完成

Final Answer: [报告内容]
```

**工具设计原则：**

```
1. 单一职责
   • 每个工具做一件事
   • 功能清晰明确

2. 输入输出规范
   • JSON Schema定义
   • 类型严格校验
   • 错误详细描述

3. 幂等性
   • 相同输入相同输出
   • 避免副作用
   • 可安全重试

4. 安全性
   • 权限控制
   • 参数校验
   • 路径限制
   • SQL注入防护

5. 可观测性
   • 详细日志
   • 执行追踪
   • 性能监控
```

**安全控制：**

```
【权限分级】

Level 1：只读操作（无风险）
• 读取文件
• 查询数据库
• 查看Git日志
→ 自动执行

Level 2：修改操作（低风险）
• 创建分支
• 写入日志
• 发送通知
→ 自动执行 + 审计

Level 3：敏感操作（中风险）
• 修改代码
• 更新数据库
• Git提交
→ 需要确认

Level 4：危险操作（高风险）
• 删除文件
• 删除数据
• 强制推送
• 系统命令
→ 禁止 或 需要管理员确认

【黑名单机制】

禁止命令：
• rm -rf
• DROP DATABASE
• format C:
• sudo rm
• git push --force

【沙箱机制】

隔离环境：
• Docker容器执行
• 资源限制
• 网络隔离
• 超时控制
```

**今天这一课，我要带你：**

**第一部分：Agent核心引擎**
- ReAct循环实现
- 任务规划器
- Memory管理
- 执行控制器

**第二部分：工具集开发**
- Git工具集
- 数据库工具
- 文件操作工具
- 分析工具

**第三部分：安全机制**
- 权限控制
- 参数验证
- 操作审计
- 异常处理

**第四部分：完整集成**
- Agent + RAG集成
- 工具自动注册
- 监控日志
- 测试验证

让我们开始打造智能Agent！"

---

## 📚 第一部分：Agent核心引擎

### 一、ReAct Agent实现

```python
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json

class ActionStatus(Enum):
    """动作状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class Action:
    """Agent动作"""
    thought: str          # 推理过程
    tool_name: str       # 工具名称
    tool_input: Dict     # 工具输入
    observation: str = "" # 执行结果
    status: ActionStatus = ActionStatus.PENDING

class ReActAgent:
    """ReAct Agent核心引擎"""
    
    def __init__(self, llm, tools: List):
        """
        初始化
        
        Args:
            llm: 语言模型
            tools: 工具列表
        """
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.memory = []  # 执行历史
        self.max_iterations = 10  # 最大迭代次数
        
        print("="*60)
        print("ReAct Agent引擎")
        print("="*60)
        print(f"可用工具：{len(self.tools)}个")
        for tool_name in self.tools:
            print(f"  • {tool_name}")
    
    def run(self, task: str) -> str:
        """
        执行任务
        
        Args:
            task: 任务描述
        
        Returns:
            执行结果
        """
        
        print("\n" + "="*60)
        print("开始执行任务")
        print("="*60)
        print(f"任务：{task}\n")
        
        # 初始化
        self.memory = []
        iteration = 0
        
        # ReAct循环
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n【迭代 {iteration}】")
            
            # Step 1: Reason（推理）
            thought, tool_name, tool_input = self._reason(task)
            
            print(f"Thought: {thought}")
            print(f"Action: {tool_name}({json.dumps(tool_input, ensure_ascii=False)})")
            
            # 检查是否完成
            if tool_name == "finish":
                print(f"\n最终答案：{tool_input['answer']}")
                return tool_input['answer']
            
            # Step 2: Act（行动）
            observation = self._act(tool_name, tool_input)
            
            print(f"Observation: {observation[:200]}...")
            
            # Step 3: 记录历史
            action = Action(
                thought=thought,
                tool_name=tool_name,
                tool_input=tool_input,
                observation=observation,
                status=ActionStatus.SUCCESS
            )
            self.memory.append(action)
        
        return "达到最大迭代次数，任务未完成"
    
    def _reason(self, task: str) -> tuple:
        """
        推理下一步行动
        
        Args:
            task: 任务描述
        
        Returns:
            (thought, tool_name, tool_input)
        """
        
        # 构建Prompt
        prompt = self._build_prompt(task)
        
        # 调用LLM（这里简化，实际需要调用真实LLM）
        # response = self.llm.generate(prompt)
        
        # 解析响应（示例）
        thought = "我需要先搜索UserService文件"
        tool_name = "file_search"
        tool_input = {"filename": "UserService.java"}
        
        return thought, tool_name, tool_input
    
    def _act(self, tool_name: str, tool_input: Dict) -> str:
        """
        执行工具
        
        Args:
            tool_name: 工具名称
            tool_input: 工具输入
        
        Returns:
            执行结果
        """
        
        if tool_name not in self.tools:
            return f"错误：工具 {tool_name} 不存在"
        
        tool = self.tools[tool_name]
        
        try:
            result = tool.run(**tool_input)
            return str(result)
        except Exception as e:
            return f"执行失败：{str(e)}"
    
    def _build_prompt(self, task: str) -> str:
        """构建推理Prompt"""
        
        # 工具描述
        tools_desc = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        
        # 历史记录
        history = "\n".join([
            f"Thought: {action.thought}\n"
            f"Action: {action.tool_name}({action.tool_input})\n"
            f"Observation: {action.observation}"
            for action in self.memory
        ])
        
        prompt = f"""你是一个智能Agent，需要完成以下任务：

任务：{task}

可用工具：
{tools_desc}

执行历史：
{history}

请思考下一步应该做什么，按以下格式回答：
Thought: [你的推理过程]
Action: [工具名称]
Action Input: [JSON格式的输入参数]

如果任务已完成，使用finish工具：
Action: finish
Action Input: {{"answer": "最终答案"}}
"""
        
        return prompt
    
    def demonstrate_react_loop(self):
        """演示ReAct循环"""
        
        print("\n" + "="*60)
        print("ReAct循环演示")
        print("="*60)
        
        print("""
任务：分析UserService类的代码行数

【迭代1】
Thought: 我需要先找到UserService文件的位置
Action: file_search
Action Input: {"filename": "UserService.java"}
Observation: 找到文件：/src/main/java/com/example/service/UserService.java

【迭代2】
Thought: 现在我知道文件位置了，需要读取文件内容
Action: file_read
Action Input: {"path": "/src/main/java/.../UserService.java"}
Observation: 文件内容已读取，包含450行

【迭代3】
Thought: 我需要统计代码行数
Action: count_lines
Action Input: {"content": "[文件内容]"}
Observation: {
  "total_lines": 450,
  "code_lines": 320,
  "comment_lines": 80,
  "blank_lines": 50
}

【迭代4】
Thought: 我已经得到了所有需要的信息，可以给出答案了
Action: finish
Action Input: {
  "answer": "UserService类共有450行，其中代码320行，注释80行，空行50行"
}

任务完成！
        """)

# 演示
agent = ReActAgent(llm=None, tools=[])
agent.demonstrate_react_loop()
```

---

## 💻 第二部分：工具集开发

### 一、Git工具集

```python
import subprocess
from typing import Dict, List
import os

class BaseTool:
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        """初始化"""
        self.name = name
        self.description = description
    
    def run(self, **kwargs) -> str:
        """执行工具（子类实现）"""
        raise NotImplementedError

class GitLogTool(BaseTool):
    """Git日志查询工具"""
    
    def __init__(self):
        """初始化"""
        super().__init__(
            name="git_log",
            description="查询Git提交日志。参数：days（最近N天，默认7）, author（作者筛选，可选）"
        )
    
    def run(self, days: int = 7, author: str = None) -> str:
        """
        执行查询
        
        Args:
            days: 最近N天
            author: 作者筛选
        
        Returns:
            提交日志
        """
        
        # 构建命令
        cmd = [
            "git", "log",
            f"--since='{days} days ago'",
            "--pretty=format:%h - %an, %ar : %s"
        ]
        
        if author:
            cmd.extend(["--author", author])
        
        try:
            # 执行命令（示例）
            print(f"\n执行命令：{' '.join(cmd)}")
            
            # 模拟结果
            result = f"""
abc123 - 张三, 2 hours ago : 修复用户登录bug
def456 - 李四, 5 hours ago : 添加订单统计功能
ghi789 - 王五, 1 day ago : 优化数据库查询性能
            """.strip()
            
            return result
            
        except Exception as e:
            return f"执行失败：{str(e)}"

class GitStatusTool(BaseTool):
    """Git状态查询工具"""
    
    def __init__(self):
        """初始化"""
        super().__init__(
            name="git_status",
            description="查询当前Git仓库状态，返回修改的文件列表"
        )
    
    def run(self) -> str:
        """
        执行查询
        
        Returns:
            仓库状态
        """
        
        try:
            # 执行git status
            print("\n执行命令：git status --short")
            
            # 模拟结果
            result = """
M  src/service/UserService.java
A  src/controller/OrderController.java
D  src/utils/OldHelper.java
?? README.md
            """.strip()
            
            return result
            
        except Exception as e:
            return f"执行失败：{str(e)}"

class GitBranchTool(BaseTool):
    """Git分支操作工具"""
    
    def __init__(self):
        """初始化"""
        super().__init__(
            name="git_branch",
            description="Git分支操作。action: list（列出分支）, create（创建分支）, switch（切换分支）"
        )
    
    def run(self, action: str, branch_name: str = None) -> str:
        """
        执行操作
        
        Args:
            action: 操作类型
            branch_name: 分支名称
        
        Returns:
            执行结果
        """
        
        if action == "list":
            return self._list_branches()
        elif action == "create":
            return self._create_branch(branch_name)
        elif action == "switch":
            return self._switch_branch(branch_name)
        else:
            return f"不支持的操作：{action}"
    
    def _list_branches(self) -> str:
        """列出分支"""
        print("\n执行命令：git branch -a")
        
        result = """
* main
  feature/login
  feature/payment
  remotes/origin/main
  remotes/origin/develop
        """.strip()
        
        return result
    
    def _create_branch(self, branch_name: str) -> str:
        """创建分支"""
        if not branch_name:
            return "错误：分支名称不能为空"
        
        print(f"\n执行命令：git checkout -b {branch_name}")
        return f"成功创建并切换到分支：{branch_name}"
    
    def _switch_branch(self, branch_name: str) -> str:
        """切换分支"""
        if not branch_name:
            return "错误：分支名称不能为空"
        
        print(f"\n执行命令：git checkout {branch_name}")
        return f"成功切换到分支：{branch_name}"

class GitToolkit:
    """Git工具集"""
    
    @staticmethod
    def get_all_tools() -> List[BaseTool]:
        """获取所有Git工具"""
        return [
            GitLogTool(),
            GitStatusTool(),
            GitBranchTool()
        ]
    
    @staticmethod
    def demonstrate():
        """演示Git工具"""
        
        print("="*60)
        print("Git工具集演示")
        print("="*60)
        
        # 工具1：查看日志
        print("\n【工具1：git_log】")
        log_tool = GitLogTool()
        result = log_tool.run(days=3)
        print(f"结果：{result}")
        
        # 工具2：查看状态
        print("\n【工具2：git_status】")
        status_tool = GitStatusTool()
        result = status_tool.run()
        print(f"结果：{result}")
        
        # 工具3：分支操作
        print("\n【工具3：git_branch】")
        branch_tool = GitBranchTool()
        result = branch_tool.run(action="list")
        print(f"结果：{result}")

# 演示
GitToolkit.demonstrate()
```

---

## 🎯 第三部分：安全机制

```python
from enum import Enum
from typing import List, Dict
import re

class PermissionLevel(Enum):
    """权限级别"""
    READ = 1      # 只读
    MODIFY = 2    # 修改
    SENSITIVE = 3 # 敏感
    DANGEROUS = 4 # 危险

class SafetyChecker:
    """安全检查器"""
    
    def __init__(self):
        """初始化"""
        self.blacklist_commands = [
            r'rm\s+-rf',
            r'DROP\s+DATABASE',
            r'format\s+[A-Z]:',
            r'sudo\s+rm',
            r'git\s+push\s+--force',
            r'>\s*/dev/null',
            r'dd\s+if=',
        ]
        
        self.dangerous_paths = [
            '/', '/etc', '/usr', '/bin', '/sys',
            'C:\\Windows', 'C:\\Program Files'
        ]
        
        print("="*60)
        print("安全检查器")
        print("="*60)
        print(f"黑名单规则：{len(self.blacklist_commands)}条")
        print(f"受保护路径：{len(self.dangerous_paths)}个")
    
    def check_command(self, command: str) -> Dict:
        """
        检查命令安全性
        
        Args:
            command: 命令字符串
        
        Returns:
            检查结果
        """
        
        result = {
            "safe": True,
            "level": PermissionLevel.READ,
            "warnings": [],
            "blocked": False
        }
        
        # 检查黑名单
        for pattern in self.blacklist_commands:
            if re.search(pattern, command, re.IGNORECASE):
                result["safe"] = False
                result["blocked"] = True
                result["warnings"].append(f"命令匹配黑名单规则：{pattern}")
                return result
        
        # 检查危险操作
        if any(keyword in command.lower() for keyword in ['delete', 'drop', 'remove', 'truncate']):
            result["level"] = PermissionLevel.DANGEROUS
            result["warnings"].append("包含危险操作关键词")
        
        # 检查路径
        for dangerous_path in self.dangerous_paths:
            if dangerous_path in command:
                result["safe"] = False
                result["warnings"].append(f"涉及受保护路径：{dangerous_path}")
        
        return result
    
    def validate_file_path(self, path: str, workspace: str) -> Dict:
        """
        验证文件路径
        
        Args:
            path: 文件路径
            workspace: 工作空间根目录
        
        Returns:
            验证结果
        """
        
        result = {
            "valid": True,
            "normalized_path": path,
            "warnings": []
        }
        
        # 检查路径遍历
        if '..' in path:
            result["valid"] = False
            result["warnings"].append("路径包含'..'，可能的路径遍历攻击")
            return result
        
        # 检查是否在工作空间内
        import os
        abs_path = os.path.abspath(os.path.join(workspace, path))
        workspace_abs = os.path.abspath(workspace)
        
        if not abs_path.startswith(workspace_abs):
            result["valid"] = False
            result["warnings"].append("路径超出工作空间范围")
            return result
        
        result["normalized_path"] = abs_path
        return result
    
    def check_sql_injection(self, sql: str) -> Dict:
        """
        检查SQL注入
        
        Args:
            sql: SQL语句
        
        Returns:
            检查结果
        """
        
        result = {
            "safe": True,
            "warnings": []
        }
        
        # 简单的SQL注入检测（实际应更复杂）
        dangerous_patterns = [
            r";\s*DROP",
            r"'\s*OR\s*'1'\s*=\s*'1",
            r"--",
            r"/\*.*\*/",
            r"UNION\s+SELECT",
            r"exec\s*\(",
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql, re.IGNORECASE):
                result["safe"] = False
                result["warnings"].append(f"检测到潜在SQL注入：{pattern}")
        
        return result
    
    def demonstrate_safety_check(self):
        """演示安全检查"""
        
        print("\n" + "="*60)
        print("安全检查演示")
        print("="*60)
        
        # 测试1：安全命令
        print("\n【测试1：安全命令】")
        cmd1 = "git log --since='7 days ago'"
        result1 = self.check_command(cmd1)
        print(f"命令：{cmd1}")
        print(f"安全：{result1['safe']}")
        print(f"级别：{result1['level'].name}")
        
        # 测试2：危险命令
        print("\n【测试2：危险命令】")
        cmd2 = "rm -rf /"
        result2 = self.check_command(cmd2)
        print(f"命令：{cmd2}")
        print(f"安全：{result2['safe']}")
        print(f"阻止：{result2['blocked']}")
        print(f"警告：{result2['warnings']}")
        
        # 测试3：路径验证
        print("\n【测试3：路径验证】")
        path3 = "../../../etc/passwd"
        result3 = self.validate_file_path(path3, "/home/user/workspace")
        print(f"路径：{path3}")
        print(f"有效：{result3['valid']}")
        print(f"警告：{result3['warnings']}")
        
        # 测试4：SQL注入检测
        print("\n【测试4：SQL注入检测】")
        sql4 = "SELECT * FROM users WHERE id = 1; DROP TABLE users;"
        result4 = self.check_sql_injection(sql4)
        print(f"SQL：{sql4}")
        print(f"安全：{result4['safe']}")
        print(f"警告：{result4['warnings']}")

# 演示
checker = SafetyChecker()
checker.demonstrate_safety_check()
```

---

## 📝 课后练习

### 练习1：工具开发
开发数据库查询工具

### 练习2：Agent集成
集成Agent和RAG系统

### 练习3：安全加固
完善安全检查机制

---

## 🎓 知识总结

### 核心要点

1. **ReAct架构**
   - Reason推理
   - Act行动
   - Observe观察

2. **工具设计**
   - 单一职责
   - 规范接口
   - 安全可靠

3. **安全机制**
   - 权限分级
   - 命令黑名单
   - 路径验证
   - SQL注入防护

4. **执行控制**
   - 迭代限制
   - 超时控制
   - 错误处理
   - 状态追踪

---

## 🚀 下节预告

下一课：**第114课：【大项目】智能研发助手-前端与集成**

- React前端开发
- API集成
- WebSocket实时通信
- 完整系统联调

**前后端打通，系统成型！** 🔥

---

**💪 记住：Agent让AI从"回答问题"升级为"执行任务"！**

**下一课见！** 🎉
