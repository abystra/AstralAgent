"""
系统路由

包含根路径、健康检查、指标等系统级端点
"""

from fastapi import FastAPI

from app.core.config.models import AppConfig
from app.core.monitoring import get_health_checker, get_metrics_collector


def create_system_routes(app: FastAPI, config: AppConfig) -> None:
    """
    创建系统路由
    
    Args:
        app: FastAPI 应用实例
        config: 应用配置
    """
    
    @app.get("/", tags=["System"])
    async def root():
        """根路径"""
        return {
            "name": config.app_name,
            "version": config.version,
            "environment": config.environment,
            "docs": "/docs" if config.debug else None,
        }
    
    @app.get("/health", tags=["System"])
    async def health_check():
        """
        健康检查端点
        
        返回系统和所有中间件的健康状态
        """
        health_checker = get_health_checker()
        results = await health_checker.check_all()
        overall_status = health_checker.get_overall_status(results)
        
        return {
            "status": overall_status.value,
            "checks": {
                name: {
                    "status": result.status.value,
                    "message": result.message,
                    "details": result.details,
                }
                for name, result in results.items()
            }
        }
    
    @app.get("/metrics", tags=["System"])
    async def metrics():
        """
        指标端点
        
        返回性能指标统计
        """
        collector = get_metrics_collector()
        
        # 请求统计
        request_stats = collector.get_histogram_stats(
            "http_request_duration_seconds"
        )
        
        return {
            "requests": {
                "total": collector.get_counter("http_requests_total"),
                "duration": request_stats,
            },
            "errors": {
                "total": collector.get_counter("errors_total"),
            }
        }
    
    @app.get("/ping", tags=["System"])
    async def ping():
        """简单的 ping 端点，用于负载均衡器健康检查"""
        return {"status": "ok"}

