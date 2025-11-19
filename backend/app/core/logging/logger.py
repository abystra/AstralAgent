"""
结构化日志器

基于 structlog 实现
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any, Dict, Optional
import structlog
from structlog.types import Processor
from pythonjsonlogger import jsonlogger


def setup_logging(
    level: str = "INFO",
    log_dir: Optional[Path] = None,
    json_output: bool = False,
    enable_console: bool = True
) -> None:
    """
    设置日志系统
    
    Args:
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        log_dir: 日志文件目录（None 则不输出到文件）
        json_output: 是否输出 JSON 格式
        enable_console: 是否输出到控制台
    """
    # 配置标准库日志
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
        handlers=[]
    )
    
    # 处理器列表
    handlers = []
    
    # 控制台处理器
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        if json_output:
            formatter = jsonlogger.JsonFormatter(
                "%(timestamp)s %(level)s %(name)s %(message)s"
            )
            console_handler.setFormatter(formatter)
        handlers.append(console_handler)
    
    # 文件处理器
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 普通日志文件
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=100 * 1024 * 1024,  # 100MB
            backupCount=10,
        )
        
        # JSON 日志文件
        json_file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.json.log",
            maxBytes=100 * 1024 * 1024,  # 100MB
            backupCount=10,
        )
        json_formatter = jsonlogger.JsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s"
        )
        json_file_handler.setFormatter(json_formatter)
        
        handlers.extend([file_handler, json_file_handler])
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.handlers = handlers
    
    # 配置 structlog
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(
            structlog.dev.ConsoleRenderer(colors=True)
        )
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """
    获取日志器
    
    Args:
        name: 日志器名称（通常使用 __name__）
        
    Returns:
        结构化日志器
    """
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    """
    绑定上下文到当前线程/协程
    
    Args:
        **kwargs: 上下文键值对
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_context(*keys: str) -> None:
    """
    解绑上下文
    
    Args:
        *keys: 要解绑的键
    """
    structlog.contextvars.unbind_contextvars(*keys)


def clear_context() -> None:
    """清空所有上下文"""
    structlog.contextvars.clear_contextvars()

