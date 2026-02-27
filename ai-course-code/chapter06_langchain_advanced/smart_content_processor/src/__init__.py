"""
智能内容处理系统 - Smart Content Processor
第6章第36课：综合实战项目

模块说明：
- monitor: 系统监控（Callback）
- analyzer: 文章类型分析器（Router）
- processor: 内容处理Pipeline（SequentialChain）
- router: 智能路由系统
- system: 主系统入口
"""

from .system import SmartContentProcessorSystem

__all__ = ["SmartContentProcessorSystem"]
