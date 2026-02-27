"""
回复生成测试
对应课程：第15课-提示词工程实战

测试目标：验证回复质量（关键词覆盖、禁用词检查、长度合理性）
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.response_generator import ResponseGenerator
from src.utils import load_test_data


def test_response_quality():
    """测试回复质量"""
    print("=" * 60)
    print("🧪 回复生成质量测试")
    print("=" * 60 + "\n")
    
    generator = ResponseGenerator()
    
    # 加载测试数据
    try:
        test_data = load_test_data("response_test.json")
    except FileNotFoundError:
        print("测试数据文件未找到，使用内置测试数据")
        test_data = [
            {
                "input": "我的订单什么时候到？",
                "intent": "order_query",
                "expected_keywords": ["订单", "查询"],
                "forbidden_words": ["不知道"],
            },
            {
                "input": "我要退货",
                "intent": "refund",
                "expected_keywords": ["退", "抱歉"],
                "forbidden_words": ["不行"],
            },
        ]
    
    total = len(test_data)
    passed = 0
    
    for i, case in enumerate(test_data, 1):
        response = generator.generate(case["input"], case["intent"])
        
        # 检查1：回复不为空
        is_not_empty = len(response) > 0
        
        # 检查2：回复长度合理（20-300字）
        is_length_ok = 20 <= len(response) <= 300
        
        # 检查3：包含期望关键词（至少命中一个）
        keywords = case.get("expected_keywords", [])
        keyword_hits = [kw for kw in keywords if kw in response]
        has_keywords = len(keyword_hits) > 0 if keywords else True
        
        # 检查4：不包含禁用词
        forbidden = case.get("forbidden_words", [])
        forbidden_hits = [fw for fw in forbidden if fw in response]
        no_forbidden = len(forbidden_hits) == 0
        
        # 综合判断
        is_passed = is_not_empty and is_length_ok and has_keywords and no_forbidden
        if is_passed:
            passed += 1
        
        status = "✓" if is_passed else "✗"
        print(f"[{i}/{total}] {status} 意图：{case['intent']}")
        print(f"  输入：{case['input']}")
        print(f"  回复：{response[:80]}{'...' if len(response) > 80 else ''}")
        print(f"  长度：{len(response)}字 {'✓' if is_length_ok else '✗'}")
        print(f"  关键词命中：{keyword_hits or '无'} {'✓' if has_keywords else '✗'}")
        if forbidden_hits:
            print(f"  ⚠️ 包含禁用词：{forbidden_hits}")
        print()
    
    # 汇总
    pass_rate = passed / total
    print("=" * 60)
    print(f"通过率：{pass_rate * 100:.1f}% ({passed}/{total})")
    print("=" * 60)
    
    if pass_rate >= 0.8:
        print("✅ 回复质量测试通过！")
    else:
        print("❌ 回复质量测试未通过，需要优化提示词")
    
    return pass_rate


def test_handoff_responses():
    """测试转人工场景的回复"""
    print("\n" + "=" * 60)
    print("🧪 转人工场景测试")
    print("=" * 60 + "\n")
    
    generator = ResponseGenerator()
    
    # 投诉场景应该包含安抚和转人工的内容
    complaint_cases = [
        "你们太过分了！",
        "我要投诉！叫你们经理来！",
        "什么破服务，再也不买了！",
    ]
    
    for text in complaint_cases:
        response = generator.generate(text, "complaint")
        has_apology = any(w in response for w in ["抱歉", "对不起", "歉意", "理解"])
        
        status = "✓" if has_apology else "✗"
        print(f"{status} 输入：{text}")
        print(f"  回复：{response[:80]}...")
        print(f"  包含安抚语：{'是' if has_apology else '否'}")
        print()


if __name__ == "__main__":
    test_response_quality()
    test_handoff_responses()
