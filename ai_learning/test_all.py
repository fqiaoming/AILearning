"""完整环境测试脚本"""
import sys

def test_imports():
    """测试所有必需的库是否已安装"""
    print("="*60)
    print("测试1：检查依赖包")
    print("="*60)
    
    # 检查Python版本
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"Python版本: {py_version}")

    if sys.version_info >= (3, 13):
        print(f"⚠️  警告：Python {py_version} 可能不被LangChain v1.x完全支持")
        print(f"   推荐使用Python 3.10-3.12")

    # 必需包（所有课程都需要）
    required_packages = [
        "langchain",
        "langchain_openai",
        "langchain_community",
        "langchain_core",
        "openai",
        "tiktoken",
    ]

    # 可选包（特定课程需要）
    optional_packages = [
        ("chromadb", "向量数据库课程（第41-70课）需要"),
    ]

    all_ok = True

    print("必需包：")
    for package in required_packages:
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "已安装")
            print(f"✅ {package:25s} {version}")
        except ImportError:
            print(f"❌ {package:25s} 未安装")
            all_ok = False
        except Exception as e:
            print(f"❌ {package:25s} 导入异常: {e}")
            all_ok = False

    print(f"\n可选包：")
    for package, note in optional_packages:
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "已安装")
            print(f"✅ {package:25s} {version}")
        except ImportError:
            print(f"⚠️  {package:25s} 未安装 - {note}")
        except Exception as e:
            print(f"⚠️  {package:25s} 导入异常 - {note}")

    return all_ok

def test_local_api():
    """测试LM Studio API连接"""
    print("\n" + "="*60)
    print("测试2：LM Studio API连接")
    print("="*60)

    try:
        import requests
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ LM Studio API连接成功")
            print(f"   可用模型数: {len(models.get('data', []))}")
            return True
        else:
            print(f"❌ LM Studio API响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到LM Studio: {e}")
        print(f"   请确保LM Studio已启动并开启API服务")
        return False

def test_langchain():
    """测试LangChain + 本地模型"""
    print("\n" + "="*60)
    print("测试3：LangChain v1.x + 本地模型")
    print("="*60)

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",
            model="qwen2.5-7b-instruct",
            temperature=0.7,
            timeout=30
        )

        print("正在调用模型...")
        response = llm.invoke([HumanMessage(content="1+1等于几？只回答数字")])

        print(f"✅ LangChain调用成功")
        print(f"   模型回答: {response.content[:50]}")
        return True

    except Exception as e:
        print(f"❌ LangChain调用失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n🚀 开始环境测试...\n")

    results = []

    # 测试1：依赖包
    results.append(("依赖包检查", test_imports()))

    # 测试2：API连接
    results.append(("LM Studio API", test_local_api()))

    # 测试3：LangChain
    results.append(("LangChain调用", test_langchain()))

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name:20s} {status}")

    all_passed = all(result[1] for result in results)

    print("\n" + "="*60)
    if all_passed:
        print("🎉 所有测试通过！环境配置完成！")
        print("✅ 你可以开始学习第一课了！")
    else:
        print("⚠️  部分测试失败，请检查上面的错误信息")
        print("💡 常见问题：")
        print("   1. 确保LM Studio已启动并开启API服务")
        print("   2. 确保虚拟环境已激活")
        print("   3. 确保所有依赖已正确安装")
    print("="*60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())