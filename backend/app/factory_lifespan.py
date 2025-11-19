"""
应用生命周期管理

处理启动和关闭事件
"""

from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI

from app.core.config.models import AppConfig
from app.core.logging import get_logger
from app.core.monitoring import get_health_checker, check_system
from app.infrastructure.middleware import get_middleware_manager
from app.infrastructure.database import DatabaseMiddleware
from app.infrastructure.cache import RedisMiddleware


def create_lifespan(config: AppConfig) -> Callable:
    """
    创建生命周期管理器
    
    Args:
        config: 应用配置
        
    Returns:
        生命周期上下文管理器
    """
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """应用生命周期"""
        logger = get_logger(__name__)
        
        # ========== 启动阶段 ==========
        logger.info("Application starting...", env=config.environment)
        
        try:
            # 1. 注册中间件
            await _register_middlewares(config, logger)
            
            # 2. 连接所有中间件
            await _connect_middlewares(logger)
            
            # 3. 注册健康检查
            await _register_health_checks(logger)
            
            logger.info("Application started successfully")
            
            yield
            
            # ========== 关闭阶段 ==========
            logger.info("Application shutting down...")
            
            # 断开所有中间件
            await _disconnect_middlewares(logger)
            
            logger.info("Application shutdown complete")
        
        except Exception as e:
            logger.error(
                "Application lifecycle error",
                error=str(e),
                exc_info=e
            )
            raise
    
    return lifespan


async def _register_middlewares(config: AppConfig, logger) -> None:
    """注册中间件"""
    middleware_manager = get_middleware_manager()
    
    # 数据库中间件
    database_url = getattr(config, 'database_url', None)
    if database_url:
        logger.info("Registering database middleware...")
        try:
            db = DatabaseMiddleware(
                name="database",
                url=database_url,
                pool_size=getattr(config, 'database_pool_size', 10),
                max_overflow=getattr(config, 'database_max_overflow', 20),
                echo=config.debug
            )
            middleware_manager.register(db)
        except Exception as e:
            logger.warning(f"Failed to register database middleware: {e}")
    
    # Redis 中间件
    redis_url = getattr(config, 'redis_url', None)
    if redis_url:
        logger.info("Registering redis middleware...")
        try:
            cache = RedisMiddleware(
                name="cache",
                url=redis_url
            )
            middleware_manager.register(cache)
        except Exception as e:
            logger.warning(f"Failed to register redis middleware: {e}")


async def _connect_middlewares(logger) -> None:
    """连接所有中间件"""
    middleware_manager = get_middleware_manager()
    await middleware_manager.connect_all()
    
    # 列出已连接的中间件
    middlewares = middleware_manager.list_all()
    logger.info(
        f"Connected {len(middlewares)} middleware(s)",
        middlewares=list(middlewares.keys())
    )


async def _disconnect_middlewares(logger) -> None:
    """断开所有中间件"""
    middleware_manager = get_middleware_manager()
    await middleware_manager.disconnect_all()


async def _register_health_checks(logger) -> None:
    """注册健康检查"""
    health_checker = get_health_checker()
    health_checker.register("system", check_system)
    
    logger.info("Health checks registered")

