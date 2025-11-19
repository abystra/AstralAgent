"""
依赖注入模块

提供：
- DI 容器
- Provider 管理
- 生命周期管理
- 装饰器支持
"""

from app.core.di.container import DIContainer, Lifecycle
from app.core.di.decorators import injectable, inject

# 全局 DI 容器实例
container = DIContainer()

__all__ = [
    "DIContainer",
    "Lifecycle",
    "injectable",
    "inject",
    "container",
]

