@echo off
REM AI学习环境快速配置脚本 (Windows)

echo 🚀 AI学习环境配置脚本
echo ================================

REM 检查Python版本
echo.
echo 检查Python版本...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python
    echo.
    echo 请从python.org下载并安装Python 3.10-3.12
    pause
    exit /b 1
)

REM 检查是否有旧的虚拟环境
if exist .venv (
    set OLD_ENV_EXISTS=1
)
if exist venv (
    set OLD_ENV_EXISTS=1
)

if defined OLD_ENV_EXISTS (
    echo.
    echo ⚠️ 检测到旧的虚拟环境
    set /p REPLY="是否删除并重新创建？(y/n): "
    if /i "%REPLY%"=="y" (
        echo 删除旧环境...
        if exist .venv rmdir /s /q .venv
        if exist venv rmdir /s /q venv
    ) else (
        echo 保留现有环境
        exit /b 0
    )
)

REM 创建虚拟环境
echo.
echo 创建虚拟环境...
python -m venv .venv

if errorlevel 1 (
    echo ❌ 创建虚拟环境失败
    pause
    exit /b 1
)

echo ✅ 虚拟环境创建成功

REM 激活虚拟环境
echo.
echo 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 升级pip
echo.
echo 升级pip...
python -m pip install --upgrade pip -q

REM 安装依赖
echo.
echo 安装LangChain v1.x及依赖...
echo 这可能需要几分钟，请耐心等待...

pip install -U langchain langchain-openai langchain-community chromadb tiktoken python-dotenv openai -q

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 验证安装
echo.
echo 验证安装...
python -c "import langchain; import langchain_openai; import langchain_core; print('✅ 所有包导入成功')"

if errorlevel 0 (
    echo.
    echo ================================
    echo 🎉 环境配置完成！
    echo.
    echo 下一步：
    echo 1. 激活虚拟环境: .venv\Scripts\activate
    echo 2. 启动LM Studio并开启API服务
    echo 3. 运行测试: python test_all.py
    echo ================================
) else (
    echo.
    echo ❌ 验证失败，请检查错误信息
    pause
    exit /b 1
)

pause

