"""
异常处理模块（企业级规范版）

特性：
- 统一错误码（数字枚举）
- 国际化支持（i18n）
- 敏感信息保护
- 标准响应格式
- 环境区分
"""

from app.core.exceptions.base import AstralException
from app.core.exceptions.error_codes import ErrorCode, HTTPStatusCode
from app.core.exceptions.i18n import Language, get_error_message, detect_language
from app.core.exceptions.handlers import register_exception_handlers
from app.core.exceptions.api_exceptions import APIException

__all__ = [
    # 核心类
    "AstralException",
    "APIException",
    
    # 错误码
    "ErrorCode",
    "HTTPStatusCode",
    
    # 国际化
    "Language",
    "get_error_message",
    "detect_language",
    
    # 处理器
    "register_exception_handlers",
]

