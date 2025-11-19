"""
中间件抽象层

统一管理数据库、缓存、消息队列等中间件
"""

from app.infrastructure.middleware.base import Middleware
from app.infrastructure.middleware.manager import MiddlewareManager, get_middleware_manager

__all__ = [
    "Middleware",
    "MiddlewareManager",
    "get_middleware_manager",
]

