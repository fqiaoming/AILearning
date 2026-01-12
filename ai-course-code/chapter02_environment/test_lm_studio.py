"""
第2章-环境配置：LM Studio连接测试
对应课程：第06课-LM-Studio安装

功能：测试LM Studio本地API是否正常工作
前置条件：
  1. LM Studio已启动
  2. 已加载模型（如Qwen2.5-7B）
  3. Local Server已启动
"""

from openai import OpenAI
import time
import sys

# LM Studio默认配置
BASE_URL = "http://localhost:1234/v1"
API_KEY = "lm-studio"  # 本地模型不需要真实key


def test_connection():
    """测试1：连接测试"""
    print("\n" + "=" * 60)
    print("测试1：连接LM Studio")
    print("=" * 60)
    
    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        models = client.models.list()
        
        print("✅ 连接成功！")
        print(f"可用模型：")
        for model in models.data:
            print(f"  - {model.id}")
        return client, models.data[0].id if models.data else None
        
    except Exception as e:
        print(f"❌ 连接失败：{e}")
        print("\n请检查：")
        print("  1. LM Studio是否已启动？")
        print("  2. 是否已加载模型？")
        print("  3. Local Server是否在运行？")
        return None, None


def test_basic_chat(client, model_id):
    """测试2：基础对话"""
    print("\n" + "=" * 60)
    print("测试2：基础对话能力")
    print("=" * 60)
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": "什么是AI大模型？用一句话回答"}
            ],
            temperature=0.7
        )
        
        print(f"问题：什么是AI大模型？用一句话回答")
        print(f"回答：{response.choices[0].message.content}")
        print(f"Token使用：{response.usage.total_tokens}")
        return True
        
    except Exception as e:
        print(f"❌ 对话失败：{e}")
        return False


def test_code_generation(client, model_id):
    """测试3：代码生成"""
    print("\n" + "=" * 60)
    print("测试3：代码生成能力")
    print("=" * 60)
    
    prompt = """请用Python实现一个函数，计算斐波那契数列的第n项。
要求：使用递归实现，添加详细注释"""
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "你是一个专业的Python程序员"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # 代码生成用较低温度
        )
        
        print(f"任务：{prompt}")
        print(f"\n生成的代码：")
        print(response.choices[0].message.content)
        return True
        
    except Exception as e:
        print(f"❌ 代码生成失败：{e}")
        return False


def test_stream_response(client, model_id):
    """测试4：流式响应"""
    print("\n" + "=" * 60)
    print("测试4：流式响应（实时输出）")
    print("=" * 60)
    
    try:
        print("问题：介绍一下Python语言的特点，100字以内")
        print("回答：", end="", flush=True)
        
        stream = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": "介绍一下Python语言的特点，100字以内"}
            ],
            temperature=0.7,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                time.sleep(0.02)  # 模拟打字效果
        
        print()  # 换行
        return True
        
    except Exception as e:
        print(f"\n❌ 流式响应失败：{e}")
        return False


def test_different_temperatures(client, model_id):
    """测试5：不同temperature参数对比"""
    print("\n" + "=" * 60)
    print("测试5：Temperature参数对比")
    print("=" * 60)
    
    prompt = "给我的AI学习项目起一个有创意的名字"
    temperatures = [0.1, 0.5, 0.9]
    
    try:
        for temp in temperatures:
            print(f"\n【Temperature = {temp}】")
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=100
            )
            print(f"回答：{response.choices[0].message.content}")
            print("-" * 40)
        return True
        
    except Exception as e:
        print(f"❌ Temperature测试失败：{e}")
        return False


def main():
    """主函数"""
    print("\n" + "🚀" * 25)
    print("      LM Studio 本地API测试      ")
    print("🚀" * 25)
    print(f"\nAPI地址：{BASE_URL}")
    
    # 测试连接
    client, model_id = test_connection()
    
    if not client or not model_id:
        print("\n❌ 无法连接到LM Studio，测试终止")
        sys.exit(1)
    
    print(f"使用模型：{model_id}")
    
    # 运行所有测试
    results = []
    results.append(("基础对话", test_basic_chat(client, model_id)))
    results.append(("代码生成", test_code_generation(client, model_id)))
    results.append(("流式响应", test_stream_response(client, model_id)))
    results.append(("Temperature对比", test_different_temperatures(client, model_id)))
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 测试结果总结")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\n总计：{passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 LM Studio配置完全正确！")
        print("\n💡 总结：")
        print("  1. 本地模型完全可用，效果不错")
        print("  2. 提示词工程很重要，好的提示词=好的输出")
        print("  3. temperature参数影响输出的创造性")
        print("  4. 流式输出提升用户体验")
        print("  5. API接口与OpenAI完全兼容")
    else:
        print("\n⚠️ 部分测试未通过，请检查LM Studio配置")


if __name__ == "__main__":
    main()

