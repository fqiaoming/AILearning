"""
智能内容处理系统 - 主入口
对应课程：第36课-第6章综合实战项目

整合所有组件：Router路由 + SequentialChain处理 + Memory历史 + Callback监控 + Cache缓存
"""

import time
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.memory import ConversationBufferMemory

from .monitor import SystemMonitor
from .router import SmartRouter
from .config import config


class SmartContentProcessorSystem:
    """
    智能内容处理系统（主入口）
    
    功能：
    - 自动分析文章类型（tech/news/general）
    - 根据类型路由到定制化处理流程
    - 生成摘要、关键词、英文翻译、配图建议
    - 完整的性能监控和成本统计
    - InMemoryCache缓存加速
    - Memory记录处理历史
    """

    def __init__(self, enable_cache: bool = True):
        """
        Args:
            enable_cache: 是否启用LLM缓存
        """
        print("🚀 初始化智能内容处理系统...")

        # 启用缓存
        if enable_cache and config.ENABLE_CACHE:
            set_llm_cache(InMemoryCache())
            print("  ✓ 缓存已启用")

        # 监控组件
        self.monitor = SystemMonitor()
        print("  ✓ 监控系统已启动")

        # 智能路由器
        self.router = SmartRouter()
        print("  ✓ 智能路由器已就绪")

        # Memory（记录处理历史）
        self.memory = ConversationBufferMemory()

        print("  ✓ 系统就绪！\n")

    def process_article(self, article: str, show_progress: bool = True) -> dict:
        """
        处理单篇文章（主方法）
        
        Args:
            article: 文章内容
            show_progress: 是否显示处理进度
            
        Returns:
            处理结果dict，失败返回None
        """
        start_time = time.time()

        if show_progress:
            print(f"{'=' * 60}")
            print(f"📝 处理新文章（{len(article)}字）")
            print(f"{'=' * 60}")

        try:
            # 路由并处理
            callbacks = [self.monitor] if config.ENABLE_MONITOR else None
            result = self.router.route_and_process(article, callbacks=callbacks)

            # 记录到Memory
            self.memory.save_context(
                {"input": article[:100] + "..."},
                {"output": f"处理完成：类型={result['article_type']}"},
            )

            elapsed = time.time() - start_time

            if show_progress:
                self._print_result(result, elapsed)

            return result

        except Exception as e:
            print(f"❌ 处理失败：{e}")
            return None

    def batch_process(self, articles: list) -> list:
        """
        批量处理多篇文章
        
        Args:
            articles: 文章列表
            
        Returns:
            处理结果列表
        """
        print(f"📦 批量处理 {len(articles)} 篇文章\n")

        results = []
        for i, article in enumerate(articles, 1):
            print(f"[{i}/{len(articles)}] 处理中...")
            result = self.process_article(article, show_progress=False)
            results.append(result)

            if result:
                print(f"[{i}/{len(articles)}] ✅ 完成（类型：{result['article_type']}）\n")
            else:
                print(f"[{i}/{len(articles)}] ❌ 失败\n")

        success_count = sum(1 for r in results if r is not None)
        print(f"批量处理完成：{success_count}/{len(articles)} 成功\n")

        return results

    def _print_result(self, result: dict, elapsed: float):
        """格式化打印处理结果"""
        print(f"\n✅ 处理完成（{elapsed:.2f}秒）\n")
        print(f"📊 类型：{result['article_type']}")
        print(f"\n📄 摘要：\n   {result.get('summary', 'N/A')}\n")
        print(f"🔖 关键词：{result.get('keywords', 'N/A')}\n")
        print(f"🌐 英文翻译：\n   {result.get('translation', 'N/A')}\n")
        print(f"🖼️  配图建议：\n   {result.get('image_suggestions', 'N/A')}\n")
        print(f"{'=' * 60}\n")

    def get_statistics(self) -> str:
        """获取监控统计面板"""
        return self.monitor.get_dashboard()

    def get_history(self) -> dict:
        """获取处理历史"""
        return self.memory.load_memory_variables({})

    def reset_monitor(self):
        """重置监控指标"""
        self.monitor.reset()
