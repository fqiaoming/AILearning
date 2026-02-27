"""
意图识别测试
对应课程：第15课-提示词工程实战

测试目标：验证意图分类器的准确率是否达到90%
"""

import sys
import os
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intent_classifier import IntentClassifier
from src.utils import load_test_data


def test_intent_classification():
    """测试意图分类准确率"""
    print("=" * 60)
    print("🧪 意图识别测试")
    print("=" * 60 + "\n")
    
    classifier = IntentClassifier()
    
    # 加载测试数据
    try:
        test_data = load_test_data("intent_test.json")
    except FileNotFoundError:
        print("测试数据文件未找到，使用内置测试数据")
        test_data = [
            {"input": "我的订单什么时候到？", "expected": "order_query"},
            {"input": "我要退货", "expected": "refund"},
            {"input": "这个手机支持5G吗？", "expected": "product_inquiry"},
            {"input": "你们服务太差了！", "expected": "complaint"},
            {"input": "忘记密码了", "expected": "account"},
            {"input": "今天天气真好", "expected": "other"},
        ]
    
    correct = 0
    total = len(test_data)
    errors = []
    
    for i, case in enumerate(test_data, 1):
        intent, conf = classifier.classify(case["input"])
        is_correct = intent == case["expected"]
        
        if is_correct:
            correct += 1
        else:
            errors.append({
                "input": case["input"],
                "expected": case["expected"],
                "predicted": intent,
            })
        
        status = "✓" if is_correct else "✗"
        print(f"[{i}/{total}] {status}")
        print(f"  输入：{case['input']}")
        print(f"  预期：{case['expected']}")
        print(f"  预测：{intent}（置信度：{conf}）")
        print()
    
    # 汇总结果
    accuracy = correct / total
    print("=" * 60)
    print(f"准确率：{accuracy * 100:.1f}% ({correct}/{total})")
    print("=" * 60)
    
    if accuracy >= 0.9:
        print("✅ 测试通过！准确率达标（目标≥90%）")
    else:
        print("❌ 测试未通过！准确率未达标（目标≥90%）")
        print(f"\n错误案例（{len(errors)}个）：")
        for err in errors:
            print(f"  - 输入：{err['input']}")
            print(f"    预期：{err['expected']}，实际：{err['predicted']}")
    
    return accuracy


if __name__ == "__main__":
    test_intent_classification()
