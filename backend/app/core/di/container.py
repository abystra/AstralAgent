"""依赖注入容器"""

from typing import Dict, Any, Type, Callable, TypeVar, Optional, get_type_hints
from enum import Enum
import inspect
import asyncio

T = TypeVar('T')


class Lifecycle(Enum):
    """组件生命周期"""
    SINGLETON = "singleton"  # 单例
    TRANSIENT = "transient"  # 瞬态（每次创建新实例）
    SCOPED = "scoped"        # 作用域（暂不实现）


class DIContainer:
    """
    依赖注入容器
    
    功能：
    - 依赖注册
    - 依赖解析
    - 生命周期管理
    - 循环依赖检测
    """
    
    def __init__(self):
        self._providers: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._lifecycle: Dict[Type, Lifecycle] = {}
        self._resolving: set = set()  # 用于检测循环依赖
    
    def register(
        self,
        interface: Type[T],
        implementation: Optional[Type[T] | Callable[[], T]] = None,
        lifecycle: Lifecycle = Lifecycle.SINGLETON,
        instance: Optional[T] = None
    ) -> None:
        """
        注册依赖
        
        Args:
            interface: 接口类型
            implementation: 实现类型或工厂函数
            lifecycle: 生命周期
            instance: 直接注册实例（用于已创建的单例）
        """
        if instance is not None:
            # 直接注册实例
            self._singletons[interface] = instance
            self._lifecycle[interface] = Lifecycle.SINGLETON
            return
        
        if implementation is None:
            # 如果没有提供实现，假设接口本身就是实现
            implementation = interface
        
        self._providers[interface] = implementation
        self._lifecycle[interface] = lifecycle
    
    def resolve(self, interface: Type[T]) -> T:
        """
        解析依赖（同步版本）
        
        Args:
            interface: 接口类型
            
        Returns:
            实例
        """
        # 检查循环依赖
        if interface in self._resolving:
            raise RuntimeError(f"Circular dependency detected: {interface}")
        
        # 检查是否已有单例实例
        if interface in self._singletons:
            return self._singletons[interface]
        
        # 检查是否注册
        if interface not in self._providers:
            raise ValueError(f"No provider registered for {interface}")
        
        lifecycle = self._lifecycle[interface]
        
        # 单例模式
        if lifecycle == Lifecycle.SINGLETON:
            if interface not in self._singletons:
                self._resolving.add(interface)
                try:
                    self._singletons[interface] = self._create_instance(interface)
                finally:
                    self._resolving.discard(interface)
            return self._singletons[interface]
        
        # 瞬态模式
        return self._create_instance(interface)
    
    async def resolve_async(self, interface: Type[T]) -> T:
        """
        解析依赖（异步版本）
        
        Args:
            interface: 接口类型
            
        Returns:
            实例
        """
        # 检查循环依赖
        if interface in self._resolving:
            raise RuntimeError(f"Circular dependency detected: {interface}")
        
        # 检查是否已有单例实例
        if interface in self._singletons:
            return self._singletons[interface]
        
        # 检查是否注册
        if interface not in self._providers:
            raise ValueError(f"No provider registered for {interface}")
        
        lifecycle = self._lifecycle[interface]
        
        # 单例模式
        if lifecycle == Lifecycle.SINGLETON:
            if interface not in self._singletons:
                self._resolving.add(interface)
                try:
                    self._singletons[interface] = await self._create_instance_async(interface)
                finally:
                    self._resolving.discard(interface)
            return self._singletons[interface]
        
        # 瞬态模式
        return await self._create_instance_async(interface)
    
    def _create_instance(self, interface: Type[T]) -> T:
        """
        创建实例（同步版本）
        
        Args:
            interface: 接口类型
            
        Returns:
            实例
        """
        provider = self._providers[interface]
        
        # 如果 provider 是函数，直接调用
        if callable(provider) and not inspect.isclass(provider):
            return provider()
        
        # 如果是类，使用自动注入
        return self._auto_inject(provider)
    
    async def _create_instance_async(self, interface: Type[T]) -> T:
        """
        创建实例（异步版本）
        
        Args:
            interface: 接口类型
            
        Returns:
            实例
        """
        provider = self._providers[interface]
        
        # 如果 provider 是异步函数，await 它
        if asyncio.iscoroutinefunction(provider):
            return await provider()
        
        # 如果是函数，直接调用
        if callable(provider) and not inspect.isclass(provider):
            return provider()
        
        # 如果是类，使用自动注入
        return await self._auto_inject_async(provider)
    
    def _auto_inject(self, cls: Type[T]) -> T:
        """
        自动注入依赖（同步版本）
        
        Args:
            cls: 类
            
        Returns:
            实例
        """
        # 获取构造函数签名
        sig = inspect.signature(cls.__init__)
        
        # 解析依赖
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # 跳过有默认值的参数
            if param.default != inspect.Parameter.empty:
                continue
            
            # 从类型注解获取依赖类型
            if param.annotation != inspect.Parameter.empty:
                dep_type = param.annotation
                kwargs[param_name] = self.resolve(dep_type)
        
        return cls(**kwargs)
    
    async def _auto_inject_async(self, cls: Type[T]) -> T:
        """
        自动注入依赖（异步版本）
        
        Args:
            cls: 类
            
        Returns:
            实例
        """
        # 获取构造函数签名
        sig = inspect.signature(cls.__init__)
        
        # 解析依赖
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # 跳过有默认值的参数
            if param.default != inspect.Parameter.empty:
                continue
            
            # 从类型注解获取依赖类型
            if param.annotation != inspect.Parameter.empty:
                dep_type = param.annotation
                kwargs[param_name] = await self.resolve_async(dep_type)
        
        return cls(**kwargs)
    
    def clear(self) -> None:
        """清空容器"""
        self._providers.clear()
        self._singletons.clear()
        self._lifecycle.clear()
        self._resolving.clear()
    
    def get_all_singletons(self) -> Dict[Type, Any]:
        """获取所有单例实例"""
        return self._singletons.copy()

