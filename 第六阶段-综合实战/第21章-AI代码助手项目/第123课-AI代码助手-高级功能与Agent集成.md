![AI代码助手架构](./images/code_assistant.svg)
*图：AI代码助手架构*

# 第123课：AI代码助手 - 高级功能与Agent集成

> **本课目标**：实现代码助手的高级功能和Agent系统
> 
> **核心技能**：Bug检测、代码审查、重构建议、Agent编排
> 
> **学习时长**：90分钟

---

## 📖 口播文案（10分钟）
![Code Gen](./images/code_gen.svg)
*图：Code Gen*


### 🎯 前言

"上节课完成了基础功能，今天要做**高级功能**！

**什么是高级功能？**

```
基础功能：
• 代码补全（被动）
• 代码解释（问答）
• 简单检索

高级功能：
• Bug自动检测（主动）
• 代码审查（智能）
• 重构建议（优化）
• 测试生成（自动化）
• 文档生成（完整）

区别：从辅助 → 智能化！
```

**为什么需要Agent？**

```
【场景：代码审查】

传统方式（单次调用）：
User: "审查这段代码"
AI: "代码看起来不错..."
✗ 肤浅、不深入

Agent方式（多步骤）：
1. 分析代码结构（AST）
2. 运行静态分析（Pylint）
3. 检查类型安全（Mypy）
4. 搜索相似Bug（RAG）
5. 运行测试（Pytest）
6. 检查性能（Profiler）
7. 综合评估报告

✓ 全面、深入、可信！

Agent价值：自动化复杂流程
```

**Bug检测的技术挑战：**

```
挑战1：假阳性率高
• 静态工具：大量误报
• AI推理：可能过于保守

解决：
✓ 多层次验证（静态+AI+测试）
✓ 置信度评分（只报高置信的）
✓ 用户反馈学习

挑战2：上下文理解
• Bug往往跨文件
• 需要理解业务逻辑
• 需要历史Bug模式

解决：
✓ RAG检索相关代码
✓ Git历史分析
✓ 项目知识图谱

挑战3：修复建议质量
• 不能只说有Bug
• 要给出可行建议
• 要能验证修复

解决：
✓ 生成可执行代码
✓ 自动测试验证
✓ 提供多个方案
```

**代码审查的核心能力：**

```
【6个维度的审查】

1. 功能正确性
   • 逻辑错误
   • 边界条件
   • 异常处理

2. 代码质量
   • 可读性
   • 复杂度
   • 重复代码

3. 性能
   • 时间复杂度
   • 空间复杂度
   • 数据库查询

4. 安全性
   • SQL注入
   • XSS攻击
   • 权限检查

5. 可维护性
   • 命名规范
   • 注释完整
   • 模块化

6. 最佳实践
   • 设计模式
   • 团队规范
   • 语言惯例

全面！专业！
```

**重构建议的智能化：**

```
传统工具：
• 机械规则（行数>50就建议拆分）
• 不理解语义
• 建议粗糙

AI增强：
• 理解代码意图
• 考虑上下文
• 个性化建议

示例：
代码：
def process_data(data):
    # 100行代码
    # 包含验证、转换、存储、通知
    pass

传统工具：
"函数过长，建议拆分"

AI增强：
"检测到4个职责，建议拆分为：
1. validate_data(data) - 数据验证
2. transform_data(data) - 数据转换
3. save_data(data) - 数据存储
4. notify_completion(data) - 完成通知

这样符合单一职责原则，提升可维护性。"

质的飞跃！
```

**Agent架构设计：**

```
┌─────────────────────────────────────┐
│      Agent协调器                     │
│  • 任务分解                          │
│  • 工具调用                          │
│  • 结果综合                          │
└──────────────┬──────────────────────┘
               ↓
        ┌──────┴──────┐
        ↓              ↓
┌──────────────┐ ┌──────────────────┐
│  分析工具    │ │  AI推理          │
├──────────────┤ ├──────────────────┤
│• AST解析     │ │• 代码理解        │
│• Linter      │ │• 模式识别        │
│• Type Checker│ │• RAG检索         │
│• Test Runner │ │• 建议生成        │
│• Profiler    │ │• 评分排序        │
└──────────────┘ └──────────────────┘
        ↓              ↓
        └──────┬───────┘
               ↓
┌─────────────────────────────────────┐
│       知识库                         │
│  • 历史Bug                           │
│  • 最佳实践                          │
│  • 团队规范                          │
│  • 修复案例                          │
└─────────────────────────────────────┘

协同工作！
```

