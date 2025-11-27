#!/bin/bash
# AI学习环境快速配置脚本

echo "🚀 AI学习环境配置脚本"
echo "================================"

# 检查Python版本
echo ""
echo "检查Python版本..."
PYTHON_CMD=""

# 优先使用Python 3.12，其次3.11、3.10
for cmd in /opt/homebrew/bin/python3.12 python3.12 python3.11 python3.10 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)
        
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ] && [ "$MINOR" -le 12 ]; then
            PYTHON_CMD=$cmd
            echo "✅ 找到Python: $cmd (版本 $VERSION)"
            if [ "$MINOR" -eq 12 ]; then
                echo "👍 Python 3.12 - 推荐版本！"
            fi
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ 错误：未找到Python 3.10-3.12"
    echo ""
    echo "推荐安装Python 3.12："
    echo "macOS: brew install python@3.12"
    echo "Ubuntu: sudo apt install python3.12 python3.12-venv"
    exit 1
fi

# 删除旧的虚拟环境（如果存在）
if [ -d ".venv" ] || [ -d "venv" ]; then
    echo ""
    echo "⚠️  检测到旧的虚拟环境"
    read -p "是否删除并重新创建？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "删除旧环境..."
        rm -rf .venv venv
    else
        echo "保留现有环境"
        exit 0
    fi
fi

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
$PYTHON_CMD -m venv .venv

if [ $? -ne 0 ]; then
    echo "❌ 创建虚拟环境失败"
    exit 1
fi

echo "✅ 虚拟环境创建成功"

# 激活虚拟环境
echo ""
echo "激活虚拟环境..."
source .venv/bin/activate

# 升级pip
echo ""
echo "升级pip..."
pip install --upgrade pip -q

# 安装依赖
echo ""
echo "安装LangChain v1.x及依赖..."
echo "这可能需要几分钟，请耐心等待..."

pip install -U langchain langchain-openai langchain-community \
    chromadb tiktoken python-dotenv openai -q

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 验证安装
echo ""
echo "验证安装..."
python -c "import langchain; import langchain_openai; import langchain_core; print('✅ 所有包导入成功')"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "🎉 环境配置完成！"
    echo ""
    echo "下一步："
    echo "1. 激活虚拟环境: source .venv/bin/activate"
    echo "2. 启动LM Studio并开启API服务"
    echo "3. 运行测试: python test_all.py"
    echo "================================"
else
    echo ""
    echo "❌ 验证失败，请检查错误信息"
    exit 1
fi

