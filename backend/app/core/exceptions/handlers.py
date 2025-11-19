"""
异常处理器

用于 FastAPI 全局异常处理
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from app.core.exceptions.base import AstralException
from app.core.exceptions.error_codes import ErrorCode
from app.core.exceptions.i18n import detect_language

logger = logging.getLogger(__name__)


async def astral_exception_handler(
    request: Request,
    exc: AstralException
) -> JSONResponse:
    """
    处理 AstralException
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSON 响应
    """
    # 记录日志
    logger.error(
        f"AstralException: {exc}",
        extra={
            "error_code": exc.error_code,
            "path": request.url.path,
            "method": request.method,
        },
        exc_info=exc
    )
    
    # 返回标准错误响应
    return JSONResponse(
        status_code=exc.get_http_status(),
        content=exc.to_dict()
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    处理 FastAPI 验证异常
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSON 响应
    """
    # 获取语言
    accept_language = request.headers.get("Accept-Language")
    language = detect_language(accept_language)
    
    # 构造验证错误详情
    details = {
        "validation_errors": []
    }
    
    for error in exc.errors():
        details["validation_errors"].append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    
    # 创建 AstralException
    from app.core.exceptions.i18n import get_error_message
    
    astral_exc = AstralException(
        error_code=ErrorCode.VALIDATION_ERROR,
        message=get_error_message(ErrorCode.VALIDATION_ERROR, language),
        details=details,
        language=language
    )
    
    logger.warning(
        f"Validation error: {details}",
        extra={
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=astral_exc.to_dict()
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    """
    处理 HTTP 异常
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSON 响应
    """
    # 获取语言
    accept_language = request.headers.get("Accept-Language")
    language = detect_language(accept_language)
    
    # 映射 HTTP 状态码到错误码
    error_code_map = {
        400: ErrorCode.INVALID_REQUEST,
        401: ErrorCode.UNAUTHORIZED,
        403: ErrorCode.INSUFFICIENT_PERMISSIONS,
        404: ErrorCode.RESOURCE_NOT_FOUND,
        429: ErrorCode.RATE_LIMIT_EXCEEDED,
        500: ErrorCode.INTERNAL_SERVER_ERROR,
        503: ErrorCode.SERVICE_UNAVAILABLE,
    }
    
    error_code = error_code_map.get(
        exc.status_code,
        ErrorCode.UNKNOWN_ERROR
    )
    
    astral_exc = AstralException(
        error_code=error_code,
        message=str(exc.detail),
        language=language
    )
    
    logger.error(
        f"HTTP exception: {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=astral_exc.to_dict()
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    处理未捕获的异常
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSON 响应
    """
    # 获取语言
    accept_language = request.headers.get("Accept-Language")
    language = detect_language(accept_language)
    
    # 记录详细错误日志
    logger.exception(
        f"Unhandled exception: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
        exc_info=exc
    )
    
    # 创建通用异常
    astral_exc = AstralException(
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        cause=exc,
        language=language
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=astral_exc.to_dict()
    )


def register_exception_handlers(app):
    """
    注册所有异常处理器
    
    Args:
        app: FastAPI 应用实例
    """
    app.add_exception_handler(AstralException, astral_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

