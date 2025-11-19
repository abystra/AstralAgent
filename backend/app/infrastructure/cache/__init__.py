"""
缓存中间件

基于 Redis 的缓存支持
"""

from app.infrastructure.cache.middleware import CacheMiddleware, RedisMiddleware
from app.infrastructure.cache.client import get_cache_client

__all__ = [
    "CacheMiddleware",
    "RedisMiddleware",
    "get_cache_client",
]

