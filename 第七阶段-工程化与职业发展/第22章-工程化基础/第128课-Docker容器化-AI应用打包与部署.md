![工程化架构](./images/engineering.svg)
*图：工程化架构*

# 第128课：Docker容器化 - AI应用打包与部署

> **本课目标**：掌握Docker容器化和AI应用部署
> 
> **核心技能**：Dockerfile、多阶段构建、Docker Compose、优化技巧
> 
> **学习时长**：90分钟

---

## 📖 口播文案（8分钟）
![Monitoring](./images/monitoring.svg)
*图：Monitoring*


### 🎯 前言

"代码写好了，测试通过了，如何部署？**Docker！**

**为什么必须用Docker？**

```
传统部署的噩梦：

问题1："在我机器上能跑！"
• 开发环境：Python 3.9
• 测试环境：Python 3.10
• 生产环境：Python 3.8
→ 依赖不兼容，崩溃！

问题2：环境配置地狱
• 安装Python
• 安装CUDA/cuDNN
• 安装系统依赖
• 配置环境变量
→ 2小时配置，5分钟部署

问题3：资源隔离
• 多个应用共享服务器
• 依赖冲突
• 资源抢占
→ A应用崩，B应用也崩

Docker解决：
✓ 环境一致（开发=测试=生产）
✓ 秒级部署（docker run）
✓ 资源隔离（容器互不影响）
✓ 易于扩展（水平扩容）

标准化！
```

**Docker vs 虚拟机：**

```
虚拟机（VM）：

Host OS
├─ Hypervisor
   ├─ Guest OS (2GB)
   │  └─ App
   ├─ Guest OS (2GB)
   │  └─ App
   └─ Guest OS (2GB)
      └─ App

• 笨重（每个几GB）
• 启动慢（分钟级）
• 资源消耗大

Docker容器：

Host OS
├─ Docker Engine
   ├─ Container (100MB)
   │  └─ App
   ├─ Container (100MB)
   │  └─ App
   └─ Container (100MB)
      └─ App

• 轻量（几百MB）
• 启动快（秒级）
• 资源利用高

10-100倍差距！
```

**AI应用Docker化的挑战：**

```
挑战1：镜像大
• Python基础镜像：~1GB
• PyTorch：~2GB
• 模型文件：~5GB
• 总计：>8GB

✗ 下载慢
✗ 存储贵
✗ 部署慢

解决：
✓ 多阶段构建（去除构建依赖）
✓ 层缓存优化（利用缓存）
✓ 模型外置（挂载卷）
→ 减小到~2GB

挑战2：GPU支持
• 需要CUDA运行时
• 需要nvidia-docker
• 显存管理

解决：
✓ 使用nvidia官方镜像
✓ 配置GPU资源限制
✓ 多容器共享GPU

挑战3：性能
• 容器网络开销
• 文件系统开销
• CPU亲和性

解决：
✓ host网络模式
✓ tmpfs内存文件系统
✓ CPU绑定

优化后接近裸机性能！
```

**多阶段构建的威力：**

```
单阶段（臃肿）：

FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

镜像大小：2.5GB
• 包含pip、setuptools
• 包含所有构建工具
• 包含不必要的文件

多阶段（精简）：

# 构建阶段
FROM python:3.9 as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 运行阶段
FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
COPY app.py .
CMD ["python", "app.py"]

镜像大小：800MB
• 只包含运行时依赖
• 去除构建工具
• 使用slim镜像

3倍减小！
```

**今天这一课，我要带你：**

**第一部分：Dockerfile编写**
- 基础镜像选择
- 层优化
- 多阶段构建

**第二部分：Docker Compose**
- 多容器编排
- 网络配置
- 数据卷管理

**第三部分：生产优化**
- 镜像瘦身
- 性能调优
- 安全加固

**第四部分：部署实战**
- 本地部署
- 云端部署
- CI/CD集成

容器化全流程！"

---

## 📚 第一部分：Dockerfile最佳实践

### 一、基础Dockerfile

```dockerfile
# Dockerfile
# 基础镜像选择
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件（利用缓存）
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/

# 创建非root用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 二、多阶段构建（AI应用）

```dockerfile
# Dockerfile.ai
# ============ 构建阶段 ============
FROM python:3.9 as builder

WORKDIR /build

# 复制依赖
COPY requirements.txt .

# 安装到用户目录
RUN pip install --user --no-cache-dir -r requirements.txt

# ============ 运行阶段 ============
FROM python:3.9-slim

WORKDIR /app

# 从构建阶段复制已安装的包
COPY --from=builder /root/.local /root/.local

# 更新PATH
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY app/ ./app/

# 创建模型目录
RUN mkdir -p /app/models

# 非root用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 三、GPU支持Dockerfile

