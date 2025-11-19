"""环境变量配置提供者"""

import os
from typing import Dict, Any
from app.core.config.base import ConfigProvider


class EnvConfigProvider(ConfigProvider):
    """
    环境变量配置提供者
    
    优先级：最高（默认 priority=100）
    """
    
    def __init__(self, prefix: str = "", priority: int = 100):
        """
        初始化环境变量配置提供者
        
        Args:
            prefix: 环境变量前缀（如 "APP_"）
            priority: 优先级
        """
        super().__init__(priority)
        self.prefix = prefix
    
    async def load(self) -> Dict[str, Any]:
        """
        从环境变量加载配置
        
        Returns:
            配置字典
        """
        config: Dict[str, Any] = {}
        
        for key, value in os.environ.items():
            # 如果有前缀，只加载带前缀的环境变量
            if self.prefix and not key.startswith(self.prefix):
                continue
            
            # 移除前缀
            config_key = key[len(self.prefix):] if self.prefix else key
            
            # 转换为小写并用点号分隔（例如 DATABASE_HOST -> database.host）
            config_key = config_key.lower().replace('_', '.')
            
            # 尝试转换类型
            config_value = self._parse_value(value)
            
            # 设置嵌套字典
            self._set_nested_dict(config, config_key, config_value)
        
        return config
    
    def _parse_value(self, value: str) -> Any:
        """
        解析环境变量值
        
        Args:
            value: 字符串值
            
        Returns:
            解析后的值（自动识别类型）
        """
        # 布尔值
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
        
        # 数字
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # 列表（逗号分隔）
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        
        # 字符串
        return value
    
    def _set_nested_dict(self, d: Dict[str, Any], key: str, value: Any) -> None:
        """
        设置嵌套字典的值
        
        Args:
            d: 字典
            key: 键（支持点号分隔，如 "database.host"）
            value: 值
        """
        keys = key.split('.')
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

