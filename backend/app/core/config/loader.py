"""配置加载器"""

import asyncio
from typing import Dict, Any, List, Optional, Callable
from app.core.config.base import ConfigProvider


class ConfigLoader:
    """
    配置加载器
    
    支持：
    - 多配置源加载和合并
    - 按优先级覆盖
    - 配置热更新
    """
    
    def __init__(self, providers: Optional[List[ConfigProvider]] = None):
        """
        初始化配置加载器
        
        Args:
            providers: 配置提供者列表
        """
        self.providers: List[ConfigProvider] = providers or []
        self._config: Dict[str, Any] = {}
        self._watch_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self._watch_task: Optional[asyncio.Task] = None
    
    def add_provider(self, provider: ConfigProvider) -> None:
        """
        添加配置提供者
        
        Args:
            provider: 配置提供者实例
        """
        self.providers.append(provider)
        # 按优先级排序（升序，后面的优先级高）
        self.providers.sort(key=lambda p: p.priority)
    
    async def load_all(self) -> Dict[str, Any]:
        """
        加载并合并所有配置源
        
        Returns:
            合并后的配置字典
        """
        merged_config: Dict[str, Any] = {}
        
        for provider in self.providers:
            try:
                provider_config = await provider.load()
                merged_config = self._deep_merge(merged_config, provider_config)
            except Exception as e:
                # 记录错误但继续加载其他配置源
                print(f"Warning: Failed to load config from {provider}: {e}")
        
        self._config = merged_config
        return merged_config
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """
        深度合并两个字典
        
        Args:
            base: 基础字典
            update: 更新字典
            
        Returns:
            合并后的字典
        """
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # 递归合并嵌套字典
                result[key] = self._deep_merge(result[key], value)
            else:
                # 直接覆盖
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键（支持点号分隔，如 "database.host"）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
    
    def on_change(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        注册配置变化回调
        
        Args:
            callback: 回调函数
        """
        self._watch_callbacks.append(callback)
    
    async def start_watch(self) -> None:
        """启动配置监听"""
        if self._watch_task is not None:
            return
        
        async def watch_task():
            """监听任务"""
            for provider in self.providers:
                try:
                    await provider.watch(self._on_config_change)
                except Exception as e:
                    print(f"Warning: Failed to start watching {provider}: {e}")
        
        self._watch_task = asyncio.create_task(watch_task())
    
    async def _on_config_change(self, new_config: Dict[str, Any]) -> None:
        """
        配置变化处理
        
        Args:
            new_config: 新的配置
        """
        # 重新加载所有配置
        await self.load_all()
        
        # 通知所有监听者
        for callback in self._watch_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self._config)
                else:
                    callback(self._config)
            except Exception as e:
                print(f"Error in config change callback: {e}")
    
    async def close(self) -> None:
        """关闭配置加载器"""
        # 取消监听任务
        if self._watch_task:
            self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass
        
        # 关闭所有提供者
        for provider in self.providers:
            try:
                await provider.close()
            except Exception as e:
                print(f"Error closing provider {provider}: {e}")

