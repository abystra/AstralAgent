"""
性能指标收集器

轻量级实现，支持后续集成 Prometheus
"""

import time
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import threading
from collections import defaultdict


@dataclass
class Metric:
    """指标数据"""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class MetricsCollector:
    """
    指标收集器
    
    收集性能指标：
    - 请求计数
    - 请求延迟
    - 错误计数
    - 自定义指标
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._metrics: List[Metric] = []
        self._counters: Dict[str, int] = defaultdict(int)
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
        self._initialized = True
    
    def increment_counter(
        self,
        name: str,
        value: int = 1,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        增加计数器
        
        Args:
            name: 指标名称
            value: 增量
            labels: 标签
        """
        with self._lock:
            key = self._make_key(name, labels)
            self._counters[key] += value
            
            self._metrics.append(Metric(
                name=name,
                value=value,
                labels=labels or {}
            ))
    
    def record_histogram(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        记录直方图数据
        
        Args:
            name: 指标名称
            value: 值
            labels: 标签
        """
        with self._lock:
            key = self._make_key(name, labels)
            self._histograms[key].append(value)
            
            self._metrics.append(Metric(
                name=name,
                value=value,
                labels=labels or {}
            ))
    
    def get_counter(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None
    ) -> int:
        """获取计数器值"""
        key = self._make_key(name, labels)
        return self._counters.get(key, 0)
    
    def get_histogram_stats(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        """
        获取直方图统计信息
        
        Returns:
            包含 min, max, avg, p50, p95, p99 的字典
        """
        key = self._make_key(name, labels)
        values = self._histograms.get(key, [])
        
        if not values:
            return {
                "count": 0,
                "min": 0,
                "max": 0,
                "avg": 0,
                "p50": 0,
                "p95": 0,
                "p99": 0,
            }
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return {
            "count": n,
            "min": sorted_values[0],
            "max": sorted_values[-1],
            "avg": sum(sorted_values) / n,
            "p50": sorted_values[int(n * 0.5)],
            "p95": sorted_values[int(n * 0.95)] if n > 1 else sorted_values[-1],
            "p99": sorted_values[int(n * 0.99)] if n > 1 else sorted_values[-1],
        }
    
    def get_all_metrics(self) -> List[Metric]:
        """获取所有指标"""
        with self._lock:
            return self._metrics.copy()
    
    def clear(self) -> None:
        """清空所有指标"""
        with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._histograms.clear()
    
    def _make_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """生成指标键"""
        if not labels:
            return name
        
        labels_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{labels_str}}}"


# 全局指标收集器
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """获取全局指标收集器"""
    return _metrics_collector


def record_request(
    method: str,
    path: str,
    status_code: int,
    duration: float
) -> None:
    """
    记录请求指标
    
    Args:
        method: HTTP 方法
        path: 路径
        status_code: 状态码
        duration: 耗时（秒）
    """
    collector = get_metrics_collector()
    
    # 请求计数
    collector.increment_counter(
        "http_requests_total",
        labels={
            "method": method,
            "path": path,
            "status": str(status_code),
        }
    )
    
    # 请求延迟
    collector.record_histogram(
        "http_request_duration_seconds",
        duration,
        labels={
            "method": method,
            "path": path,
        }
    )


def record_error(
    error_type: str,
    error_code: Optional[int] = None
) -> None:
    """
    记录错误
    
    Args:
        error_type: 错误类型
        error_code: 错误码
    """
    collector = get_metrics_collector()
    
    labels = {"type": error_type}
    if error_code is not None:
        labels["code"] = str(error_code)
    
    collector.increment_counter("errors_total", labels=labels)


def record_duration(
    operation: str,
    duration: float,
    labels: Optional[Dict[str, str]] = None
) -> None:
    """
    记录操作耗时
    
    Args:
        operation: 操作名称
        duration: 耗时（秒）
        labels: 额外标签
    """
    collector = get_metrics_collector()
    
    final_labels = {"operation": operation}
    if labels:
        final_labels.update(labels)
    
    collector.record_histogram(
        "operation_duration_seconds",
        duration,
        labels=final_labels
    )

