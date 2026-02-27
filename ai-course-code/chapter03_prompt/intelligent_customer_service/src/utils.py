"""
工具函数模块
提供项目中通用的辅助功能
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


def get_project_root() -> Path:
    """获取项目根目录"""
    return PROJECT_ROOT


def load_prompt(prompt_path: str) -> str:
    """
    从markdown文件中加载提示词内容
    
    提示词文件格式：markdown文件中用 ``` 包裹的部分为提示词内容
    
    Args:
        prompt_path: 相对于项目根目录的提示词文件路径
        
    Returns:
        提示词模板字符串
    """
    full_path = PROJECT_ROOT / prompt_path
    
    if not full_path.exists():
        raise FileNotFoundError(f"提示词文件不存在：{full_path}")
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取 ``` 之间的内容（第一个代码块）
    blocks = content.split("```")
    if len(blocks) >= 3:
        return blocks[1].strip()
    
    raise ValueError(f"提示词文件格式错误，未找到代码块：{prompt_path}")


def get_llm_config() -> dict:
    """
    获取LLM配置
    
    Returns:
        {
            'base_url': API地址,
            'api_key': API密钥,
            'model': 模型名称
        }
    """
    return {
        "base_url": os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        "api_key": os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        "model": os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct"),
    }


def format_conversation_history(history: list, max_turns: int = 5) -> str:
    """
    格式化对话历史为字符串
    
    Args:
        history: 对话历史列表，每项包含 user 和 bot 字段
        max_turns: 最多保留的对话轮数
        
    Returns:
        格式化后的对话历史字符串
    """
    if not history:
        return "无"
    
    # 只保留最近的几轮
    recent = history[-max_turns:]
    
    lines = []
    for turn in recent:
        lines.append(f"用户：{turn['user']}")
        lines.append(f"客服：{turn['bot']}")
    
    return "\n".join(lines)


def log_conversation(user_input: str, intent: str, response: str,
                     confidence: float, log_dir: str = "logs"):
    """
    记录对话日志（JSON Lines格式）
    
    Args:
        user_input: 用户输入
        intent: 识别的意图
        response: 生成的回复
        confidence: 置信度
        log_dir: 日志目录
    """
    log_path = PROJECT_ROOT / log_dir
    log_path.mkdir(exist_ok=True)
    
    log_file = log_path / "conversations.jsonl"
    
    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": user_input,
        "intent": intent,
        "confidence": confidence,
        "response": response,
    }
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_test_data(filename: str) -> list:
    """
    加载测试数据
    
    Args:
        filename: 测试数据文件名（位于 tests/test_data/ 目录下）
        
    Returns:
        测试数据列表
    """
    test_file = PROJECT_ROOT / "tests" / "test_data" / filename
    
    if not test_file.exists():
        raise FileNotFoundError(f"测试数据文件不存在：{test_file}")
    
    with open(test_file, "r", encoding="utf-8") as f:
        return json.load(f)
