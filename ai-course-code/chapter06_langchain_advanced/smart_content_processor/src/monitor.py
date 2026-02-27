"""
系统监控组件
对应课程：第36课-第6章综合实战项目

基于LangChain Callback机制，实现请求统计、性能监控、成本估算
涉及知识点：第33课-Callback系统与监控
"""

import time
from datetime import datetime
from langchain.callbacks.base import BaseCallbackHandler

from .config import config


class SystemMonitor(BaseCallbackHandler):
    """
    系统监控 - 基于LangChain Callback
    
    监控指标：
    - 请求数、成功率、错误数
    - 平均响应时间
    - LLM调用次数和耗时
    - Token用量和成本估算
    """

    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "success": 0,
            "errors": 0,
            "total_time": 0.0,
            "llm_calls": 0,
            "llm_time": 0.0,
            "total_tokens": 0,
        }
        self.start_times = {}
        self.request_logs = []

    # ---- Chain 生命周期 ----

    def on_chain_start(self, serialized, inputs, **kwargs):
        """Chain开始执行"""
        run_id = kwargs.get("run_id")
        self.start_times[f"chain_{run_id}"] = time.time()
        self.metrics["total_requests"] += 1

        self.request_logs.append({
            "type": "chain_start",
            "timestamp": datetime.now().isoformat(),
            "run_id": str(run_id),
            "inputs": str(inputs)[:100],
        })

    def on_chain_end(self, outputs, **kwargs):
        """Chain执行成功"""
        run_id = kwargs.get("run_id")
        key = f"chain_{run_id}"

        if key in self.start_times:
            elapsed = time.time() - self.start_times.pop(key)
            self.metrics["total_time"] += elapsed
            self.metrics["success"] += 1

            self.request_logs.append({
                "type": "chain_success",
                "timestamp": datetime.now().isoformat(),
                "run_id": str(run_id),
                "duration": round(elapsed, 3),
            })

            # 慢请求告警
            if elapsed > config.SLOW_REQUEST_THRESHOLD:
                print(f"⚠️  性能告警：请求耗时 {elapsed:.2f}秒（阈值 {config.SLOW_REQUEST_THRESHOLD}秒）")

    def on_chain_error(self, error, **kwargs):
        """Chain执行失败"""
        self.metrics["errors"] += 1
        self.request_logs.append({
            "type": "chain_error",
            "timestamp": datetime.now().isoformat(),
            "error": str(error)[:200],
        })
        print(f"❌ Chain错误：{error}")

    # ---- LLM 生命周期 ----

    def on_llm_start(self, serialized, prompts, **kwargs):
        """LLM调用开始"""
        run_id = kwargs.get("run_id")
        self.start_times[f"llm_{run_id}"] = time.time()
        self.metrics["llm_calls"] += 1

    def on_llm_end(self, response, **kwargs):
        """LLM调用结束"""
        run_id = kwargs.get("run_id")
        key = f"llm_{run_id}"

        if key in self.start_times:
            elapsed = time.time() - self.start_times.pop(key)
            self.metrics["llm_time"] += elapsed

        # 统计token用量
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            self.metrics["total_tokens"] += usage.get("total_tokens", 0)

    # ---- 报告 ----

    def get_dashboard(self) -> str:
        """生成监控面板"""
        total = self.metrics["total_requests"]
        avg_time = self.metrics["total_time"] / total if total > 0 else 0
        success_rate = self.metrics["success"] / total * 100 if total > 0 else 0
        cost = self.metrics["total_tokens"] * 0.0005 / 1000  # 粗略估算

        return f"""
╔════════════════════════════════════════════════════════════╗
║                     系统监控面板                           ║
╠════════════════════════════════════════════════════════════╣
║ 请求：{total}次  成功：{self.metrics['success']}  失败：{self.metrics['errors']}  成功率：{success_rate:.1f}%
║ 平均响应：{avg_time:.2f}秒  LLM调用：{self.metrics['llm_calls']}次
║ LLM总耗时：{self.metrics['llm_time']:.2f}秒
║ Token：{self.metrics['total_tokens']}  成本估算：${cost:.4f}
╚════════════════════════════════════════════════════════════╝"""

    def reset(self):
        """重置所有指标"""
        for key in self.metrics:
            self.metrics[key] = 0
        self.start_times.clear()
        self.request_logs.clear()