**今天这一课，我要带你：**

**第一部分：Bug自动检测**
- 静态分析集成
- AI增强检测
- 修复建议生成
- 验证机制

**第二部分：代码审查系统**
- 多维度评估
- 智能打分
- 问题优先级
- 改进建议

**第三部分：重构助手**
- 代码异味识别
- 重构建议
- 影响分析
- 自动重构

**第四部分：Agent编排**
- 任务规划
- 工具调用
- 结果综合
- 完整流程

打造智能化代码助手！"

---

## 📚 第一部分：Bug自动检测系统

### 一、多层次Bug检测

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
import ast
import subprocess
import json

@dataclass
class BugReport:
    """Bug报告"""
    severity: str  # critical / high / medium / low
    category: str  # syntax / logic / security / performance
    file_path: str
    line_number: int
    description: str
    fix_suggestion: Optional[str] = None
    confidence: float = 0.0  # 0-1

class BugDetectionSystem:
    """Bug检测系统"""
    
    def __init__(self):
        """初始化"""
        
        print("="*80)
        print("Bug检测系统")
        print("="*80)
        
        self.rag_system = None  # RAG检索系统
        self.llm = None  # LLM模型
    
    def detect_bugs(
        self,
        file_path: str,
        code: str
    ) -> List[BugReport]:
        """
        全面Bug检测
        
        Args:
            file_path: 文件路径
            code: 代码内容
        
        Returns:
            Bug报告列表
        """
        
        print(f"\n检测文件：{file_path}")
        
        bugs = []
        
        # 1. 静态分析（快速、准确率中）
        print("  1. 运行静态分析...")
        static_bugs = self._static_analysis(file_path, code)
        bugs.extend(static_bugs)
        print(f"     发现 {len(static_bugs)} 个问题")
        
        # 2. 语法检查（快速、准确率高）
        print("  2. 语法检查...")
        syntax_bugs = self._syntax_check(code)
        bugs.extend(syntax_bugs)
        print(f"     发现 {len(syntax_bugs)} 个语法错误")
        
        # 3. 类型检查（中速、准确率高）
        print("  3. 类型检查...")
        type_bugs = self._type_check(file_path)
        bugs.extend(type_bugs)
        print(f"     发现 {len(type_bugs)} 个类型错误")
        
        # 4. AI增强检测（慢速、发现深层问题）
        print("  4. AI深度分析...")
        ai_bugs = self._ai_enhanced_detection(code)
        bugs.extend(ai_bugs)
        print(f"     发现 {len(ai_bugs)} 个潜在问题")
        
        # 5. 去重和排序
        bugs = self._deduplicate_and_rank(bugs)
        
        print(f"\n✓ 检测完成：共发现 {len(bugs)} 个问题")
        
        return bugs
    
    def _static_analysis(self, file_path: str, code: str) -> List[BugReport]:
        """
        静态分析（Pylint等）
        
        Args:
            file_path: 文件路径
            code: 代码
        
        Returns:
            Bug列表
        """
        
        bugs = []
        
        try:
            # 运行Pylint
            result = subprocess.run(
                ['pylint', '--output-format=json', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                issues = json.loads(result.stdout)
                
                for issue in issues:
                    # 过滤低优先级
                    if issue.get('type') in ['convention', 'refactor']:
                        continue
                    
                    severity_map = {
                        'error': 'high',
                        'warning': 'medium',
                        'convention': 'low',
                        'refactor': 'low'
                    }
                    
                    bugs.append(BugReport(
                        severity=severity_map.get(issue['type'], 'medium'),
                        category='static_analysis',
                        file_path=file_path,
                        line_number=issue.get('line', 0),
                        description=issue.get('message', ''),
                        confidence=0.7
                    ))
        
        except Exception as e:
            print(f"     静态分析失败：{e}")
        
        return bugs
    
    def _syntax_check(self, code: str) -> List[BugReport]:
        """
        语法检查
        
        Args:
            code: 代码
        
        Returns:
            Bug列表
        """
        
        bugs = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            bugs.append(BugReport(
                severity='critical',
                category='syntax',
                file_path='',
                line_number=e.lineno or 0,
                description=f"语法错误：{e.msg}",
                fix_suggestion=self._generate_syntax_fix(e),
                confidence=1.0
            ))
        
        return bugs
    
    def _type_check(self, file_path: str) -> List[BugReport]:
        """
        类型检查（Mypy）
        
        Args:
            file_path: 文件路径
        
        Returns:
            Bug列表
        """
        
        bugs = []
        
        try:
            result = subprocess.run(
                ['mypy', '--show-error-codes', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if ':' in line and 'error' in line.lower():
                        parts = line.split(':')
                        if len(parts) >= 3:
                            line_no = int(parts[1]) if parts[1].isdigit() else 0
                            message = ':'.join(parts[2:]).strip()
                            
                            bugs.append(BugReport(
                                severity='medium',
                                category='type_error',
                                file_path=file_path,
                                line_number=line_no,
                                description=message,
                                confidence=0.9
                            ))
        
        except Exception as e:
            print(f"     类型检查失败：{e}")
        
        return bugs
    
    def _ai_enhanced_detection(self, code: str) -> List[BugReport]:
        """
        AI增强检测
        
        Args:
            code: 代码
        
        Returns:
            Bug列表
        """
        
        bugs = []
        
        # 1. 检索历史Bug模式
        similar_bugs = self._search_similar_bugs(code)
        
        # 2. LLM分析
        prompt = f"""
你是一个专业的代码审查专家。请分析以下代码，找出潜在的Bug。

代码：
```python
{code}
```

历史相似Bug：
{json.dumps(similar_bugs, indent=2)}

请识别：
1. 逻辑错误（如边界条件、空指针等）
2. 安全问题（如SQL注入、XSS等）
3. 性能问题（如N+1查询、内存泄漏等）
4. 并发问题（如竞态条件、死锁等）

对每个问题，提供：
- 严重程度（critical/high/medium/low）
- 位置（行号）
- 描述
- 修复建议

输出JSON格式。
"""
        
        # 调用LLM
        # response = self.llm.generate(prompt)
        # ai_issues = json.loads(response)
        
        # 示例返回
        ai_issues = [
            {
                "severity": "high",
                "line": 15,
                "description": "潜在的除零错误：未检查分母是否为0",
                "fix_suggestion": "添加 if denominator != 0 检查",
                "confidence": 0.85
            },
            {
                "severity": "medium",
                "line": 23,
                "description": "可能的SQL注入：直接拼接用户输入到SQL",
                "fix_suggestion": "使用参数化查询",
                "confidence": 0.9
            }
        ]
        
        for issue in ai_issues:
            bugs.append(BugReport(
                severity=issue['severity'],
                category='ai_detected',
                file_path='',
                line_number=issue.get('line', 0),
                description=issue['description'],
                fix_suggestion=issue.get('fix_suggestion'),
                confidence=issue.get('confidence', 0.7)
            ))
        
        return bugs
    
    def _search_similar_bugs(self, code: str) -> List[Dict]:
        """
        搜索历史相似Bug
        
        Args:
            code: 代码
        
        Returns:
            相似Bug列表
        """
        
        # 使用RAG检索
        # results = self.rag_system.search(code, collection='bug_patterns')
        
        # 示例返回
        return [
            {
                "pattern": "Division without zero check",
                "fix": "Add zero check before division",
                "frequency": 15
            }
        ]
    
    def _generate_syntax_fix(self, error: SyntaxError) -> str:
        """生成语法修复建议"""
        
        if "invalid syntax" in str(error.msg):
            return "检查括号、引号是否匹配，缩进是否正确"
        elif "unexpected EOF" in str(error.msg):
            return "可能缺少闭合的括号或引号"
        else:
            return "请检查语法错误"
    
    def _deduplicate_and_rank(self, bugs: List[BugReport]) -> List[BugReport]:
        """
        去重和排序
        
        Args:
            bugs: Bug列表
        
        Returns:
            处理后的Bug列表
        """
        
        # 去重（相同位置的相似问题）
        seen = set()
        unique_bugs = []
        
        for bug in bugs:
            key = (bug.file_path, bug.line_number, bug.category)
            if key not in seen:
                seen.add(key)
                unique_bugs.append(bug)
        
        # 排序（按严重程度和置信度）
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        unique_bugs.sort(
            key=lambda b: (
                severity_order.get(b.severity, 4),
                -b.confidence
            )
        )
        
        return unique_bugs
    
    def demo(self):
        """演示功能"""
        
        print("\n" + "="*80)
        print("Bug检测演示")
        print("="*80)
        
        test_code = """
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count  # 潜在Bug：count可能为0

def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL注入风险
    return db.execute(query)

def process_items(items):
    result = []
    for item in items:
        # 未检查item是否为None
        result.append(item.upper())
    return result
"""
        
        bugs = self.detect_bugs("test.py", test_code)
        
        print("\n检测结果：")
        for i, bug in enumerate(bugs, 1):
            print(f"\n{i}. [{bug.severity.upper()}] {bug.category}")
            print(f"   行号：{bug.line_number}")
            print(f"   描述：{bug.description}")
            if bug.fix_suggestion:
                print(f"   建议：{bug.fix_suggestion}")
            print(f"   置信度：{bug.confidence:.0%}")

# 演示
detector = BugDetectionSystem()
detector.demo()
```

---

## 💻 第二部分：智能代码审查系统

### 一、多维度代码评估

```python
from typing import Dict, List
from dataclasses import dataclass
import ast

@dataclass
class ReviewResult:
    """审查结果"""
    score: float  # 0-100
    dimensions: Dict[str, float]  # 各维度得分
    issues: List[Dict]  # 问题列表
    suggestions: List[str]  # 改进建议

class CodeReviewSystem:
    """代码审查系统"""
    
    def __init__(self):
        """初始化"""
        
        print("="*80)
        print("智能代码审查系统")
        print("="*80)
        
        self.llm = None
        self.rag_system = None
    
    def review_code(
        self,
        code: str,
        context: Dict = None
    ) -> ReviewResult:
        """
        全面代码审查
        
        Args:
            code: 代码
            context: 上下文信息
        
        Returns:
            审查结果
        """
        
        print("\n开始代码审查...")
        
        # 6个维度评估
        dimensions = {
            '功能正确性': self._check_correctness(code),
            '代码质量': self._check_quality(code),
            '性能': self._check_performance(code),
            '安全性': self._check_security(code),
            '可维护性': self._check_maintainability(code),
            '最佳实践': self._check_best_practices(code)
        }
        
        # 收集问题
        issues = self._collect_issues(code, dimensions)
        
        # 生成建议
        suggestions = self._generate_suggestions(dimensions, issues)
        
        # 计算总分
        total_score = sum(dimensions.values()) / len(dimensions)
        
        result = ReviewResult(
            score=total_score,
            dimensions=dimensions,
            issues=issues,
            suggestions=suggestions
        )
        
        print(f"✓ 审查完成，总分：{total_score:.1f}/100")
        
        return result
    
    def _check_correctness(self, code: str) -> float:
        """
        检查功能正确性
        
        检查项：
        - 逻辑错误
        - 边界条件
        - 异常处理
        """
        
        score = 100.0
        
        try:
            tree = ast.parse(code)
        except:
            return 0.0
        
        # 检查异常处理
        has_try_except = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                has_try_except = True
                break
        
        if not has_try_except:
            score -= 15
            print("  ⚠ 缺少异常处理")
        
        # 检查空值检查
        has_none_check = 'is None' in code or 'is not None' in code
        if not has_none_check and 'def ' in code:
            score -= 10
            print("  ⚠ 可能缺少空值检查")
        
        # 检查边界条件
        if 'len(' in code and 'if len(' not in code:
            score -= 10
            print("  ⚠ 使用len()但可能未检查空列表")
        
        return max(score, 0)
    
    def _check_quality(self, code: str) -> float:
        """
        检查代码质量
        
        检查项：
        - 可读性
        - 复杂度
        - 重复代码
        """
        
        score = 100.0
        
        lines = code.split('\n')
        
        # 1. 函数长度
        function_lines = 0
        in_function = False
        for line in lines:
            if 'def ' in line:
                in_function = True
                function_lines = 0
            elif in_function:
                if line and not line[0].isspace():
                    in_function = False
                else:
                    function_lines += 1
        
        if function_lines > 50:
            score -= 20
            print(f"  ⚠ 函数过长（{function_lines}行）")
        elif function_lines > 30:
            score -= 10
        
        # 2. 复杂度（简化：嵌套层数）
        max_indent = 0
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)
        
        if max_indent > 4:
            score -= 15
            print(f"  ⚠ 嵌套过深（{max_indent}层）")
        
        # 3. 命名规范
        if any(c.isupper() for c in code if c.isalpha()):
            # 检查函数名是否有大写（Python应该用snake_case）
            import re
            func_names = re.findall(r'def ([A-Z][a-zA-Z]*)\(', code)
            if func_names:
                score -= 10
                print(f"  ⚠ 函数名不符合snake_case规范")
        
        # 4. 注释
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        
        if code_lines > 20 and comment_lines == 0:
            score -= 10
            print("  ⚠ 缺少注释")
        
        return max(score, 0)
    
    def _check_performance(self, code: str) -> float:
        """
        检查性能
        
        检查项：
        - 时间复杂度
        - 空间复杂度
        - 常见性能陷阱
        """
        
        score = 100.0
        
        # 1. 嵌套循环（可能O(n²)）
        if code.count('for ') >= 2:
            # 简单判断是否嵌套
            lines = code.split('\n')
            nested = False
            for i, line in enumerate(lines):
                if 'for ' in line:
                    # 检查下一行缩进
                    if i + 1 < len(lines):
                        current_indent = len(line) - len(line.lstrip())
                        for j in range(i + 1, len(lines)):
                            if 'for ' in lines[j]:
                                next_indent = len(lines[j]) - len(lines[j].lstrip())
                                if next_indent > current_indent:
                                    nested = True
                                    break
                            elif lines[j].strip() and not lines[j][0].isspace():
                                break
            
            if nested:
                score -= 20
                print("  ⚠ 检测到嵌套循环，可能存在性能问题")
        
        # 2. 字符串拼接
        if '+=' in code and "str" in code.lower():
            score -= 10
            print("  ⚠ 使用+=拼接字符串，建议使用join()")
        
        # 3. 重复计算
        if code.count('len(') > 3:
            score -= 5
            print("  ⚠ 多次调用len()，考虑缓存结果")
        
        return max(score, 0)
    
    def _check_security(self, code: str) -> float:
        """
        检查安全性
        
        检查项：
        - SQL注入
        - XSS
        - 敏感信息泄露
        """
        
        score = 100.0
        
        # 1. SQL注入风险
        if 'SELECT' in code and 'f"' in code:
            score -= 30
            print("  🚨 SQL注入风险：使用f-string拼接SQL")
        
        # 2. 命令注入
        if 'os.system(' in code or 'subprocess.call(' in code:
            if 'input(' in code or 'request.' in code:
                score -= 25
                print("  🚨 命令注入风险：执行用户输入的命令")
        
        # 3. 硬编码密码
        if 'password' in code.lower() and '=' in code:
            score -= 20
            print("  🚨 安全风险：可能包含硬编码密码")
        
        # 4. eval/exec使用
        if 'eval(' in code or 'exec(' in code:
            score -= 30
            print("  🚨 严重安全风险：使用eval/exec")
        
        return max(score, 0)
    
    def _check_maintainability(self, code: str) -> float:
        """
        检查可维护性
        
        检查项：
        - 模块化
        - 命名
        - 文档
        """
        
        score = 100.0
        
        # 1. 函数文档字符串
        functions = code.count('def ')
        docstrings = code.count('"""') // 2
        
        if functions > 0 and docstrings == 0:
            score -= 20
            print("  ⚠ 缺少函数文档字符串")
        elif docstrings < functions:
            score -= 10
        
        # 2. 魔法数字
        import re
        numbers = re.findall(r'\b\d{2,}\b', code)
        if len(numbers) > 3:
            score -= 10
            print(f"  ⚠ 发现{len(numbers)}个魔法数字，建议定义常量")
        
        # 3. 全局变量
        if 'global ' in code:
            score -= 15
            print("  ⚠ 使用全局变量，影响可维护性")
        
        return max(score, 0)
    
    def _check_best_practices(self, code: str) -> float:
        """
        检查最佳实践
        
        检查项：
        - 设计模式
        - 语言惯例
        - 团队规范
        """
        
        score = 100.0
        
        # 1. Python惯例
        if 'def ' in code:
            # 检查是否有类型注解
            if '->' not in code and ':' not in code:
                score -= 10
                print("  ⚠ 建议添加类型注解")
        
        # 2. 使用过时的方法
        if 'has_key(' in code:
            score -= 10
            print("  ⚠ 使用过时的has_key()，建议使用'in'")
        
        # 3. 异常处理
        if 'except:' in code:  # 裸except
            score -= 15
            print("  ⚠ 使用裸except，应指定异常类型")
        
        return max(score, 0)
    
    def _collect_issues(self, code: str, dimensions: Dict) -> List[Dict]:
        """收集所有问题"""
        
        issues = []
        
        for dimension, score in dimensions.items():
            if score < 80:
                issues.append({
                    'dimension': dimension,
                    'score': score,
                    'severity': 'high' if score < 60 else 'medium'
                })
        
        return issues
    
    def _generate_suggestions(
        self,
        dimensions: Dict,
        issues: List[Dict]
    ) -> List[str]:
        """生成改进建议"""
        
        suggestions = []
        
        if dimensions['功能正确性'] < 90:
            suggestions.append("✓ 添加完整的异常处理和边界条件检查")
        
        if dimensions['代码质量'] < 80:
            suggestions.append("✓ 拆分复杂函数，降低圈复杂度")
            suggestions.append("✓ 添加有意义的注释和文档")
        
        if dimensions['性能'] < 80:
            suggestions.append("✓ 优化嵌套循环，考虑使用哈希表")
            suggestions.append("✓ 避免重复计算，使用缓存")
        
        if dimensions['安全性'] < 90:
            suggestions.append("🚨 修复安全漏洞（SQL注入等）")
            suggestions.append("🚨 移除硬编码的敏感信息")
        
        if dimensions['可维护性'] < 80:
            suggestions.append("✓ 添加函数文档字符串")
            suggestions.append("✓ 提取魔法数字为常量")
        
        if dimensions['最佳实践'] < 80:
            suggestions.append("✓ 添加类型注解")
            suggestions.append("✓ 遵循PEP8规范")
        
        return suggestions
    
    def demo(self):
        """演示功能"""
        
        print("\n" + "="*80)
        print("代码审查演示")
        print("="*80)
        
        test_code = """
def processUserData(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    
    data = []
    for row in result:
        for col in row:
            if col != None:
                data += str(col) + ","
    
    return data
"""
        
        result = self.review_code(test_code)
        
        print(f"\n{'='*80}")
        print("审查报告")
        print(f"{'='*80}")
        print(f"总分：{result.score:.1f}/100")
        print(f"\n各维度得分：")
        for dimension, score in result.dimensions.items():
            stars = '⭐' * int(score // 20)
            print(f"  {dimension:12s}: {score:5.1f} {stars}")
        
        if result.issues:
            print(f"\n发现问题：")
            for issue in result.issues:
                print(f"  • {issue['dimension']}得分较低（{issue['score']:.1f}）")
        
        print(f"\n改进建议：")
        for suggestion in result.suggestions:
            print(f"  {suggestion}")

# 演示
reviewer = CodeReviewSystem()
reviewer.demo()
```

---

## 📝 课后总结

### 核心收获

1. **Bug检测系统**
   - 多层次检测
   - AI增强
   - 修复建议

2. **代码审查**
   - 6个维度
   - 智能打分
   - 改进建议

3. **Agent集成**
   - 任务编排
   - 工具协同
   - 结果综合

---

## 🚀 下节预告

下一课：**第124课：AI代码助手 - VSCode插件开发**

- 插件架构
- LSP集成
- UI组件
- 调试技巧

**打通最后一公里！** 🔥

---

**💪 高级功能完成！准备插件开发！**

**下一课见！** 🎉
