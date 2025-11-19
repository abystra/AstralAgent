"""API 相关异常（重构版）"""

from typing import Optional, Dict, Any
from app.core.exceptions.base import AstralException
from app.core.exceptions.error_codes import ErrorCode
from app.core.exceptions.i18n import Language


class APIException(AstralException):
    """API 异常基类"""
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
        language: Language = Language.ZH_CN
    ):
        """
        初始化 API 异常
        
        Args:
            error_code: 错误码
            message: 自定义错误消息
            details: 错误详情
            cause: 原始异常
            language: 语言
        """
        super().__init__(error_code, message, details, cause, language)


class ValidationException(APIException):
    """数据验证异常"""
    
    def __init__(
        self,
        message: str = "Validation error",
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        details = details or {}
        if field:
            details["field"] = field
        super().__init__(
            message=message,
            status_code=422,
            code="VALIDATION_ERROR",
            details=details,
            cause=cause
        )


class AuthenticationException(APIException):
    """认证异常"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            status_code=401,
            code="AUTHENTICATION_ERROR",
            details=details,
            cause=cause
        )


class AuthorizationException(APIException):
    """授权异常"""
    
    def __init__(
        self,
        message: str = "Permission denied",
        resource: Optional[str] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        details = details or {}
        if resource:
            details["resource"] = resource
        if action:
            details["action"] = action
        super().__init__(
            message=message,
            status_code=403,
            code="AUTHORIZATION_ERROR",
            details=details,
            cause=cause
        )


class ResourceNotFoundException(APIException):
    """资源不存在异常"""
    
    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        details = details or {}
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id
        super().__init__(
            message=message,
            status_code=404,
            code="RESOURCE_NOT_FOUND",
            details=details,
            cause=cause
        )


class RateLimitException(APIException):
    """限流异常"""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        limit: Optional[int] = None,
        window: Optional[int] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        details = details or {}
        if limit:
            details["limit"] = limit
        if window:
            details["window"] = window
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(
            message=message,
            status_code=429,
            code="RATE_LIMIT_EXCEEDED",
            details=details,
            cause=cause
        )

