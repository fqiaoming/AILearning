"""
Agent核心层
实现ReAct循环、对话管理、状态追踪
"""
import logging
import json
import re
from typing import Dict, List, Optional

from langchain_openai import ChatOpenAI

from .config import Config
from .tools import PersonalAssistantTools


def setup_logger(enable: bool, log_file: str) -> logging.Logger:
    """配置日志"""
    logger = logging.getLogger("PersonalAssistant")
    logger.setLevel(logging.INFO if enable else logging.WARNING)
    if enable and not logger.handlers:
        # 文件Handler
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
        # 控制台Handler
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        sh.setLevel(logging.DEBUG)
        logger.addHandler(sh)
    return logger


class PersonalAssistantAgent:
    """
    个人助手Agent - 生产级实现

    功能：
    - 6个工具（天气、日程、搜索、计算、笔记、汇率）
    - ReAct推理循环
    - 对话历史管理
    - 日志监控与统计
    """

    def __init__(self, max_iterations: int = None, enable_logging: bool = None):
        config = Config()

        # 初始化LLM
        self.llm = ChatOpenAI(
            base_url=config.LM_STUDIO_BASE_URL,
            api_key=config.LM_STUDIO_API_KEY,
            model=config.LM_STUDIO_MODEL,
            temperature=0,
        )

        self.max_iterations = max_iterations or config.MAX_ITERATIONS
        self.enable_logging = enable_logging if enable_logging is not None else config.ENABLE_LOGGING

        # 初始化工具
        self.tool_manager = PersonalAssistantTools()

        # 对话历史
        self.conversation_history: List[Dict] = []

        # 统计信息
        self.stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_tool_calls": 0,
            "tool_call_stats": {},
        }

        # 日志
        self.logger = setup_logger(self.enable_logging, config.LOG_FILE)
        self.logger.info("PersonalAssistantAgent 初始化完成")

    def run(self, user_input: str, verbose: bool = True) -> str:
        """处理用户输入 - 主入口"""
        self.stats["total_queries"] += 1

        if verbose:
            print(f"\n{'🤖' * 30}")
            print(f"用户: {user_input}")
            print(f"{'🤖' * 30}\n")

        self.logger.info(f"用户输入: {user_input}")

        # 添加到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})

        try:
            answer = self._react_loop(user_input, verbose)
            self.conversation_history.append({"role": "assistant", "content": answer})
            self.stats["successful_queries"] += 1

            if verbose:
                print(f"\n✅ Agent: {answer}\n")
            return answer

        except Exception as e:
            self.stats["failed_queries"] += 1
            error_msg = f"抱歉，处理您的请求时出错了：{str(e)}"
            self.logger.error(f"处理失败: {str(e)}", exc_info=True)
            if verbose:
                print(f"\n❌ {error_msg}\n")
            return error_msg

    def _react_loop(self, user_input: str, verbose: bool) -> str:
        """ReAct执行循环：Thought → Action → Observation → ... → Answer"""
        thought_action_history: List[Dict] = []

        for iteration in range(self.max_iterations):
            if verbose:
                print(f"--- 迭代 {iteration + 1}/{self.max_iterations} ---")

            next_step = self._generate_next_step(user_input, thought_action_history)

            # 完成任务
            if next_step.get("type") == "answer":
                return next_step["content"]

            thought = next_step.get("thought", "")
            action = next_step.get("action", "")
            action_input = next_step.get("action_input", "")

            if verbose:
                print(f"💭 Thought: {thought}")
                print(f"🔧 Action: {action}({action_input})")

            # 执行工具
            observation = self._execute_tool(action, action_input)

            if verbose:
                print(f"👁️  Observation: {observation}\n")

            thought_action_history.append({
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": observation,
            })

        return "抱歉，任务太复杂了，我无法在限定步骤内完成。请尝试简化您的请求。"

    def _generate_next_step(self, user_input: str, history: List[Dict]) -> Dict:
        """调用LLM生成下一步行动"""
        tools_desc = self.tool_manager.get_tools_description()

        # 格式化已执行步骤
        history_text = ""
        for item in history:
            history_text += f"Thought: {item['thought']}\n"
            history_text += f"Action: {item['action']}\n"
            history_text += f"Action Input: {item['action_input']}\n"
            history_text += f"Observation: {item['observation']}\n\n"

        # 最近对话（最多5轮）
        recent = self.conversation_history[-10:]
        conv_text = "\n".join(f"{m['role']}: {m['content']}" for m in recent)

        prompt = f"""你是一个智能个人助手，使用ReAct框架处理用户请求。

可用工具：
{tools_desc}

最近对话：
{conv_text}

当前任务：{user_input}

已执行步骤：
{history_text}

请严格按以下格式回复：

如果还需要使用工具：
Thought: <你的思考>
Action: <工具名称>
Action Input: <工具参数，JSON格式如{{"key": "value"}}或简单字符串>

如果已完成任务：
Thought: <总结思考>
Answer: <最终回答>

你的回复："""

        response = self.llm.invoke(prompt)
        return self._parse_output(response.content)

    def _parse_output(self, content: str) -> Dict:
        """解析LLM输出为结构化数据"""
        result = {"type": "action", "thought": "", "action": "", "action_input": ""}

        lines = content.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("Thought:"):
                result["thought"] = line[len("Thought:"):].strip()
            elif line.startswith("Action:"):
                result["action"] = line[len("Action:"):].strip()
            elif line.startswith("Action Input:"):
                result["action_input"] = line[len("Action Input:"):].strip()
            elif line.startswith("Answer:"):
                result["type"] = "answer"
                # Answer可能跨多行
                answer_start = content.index("Answer:") + len("Answer:")
                result["content"] = content[answer_start:].strip()
                return result

        return result

    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """执行工具调用"""
        self.stats["total_tool_calls"] += 1
        self.stats["tool_call_stats"][tool_name] = self.stats["tool_call_stats"].get(tool_name, 0) + 1
        self.logger.info(f"调用工具: {tool_name}({tool_input})")

        tool = self.tool_manager.tools.get(tool_name)
        if not tool:
            available = ", ".join(self.tool_manager.tools.keys())
            return f"❌ 工具 '{tool_name}' 不存在。可用工具：{available}"

        try:
            # 尝试解析JSON参数
            kwargs = self._parse_tool_input(tool_name, tool_input)
            result = tool.run(**kwargs)

            if result.success:
                self.logger.info(f"工具成功: {tool_name}, 耗时={result.execution_time:.3f}s")
                return str(result.result)
            else:
                self.logger.error(f"工具失败: {tool_name}, error={result.error}")
                return f"❌ 工具执行错误：{result.error}"

        except Exception as e:
            self.logger.error(f"工具异常: {tool_name}, {str(e)}")
            return f"❌ 工具执行异常：{str(e)}"

    def _parse_tool_input(self, tool_name: str, raw_input: str) -> Dict:
        """智能解析工具输入参数"""
        # 尝试JSON解析
        try:
            parsed = json.loads(raw_input)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass

        # 根据工具名称做智能映射
        param_mapping = {
            "get_weather": "date",
            "search": "query",
            "calculate": "expression",
            "add_note": "content",
            "list_calendar": None,
            "list_notes": None,
        }

        if tool_name in param_mapping:
            param_name = param_mapping[tool_name]
            if param_name is None:
                return {}
            return {param_name: raw_input}

        # add_calendar: 尝试拆分 time, event
        if tool_name == "add_calendar":
            if "," in raw_input:
                parts = raw_input.split(",", 1)
                return {"time": parts[0].strip(), "event": parts[1].strip()}
            return {"time": raw_input, "event": raw_input}

        # convert_currency: 尝试拆分 amount, from, to
        if tool_name == "convert_currency":
            parts = [p.strip() for p in raw_input.split(",")]
            if len(parts) >= 3:
                return {"amount": parts[0], "from_currency": parts[1], "to_currency": parts[2]}
            return {"amount": raw_input, "from_currency": "USD", "to_currency": "CNY"}

        return {"input": raw_input}

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()

    def print_stats(self):
        """打印统计信息"""
        s = self.stats
        print(f"\n{'=' * 60}")
        print("📊 Agent统计信息")
        print(f"{'=' * 60}")
        total = s["total_queries"]
        if total > 0:
            print(f"总查询数: {total}")
            print(f"  成功: {s['successful_queries']}")
            print(f"  失败: {s['failed_queries']}")
            print(f"  成功率: {s['successful_queries'] / total:.1%}")
        print(f"\n🔧 工具调用统计:")
        print(f"  总调用次数: {s['total_tool_calls']}")
        for tool, count in sorted(s["tool_call_stats"].items(), key=lambda x: -x[1]):
            print(f"    {tool}: {count}次")
        print(f"{'=' * 60}")
