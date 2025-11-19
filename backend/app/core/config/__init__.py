"""
配置管理模块

支持多种配置源：
- 环境变量
- .env 文件
- TOML 文件
- Nacos 配置中心
- Consul 配置中心
"""

from app.core.config.base import ConfigProvider
from app.core.config.loader import ConfigLoader
from app.core.config.registry import ConfigRegistry
from app.core.config.models import (
    AppConfig,
    DatabaseConfig,
    RedisConfig,
    ModelConfig,
    SecurityConfig,
    LoggingConfig,
    MonitoringConfig,
)

# 全局配置实例
_config_instance = None


def get_config() -> AppConfig:
    """
    获取全局配置
    
    使用 Pydantic Settings 直接加载配置（简化实现）
    支持从 .env 文件和环境变量加载
    
    Returns:
        应用配置对象
    """
    global _config_instance
    
    if _config_instance is None:
        # 直接使用 Pydantic Settings 加载配置
        # 它会自动从 .env 文件和环境变量加载
        _config_instance = AppConfig()
    
    return _config_instance


__all__ = [
    "ConfigProvider",
    "ConfigLoader",
    "ConfigRegistry",
    "AppConfig",
    "DatabaseConfig",
    "RedisConfig",
    "ModelConfig",
    "SecurityConfig",
    "LoggingConfig",
    "MonitoringConfig",
    "get_config",
]

