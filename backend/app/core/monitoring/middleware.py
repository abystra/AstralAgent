"""
监控中间件

自动收集请求指标
"""

import time
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.monitoring.metrics import record_request, record_error


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    指标收集中间件
    
    自动记录：
    - 请求总数
    - 请求延迟
    - 错误计数
    """
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """处理请求"""
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 计算耗时
            duration = time.time() - start_time
            
            # 记录指标
            record_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration
            )
            
            # 记录错误（5xx）
            if response.status_code >= 500:
                record_error(
                    error_type="http_5xx",
                    error_code=response.status_code
                )
            
            return response
        
        except Exception as exc:
            # 计算耗时
            duration = time.time() - start_time
            
            # 记录异常
            record_request(
                method=request.method,
                path=request.url.path,
                status_code=500,
                duration=duration
            )
            
            record_error(
                error_type=type(exc).__name__
            )
            
            raise

