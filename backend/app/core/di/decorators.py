"""依赖注入装饰器"""

from typing import Type, TypeVar, Callable
from functools import wraps
from app.core.di.container import Lifecycle

T = TypeVar('T')


def injectable(lifecycle: Lifecycle = Lifecycle.SINGLETON):
    """
    标记类为可注入
    
    Args:
        lifecycle: 生命周期
        
    Usage:
        @injectable(lifecycle=Lifecycle.SINGLETON)
        class MyService:
            pass
    """
    def decorator(cls: Type[T]) -> Type[T]:
        # 保存生命周期元数据
        cls.__lifecycle__ = lifecycle
        return cls
    return decorator


def inject(param_name: str, interface: Type):
    """
    注入依赖到函数参数
    
    Args:
        param_name: 参数名
        interface: 接口类型
        
    Usage:
        @inject("service", MyService)
        def my_function(service):
            return service.do_something()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from app.core.di import container
            # 解析依赖
            dependency = container.resolve(interface)
            # 注入到参数
            kwargs[param_name] = dependency
            return func(*args, **kwargs)
        return wrapper
    return decorator

