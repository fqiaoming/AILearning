"""
第22-25章-工程化：项目结构最佳实践
对应课程：第104-105课

好的项目结构让代码可维护、可扩展
"""


def demo_project_structure():
    """项目结构示例"""
    print("=" * 60)
    print("AI应用项目结构最佳实践")
    print("=" * 60)
    
    structure = """
my_ai_project/
├── README.md              # 项目说明
├── requirements.txt       # 依赖管理
├── .env.example          # 环境变量模板
├── .gitignore            # Git忽略文件
│
├── src/                  # 源代码
│   ├── __init__.py
│   ├── main.py           # 入口文件
│   │
│   ├── core/             # 核心逻辑
│   │   ├── __init__.py
│   │   ├── llm.py        # LLM客户端封装
│   │   ├── chain.py      # Chain定义
│   │   └── agent.py      # Agent定义
│   │
│   ├── tools/            # 工具定义
│   │   ├── __init__.py
│   │   ├── search.py
│   │   └── calculator.py
│   │
│   ├── prompts/          # 提示词模板
│   │   ├── __init__.py
│   │   └── templates.py
│   │
│   ├── utils/            # 工具函数
│   │   ├── __init__.py
│   │   ├── logger.py     # 日志配置
│   │   └── helpers.py
│   │
│   └── config/           # 配置文件
│       ├── __init__.py
│       └── settings.py
│
├── tests/                # 测试代码
│   ├── __init__.py
│   ├── test_llm.py
│   └── test_chain.py
│
├── data/                 # 数据文件
│   ├── raw/              # 原始数据
│   └── processed/        # 处理后数据
│
├── notebooks/            # Jupyter笔记本
│   └── exploration.ipynb
│
└── docker/               # Docker配置
    ├── Dockerfile
    └── docker-compose.yml
"""
    print(structure)


def demo_config_management():
    """配置管理"""
    print("\n" + "=" * 60)
    print("配置管理最佳实践")
    print("=" * 60)
    
    config_code = """
# config/settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # LLM配置
    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    
    # 本地LLM配置
    lm_studio_base_url: str = "http://localhost:1234/v1"
    lm_studio_model: str = "qwen2.5-7b-instruct"
    
    # 向量数据库
    chroma_persist_dir: str = "./chroma_db"
    
    # 应用配置
    log_level: str = "INFO"
    debug: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

# 使用方式
settings = get_settings()
print(settings.openai_model)
"""
    print(config_code)


def demo_llm_wrapper():
    """LLM封装"""
    print("\n" + "=" * 60)
    print("LLM客户端封装")
    print("=" * 60)
    
    wrapper_code = """
# core/llm.py
from langchain_openai import ChatOpenAI
from config.settings import get_settings

class LLMClient:
    '''统一的LLM客户端'''
    
    def __init__(self):
        self.settings = get_settings()
        self._client = None
    
    def get_client(self):
        if self._client is None:
            if self.settings.llm_provider == "local":
                self._client = ChatOpenAI(
                    base_url=self.settings.lm_studio_base_url,
                    api_key="lm-studio",
                    model=self.settings.lm_studio_model
                )
            else:
                self._client = ChatOpenAI(
                    api_key=self.settings.openai_api_key,
                    model=self.settings.openai_model
                )
        return self._client
    
    def chat(self, message):
        client = self.get_client()
        return client.invoke(message)

# 使用方式
llm = LLMClient()
response = llm.chat("你好")
"""
    print(wrapper_code)


def demo_dependency_management():
    """依赖管理"""
    print("\n" + "=" * 60)
    print("依赖管理")
    print("=" * 60)
    
    print("""
requirements.txt 示例：

# 核心依赖
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-community>=0.0.10

# 向量数据库
chromadb>=0.4.0

# 嵌入模型
sentence-transformers>=2.2.0

# 配置管理
pydantic-settings>=2.0.0
python-dotenv>=1.0.0

# 开发工具
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0

# 可选：API服务
fastapi>=0.100.0
uvicorn>=0.23.0

建议：
1. 锁定主要版本号
2. 开发依赖单独列出
3. 定期更新检查安全漏洞
""")


if __name__ == "__main__":
    demo_project_structure()
    demo_config_management()
    demo_llm_wrapper()
    demo_dependency_management()
    
    print("\n" + "=" * 60)
    print("✅ 项目结构学习完成！")
    print("\n关键点：")
    print("  • 模块化：按功能划分目录")
    print("  • 配置分离：环境变量 + pydantic")
    print("  • 封装LLM：便于切换provider")

