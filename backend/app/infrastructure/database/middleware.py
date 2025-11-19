"""
数据库中间件实现
"""

from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import text

from app.infrastructure.middleware.base import Middleware, MiddlewareStatus
from app.core.logging import get_logger


class DatabaseMiddleware(Middleware):
    """
    数据库中间件
    
    特性：
    - 异步连接池
    - 自动重连
    - 健康检查
    - 会话管理
    """
    
    def __init__(
        self,
        name: str = "database",
        url: str = None,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_timeout: float = 30.0,
        pool_recycle: int = 3600,
        echo: bool = False,
        **kwargs
    ):
        """
        初始化数据库中间件
        
        Args:
            name: 中间件名称
            url: 数据库连接 URL
            pool_size: 连接池大小（会自动转换为 int）
            max_overflow: 连接池最大溢出（会自动转换为 int）
            pool_timeout: 连接超时（会自动转换为 float）
            pool_recycle: 连接回收时间（会自动转换为 int）
            echo: 是否打印 SQL
            **kwargs: 其他配置参数
        """
        # 确保类型正确（从配置读取时可能是字符串）
        config = {
            "url": url,
            "pool_size": int(pool_size) if pool_size is not None else 10,
            "max_overflow": int(max_overflow) if max_overflow is not None else 20,
            "pool_timeout": float(pool_timeout) if pool_timeout is not None else 30.0,
            "pool_recycle": int(pool_recycle) if pool_recycle is not None else 3600,
            "echo": bool(echo) if echo is not None else False,
            **kwargs
        }
        super().__init__(name, config)
        
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._logger = get_logger(__name__)
    
    async def connect(self) -> None:
        """建立数据库连接"""
        try:
            url = self.config["url"]
            if not url:
                raise ValueError("Database URL is required")
            
            # 创建异步引擎
            self._engine = create_async_engine(
                url,
                poolclass=QueuePool,
                pool_size=self.config["pool_size"],
                max_overflow=self.config["max_overflow"],
                pool_timeout=self.config["pool_timeout"],
                pool_recycle=self.config["pool_recycle"],
                echo=self.config["echo"],
                future=True,
            )
            
            # 创建会话工厂
            self._session_factory = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            # 测试连接
            async with self._engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            
            self._set_status(MiddlewareStatus.CONNECTED)
            self._logger.info(f"Database connected: {self.name}")
        
        except Exception as e:
            self._set_status(MiddlewareStatus.ERROR, e)
            self._logger.error(f"Failed to connect database: {e}", exc_info=e)
            raise
    
    async def disconnect(self) -> None:
        """断开数据库连接"""
        try:
            if self._engine:
                await self._engine.dispose()
                self._engine = None
                self._session_factory = None
            
            self._set_status(MiddlewareStatus.DISCONNECTED)
            self._logger.info(f"Database disconnected: {self.name}")
        
        except Exception as e:
            self._set_status(MiddlewareStatus.ERROR, e)
            self._logger.error(f"Failed to disconnect database: {e}", exc_info=e)
            raise
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._engine:
                return False
            
            # 执行简单查询
            async with self._engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                return result is not None
        
        except Exception as e:
            self._logger.warning(f"Database health check failed: {e}")
            return False
    
    def get_session(self) -> AsyncSession:
        """
        获取数据库会话
        
        Returns:
            异步会话对象
        """
        if not self._session_factory:
            raise RuntimeError("Database not connected")
        
        return self._session_factory()
    
    @property
    def engine(self) -> Optional[AsyncEngine]:
        """获取引擎"""
        return self._engine

