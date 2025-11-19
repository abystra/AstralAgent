"""
中间件注册

集中管理所有 FastAPI 中间件
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config.models import AppConfig
from app.core.logging import LoggingMiddleware
from app.core.monitoring import MetricsMiddleware


def register_middlewares(app: FastAPI, config: AppConfig) -> None:
    """
    注册所有中间件
    
    注意：中间件的注册顺序很重要！
    后注册的中间件会先执行（洋葱模型）
    
    执行顺序：Metrics -> Logging -> CORS -> GZip -> 业务逻辑
    
    Args:
        app: FastAPI 应用实例
        config: 应用配置
    """
    # 1. CORS 中间件（最外层，最先处理）
    _register_cors(app, config)
    
    # 2. GZip 压缩（可选，生产环境建议）
    if not config.debug:
        app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # 3. Trusted Host（生产环境）
    if not config.debug and hasattr(config, 'trusted_hosts'):
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=config.trusted_hosts
        )
    
    # 4. 日志中间件（记录请求日志）
    app.add_middleware(LoggingMiddleware)
    
    # 5. 指标收集中间件（最内层，最后执行）
    app.add_middleware(MetricsMiddleware)


def _register_cors(app: FastAPI, config: AppConfig) -> None:
    """注册 CORS 中间件"""
    # 从配置获取 CORS 设置
    allow_origins = getattr(config, 'cors_allow_origins', ["*"])
    allow_credentials = getattr(config, 'cors_allow_credentials', True)
    allow_methods = getattr(config, 'cors_allow_methods', ["*"])
    allow_headers = getattr(config, 'cors_allow_headers', ["*"])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )

