"""
日志中间件

为每个请求添加 request_id 并记录日志
"""

import time
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging.logger import get_logger, bind_context, clear_context


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件
    
    功能：
    - 为每个请求生成唯一 request_id
    - 记录请求日志（路径、方法、耗时、状态码）
    - 绑定上下文到日志
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = get_logger(__name__)
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """处理请求"""
        # 生成 request_id
        request_id = str(uuid.uuid4())
        
        # 绑定上下文
        bind_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )
        
        # 记录请求开始
        start_time = time.time()
        self.logger.info(
            "request_started",
            url=str(request.url),
            headers=dict(request.headers),
        )
        
        try:
            # 将 request_id 添加到请求状态
            request.state.request_id = request_id
            
            # 处理请求
            response = await call_next(request)
            
            # 计算耗时
            duration = time.time() - start_time
            
            # 记录请求完成
            self.logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )
            
            # 添加 request_id 到响应头
            response.headers["X-Request-ID"] = request_id
            
            return response
        
        except Exception as exc:
            # 计算耗时
            duration = time.time() - start_time
            
            # 记录错误
            self.logger.error(
                "request_failed",
                error=str(exc),
                error_type=type(exc).__name__,
                duration_ms=round(duration * 1000, 2),
                exc_info=exc,
            )
            raise
        
        finally:
            # 清理上下文
            clear_context()

