"""
配置管理
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置"""

    # LLM配置
    LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
    LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")

    # Agent配置
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
    ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
    LOG_FILE = os.getenv("LOG_FILE", "agent.log")
