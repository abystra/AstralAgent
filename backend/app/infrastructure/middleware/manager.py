"""
中间件管理器

统一管理所有中间件的生命周期
"""

from typing import Dict, Optional, Type
import asyncio
from app.infrastructure.middleware.base import Middleware, MiddlewareStatus
from app.core.logging import get_logger


class MiddlewareManager:
    """
    中间件管理器
    
    功能：
    - 注册中间件
    - 统一连接/断开
    - 健康检查
    - 优雅关闭
    """
    
    def __init__(self):
        self._middlewares: Dict[str, Middleware] = {}
        self._logger = get_logger(__name__)
    
    def register(
        self,
        middleware: Middleware,
        auto_connect: bool = False
    ) -> None:
        """
        注册中间件
        
        Args:
            middleware: 中间件实例
            auto_connect: 是否自动连接
        """
        if middleware.name in self._middlewares:
            self._logger.warning(
                f"Middleware '{middleware.name}' already registered, replacing"
            )
        
        self._middlewares[middleware.name] = middleware
        self._logger.info(f"Registered middleware: {middleware.name}")
        
        if auto_connect:
            # 注意：这里不能直接 await，需要在异步上下文中调用
            self._logger.debug(f"Auto-connect flag set for: {middleware.name}")
    
    def get(self, name: str) -> Optional[Middleware]:
        """
        获取中间件
        
        Args:
            name: 中间件名称
            
        Returns:
            中间件实例，如果不存在返回 None
        """
        return self._middlewares.get(name)
    
    async def connect_all(self) -> None:
        """连接所有中间件"""
        self._logger.info("Connecting all middlewares...")
        
        tasks = []
        for middleware in self._middlewares.values():
            if not middleware.is_connected:
                tasks.append(self._connect_middleware(middleware))
        
        if tasks:
            # 使用 return_exceptions=True 允许部分中间件连接失败
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 统计成功和失败的中间件
            success_count = sum(1 for r in results if not isinstance(r, Exception))
            failed_count = len(results) - success_count
            
            if failed_count > 0:
                self._logger.warning(
                    f"Some middlewares failed to connect: {success_count} succeeded, {failed_count} failed"
                )
        
        self._logger.info("All middlewares connection attempt completed")
    
    async def disconnect_all(self) -> None:
        """断开所有中间件"""
        self._logger.info("Disconnecting all middlewares...")
        
        tasks = []
        for middleware in self._middlewares.values():
            if middleware.is_connected:
                tasks.append(self._disconnect_middleware(middleware))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self._logger.info("All middlewares disconnected")
    
    async def health_check_all(self) -> Dict[str, bool]:
        """
        检查所有中间件的健康状态
        
        Returns:
            中间件名称到健康状态的映射
        """
        results = {}
        
        for name, middleware in self._middlewares.items():
            try:
                if middleware.is_connected:
                    is_healthy = await middleware.health_check()
                    results[name] = is_healthy
                else:
                    results[name] = False
            except Exception as e:
                self._logger.error(
                    f"Health check failed for {name}: {e}",
                    exc_info=e
                )
                results[name] = False
        
        return results
    
    async def _connect_middleware(self, middleware: Middleware) -> None:
        """连接单个中间件"""
        try:
            self._logger.info(f"Connecting middleware: {middleware.name}")
            await middleware.connect()
            middleware._set_status(MiddlewareStatus.CONNECTED)
            self._logger.info(f"Connected middleware: {middleware.name}")
        except Exception as e:
            self._logger.error(
                f"Failed to connect middleware {middleware.name}: {e}",
                exc_info=e
            )
            middleware._set_status(MiddlewareStatus.ERROR, e)
            raise
    
    async def _disconnect_middleware(self, middleware: Middleware) -> None:
        """断开单个中间件"""
        try:
            self._logger.info(f"Disconnecting middleware: {middleware.name}")
            await middleware.disconnect()
            middleware._set_status(MiddlewareStatus.DISCONNECTED)
            self._logger.info(f"Disconnected middleware: {middleware.name}")
        except Exception as e:
            self._logger.error(
                f"Failed to disconnect middleware {middleware.name}: {e}",
                exc_info=e
            )
            middleware._set_status(MiddlewareStatus.ERROR, e)
    
    def list_all(self) -> Dict[str, Middleware]:
        """列出所有中间件"""
        return self._middlewares.copy()


# 全局中间件管理器
_middleware_manager = MiddlewareManager()


def get_middleware_manager() -> MiddlewareManager:
    """获取全局中间件管理器"""
    return _middleware_manager

