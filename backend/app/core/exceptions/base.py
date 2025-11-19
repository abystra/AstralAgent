"""
异常基类

符合主流大厂规范：
- 统一错误码（数字）
- 标准响应格式
- 国际化支持
- 敏感信息保护
"""

from typing import Optional, Dict, Any
import traceback
import os
from app.core.exceptions.error_codes import ErrorCode, get_http_status
from app.core.exceptions.i18n import Language, get_error_message


class AstralException(Exception):
    """
    AstralAgent 异常基类
    
    所有自定义异常都应继承此类
    
    特性：
    - 统一错误码（数字枚举）
    - 国际化支持
    - 敏感信息过滤
    - 环境区分（开发/生产）
    """
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
        language: Language = Language.ZH_CN
    ):
        """
        初始化异常
        
        Args:
            error_code: 错误码（使用 ErrorCode 枚举）
            message: 自定义错误消息（可选，优先级最高）
            details: 错误详情（仅开发环境显示）
            cause: 原始异常
            language: 语言
        """
        self.error_code = error_code
        self.language = language
        self.details = details or {}
        self.cause = cause
        
        # 获取错误消息（优先使用自定义消息）
        self.message = get_error_message(error_code, language, message)
        
        # 获取 HTTP 状态码
        self.http_status = get_http_status(error_code)
        
        # 保存堆栈跟踪（仅开发环境）
        if self._is_debug_mode():
            self.traceback_str = ''.join(traceback.format_tb(self.__traceback__))
        else:
            self.traceback_str = None
        
        super().__init__(self.message)
    
    def _is_debug_mode(self) -> bool:
        """检查是否为调试模式"""
        return os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    
    def to_dict(self, include_sensitive: bool = None) -> Dict[str, Any]:
        """
        转换为标准错误响应格式
        
        参考 RFC 7807 和主流大厂规范
        
        Args:
            include_sensitive: 是否包含敏感信息（None 则根据环境自动判断）
            
        Returns:
            标准错误响应字典
            
        格式：
        {
            "code": 10001,  # 业务错误码
            "message": "参数无效",  # 错误消息（国际化）
            "success": false,  # 请求是否成功
            "data": null,  # 数据字段（错误时为 null）
            "timestamp": 1700000000,  # 时间戳
            "request_id": "xxx",  # 请求 ID（从 context 获取）
            "details": {...}  # 错误详情（仅开发环境）
        }
        """
        import time
        from contextvars import ContextVar
        
        # 获取 request_id（从 context）
        request_id_var: ContextVar[str] = ContextVar('request_id', default='')
        request_id = request_id_var.get() or "unknown"
        
        # 判断是否包含敏感信息
        if include_sensitive is None:
            include_sensitive = self._is_debug_mode()
        
        # 基础响应
        response = {
            "code": int(self.error_code),
            "message": self.message,
            "success": False,
            "data": None,
            "timestamp": int(time.time()),
            "request_id": request_id,
        }
        
        # 开发环境：包含详细信息
        if include_sensitive:
            if self.details:
                response["details"] = self._filter_sensitive_data(self.details)
            
            if self.cause:
                response["cause"] = {
                    "type": type(self.cause).__name__,
                    "message": str(self.cause),
                }
            
            if self.traceback_str:
                response["traceback"] = self.traceback_str
        
        return response
    
    def _filter_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        过滤敏感数据
        
        Args:
            data: 原始数据
            
        Returns:
            过滤后的数据
        """
        # 敏感字段列表
        sensitive_keys = {
            "password", "passwd", "pwd",
            "secret", "token", "key",
            "api_key", "apikey", "access_key",
            "private_key", "credential", "auth",
        }
        
        filtered = {}
        for key, value in data.items():
            # 检查键名是否包含敏感词
            key_lower = key.lower()
            is_sensitive = any(sensitive in key_lower for sensitive in sensitive_keys)
            
            if is_sensitive:
                # 脱敏处理
                filtered[key] = "***"
            elif isinstance(value, dict):
                # 递归过滤嵌套字典
                filtered[key] = self._filter_sensitive_data(value)
            else:
                filtered[key] = value
        
        return filtered
    
    def get_http_status(self) -> int:
        """获取 HTTP 状态码"""
        return self.http_status
    
    def __str__(self) -> str:
        """字符串表示"""
        cause_str = f", caused by: {self.cause}" if self.cause else ""
        return f"[{self.error_code}] {self.message}{cause_str}"
    
    def __repr__(self) -> str:
        """调试表示"""
        return (
            f"{self.__class__.__name__}("
            f"error_code={self.error_code}, "
            f"message={self.message!r}, "
            f"http_status={self.http_status})"
        )

