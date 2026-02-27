"""
第22-25章-工程化：AI应用测试策略
对应课程：第106-107课

AI应用的测试比传统应用更复杂
"""


def demo_testing_challenges():
    """AI测试挑战"""
    print("=" * 60)
    print("AI应用测试的挑战")
    print("=" * 60)
    
    print("""
传统应用测试：
- 输入确定 → 输出确定
- 可以精确断言

AI应用测试的挑战：
- 输入相同，输出可能不同（LLM的随机性）
- 输出是自然语言，难以精确匹配
- 质量是主观的

解决思路：
1. 控制随机性（temperature=0）
2. 使用模糊匹配
3. 分层测试策略
""")


def demo_testing_layers():
    """分层测试"""
    print("\n" + "=" * 60)
    print("分层测试策略")
    print("=" * 60)
    
    print("""
┌─────────────────────────────────────┐
│          端到端测试                  │  少量，验证整体流程
│    (E2E Tests)                      │
├─────────────────────────────────────┤
│          集成测试                    │  中等，验证模块协作
│    (Integration Tests)              │
├─────────────────────────────────────┤
│          单元测试                    │  大量，验证单个函数
│    (Unit Tests)                     │
└─────────────────────────────────────┘

AI应用重点测试：
1. Prompt测试 - 提示词是否有效
2. 工具测试 - 工具是否正确执行
3. 链测试 - 组件串联是否正确
4. 评估测试 - 输出质量是否达标
""")


def demo_unit_test():
    """单元测试示例"""
    print("\n" + "=" * 60)
    print("单元测试示例")
    print("=" * 60)
    
    test_code = """
# tests/test_tools.py
import pytest
from src.tools.calculator import calculate

class TestCalculator:
    def test_addition(self):
        result = calculate("2 + 3")
        assert result == 5
    
    def test_multiplication(self):
        result = calculate("4 * 5")
        assert result == 20
    
    def test_invalid_expression(self):
        with pytest.raises(ValueError):
            calculate("invalid")


# tests/test_prompts.py
from src.prompts.templates import get_qa_prompt

class TestPrompts:
    def test_qa_prompt_contains_context(self):
        prompt = get_qa_prompt()
        assert "{context}" in prompt.template
    
    def test_qa_prompt_contains_question(self):
        prompt = get_qa_prompt()
        assert "{question}" in prompt.template
"""
    print(test_code)


def demo_llm_test():
    """LLM输出测试"""
    print("\n" + "=" * 60)
    print("LLM输出测试")
    print("=" * 60)
    
    llm_test_code = """
# tests/test_llm_output.py
import pytest

class TestLLMOutput:
    '''测试LLM输出质量'''
    
    def test_response_not_empty(self, llm_client):
        '''测试响应不为空'''
        response = llm_client.chat("你好")
        assert response is not None
        assert len(response) > 0
    
    def test_response_in_chinese(self, llm_client):
        '''测试中文问题返回中文'''
        response = llm_client.chat("今天天气怎么样？")
        # 检查是否包含中文字符
        assert any('\\u4e00' <= char <= '\\u9fff' for char in response)
    
    def test_response_relevance(self, llm_client):
        '''测试回答相关性'''
        question = "Python是什么？"
        response = llm_client.chat(question)
        # 相关性检查：回答应该包含某些关键词
        keywords = ["编程", "语言", "程序", "代码", "Python"]
        assert any(kw in response for kw in keywords)
    
    def test_structured_output(self, llm_client):
        '''测试结构化输出'''
        prompt = "列出3个Python优点，用JSON格式返回"
        response = llm_client.chat(prompt)
        # 尝试解析JSON
        import json
        try:
            data = json.loads(response)
            assert isinstance(data, (list, dict))
        except json.JSONDecodeError:
            pytest.fail("输出不是有效的JSON")
"""
    print(llm_test_code)


def demo_evaluation_test():
    """评估测试"""
    print("\n" + "=" * 60)
    print("评估测试（Golden Dataset）")
    print("=" * 60)
    
    eval_code = """
# tests/test_evaluation.py
import pytest

# 黄金数据集：人工标注的正确答案
GOLDEN_DATASET = [
    {
        "question": "Python什么时候发布的？",
        "expected_keywords": ["1991", "Guido"],
        "expected_not": ["错误", "不知道"]
    },
    {
        "question": "1+1等于几？",
        "expected_keywords": ["2"],
        "expected_not": ["3", "4"]
    }
]

class TestEvaluation:
    @pytest.mark.parametrize("test_case", GOLDEN_DATASET)
    def test_golden_dataset(self, llm_client, test_case):
        response = llm_client.chat(test_case["question"])
        
        # 检查应该包含的关键词
        for keyword in test_case["expected_keywords"]:
            assert keyword in response, f"Missing keyword: {keyword}"
        
        # 检查不应该包含的内容
        for keyword in test_case["expected_not"]:
            assert keyword not in response, f"Unexpected: {keyword}"
"""
    print(eval_code)


if __name__ == "__main__":
    demo_testing_challenges()
    demo_testing_layers()
    demo_unit_test()
    demo_llm_test()
    demo_evaluation_test()
    
    print("\n" + "=" * 60)
    print("✅ 测试策略学习完成！")
    print("\n关键点：")
    print("  • 分层测试：单元→集成→端到端")
    print("  • LLM测试：关键词检查、相关性检查")
    print("  • 黄金数据集：人工标注的测试用例")

