"""配置提供者抽象接口"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Optional


class ConfigProvider(ABC):
    """配置提供者抽象基类"""
    
    def __init__(self, priority: int = 0):
        """
        初始化配置提供者
        
        Args:
            priority: 优先级，数字越大优先级越高
        """
        self._priority = priority
    
    @property
    def priority(self) -> int:
        """获取优先级"""
        return self._priority
    
    @abstractmethod
    async def load(self) -> Dict[str, Any]:
        """
        加载配置
        
        Returns:
            配置字典
        """
        raise NotImplementedError
    
    async def watch(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        监听配置变化（可选实现）
        
        Args:
            callback: 配置变化时的回调函数
        """
        pass  # 默认不支持监听
    
    async def close(self) -> None:
        """关闭配置提供者（清理资源）"""
        pass  # 默认无需清理
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(priority={self.priority})"

