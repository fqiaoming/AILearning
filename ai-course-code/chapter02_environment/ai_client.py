"""
第2章-环境配置：统一AI客户端
对应课程：第07课-本地vs云端模型

功能：支持灵活切换本地模型和云端API的统一客户端
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
from enum import Enum
from typing import Optional

# 加载环境变量
load_dotenv()


class ModelProvider(Enum):
    """模型提供商枚举"""
    LOCAL = "local"              # 本地LM Studio
    OPENAI = "openai"            # OpenAI
    DEEPSEEK = "deepseek"        # DeepSeek


class AIClient:
    """统一的AI客户端"""
    
    def __init__(self, provider: ModelProvider = ModelProvider.LOCAL):
        """
        初始化AI客户端
        
        Args:
            provider: 模型提供商
        """
        self.provider = provider
        self._init_client()
    
    def _init_client(self):
        """根据provider初始化对应的客户端"""
        if self.provider == ModelProvider.LOCAL:
            self.client = OpenAI(
                base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
                api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio")
            )
            self.model = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")
            
        elif self.provider == ModelProvider.OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("未配置OPENAI_API_KEY环境变量")
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-3.5-turbo"
            
        elif self.provider == ModelProvider.DEEPSEEK:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("未配置DEEPSEEK_API_KEY环境变量")
            self.client = OpenAI(
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
                api_key=api_key
            )
            self.model = "deepseek-chat"
    
    def chat(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        统一的对话接口
        
        Args:
            user_message: 用户消息
            system_message: 系统消息
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            AI的回复
        """
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
                
        except Exception as e:
            return f"错误：{str(e)}"
    
    def switch_provider(self, provider: ModelProvider):
        """切换模型提供商"""
        self.provider = provider
        self._init_client()
        print(f"✅ 已切换到：{provider.value}")


def demo_switch_models():
    """演示模型切换"""
    print("=" * 60)
    print("AI Client - 灵活切换模型演示")
    print("=" * 60)
    
    # 测试问题
    question = "用一句话解释什么是快速排序算法"
    
    # 测试本地模型
    print("\n【测试1：本地模型 - LM Studio】")
    print(f"问题：{question}")
    
    try:
        client = AIClient(ModelProvider.LOCAL)
        answer = client.chat(question, temperature=0.3)
        print(f"回答：{answer}")
        print(f"成本：0元")
    except Exception as e:
        print(f"本地模型测试失败：{e}")
    
    # 尝试切换到DeepSeek（如果有配置）
    if os.getenv("DEEPSEEK_API_KEY"):
        print("\n" + "-" * 60)
        print("\n【测试2：DeepSeek API】")
        print(f"问题：{question}")
        
        try:
            client = AIClient(ModelProvider.DEEPSEEK)
            answer = client.chat(question, temperature=0.3)
            print(f"回答：{answer}")
            print(f"成本：约0.00001元")
        except Exception as e:
            print(f"DeepSeek测试失败：{e}")
    else:
        print("\n⚠️ 未配置DEEPSEEK_API_KEY，跳过DeepSeek测试")
    
    # 尝试切换到OpenAI（如果有配置）
    if os.getenv("OPENAI_API_KEY"):
        print("\n" + "-" * 60)
        print("\n【测试3：OpenAI GPT-3.5】")
        print(f"问题：{question}")
        
        try:
            client = AIClient(ModelProvider.OPENAI)
            answer = client.chat(question, temperature=0.3)
            print(f"回答：{answer}")
            print(f"成本：约0.0001元")
        except Exception as e:
            print(f"OpenAI测试失败：{e}")
    else:
        print("\n⚠️ 未配置OPENAI_API_KEY，跳过OpenAI测试")


def demo_smart_routing():
    """演示智能路由"""
    print("\n" + "=" * 60)
    print("智能路由演示 - 根据任务复杂度选择模型")
    print("=" * 60)
    
    # 定义不同复杂度的任务
    tasks = [
        {
            "question": "今天星期几？",
            "complexity": "simple",
            "provider": ModelProvider.LOCAL
        },
        {
            "question": "介绍一下Python的列表推导式",
            "complexity": "medium",
            "provider": ModelProvider.LOCAL
        },
    ]
    
    try:
        client = AIClient(ModelProvider.LOCAL)
        
        for i, task in enumerate(tasks, 1):
            print(f"\n【任务{i}】")
            print(f"问题：{task['question']}")
            print(f"复杂度：{task['complexity']}")
            print(f"选择模型：{task['provider'].value}")
            
            # 获取回答
            answer = client.chat(task['question'], max_tokens=200)
            print(f"回答：{answer[:150]}..." if len(answer) > 150 else f"回答：{answer}")
            print("-" * 60)
            
    except Exception as e:
        print(f"智能路由测试失败：{e}")


if __name__ == "__main__":
    # 运行演示
    demo_switch_models()
    demo_smart_routing()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("\n💡 总结：")
    print("  1. 统一的接口设计让切换模型非常简单")
    print("  2. 根据任务复杂度智能选择模型")
    print("  3. 简单任务用本地（0成本）")
    print("  4. 复杂任务用云端（精准投入）")
    print("  5. 这样可以降低80%以上的成本！")

