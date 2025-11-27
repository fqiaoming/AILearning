# AI学习环境快速搭建指南

## 🎯 5分钟快速开始

### 1. 安装Python 3.12

```bash
# macOS
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv

# Windows
# 从python.org下载3.12安装包
```

### 2. 创建项目环境

```bash
# 进入项目目录
cd ai_learning

# 创建虚拟环境（macOS）
/opt/homebrew/bin/python3.12 -m venv .venv

# 创建虚拟环境（Linux）
python3.12 -m venv .venv

# 创建虚拟环境（Windows）
python -m venv .venv

# 激活环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install --upgrade pip
pip install -U langchain langchain-openai langchain-community chromadb tiktoken python-dotenv openai
```

### 4. 测试环境

```bash
python test_all.py
```

**预期结果**：
```
✅ langchain                 1.1.0
✅ langchain_openai          已安装
✅ langchain_community       0.4.1
✅ langchain_core            1.1.0
✅ openai                    2.8.1
✅ chromadb                  1.3.5
✅ tiktoken                  0.12.0

🎉 所有测试通过！环境配置完成！
```

## ✅ 完成！

现在你可以：
- 开始学习第一课
- 运行所有课程代码
- 使用本地LM Studio模型
- 使用向量数据库

## 🔧 自动化脚本

如果手动配置有问题，运行自动脚本：

```bash
./setup_env.sh  # macOS/Linux
```

## 📖 详细文档

查看完整的环境搭建指南：`../00-本地模型环境搭建指南.md`