```dockerfile
# Dockerfile.gpu
# 使用NVIDIA官方镜像
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 安装Python
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装PyTorch（GPU版本）
RUN pip3 install --no-cache-dir \
    torch==2.0.0+cu118 \
    torchvision==0.15.0+cu118 \
    --extra-index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制应用
COPY app/ ./app/

# 环境变量
ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

---

## 💻 第二部分：Docker Compose编排

### 一、完整应用栈

```yaml
# docker-compose.yml
version: '3.8'

services:
  # API服务
  api:
    build:
      context: .
      dockerfile: Dockerfile
    image: ai-api:latest
    container_name: ai-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/aidb
      - REDIS_URL=redis://redis:6379/0
      - MODEL_PATH=/models
    volumes:
      - ./models:/models:ro
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    networks:
      - ai-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # PostgreSQL数据库
  postgres:
    image: postgres:15-alpine
    container_name: ai-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=aidb
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - ai-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: ai-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - ai-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: ai-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - ai-network

  # Prometheus监控
  prometheus:
    image: prom/prometheus:latest
    container_name: ai-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    networks:
      - ai-network

  # Grafana可视化
  grafana:
    image: grafana/grafana:latest
    container_name: ai-grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
  prometheus-data:
  grafana-data:
```

### 二、GPU版本Compose

```yaml
# docker-compose.gpu.yml
version: '3.8'

services:
  ai-gpu:
    build:
      context: .
      dockerfile: Dockerfile.gpu
    image: ai-api-gpu:latest
    container_name: ai-api-gpu
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ./models:/models:ro
    ports:
      - "8000:8000"
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge
```

### 三、开发环境Compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  api-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder
    image: ai-api-dev:latest
    container_name: ai-api-dev
    volumes:
      - ./app:/app/app:delegated  # 代码热重载
      - ./models:/models:ro
    ports:
      - "8000:8000"
      - "5678:5678"  # debugpy端口
    environment:
      - DEBUG=true
      - RELOAD=true
    command: >
      uvicorn app.main:app 
      --host 0.0.0.0 
      --reload 
      --reload-dir /app/app
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge
```

---

## 🎯 第三部分：优化与安全

### 一、.dockerignore

```bash
# .dockerignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# 测试
.pytest_cache/
.coverage
htmlcov/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# 文档
*.md
docs/

# 模型（太大，应挂载）
models/
*.pth
*.bin
*.safetensors

# 数据
data/
datasets/
```

### 二、镜像优化

```bash
# build.sh
#!/bin/bash

# 构建优化后的镜像

echo "构建AI API镜像..."

# 多阶段构建
docker build \
  --tag ai-api:latest \
  --tag ai-api:v1.0.0 \
  --build-arg PYTHON_VERSION=3.9 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --file Dockerfile \
  --target production \
  .

echo "✓ 构建完成"

# 查看镜像大小
docker images ai-api:latest

# 扫描安全漏洞
echo "\n扫描安全漏洞..."
docker scan ai-api:latest

# 推送到仓库（可选）
if [ "$1" == "push" ]; then
    echo "\n推送到Docker Hub..."
    docker push ai-api:latest
    docker push ai-api:v1.0.0
fi
```

### 三、运行脚本

```bash
# run.sh
#!/bin/bash

# 启动应用栈

set -e

echo "启动AI应用..."

# 停止旧容器
docker-compose down

# 拉取最新镜像
docker-compose pull

# 启动服务
docker-compose up -d

# 等待服务就绪
echo "等待服务就绪..."
sleep 10

# 健康检查
echo "\n健康检查..."
curl -f http://localhost:8000/health || exit 1

echo "\n✓ 应用已启动"
echo "\nAPI: http://localhost:8000"
echo "文档: http://localhost:8000/docs"
echo "监控: http://localhost:9090"
echo "可视化: http://localhost:3000"

# 查看日志
echo "\n查看日志: docker-compose logs -f"
```

---

## 📝 课后总结

### 核心收获

1. **Dockerfile编写**
   - 基础镜像选择
   - 多阶段构建
   - 层缓存优化

2. **Docker Compose**
   - 多容器编排
   - 网络配置
   - 数据持久化

3. **生产优化**
   - 镜像瘦身
   - GPU支持
   - 安全加固

4. **部署实战**
   - 本地测试
   - 生产部署
   - 监控配置

---

## 🚀 下节预告

下一课：**第129课：性能优化 - 缓存、并发、负载均衡**

- 缓存策略
- 异步优化
- 负载均衡
- 性能监控

**榨干每一滴性能！** 🔥

---

## 📊 **Docker命令速查**

```bash
# 构建
docker build -t image:tag .

# 运行
docker run -d -p 8000:8000 image:tag

# 查看容器
docker ps

# 查看日志
docker logs container-name

# 进入容器
docker exec -it container-name bash

# 停止容器
docker stop container-name

# 删除容器
docker rm container-name

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose ps
docker-compose exec service bash

# 清理
docker system prune -a
```

---

**💪 容器化部署完成！应用可随处运行！**

**下一课见！** 🎉
