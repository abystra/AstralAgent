"""
Redis 缓存中间件实现
"""

from typing import Optional, Any, Dict
from abc import ABC, abstractmethod
import json
import redis.asyncio as aioredis
from redis.asyncio.connection import ConnectionPool

from app.infrastructure.middleware.base import Middleware, MiddlewareStatus
from app.core.logging import get_logger


class CacheMiddleware(Middleware, ABC):
    """
    缓存中间件抽象类
    
    定义统一的缓存接口
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        pass
    
    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """设置缓存"""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        pass
    
    @abstractmethod
    async def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        pass


class RedisMiddleware(CacheMiddleware):
    """
    Redis 中间件
    
    特性：
    - 连接池
    - 自动序列化/反序列化
    - 健康检查
    """
    
    def __init__(
        self,
        name: str = "redis",
        url: str = None,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50,
        decode_responses: bool = True,
        **kwargs
    ):
        """
        初始化 Redis 中间件
        
        Args:
            name: 中间件名称
            url: Redis 连接 URL（优先级最高）
            host: 主机
            port: 端口
            db: 数据库编号
            password: 密码
            max_connections: 最大连接数
            decode_responses: 是否自动解码响应
            **kwargs: 其他配置参数
        """
        config = {
            "url": url,
            "host": host,
            "port": port,
            "db": db,
            "password": password,
            "max_connections": max_connections,
            "decode_responses": decode_responses,
            **kwargs
        }
        super().__init__(name, config)
        
        self._client: Optional[aioredis.Redis] = None
        self._pool: Optional[ConnectionPool] = None
        self._logger = get_logger(__name__)
    
    async def connect(self) -> None:
        """建立 Redis 连接"""
        try:
            # 创建连接池
            if self.config["url"]:
                self._pool = ConnectionPool.from_url(
                    self.config["url"],
                    max_connections=self.config["max_connections"],
                    decode_responses=self.config["decode_responses"],
                )
            else:
                self._pool = ConnectionPool(
                    host=self.config["host"],
                    port=self.config["port"],
                    db=self.config["db"],
                    password=self.config["password"],
                    max_connections=self.config["max_connections"],
                    decode_responses=self.config["decode_responses"],
                )
            
            # 创建客户端
            self._client = aioredis.Redis(connection_pool=self._pool)
            
            # 测试连接
            await self._client.ping()
            
            self._set_status(MiddlewareStatus.CONNECTED)
            self._logger.info(f"Redis connected: {self.name}")
        
        except Exception as e:
            self._set_status(MiddlewareStatus.ERROR, e)
            self._logger.error(f"Failed to connect Redis: {e}", exc_info=e)
            raise
    
    async def disconnect(self) -> None:
        """断开 Redis 连接"""
        try:
            if self._client:
                await self._client.close()
                self._client = None
            
            if self._pool:
                await self._pool.disconnect()
                self._pool = None
            
            self._set_status(MiddlewareStatus.DISCONNECTED)
            self._logger.info(f"Redis disconnected: {self.name}")
        
        except Exception as e:
            self._set_status(MiddlewareStatus.ERROR, e)
            self._logger.error(f"Failed to disconnect Redis: {e}", exc_info=e)
            raise
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._client:
                return False
            
            result = await self._client.ping()
            return result is True
        
        except Exception as e:
            self._logger.warning(f"Redis health check failed: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self._client:
            raise RuntimeError("Redis not connected")
        
        try:
            value = await self._client.get(key)
            if value is None:
                return None
            
            # 尝试 JSON 反序列化
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        
        except Exception as e:
            self._logger.error(f"Failed to get key {key}: {e}", exc_info=e)
            raise
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """设置缓存"""
        if not self._client:
            raise RuntimeError("Redis not connected")
        
        try:
            # 序列化值
            if not isinstance(value, (str, bytes, int, float)):
                value = json.dumps(value)
            
            # 设置键值
            if ttl:
                result = await self._client.setex(key, ttl, value)
            else:
                result = await self._client.set(key, value)
            
            return result is True
        
        except Exception as e:
            self._logger.error(f"Failed to set key {key}: {e}", exc_info=e)
            raise
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self._client:
            raise RuntimeError("Redis not connected")
        
        try:
            result = await self._client.delete(key)
            return result > 0
        
        except Exception as e:
            self._logger.error(f"Failed to delete key {key}: {e}", exc_info=e)
            raise
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self._client:
            raise RuntimeError("Redis not connected")
        
        try:
            result = await self._client.exists(key)
            return result > 0
        
        except Exception as e:
            self._logger.error(f"Failed to check key {key}: {e}", exc_info=e)
            raise
    
    async def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        if not self._client:
            raise RuntimeError("Redis not connected")
        
        try:
            result = await self._client.expire(key, ttl)
            return result is True
        
        except Exception as e:
            self._logger.error(f"Failed to expire key {key}: {e}", exc_info=e)
            raise
    
    @property
    def client(self) -> Optional[aioredis.Redis]:
        """获取 Redis 客户端"""
        return self._client

