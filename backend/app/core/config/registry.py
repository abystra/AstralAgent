"""配置注册中心（全局单例）"""

from typing import Optional
from app.core.config.loader import ConfigLoader


class ConfigRegistry:
    """配置注册中心（单例）"""
    
    _instance: Optional['ConfigRegistry'] = None
    _loader: Optional[ConfigLoader] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_loader(cls, loader: ConfigLoader) -> None:
        """
        设置配置加载器
        
        Args:
            loader: 配置加载器实例
        """
        cls._loader = loader
    
    @classmethod
    def get_loader(cls) -> Optional[ConfigLoader]:
        """
        获取配置加载器
        
        Returns:
            配置加载器实例
        """
        return cls._loader
    
    @classmethod
    def get(cls, key: str, default: any = None) -> any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        if cls._loader is None:
            return default
        return cls._loader.get(key, default)
    
    @classmethod
    async def reload(cls) -> None:
        """重新加载配置"""
        if cls._loader:
            await cls._loader.load_all()


# 全局配置注册中心实例
config_registry = ConfigRegistry()

