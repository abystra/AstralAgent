"""
日志系统

特性：
- 结构化日志（structlog）
- 多输出（控制台、文件、JSON）
- 上下文传递（request_id、user_id）
- 性能监控集成
"""

from app.core.logging.logger import (
    get_logger,
    setup_logging,
    bind_context,
    unbind_context,
)
from app.core.logging.middleware import LoggingMiddleware

__all__ = [
    "get_logger",
    "setup_logging",
    "bind_context",
    "unbind_context",
    "LoggingMiddleware",
]

