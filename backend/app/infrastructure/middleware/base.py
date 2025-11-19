"""
中间件基类

定义统一的中间件接口
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from enum import Enum


class MiddlewareStatus(str, Enum):
    """中间件状态"""
    INITIALIZED = "initialized"  # 已初始化
    CONNECTED = "connected"      # 已连接
    DISCONNECTED = "disconnected"  # 已断开
    ERROR = "error"              # 错误状态


class Middleware(ABC):
    """
    中间件基类
    
    所有中间件都应继承此类并实现以下方法：
    - connect: 建立连接
    - disconnect: 断开连接
    - health_check: 健康检查
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        初始化中间件
        
        Args:
            name: 中间件名称
            config: 配置参数
        """
        self.name = name
        self.config = config
        self._status = MiddlewareStatus.INITIALIZED
        self._error: Optional[Exception] = None
    
    @abstractmethod
    async def connect(self) -> None:
        """
        建立连接
        
        应该在这里初始化连接池、客户端等
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """
        断开连接
        
        应该在这里关闭连接池、释放资源等
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            如果中间件健康返回 True，否则返回 False
        """
        pass
    
    @property
    def status(self) -> MiddlewareStatus:
        """获取状态"""
        return self._status
    
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._status == MiddlewareStatus.CONNECTED
    
    @property
    def error(self) -> Optional[Exception]:
        """获取错误信息"""
        return self._error
    
    def _set_status(self, status: MiddlewareStatus, error: Optional[Exception] = None) -> None:
        """设置状态"""
        self._status = status
        self._error = error
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, status={self._status})"

