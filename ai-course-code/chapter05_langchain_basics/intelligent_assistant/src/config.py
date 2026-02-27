"""
配置管理
对应课程：第28课-LangChain实战项目1

集中管理所有配置项，支持环境变量覆盖
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Config:
    """全局配置"""

    # 项目路径
    PROJECT_ROOT = PROJECT_ROOT

    # API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    LOCAL_LLM_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    LOCAL_LLM_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")

    # 模型配置
    PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "qwen2.5-7b-instruct")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "qwen2.5-7b-instruct")
    LOCAL_MODEL = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")

    # 性能配置
    ENABLE_CACHE = True
    MAX_CONVERSATION_HISTORY = 10
    TIMEOUT = 30
    MAX_RETRIES = 3

    # 功能开关
    ENABLE_TOOLS = True
    ENABLE_INTENT_CLASSIFICATION = True
    ENABLE_FALLBACK = True

    # 使用本地模型（LM Studio）还是 OpenAI
    USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", "true").lower() == "true"


config = Config()
