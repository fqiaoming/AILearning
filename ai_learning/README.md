# AI学习项目环境

这是AI学习课程的代码目录，使用**LangChain v1.x**最新版本。

## ⚠️ 重要提示

**Python版本要求：推荐3.12，也可以3.10-3.11**
- ✅ Python 3.12 - **推荐版本**（所有功能完美支持）
- ✅ Python 3.10-3.11 - 可以使用
- ❌ Python 3.13+ - 不兼容

使用Python 3.12：
```bash
# macOS
brew install python@3.12
/opt/homebrew/bin/python3.12 -m venv .venv

# Ubuntu/Debian  
sudo apt install python3.12 python3.12-venv
python3.12 -m venv .venv

# Windows
# 从python.org下载3.12安装包
py -3.12 -m venv .venv
```

## 📚 参考文档

- [LangChain v1.x 官方文档](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain v1 发布说明](https://docs.langchain.com/oss/python/releases/langchain-v1)
- [LangChain v1 迁移指南](https://docs.langchain.com/oss/python/migrate/langchain-v1)

## 🚀 快速开始

### 0. 快速修复（如果Python版本不对）

如果你的Python是3.13或3.14，运行自动配置脚本：

```bash
# macOS/Linux
./setup_env.sh

# Windows
setup_env.bat
```

脚本会自动检测合适的Python版本并完成所有配置。

### 1. 检查Python版本

```bash
python3 --version
# 应该显示：Python 3.10.x、3.11.x 或 3.12.x
# 如果是3.13+，请运行上面的快速修复脚本
```

### 2. 激活虚拟环境

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. 安装依赖（首次）

```bash
# 升级pip
pip install --upgrade pip

# 安装LangChain v1.x（最新版）
pip install -U langchain
pip install -U langchain-openai
pip install -U langchain-community

# 安装其他工具
pip install -U chromadb
pip install -U tiktoken
pip install -U python-dotenv
pip install -U openai
```

### 4. 验证安装

```bash
# 验证LangChain
python -c "import langchain; print('LangChain版本:', langchain.__version__)"

# 验证langchain-openai（导入测试）
python -c "import langchain_openai; print('langchain-openai 安装成功')"

# 检查Python版本
python -c "import sys; v=sys.version_info; print(f'Python: {v.major}.{v.minor}.{v.micro}')"
```

### 5. 启动LM Studio

确保LM Studio已启动并开启API服务（http://localhost:1234）

### 6. 运行测试

```bash
# 完整测试
python test_all.py

# 或单独测试LangChain
python test_langchain_local.py
```

## 📁 文件说明

- `test_local_llm.py` - 测试OpenAI SDK + LM Studio
- `test_langchain_local.py` - 测试LangChain v1.x + LM Studio  
- `test_all.py` - 完整环境测试（包含Python版本检查）
- `.env` - 配置文件（可选，代码有默认值）

## ⚠️ 版本说明

本课程使用**LangChain v1.x**：
- 版本号：`1.x.x`
- Python要求：**3.10、3.11或3.12**（不支持3.13+）
- 这是官方最新的稳定版本

## ❓ 常见问题

**Q: 所有包都安装成功了吗？**
- **检查**：运行 `python test_all.py`
- **预期**：所有包都应该显示 ✅
- **如果失败**：检查Python版本是否为3.10-3.12

**Q: 报错 ModuleNotFoundError**
- 确保虚拟环境已激活（看到 `(.venv)` 前缀）
- 重新安装：`pip install -U langchain langchain-openai langchain-community chromadb tiktoken python-dotenv openai`

**Q: 为什么推荐Python 3.12？**
- LangChain v1.x完全支持
- chromadb完全兼容
- 所有依赖都能正常安装
- 最稳定的版本选择

**Q: LangChain版本问题**
- 确保安装的是v1.x：`python -c "import langchain; print(langchain.__version__)"`
- 如果版本不对：`pip install -U langchain`

**Q: 无法连接到LM Studio**
- 确保LM Studio已启动
- 确保API服务已开启（Local Server页面）
- 检查端口是否为1234

**Q: 模型响应慢**
- 使用更小的模型（7B而不是14B）
- 使用Q4量化版本
- 如果有GPU，开启GPU加速

## 📖 学习资源

- [LangChain官方文档](https://docs.langchain.com)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangSmith调试工具](https://smith.langchain.com)
