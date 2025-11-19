"""
缓存客户端获取
"""

from typing import Optional
from app.infrastructure.middleware.manager import get_middleware_manager
from app.infrastructure.cache.middleware import CacheMiddleware


def get_cache_client() -> CacheMiddleware:
    """
    获取缓存客户端
    
    Returns:
        缓存中间件实例
        
    Example:
        cache = get_cache_client()
        await cache.set("key", "value", ttl=60)
        value = await cache.get("key")
    """
    manager = get_middleware_manager()
    cache_middleware = manager.get("cache")
    
    if not cache_middleware:
        raise RuntimeError("Cache middleware not registered")
    
    if not isinstance(cache_middleware, CacheMiddleware):
        raise TypeError("Middleware 'cache' is not CacheMiddleware")
    
    if not cache_middleware.is_connected:
        raise RuntimeError("Cache not connected")
    
    return cache_middleware

