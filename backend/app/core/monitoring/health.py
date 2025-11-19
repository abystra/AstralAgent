"""
健康检查

支持多组件健康检查
"""

from enum import Enum
from typing import Dict, Callable, Awaitable, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio


class HealthStatus(str, Enum):
    """健康状态"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


@dataclass
class HealthCheckResult:
    """健康检查结果"""
    name: str
    status: HealthStatus
    message: Optional[str] = None
    details: Optional[Dict] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


HealthCheckFunc = Callable[[], Awaitable[HealthCheckResult]]


class HealthChecker:
    """
    健康检查器
    
    支持注册多个组件的健康检查
    """
    
    def __init__(self):
        self._checks: Dict[str, HealthCheckFunc] = {}
    
    def register(
        self,
        name: str,
        check_func: HealthCheckFunc
    ) -> None:
        """
        注册健康检查
        
        Args:
            name: 组件名称
            check_func: 异步检查函数
        """
        self._checks[name] = check_func
    
    def unregister(self, name: str) -> None:
        """取消注册"""
        self._checks.pop(name, None)
    
    async def check(self, name: str) -> HealthCheckResult:
        """
        检查单个组件
        
        Args:
            name: 组件名称
            
        Returns:
            健康检查结果
        """
        if name not in self._checks:
            return HealthCheckResult(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=f"Check '{name}' not found"
            )
        
        try:
            result = await self._checks[name]()
            return result
        except Exception as e:
            return HealthCheckResult(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=str(e),
                details={"error_type": type(e).__name__}
            )
    
    async def check_all(
        self,
        timeout: float = 5.0
    ) -> Dict[str, HealthCheckResult]:
        """
        检查所有组件
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            所有组件的检查结果
        """
        results = {}
        
        # 并发执行所有检查
        tasks = {
            name: asyncio.create_task(self.check(name))
            for name in self._checks
        }
        
        # 等待所有任务完成（带超时）
        done, pending = await asyncio.wait(
            tasks.values(),
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED
        )
        
        # 收集结果
        for name, task in tasks.items():
            if task in done:
                try:
                    results[name] = await task
                except Exception as e:
                    results[name] = HealthCheckResult(
                        name=name,
                        status=HealthStatus.UNHEALTHY,
                        message=str(e)
                    )
            else:
                # 超时
                task.cancel()
                results[name] = HealthCheckResult(
                    name=name,
                    status=HealthStatus.UNHEALTHY,
                    message="Health check timeout"
                )
        
        return results
    
    async def is_healthy(self) -> bool:
        """
        检查整体健康状态
        
        Returns:
            如果所有组件都健康则返回 True
        """
        results = await self.check_all()
        return all(
            result.status == HealthStatus.HEALTHY
            for result in results.values()
        )
    
    def get_overall_status(
        self,
        results: Dict[str, HealthCheckResult]
    ) -> HealthStatus:
        """
        获取整体状态
        
        Args:
            results: 所有组件的检查结果
            
        Returns:
            整体健康状态
        """
        if not results:
            return HealthStatus.HEALTHY
        
        statuses = [result.status for result in results.values()]
        
        if all(s == HealthStatus.HEALTHY for s in statuses):
            return HealthStatus.HEALTHY
        elif any(s == HealthStatus.UNHEALTHY for s in statuses):
            return HealthStatus.UNHEALTHY
        else:
            return HealthStatus.DEGRADED


# 全局健康检查器
_health_checker = HealthChecker()


def get_health_checker() -> HealthChecker:
    """获取全局健康检查器"""
    return _health_checker


# 内置健康检查

async def check_system() -> HealthCheckResult:
    """系统健康检查"""
    import psutil
    
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # 简单的阈值检查
        is_healthy = (
            cpu_percent < 90 and
            memory.percent < 90
        )
        
        return HealthCheckResult(
            name="system",
            status=HealthStatus.HEALTHY if is_healthy else HealthStatus.DEGRADED,
            details={
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
            }
        )
    except Exception as e:
        return HealthCheckResult(
            name="system",
            status=HealthStatus.UNHEALTHY,
            message=str(e)
        )

