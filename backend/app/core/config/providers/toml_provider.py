"""TOML 文件配置提供者"""

from pathlib import Path
from typing import Dict, Any, Optional
import toml
from app.core.config.base import ConfigProvider


class TomlConfigProvider(ConfigProvider):
    """
    TOML 文件配置提供者
    
    优先级：中等（默认 priority=50）
    """
    
    def __init__(
        self,
        file_path: str = "config.toml",
        priority: int = 50,
        required: bool = False
    ):
        """
        初始化 TOML 配置提供者
        
        Args:
            file_path: TOML 文件路径
            priority: 优先级
            required: 是否必须存在
        """
        super().__init__(priority)
        self.file_path = Path(file_path)
        self.required = required
    
    async def load(self) -> Dict[str, Any]:
        """
        从 TOML 文件加载配置
        
        Returns:
            配置字典
        """
        if not self.file_path.exists():
            if self.required:
                raise FileNotFoundError(f"Config file not found: {self.file_path}")
            return {}
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                config = toml.load(f)
            return config
        except Exception as e:
            if self.required:
                raise RuntimeError(f"Failed to load config from {self.file_path}: {e}")
            print(f"Warning: Failed to load TOML config: {e}")
            return {}

