![工程化架构](./images/engineering.svg)
*图：工程化架构*

# 第126课：FastAPI实战 - 构建生产级API服务

> **本课目标**：掌握FastAPI生产级开发的最佳实践
> 
> **核心技能**：API设计、性能优化、错误处理、生产部署
> 
> **学习时长**：90分钟

---

## 📖 口播文案（8分钟）
![Monitoring](./images/monitoring.svg)
*图：Monitoring*


### 🎯 前言

"进入工程化阶段！今天学**FastAPI生产级开发**！

**为什么是FastAPI？**

```
市场数据（2024）：
• GitHub Stars：70K+
• 采用率：Top 3 Python Web框架
• 性能：仅次于Go/Rust框架
• 开发速度：提升2-3倍

AI项目首选：
✓ 异步支持（高并发）
✓ 自动文档（Swagger/ReDoc）
✓ 类型提示（减少Bug）
✓ 性能优秀（Starlette + Pydantic）

大厂都在用！
```

**生产级 vs 玩具级的区别：**

```
玩具级（Demo）：
@app.post("/predict")
def predict(data: dict):
    result = model.predict(data)
    return {"result": result}

✗ 无错误处理
✗ 无输入验证
✗ 无日志
✗ 无监控
✗ 崩溃影响全局

生产级（Production）：
@app.post("/predict")
@limiter.limit("100/minute")
async def predict(
    request: PredictRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> PredictResponse:
    try:
        # 输入验证（Pydantic）
        validated_data = request.dict()
        
        # 业务逻辑
        result = await model_service.predict(validated_data)
        
        # 异步日志
        background_tasks.add_task(log_prediction, result)
        
        # 结构化响应
        return PredictResponse(
            success=True,
            data=result,
            request_id=generate_id()
        )
    
    except ValidationError as e:
        logger.warning(f"验证失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except ModelError as e:
        logger.error(f"模型错误：{e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用")

✓ 完整错误处理
✓ 输入验证
✓ 限流保护
✓ 异步处理
✓ 结构化日志
✓ 优雅降级

天壤之别！
```

**生产级API的7个要素：**

```
1. 输入验证（Pydantic）
   • 类型检查
   • 数据清洗
   • 业务规则

2. 错误处理
   • 全局异常捕获
   • 自定义异常
   • 友好错误信息

3. 日志系统
   • 结构化日志
   • 请求追踪
   • 性能监控

4. 认证鉴权
   • JWT Token
   • API Key
   • OAuth2

5. 限流防护
   • IP限流
   • 用户限流
   • 熔断降级

6. 文档完善
   • 自动生成
   • 示例完整
   • 版本管理

7. 性能优化
   • 异步处理
   • 连接池
   • 缓存策略

缺一不可！
```

**性能优化的关键点：**

```
【同步 vs 异步】

同步（阻塞）：
def get_user(user_id):
    user = db.query(User).get(user_id)  # 阻塞
    profile = api.get_profile(user_id)  # 阻塞
    return {"user": user, "profile": profile}

QPS: ~100

异步（非阻塞）：
async def get_user(user_id):
    user, profile = await asyncio.gather(
        db_async.get_user(user_id),
        api_async.get_profile(user_id)
    )
    return {"user": user, "profile": profile}

QPS: ~1000+（10倍提升！）

【数据库连接池】

差的实践：
def query_data():
    conn = psycopg2.connect(...)  # 每次新建
    result = conn.execute(query)
    conn.close()

✗ 连接开销大
✗ 并发性能差

好的实践：
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)

✓ 连接复用
✓ 并发友好
✓ 自动重连
```

**今天这一课，我要带你：**

**第一部分：项目结构**
- 标准项目结构
- 配置管理
- 依赖注入

**第二部分：核心功能**
- 请求验证
- 响应序列化
- 错误处理

**第三部分：进阶特性**
- 异步处理
- 后台任务
- 中间件

**第四部分：生产优化**
- 性能优化
- 安全加固
- 监控日志

从Demo到生产！"

---

## 📚 第一部分：生产级项目结构

### 一、标准目录结构

```bash
fastapi-production/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── dependencies.py      # 依赖注入
│   │
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py
│   │   │   ├── users.py
│   │   │   └── health.py
│   │
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── request.py       # 请求模型
│   │   ├── response.py      # 响应模型
│   │   └── database.py      # 数据库模型
│   │
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── prediction.py
│   │   └── user.py
│   │
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py      # 安全相关
│   │   ├── logging.py       # 日志配置
│   │   └── exceptions.py    # 自定义异常
│   │
│   ├── middleware/          # 中间件
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── rate_limit.py
│   │   └── cors.py
│   │
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── helpers.py
│
├── tests/                   # 测试
│   ├── test_api.py
│   └── test_services.py
│
├── requirements.txt         # 依赖
├── .env                     # 环境变量
├── Dockerfile              # Docker配置
└── README.md
```

### 二、配置管理（config.py）

