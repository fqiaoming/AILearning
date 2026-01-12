"""
第2章-环境配置：环境验证脚本
对应课程：第05课-Python环境配置

功能：验证Python环境是否配置正确
"""

import sys
import subprocess


def check_python_version():
    """检查Python版本"""
    print("=" * 50)
    print("🔍 检查Python版本")
    print("=" * 50)
    
    version = sys.version_info
    print(f"当前版本：Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Python版本符合要求 (3.10+)")
        return True
    else:
        print("⚠️ 建议使用Python 3.10或更高版本")
        return False


def check_packages():
    """检查必要的包是否安装"""
    print("\n" + "=" * 50)
    print("🔍 检查已安装的包")
    print("=" * 50)
    
    required_packages = [
        ("openai", "OpenAI SDK - 调用AI模型"),
        ("python-dotenv", "环境变量管理"),
    ]
    
    optional_packages = [
        ("langchain", "LangChain框架"),
        ("chromadb", "向量数据库"),
        ("fastapi", "Web框架"),
    ]
    
    print("\n必要的包：")
    all_required_installed = True
    for package, desc in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}: 已安装 - {desc}")
        except ImportError:
            print(f"  ❌ {package}: 未安装 - {desc}")
            all_required_installed = False
    
    print("\n可选的包（后续课程会用到）：")
    for package, desc in optional_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}: 已安装 - {desc}")
        except ImportError:
            print(f"  ⬚ {package}: 未安装 - {desc}")
    
    return all_required_installed


def check_virtual_env():
    """检查是否在虚拟环境中"""
    print("\n" + "=" * 50)
    print("🔍 检查虚拟环境")
    print("=" * 50)
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or \
              (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print(f"✅ 正在使用虚拟环境")
        print(f"   路径：{sys.prefix}")
        return True
    else:
        print("⚠️ 未检测到虚拟环境")
        print("   建议：使用虚拟环境隔离项目依赖")
        print("   创建方法：python -m venv venv")
        return False


def main():
    """主函数"""
    print("\n" + "🚀" * 25)
    print("      AI课程环境验证工具      ")
    print("🚀" * 25 + "\n")
    
    # 运行所有检查
    python_ok = check_python_version()
    packages_ok = check_packages()
    venv_ok = check_virtual_env()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 验证结果总结")
    print("=" * 50)
    
    if python_ok and packages_ok:
        print("\n✅ 环境配置正确！可以开始学习了！")
        print("\n下一步：")
        print("  1. 安装LM Studio（第06课）")
        print("  2. 下载本地模型")
        print("  3. 运行 test_lm_studio.py 测试")
    else:
        print("\n⚠️ 部分配置需要完善：")
        if not python_ok:
            print("  - 建议升级Python到3.10+")
        if not packages_ok:
            print("  - 运行: pip install openai python-dotenv")
        if not venv_ok:
            print("  - 建议创建虚拟环境")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

