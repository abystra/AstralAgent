"""
路由注册

集中管理所有 API 路由
"""

from fastapi import FastAPI

from app.core.config.models import AppConfig
from app.core.logging import get_logger
from app.api.v1 import router as v1_router
from app.api.system import create_system_routes


def register_routes(app: FastAPI, config: AppConfig) -> None:
    """
    注册所有路由
    
    Args:
        app: FastAPI 应用实例
        config: 应用配置
    """
    logger = get_logger(__name__)
    
    # 1. 系统路由（根路径、健康检查、指标）
    create_system_routes(app, config)
    
    # 2. API v1 路由
    app.include_router(
        v1_router.router,
        prefix=config.api_v1_prefix
    )
    
    # 3. 未来可扩展的路由
    # app.include_router(v2_router, prefix="/api/v2")
    # app.include_router(admin_router, prefix="/admin")
    
    logger.info(
        "Routes registered",
        api_v1_prefix=config.api_v1_prefix
    )