```python
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    
    # 应用设置
    APP_NAME: str = "AI API Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 服务器设置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # 数据库设置
    DATABASE_URL: str = "postgresql://user:pass@localhost/db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    
    # Redis设置
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600
    
    # 安全设置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 限流设置
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # 模型设置
    MODEL_PATH: str = "./models"
    MODEL_DEVICE: str = "cuda"
    MODEL_BATCH_SIZE: int = 32
    
    # 日志设置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # CORS设置
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # 监控设置
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """获取配置（单例）"""
    return Settings()

# 使用示例
settings = get_settings()
```

---

## 💻 第二部分：核心API实现

### 一、请求/响应模型（models/request.py）

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class PredictRequest(BaseModel):
    """预测请求"""
    
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="输入文本"
    )
    
    model_name: str = Field(
        default="default",
        description="模型名称"
    )
    
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="生成温度"
    )
    
    max_tokens: int = Field(
        default=100,
        ge=1,
        le=2000,
        description="最大token数"
    )
    
    @validator('text')
    def validate_text(cls, v):
        """验证文本"""
        if not v.strip():
            raise ValueError('文本不能为空')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "text": "请解释什么是机器学习",
                "model_name": "gpt-3.5",
                "temperature": 0.7,
                "max_tokens": 500
            }
        }

class PredictResponse(BaseModel):
    """预测响应"""
    
    success: bool = Field(description="是否成功")
    data: Optional[dict] = Field(default=None, description="结果数据")
    message: str = Field(default="", description="消息")
    request_id: str = Field(description="请求ID")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "result": "机器学习是...",
                    "tokens_used": 150
                },
                "message": "预测成功",
                "request_id": "req_abc123",
                "timestamp": "2024-01-15T10:30:00"
            }
        }
```

### 二、主应用（main.py）

```python
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import uuid

from app.config import get_settings
from app.api.v1 import predict, users, health
from app.core.logging import setup_logging
from app.core.exceptions import APIException
from app.middleware.rate_limit import RateLimitMiddleware

settings = get_settings()

# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    
    # 启动时
    print("🚀 应用启动中...")
    setup_logging()
    # 加载模型
    # await load_models()
    print("✓ 应用已就绪")
    
    yield
    
    # 关闭时
    print("🛑 应用关闭中...")
    # 清理资源
    print("✓ 资源已清理")

# 创建应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip压缩
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 自定义中间件：请求追踪
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """添加请求ID"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# 自定义中间件：日志
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录请求"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"[{request.state.request_id}]"
    )
    
    response = await call_next(request)
    
    logger.info(
        f"Response: {response.status_code} "
        f"[{request.state.request_id}]"
    )
    
    return response

# 全局异常处理
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """API异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "detail": exc.detail,
            "request_id": request.state.request_id
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """验证异常处理"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "输入验证失败",
            "detail": exc.errors(),
            "request_id": request.state.request_id
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"未处理的异常：{exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "服务器内部错误",
            "request_id": request.state.request_id
        }
    )

# 注册路由
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])
app.include_router(predict.router, prefix="/api/v1", tags=["预测"])
app.include_router(users.router, prefix="/api/v1", tags=["用户"])

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
        log_level=settings.LOG_LEVEL.lower()
    )
```

### 三、预测API（api/v1/predict.py）

```python
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.models.request import PredictRequest
from app.models.response import PredictResponse
from app.services.prediction import PredictionService
from app.dependencies import get_prediction_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=PredictResponse)
async def predict(
    request: PredictRequest,
    background_tasks: BackgroundTasks,
    service: PredictionService = Depends(get_prediction_service)
):
    """
    预测接口
    
    - **text**: 输入文本
    - **model_name**: 模型名称
    - **temperature**: 生成温度
    - **max_tokens**: 最大token数
    """
    
    try:
        # 执行预测
        result = await service.predict(
            text=request.text,
            model_name=request.model_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # 后台任务：记录日志
        background_tasks.add_task(
            log_prediction,
            request.text,
            result
        )
        
        return PredictResponse(
            success=True,
            data=result,
            message="预测成功",
            request_id=generate_request_id()
        )
    
    except ValueError as e:
        logger.warning(f"输入错误：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"预测失败：{e}", exc_info=True)
        raise HTTPException(status_code=500, detail="预测服务暂时不可用")

def log_prediction(text: str, result: dict):
    """记录预测日志"""
    logger.info(f"预测记录：输入长度={len(text)}, 结果={result}")

def generate_request_id() -> str:
    """生成请求ID"""
    import uuid
    return f"req_{uuid.uuid4().hex[:12]}"
```

---

## 📝 课后总结

### 核心收获

1. **项目结构**
   - 标准化目录
   - 配置管理
   - 模块划分

2. **核心功能**
   - 请求验证
   - 错误处理
   - 中间件

3. **生产特性**
   - 异步处理
   - 日志系统
   - 性能优化

---

## 🚀 下节预告

下一课：**第127课：测试与质量 - 单元测试与集成测试**

- 测试金字塔
- Pytest实战
- 覆盖率分析
- CI集成

**保证代码质量！** 🔥

---

**💪 FastAPI生产实战完成！准备测试！**

**下一课见！** 🎉
