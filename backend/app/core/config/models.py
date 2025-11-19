"""配置数据模型（使用 Pydantic）"""

from typing import Optional, List
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """应用配置"""
    
    app_name: str = Field(default="AstralAgent", description="应用名称")
    version: str = Field(default="0.1.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    environment: str = Field(default="development", description="运行环境")
    
    # API 配置
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 前缀")
    api_host: str = Field(default="0.0.0.0", description="API 主机")
    api_port: int = Field(default=8000, description="API 端口")
    
    # CORS 配置
    cors_allow_origins: List[str] = Field(default=["*"], description="CORS 允许源")
    cors_allow_credentials: bool = Field(default=True, description="CORS 允许凭证")
    cors_allow_methods: List[str] = Field(default=["*"], description="CORS 允许方法")
    cors_allow_headers: List[str] = Field(default=["*"], description="CORS 允许头")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(default="console", description="日志格式（console/json）")
    log_to_file: bool = Field(default=False, description="是否输出到文件")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow",
    }


class DatabaseConfig(BaseSettings):
    """数据库配置"""
    
    database_url: str = Field(
        default="postgresql+asyncpg://astralagent:password@localhost:5432/astralagent",
        description="数据库连接字符串"
    )
    database_pool_size: int = Field(default=10, description="连接池大小")
    database_max_overflow: int = Field(default=20, description="连接池最大溢出")
    database_pool_timeout: int = Field(default=30, description="连接池超时")
    database_echo: bool = Field(default=False, description="是否输出 SQL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class RedisConfig(BaseSettings):
    """Redis 配置"""
    
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis 连接字符串"
    )
    redis_max_connections: int = Field(default=50, description="最大连接数")
    redis_socket_timeout: int = Field(default=5, description="Socket 超时")
    redis_socket_connect_timeout: int = Field(default=5, description="连接超时")
    redis_decode_responses: bool = Field(default=True, description="解码响应")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class ModelConfig(BaseSettings):
    """模型配置"""
    
    # OpenAI
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="OpenAI Base URL"
    )
    openai_default_model: str = Field(default="gpt-4", description="默认模型")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small",
        description="嵌入模型"
    )
    openai_max_retries: int = Field(default=3, description="最大重试次数")
    openai_timeout: int = Field(default=60, description="请求超时")
    
    # 模型路由
    default_model_provider: str = Field(default="openai", description="默认模型提供者")
    enable_model_fallback: bool = Field(default=True, description="启用模型 Fallback")
    enable_model_load_balancing: bool = Field(
        default=False,
        description="启用负载均衡"
    )
    
    @validator("openai_api_key")
    def validate_api_key(cls, v):
        if not v:
            raise ValueError("OpenAI API Key is required")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class SecurityConfig(BaseSettings):
    """安全配置"""
    
    secret_key: str = Field(..., description="密钥")
    jwt_algorithm: str = Field(default="HS256", description="JWT 算法")
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        description="访问 Token 过期时间"
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7,
        description="刷新 Token 过期天数"
    )
    
    @validator("secret_key")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class LoggingConfig(BaseSettings):
    """日志配置"""
    
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(default="json", description="日志格式")
    log_file: Optional[str] = Field(default=None, description="日志文件路径")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class MonitoringConfig(BaseSettings):
    """监控配置"""
    
    enable_metrics: bool = Field(default=True, description="启用指标收集")
    metrics_port: int = Field(default=9090, description="指标端口")
    
    enable_tracing: bool = Field(default=False, description="启用分布式追踪")
    otlp_endpoint: str = Field(
        default="http://localhost:4317",
        description="OTLP 端点"
    )
    
    enable_sentry: bool = Field(default=False, description="启用 Sentry")
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

