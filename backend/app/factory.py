"""
Application Factory

采用工厂模式创建 FastAPI 应用实例
遵循 Flask 的 App Factory 模式最佳实践
"""

from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_config
from app.core.config.models import AppConfig
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import register_exception_handlers

# 延迟导入，避免循环依赖
from app.factory_middleware import register_middlewares
from app.factory_routes import register_routes
from app.factory_lifespan import create_lifespan


def create_app(
    config: Optional[AppConfig] = None,
    log_level: Optional[str] = None,
    log_dir: Optional[Path] = None,
) -> FastAPI:
    """
    应用工厂函数
    
    Args:
        config: 配置对象（可选，用于测试）
        log_level: 日志级别（可选）
        log_dir: 日志目录（可选）
        
    Returns:
        FastAPI 应用实例
        
    Example:
        # 生产环境
        app = create_app()
        
        # 测试环境
        test_config = AppConfig(debug=True)
        app = create_app(config=test_config)
    """
    # 1. 加载配置
    if config is None:
        config = get_config()
    
    # 2. 初始化日志
    _setup_logging(config, log_level, log_dir)
    
    logger = get_logger(__name__)
    logger.info("Creating FastAPI application...")
    
    # 3. 创建 FastAPI 实例
    app = _create_fastapi_instance(config)
    
    # 4. 注册异常处理器
    register_exception_handlers(app)
    
    # 5. 注册中间件
    register_middlewares(app, config)
    
    # 6. 注册路由
    register_routes(app, config)
    
    logger.info("FastAPI application created successfully")
    
    return app


def _setup_logging(
    config: AppConfig,
    log_level: Optional[str] = None,
    log_dir: Optional[Path] = None
) -> None:
    """设置日志系统"""
    import os
    
    # 优先级：参数 > 环境变量 > 配置
    level = log_level or os.getenv("LOG_LEVEL", config.log_level)
    
    # 日志目录
    if log_dir is None:
        if os.getenv("LOG_TO_FILE") or config.log_to_file:
            log_dir = Path("logs")
    
    # 日志格式
    json_output = (
        os.getenv("LOG_FORMAT", config.log_format).lower() == "json"
    )
    
    setup_logging(
        level=level,
        log_dir=log_dir,
        json_output=json_output,
    )


def _create_fastapi_instance(config: AppConfig) -> FastAPI:
    """创建 FastAPI 实例"""
    return FastAPI(
        title="AstralAgent API",
        description="企业级多智能体平台 - AI-Native Architecture",
        version=config.version,
        lifespan=create_lifespan(config),
        docs_url="/docs" if config.debug else None,
        redoc_url="/redoc" if config.debug else None,
        openapi_url="/openapi.json" if config.debug else None,
    )

