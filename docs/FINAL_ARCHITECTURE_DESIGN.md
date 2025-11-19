# AstralAgent 最终架构设计方案

> **版本**: v1.0  
> **日期**: 2024-11  
> **状态**: 待实施

---

## 目录

1. [架构概览](#一架构概览)
2. [系统架构](#二系统架构)
3. [模块设计](#三模块设计详解)
4. [数据流设计](#四数据流设计)
5. [接口设计](#五接口设计规范)
6. [部署架构](#六部署架构)
7. [技术选型](#七技术选型)
8. [性能设计](#八性能设计)
9. [安全设计](#九安全设计)
10. [实施计划](#十实施计划)

---

## 一、架构概览

### 1.1 系统定位

**AstralAgent** 是企业级多智能体平台，融合：
- **Multi-Agent 协作**：多智能体编排和协作
- **RAG 知识库**：企业知识检索和问答
- **AI 助手**：Chat、Task、Automation
- **多模型接入**：OpenAI、DeepSeek、Ollama 等
- **插件化扩展**：Agent、Tool、Workflow 可插拔
- **LangGraph 编排**：智能工作流引擎

### 1.2 设计原则

| 原则 | 说明 |
|-----|------|
| **Clean Architecture** | 依赖倒置，内层不依赖外层 |
| **横向分层 + 纵向领域** | 工程化能力 + AI 原生能力 |
| **接口抽象** | 所有组件通过接口交互 |
| **依赖注入** | 统一的 DI 容器管理生命周期 |
| **事件驱动** | 解耦组件，异步通信 |
| **配置驱动** | 行为通过配置而非代码控制 |
| **可观测性** | Logging + Metrics + Tracing |
| **安全第一** | 认证、授权、审计、隔离 |

### 1.3 架构特点

✅ **高内聚低耦合**：清晰的模块边界  
✅ **可测试性**：接口抽象，Mock 友好  
✅ **可扩展性**：插件化设计  
✅ **高性能**：异步 IO，缓存优化  
✅ **企业级**：安全、审计、多租户  

---

## 二、系统架构

### 2.1 总体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          External Clients                                │
│              Browser  │  Mobile App  │  Third-party System              │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      API Gateway / Load Balancer                         │
│              Rate Limiting │ Auth │ Logging │ Monitoring                │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
         ┌─────────────────┐       ┌─────────────────┐
         │   API Layer     │       │  Streaming      │
         │   (REST API)    │       │  (SSE/WS)       │
         └────────┬────────┘       └────────┬────────┘
                  │                         │
                  └──────────┬──────────────┘
                             ▼
         ┌──────────────────────────────────────────┐
         │        Application Layer                  │
         │  ┌────────────┐  ┌──────────────────┐   │
         │  │Chat Service│  │Agent Exec Service│   │
         │  └────────────┘  └──────────────────┘   │
         │  ┌────────────┐  ┌──────────────────┐   │
         │  │RAG Service │  │Workflow Service  │   │
         │  └────────────┘  └──────────────────┘   │
         └──────────────────┬───────────────────────┘
                            │
         ┌──────────────────┴───────────────────────────────────────────┐
         │                   AI Native Layer                             │
         │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
         │  │  Memory  │  │  Tools   │  │  Agents  │  │Workflows │     │
         │  │   Layer  │  │  Layer   │  │  Layer   │  │  Layer   │     │
         │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
         │   - Vector DB   - HTTP Tool   - ReAct      - LangGraph       │
         │   - RAG Engine  - DB Tool     - Reflection - State Machine   │
         │   - Conversation- RAG Tool    - Planner    - Checkpoint      │
         └────────────────────────────┬─────────────────────────────────┘
                                      │
         ┌────────────────────────────┴─────────────────────────────────┐
         │              Infrastructure Layer                             │
         │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
         │  │Model Provider│  │  Middleware  │  │  Plugin System   │   │
         │  ├──────────────┤  ├──────────────┤  ├──────────────────┤   │
         │  │ - OpenAI     │  │ - PostgreSQL │  │ - Loader         │   │
         │  │ - DeepSeek   │  │ - Redis      │  │ - Registry       │   │
         │  │ - Ollama     │  │ - RabbitMQ   │  │ - Sandbox        │   │
         │  │ - Router     │  │ - OSS/S3     │  │ - Lifecycle      │   │
         │  └──────────────┘  └──────────────┘  └──────────────────┘   │
         └────────────────────────────┬─────────────────────────────────┘
                                      │
         ┌────────────────────────────┴─────────────────────────────────┐
         │                    Core Layer (横切关注点)                    │
         │  ┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
         │  │Config│ │  DI  │ │Exception│ │ Logging  │ │Monitoring│   │
         │  └──────┘ └──────┘ └──────────┘ └──────────┘ └──────────┘   │
         │  ┌──────────┐ ┌──────────┐ ┌──────────┐                     │
         │  │ Security │ │  Events  │ │  Cache   │                     │
         │  └──────────┘ └──────────┘ └──────────┘                     │
         └──────────────────────────────────────────────────────────────┘
```

### 2.2 分层职责

| 层次 | 职责 | 主要组件 |
|-----|------|---------|
| **API Layer** | HTTP 接口、路由注册、请求响应 | FastAPI, Router Registry, Swagger |
| **Application Layer** | 业务编排、用例执行、DTO 转换 | Services, Use Cases, DTOs |
| **AI Native Layer** | Agent 执行、工作流编排、知识检索 | Agents, Workflows, Memory, Tools |
| **Infrastructure Layer** | 外部服务、中间件、模型调用 | Model Providers, DB, Cache, MQ |
| **Core Layer** | 配置、DI、日志、监控、安全 | Config, DI Container, Logger |

### 2.3 依赖方向

```
API Layer
    ↓ (依赖)
Application Layer
    ↓ (依赖)
AI Native Layer ← (接口抽象) → Infrastructure Layer
    ↓                              ↓
    └──────────→ Core Layer ←──────┘
```

**关键**：
- 内层不依赖外层
- 所有层都可以依赖 Core Layer
- AI Native Layer 通过接口依赖 Infrastructure Layer

---

## 三、模块设计详解

### 3.1 Core Layer（核心层）

#### 3.1.1 配置管理（Config）

**职责**：统一配置加载、多源支持、类型安全

```python
# app/core/config/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Callable

class ConfigProvider(ABC):
    """配置提供者抽象接口"""
    
    @abstractmethod
    async def load(self) -> Dict[str, Any]:
        """加载配置"""
        
    @abstractmethod
    async def watch(self, callback: Callable) -> None:
        """监听配置变化（可选）"""
        
    @abstractmethod
    def get_priority(self) -> int:
        """获取优先级（数字越大优先级越高）"""

# app/core/config/loader.py
class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, providers: List[ConfigProvider]):
        # 按优先级排序
        self.providers = sorted(providers, key=lambda p: p.get_priority())
    
    async def load_all(self) -> Dict[str, Any]:
        """合并所有提供者的配置（后者覆盖前者）"""
        config = {}
        for provider in self.providers:
            provider_config = await provider.load()
            config = self._deep_merge(config, provider_config)
        return config
```

**配置源优先级**：
1. 环境变量（优先级最高）
2. Nacos/Consul（配置中心）
3. TOML 文件
4. .env 文件（默认值）

**目录结构**：
```
app/core/config/
├── __init__.py
├── base.py              # 抽象接口
├── loader.py            # 配置加载器
├── registry.py          # 配置注册中心
├── models.py            # Pydantic 配置模型
└── providers/
    ├── env_provider.py
    ├── toml_provider.py
    ├── nacos_provider.py
    └── consul_provider.py
```

#### 3.1.2 依赖注入（DI Container）

**职责**：管理组件生命周期、依赖注入

```python
# app/core/di/container.py
from typing import Dict, Any, Type, Callable
from enum import Enum

class Lifecycle(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"

class DIContainer:
    """依赖注入容器"""
    
    def __init__(self):
        self._providers: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._lifecycle: Dict[Type, Lifecycle] = {}
    
    def register(
        self, 
        interface: Type, 
        implementation: Type | Callable,
        lifecycle: Lifecycle = Lifecycle.SINGLETON
    ):
        """注册依赖"""
        self._providers[interface] = implementation
        self._lifecycle[interface] = lifecycle
    
    def resolve(self, interface: Type) -> Any:
        """解析依赖"""
        if interface not in self._providers:
            raise ValueError(f"No provider for {interface}")
        
        lifecycle = self._lifecycle[interface]
        
        # 单例模式
        if lifecycle == Lifecycle.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_instance(interface)
            return self._singletons[interface]
        
        # 瞬态模式（每次创建新实例）
        return self._create_instance(interface)
```

**使用示例**：
```python
# 注册
container = DIContainer()
container.register(IModelProvider, OpenAIProvider, Lifecycle.SINGLETON)
container.register(IVectorStore, MilvusVectorStore, Lifecycle.SINGLETON)

# 解析
model_provider = container.resolve(IModelProvider)
vector_store = container.resolve(IVectorStore)
```

#### 3.1.3 异常体系

**职责**：统一异常定义、分类、处理

```python
# app/core/exceptions/base.py
from typing import Optional, Dict, Any

class AstralException(Exception):
    """异常基类"""
    
    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        self.cause = cause
        super().__init__(message)

# 业务异常
class BusinessException(AstralException):
    """业务异常"""
    pass

# API 异常
class APIException(AstralException):
    """API 异常"""
    def __init__(self, message: str, status_code: int = 400, **kwargs):
        super().__init__(message, **kwargs)
        self.status_code = status_code

# Agent 异常
class AgentException(AstralException):
    """Agent 执行异常"""
    pass

# 模型异常
class ModelException(AstralException):
    """模型调用异常"""
    pass
```

**异常分类**：
- `ConfigException`：配置错误
- `AuthException`：认证授权错误
- `ValidationException`：数据验证错误
- `ResourceNotFoundException`：资源不存在
- `RateLimitException`：限流异常
- `TimeoutException`：超时异常

#### 3.1.4 日志系统

**职责**：结构化日志、全链路追踪

```python
# app/core/logging/logger.py
import structlog
from contextvars import ContextVar

# 全链路 TraceID
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')

class StructuredLogger:
    """结构化日志器"""
    
    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)
    
    def info(self, event: str, **kwargs):
        """记录 info 日志"""
        kwargs['trace_id'] = trace_id_var.get()
        self.logger.info(event, **kwargs)
    
    def error(self, event: str, exc: Exception = None, **kwargs):
        """记录 error 日志"""
        kwargs['trace_id'] = trace_id_var.get()
        if exc:
            kwargs['exception'] = str(exc)
            kwargs['exception_type'] = type(exc).__name__
        self.logger.error(event, **kwargs)
```

**日志格式**：
```json
{
  "timestamp": "2024-11-20T10:30:00Z",
  "level": "info",
  "event": "agent_executed",
  "trace_id": "abc-123-xyz",
  "agent_id": "retrieval_agent",
  "duration_ms": 250,
  "token_usage": 150
}
```

#### 3.1.5 监控系统

**职责**：指标收集、性能追踪

```python
# app/core/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# 定义指标
agent_execution_count = Counter(
    'agent_execution_total',
    'Total agent executions',
    ['agent_name', 'status']
)

agent_execution_duration = Histogram(
    'agent_execution_duration_seconds',
    'Agent execution duration',
    ['agent_name']
)

model_token_usage = Counter(
    'model_token_usage_total',
    'Total tokens used',
    ['model_name', 'type']
)

active_workflows = Gauge(
    'active_workflows',
    'Number of active workflows'
)
```

**追踪示例**：
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("agent_execution") as span:
    span.set_attribute("agent.name", "retrieval_agent")
    span.set_attribute("agent.version", "v1")
    
    # 执行 Agent
    result = await agent.execute(input_data)
    
    span.set_attribute("agent.output_tokens", result.token_usage)
```

---

### 3.2 Infrastructure Layer（基础设施层）

#### 3.2.1 Model Provider（模型提供者）

**架构设计**：

```
┌────────────────────────────────────────┐
│         Model Provider Client           │
│  (统一接口，屏蔽不同模型差异)            │
└─────────────────┬──────────────────────┘
                  │
        ┌─────────┴─────────┐
        │   Model Router    │
        │  (路由、负载均衡)  │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐  ┌────────┐   ┌────────┐
│ OpenAI │  │DeepSeek│   │ Ollama │
│Provider│  │Provider│   │Provider│
└────────┘  └────────┘   └────────┘
```

**接口定义**：

```python
# app/infrastructure/models/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncIterator
from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str  # system, user, assistant
    content: str

@dataclass
class ChatResponse:
    content: str
    model: str
    token_usage: Dict[str, int]  # prompt_tokens, completion_tokens, total_tokens
    finish_reason: str

class IModelProvider(ABC):
    """模型提供者接口"""
    
    @abstractmethod
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> ChatResponse:
        """对话补全"""
    
    @abstractmethod
    async def chat_stream(
        self,
        messages: List[ChatMessage],
        **kwargs
    ) -> AsyncIterator[str]:
        """流式对话"""
    
    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """文本嵌入"""
```

**模型路由器**：

```python
# app/infrastructure/models/router.py
from typing import List, Dict
import random

class ModelRouter:
    """模型路由器（支持负载均衡、灰度发布）"""
    
    def __init__(self):
        self.providers: Dict[str, IModelProvider] = {}
        self.weights: Dict[str, float] = {}  # 权重配置
    
    def register(self, name: str, provider: IModelProvider, weight: float = 1.0):
        """注册模型提供者"""
        self.providers[name] = provider
        self.weights[name] = weight
    
    async def route(self, strategy: str = "random") -> IModelProvider:
        """路由到具体提供者"""
        if strategy == "random":
            # 按权重随机选择
            choices = list(self.providers.keys())
            weights = [self.weights[name] for name in choices]
            selected = random.choices(choices, weights=weights, k=1)[0]
            return self.providers[selected]
        
        elif strategy == "round_robin":
            # 轮询
            pass
        
        elif strategy == "least_loaded":
            # 负载最低
            pass
```

**Fallback 机制**：

```python
# app/infrastructure/models/fallback.py
class FallbackModelProvider(IModelProvider):
    """支持 Fallback 的模型提供者"""
    
    def __init__(self, primary: IModelProvider, fallback: IModelProvider):
        self.primary = primary
        self.fallback = fallback
    
    async def chat(self, messages: List[ChatMessage], **kwargs) -> ChatResponse:
        try:
            return await self.primary.chat(messages, **kwargs)
        except Exception as e:
            logger.warning(f"Primary model failed, falling back: {e}")
            return await self.fallback.chat(messages, **kwargs)
```

#### 3.2.2 Middleware（中间件）

**统一接口**：

```python
# app/infrastructure/middleware/base.py
from abc import ABC, abstractmethod

class IMiddleware(ABC):
    """中间件抽象接口"""
    
    @abstractmethod
    async def connect(self) -> None:
        """建立连接"""
    
    @abstractmethod
    async def disconnect(self) -> None:
        """关闭连接"""
    
    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查"""
```

**数据库中间件**：

```python
# app/infrastructure/middleware/database/postgres.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class PostgreSQLMiddleware(IMiddleware):
    """PostgreSQL 中间件"""
    
    def __init__(self, connection_string: str, pool_size: int = 10):
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.engine = None
        self.session_factory = None
    
    async def connect(self) -> None:
        """建立连接池"""
        self.engine = create_async_engine(
            self.connection_string,
            pool_size=self.pool_size,
            max_overflow=20,
            pool_pre_ping=True  # 连接检查
        )
        
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def disconnect(self) -> None:
        """关闭连接"""
        if self.engine:
            await self.engine.dispose()
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            async with self.session_factory() as session:
                await session.execute("SELECT 1")
            return True
        except Exception:
            return False
    
    def get_session(self) -> AsyncSession:
        """获取数据库会话"""
        return self.session_factory()
```

**Redis 中间件**：

```python
# app/infrastructure/middleware/cache/redis.py
import aioredis
from typing import Optional, Any
import json

class RedisMiddleware(IMiddleware):
    """Redis 缓存中间件"""
    
    def __init__(self, url: str, max_connections: int = 50):
        self.url = url
        self.max_connections = max_connections
        self.redis = None
    
    async def connect(self) -> None:
        """建立连接"""
        self.redis = await aioredis.create_redis_pool(
            self.url,
            maxsize=self.max_connections
        )
    
    async def disconnect(self) -> None:
        """关闭连接"""
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """设置缓存"""
        await self.redis.setex(key, ttl, json.dumps(value))
    
    async def delete(self, key: str):
        """删除缓存"""
        await self.redis.delete(key)
```

**中间件管理器**：

```python
# app/infrastructure/middleware/manager.py
class MiddlewareManager:
    """中间件管理器"""
    
    def __init__(self):
        self.middlewares: Dict[str, IMiddleware] = {}
    
    def register(self, name: str, middleware: IMiddleware):
        """注册中间件"""
        self.middlewares[name] = middleware
    
    async def startup(self):
        """启动所有中间件"""
        for name, middleware in self.middlewares.items():
            logger.info(f"Connecting middleware: {name}")
            await middleware.connect()
    
    async def shutdown(self):
        """关闭所有中间件"""
        for name, middleware in self.middlewares.items():
            logger.info(f"Disconnecting middleware: {name}")
            await middleware.disconnect()
    
    async def health_check(self) -> Dict[str, bool]:
        """健康检查所有中间件"""
        results = {}
        for name, middleware in self.middlewares.items():
            results[name] = await middleware.health_check()
        return results
```

#### 3.2.3 Plugin System（插件系统）

**插件结构**：

```
plugins/
└── example_plugin/
    ├── manifest.json        # 插件元数据
    ├── __init__.py
    ├── agents/              # 插件提供的 Agent
    │   └── custom_agent.py
    ├── tools/               # 插件提供的 Tool
    │   └── custom_tool.py
    └── workflows/           # 插件提供的 Workflow
        └── custom_flow.py
```

**manifest.json**：

```json
{
  "name": "example_plugin",
  "version": "1.0.0",
  "description": "Example plugin",
  "author": "AstralAgent Team",
  "dependencies": {
    "langchain": ">=0.1.0",
    "requests": ">=2.31.0"
  },
  "provides": {
    "agents": ["custom_agent"],
    "tools": ["custom_tool"],
    "workflows": ["custom_flow"]
  },
  "permissions": ["http", "database"],
  "entry_point": "example_plugin:init"
}
```

**插件加载器**：

```python
# app/infrastructure/plugins/loader.py
import importlib
import json
from pathlib import Path

class PluginLoader:
    """插件加载器"""
    
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.loaded_plugins: Dict[str, Any] = {}
    
    async def load_plugin(self, plugin_name: str):
        """加载插件"""
        plugin_path = self.plugins_dir / plugin_name
        manifest_path = plugin_path / "manifest.json"
        
        # 1. 读取 manifest
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # 2. 验证插件
        self._validate_plugin(manifest)
        
        # 3. 安装依赖（如果需要）
        await self._install_dependencies(manifest.get("dependencies", {}))
        
        # 4. 加载插件模块
        module_name = manifest["entry_point"].split(":")[0]
        module = importlib.import_module(f"plugins.{plugin_name}.{module_name}")
        
        # 5. 调用初始化函数
        init_func_name = manifest["entry_point"].split(":")[1]
        init_func = getattr(module, init_func_name)
        plugin_instance = await init_func()
        
        self.loaded_plugins[plugin_name] = {
            "manifest": manifest,
            "instance": plugin_instance
        }
        
        logger.info(f"Plugin loaded: {plugin_name} v{manifest['version']}")
    
    def _validate_plugin(self, manifest: Dict):
        """验证插件配置"""
        required_fields = ["name", "version", "entry_point"]
        for field in required_fields:
            if field not in manifest:
                raise ValueError(f"Missing required field: {field}")
```

---

### 3.3 AI Native Layer（AI 原生层）

#### 3.3.1 Memory Layer（记忆层）

**向量存储接口**：

```python
# app/memory/vector/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Document:
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float] = None

@dataclass
class SearchResult:
    document: Document
    score: float

class IVectorStore(ABC):
    """向量存储接口"""
    
    @abstractmethod
    async def add(self, documents: List[Document]) -> None:
        """添加文档"""
    
    @abstractmethod
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Dict[str, Any] = None
    ) -> List[SearchResult]:
        """向量检索"""
    
    @abstractmethod
    async def delete(self, ids: List[str]) -> None:
        """删除文档"""
```

**RAG 引擎**：

```python
# app/memory/rag/engine.py
class RAGEngine:
    """RAG 检索引擎"""
    
    def __init__(
        self,
        vector_store: IVectorStore,
        embedder: IModelProvider,
        reranker: Optional[Any] = None
    ):
        self.vector_store = vector_store
        self.embedder = embedder
        self.reranker = reranker
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        use_rerank: bool = True
    ) -> List[Document]:
        """检索相关文档"""
        
        # 1. 生成查询向量
        query_embedding = await self.embedder.embed([query])
        
        # 2. 向量检索
        results = await self.vector_store.search(
            query_embedding[0],
            top_k=top_k * 2 if use_rerank else top_k
        )
        
        # 3. Reranking（如果启用）
        if use_rerank and self.reranker:
            results = await self.reranker.rerank(query, results)
            results = results[:top_k]
        
        return [r.document for r in results]
```

**会话记忆**：

```python
# app/memory/conversation/memory.py
from collections import deque

class ConversationMemory:
    """会话记忆"""
    
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.messages = deque(maxlen=max_turns * 2)  # user + assistant
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> List[Dict[str, str]]:
        """获取消息历史"""
        return list(self.messages)
    
    def clear(self):
        """清空记忆"""
        self.messages.clear()
```

#### 3.3.2 Tools Layer（工具层）

**工具接口**：

```python
# app/tools/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class ToolInput(BaseModel):
    """工具输入（子类定义具体参数）"""
    pass

class ToolOutput(BaseModel):
    """工具输出"""
    success: bool
    result: Any
    error: str = None

class ITool(ABC):
    """工具抽象接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """工具名称"""
    
    @property
    @abstractmethod
    def description(self) -> str:
        """工具描述"""
    
    @property
    @abstractmethod
    def input_schema(self) -> Type[ToolInput]:
        """输入参数 Schema"""
    
    @abstractmethod
    async def execute(self, input_data: ToolInput) -> ToolOutput:
        """执行工具"""
```

**工具示例 - RAG 检索工具**：

```python
# app/tools/builtin/rag_tool.py
class RAGToolInput(ToolInput):
    query: str
    top_k: int = 5

class RAGTool(ITool):
    """RAG 检索工具"""
    
    def __init__(self, rag_engine: RAGEngine):
        self.rag_engine = rag_engine
    
    @property
    def name(self) -> str:
        return "rag_retrieval"
    
    @property
    def description(self) -> str:
        return "从知识库中检索相关文档"
    
    @property
    def input_schema(self) -> Type[ToolInput]:
        return RAGToolInput
    
    async def execute(self, input_data: RAGToolInput) -> ToolOutput:
        try:
            documents = await self.rag_engine.retrieve(
                input_data.query,
                top_k=input_data.top_k
            )
            return ToolOutput(
                success=True,
                result=[doc.content for doc in documents]
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
```

**工具注册中心**：

```python
# app/tools/registry.py
class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self.tools: Dict[str, ITool] = {}
    
    def register(self, tool: ITool):
        """注册工具"""
        self.tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")
    
    def get(self, name: str) -> ITool:
        """获取工具"""
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")
        return self.tools[name]
    
    def list_tools(self) -> List[Dict[str, str]]:
        """列出所有工具"""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]
```

#### 3.3.3 Agents Layer（智能体层）

**Agent 接口**：

```python
# app/agents/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class AgentInput:
    query: str
    context: Dict[str, Any] = None

@dataclass
class AgentOutput:
    answer: str
    reasoning: str
    tool_calls: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

class IAgent(ABC):
    """Agent 抽象接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Agent 名称"""
    
    @abstractmethod
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """执行 Agent"""
```

**ReAct Agent 实现**：

```python
# app/agents/strategies/react.py
class ReActAgent(IAgent):
    """ReAct 策略 Agent"""
    
    def __init__(
        self,
        model_provider: IModelProvider,
        tools: List[ITool],
        max_iterations: int = 5
    ):
        self.model_provider = model_provider
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
    
    @property
    def name(self) -> str:
        return "react_agent"
    
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """执行 ReAct 循环"""
        
        reasoning_steps = []
        tool_calls = []
        
        for i in range(self.max_iterations):
            # 1. Thought: 让模型思考下一步
            thought_prompt = self._build_thought_prompt(
                input_data.query,
                reasoning_steps
            )
            
            thought_response = await self.model_provider.chat([
                ChatMessage(role="system", content="You are a helpful assistant."),
                ChatMessage(role="user", content=thought_prompt)
            ])
            
            # 2. Act: 解析并执行工具调用
            action = self._parse_action(thought_response.content)
            
            if action["type"] == "finish":
                # 结束，返回最终答案
                return AgentOutput(
                    answer=action["answer"],
                    reasoning="\n".join(reasoning_steps),
                    tool_calls=tool_calls
                )
            
            # 3. Observe: 执行工具并获取结果
            tool_result = await self._execute_tool(action["tool"], action["input"])
            
            reasoning_steps.append(
                f"Thought: {thought_response.content}\n"
                f"Action: {action['tool']}({action['input']})\n"
                f"Observation: {tool_result}"
            )
            tool_calls.append(action)
        
        # 达到最大迭代次数
        return AgentOutput(
            answer="抱歉，无法在规定步骤内完成任务",
            reasoning="\n".join(reasoning_steps),
            tool_calls=tool_calls
        )
```

#### 3.3.4 Workflows Layer（工作流层）

**基于 LangGraph 的工作流**：

```python
# app/workflows/base.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class WorkflowState(TypedDict):
    """工作流状态"""
    query: str
    documents: List[str]
    answer: str
    metadata: dict

class BaseWorkflow:
    """工作流基类"""
    
    def __init__(self):
        self.graph = StateGraph(WorkflowState)
        self._build_graph()
    
    def _build_graph(self):
        """构建工作流图（子类实现）"""
        raise NotImplementedError
    
    async def execute(self, initial_state: WorkflowState) -> WorkflowState:
        """执行工作流"""
        compiled_graph = self.graph.compile()
        final_state = await compiled_graph.ainvoke(initial_state)
        return final_state
```

**RAG 工作流示例**：

```python
# app/workflows/builtin/rag_flow.py
class RAGWorkflow(BaseWorkflow):
    """RAG 工作流"""
    
    def __init__(
        self,
        retrieval_agent: IAgent,
        answer_agent: IAgent
    ):
        self.retrieval_agent = retrieval_agent
        self.answer_agent = answer_agent
        super().__init__()
    
    def _build_graph(self):
        """构建 RAG 工作流图"""
        
        # 定义节点
        async def retrieve_node(state: WorkflowState) -> WorkflowState:
            """检索节点"""
            result = await self.retrieval_agent.execute(
                AgentInput(query=state["query"])
            )
            state["documents"] = result.answer
            return state
        
        async def answer_node(state: WorkflowState) -> WorkflowState:
            """回答节点"""
            context = "\n".join(state["documents"])
            result = await self.answer_agent.execute(
                AgentInput(
                    query=state["query"],
                    context={"documents": context}
                )
            )
            state["answer"] = result.answer
            return state
        
        # 添加节点
        self.graph.add_node("retrieve", retrieve_node)
        self.graph.add_node("answer", answer_node)
        
        # 添加边
        self.graph.set_entry_point("retrieve")
        self.graph.add_edge("retrieve", "answer")
        self.graph.add_edge("answer", END)
```

---

### 3.4 Application Layer（应用层）

#### 3.4.1 Chat Service

```python
# app/application/services/chat_service.py
class ChatService:
    """聊天服务"""
    
    def __init__(
        self,
        workflow: BaseWorkflow,
        memory: ConversationMemory
    ):
        self.workflow = workflow
        self.memory = memory
    
    async def chat(self, user_input: str) -> str:
        """处理用户输入"""
        
        # 1. 添加到记忆
        self.memory.add_message("user", user_input)
        
        # 2. 执行工作流
        initial_state = WorkflowState(
            query=user_input,
            documents=[],
            answer="",
            metadata={}
        )
        
        final_state = await self.workflow.execute(initial_state)
        
        # 3. 添加回复到记忆
        self.memory.add_message("assistant", final_state["answer"])
        
        return final_state["answer"]
    
    async def chat_stream(self, user_input: str) -> AsyncIterator[str]:
        """流式聊天"""
        # 实现流式输出
        pass
```

---

### 3.5 API Layer（API 层）

#### 3.5.1 统一响应格式

```python
# app/api/responses.py
from typing import Any, Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    """统一 API 响应格式"""
    code: int  # 业务状态码
    message: str
    data: Any = None
    trace_id: str = None

def success(data: Any = None, message: str = "Success") -> APIResponse:
    """成功响应"""
    return APIResponse(code=0, message=message, data=data)

def error(code: int, message: str) -> APIResponse:
    """错误响应"""
    return APIResponse(code=code, message=message)
```

#### 3.5.2 路由注册

```python
# app/api/registry.py
class APIRegistry:
    """API 路由注册中心"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.routers: Dict[str, APIRouter] = {}
    
    def register(self, prefix: str, router: APIRouter, tags: List[str] = None):
        """注册路由"""
        self.routers[prefix] = router
        self.app.include_router(router, prefix=prefix, tags=tags or [])
        logger.info(f"Router registered: {prefix}")
    
    def auto_discover(self, endpoints_dir: str):
        """自动发现并注册端点"""
        # 扫描 endpoints 目录，自动导入并注册路由
        pass
```

#### 3.5.3 Chat API 示例

```python
# app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
) -> APIResponse:
    """聊天接口"""
    try:
        answer = await chat_service.chat(request.message)
        return success(data={"answer": answer})
    except Exception as e:
        logger.error("Chat failed", exc=e)
        return error(code=500, message=str(e))

@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """流式聊天接口"""
    async def generate():
        async for chunk in chat_service.chat_stream(request.message):
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## 四、数据流设计

### 4.1 Chat 请求全链路

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. POST /api/v1/chat
     ▼
┌──────────────────┐
│   API Gateway    │ 2. 认证、限流、日志
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│  Chat Endpoint   │ 3. 参数验证
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│   Chat Service   │ 4. 添加到记忆
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│  RAG Workflow    │ 5. 工作流编排
└────┬─────────────┘
     │
     ├──────────────────┐
     │                  │
     ▼                  ▼
┌─────────────┐  ┌──────────────┐
│Retrieval    │  │ Answer Agent │
│   Agent     │  └──────┬───────┘
└─────┬───────┘         │
      │                 │
      ▼                 │
┌─────────────┐         │
│ RAG Engine  │         │
└─────┬───────┘         │
      │                 │
      ▼                 │
┌─────────────┐         │
│Vector Store │         │
└─────────────┘         │
      │                 │
      └────────┬────────┘
               │
               ▼
        ┌─────────────┐
        │   Model     │
        │  Provider   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   OpenAI    │
        └──────┬──────┘
               │
               │ 6. 返回结果
               ▼
        ┌─────────────┐
        │  Response   │
        └─────────────┘
```

### 4.2 Plugin 加载流程

```
1. 启动时扫描 plugins/ 目录
2. 读取每个插件的 manifest.json
3. 验证插件配置和权限
4. 安装插件依赖
5. 导入插件模块
6. 调用插件初始化函数
7. 注册 Agent/Tool/Workflow 到对应的 Registry
8. 插件加载完成，进入 Ready 状态
```

---

## 五、接口设计规范

### 5.1 API 设计规范

#### 请求格式

```json
POST /api/v1/chat
Content-Type: application/json

{
  "message": "你好",
  "session_id": "abc-123",
  "options": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

#### 响应格式

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "answer": "你好！有什么我可以帮助你的吗？",
    "session_id": "abc-123",
    "token_usage": {
      "prompt_tokens": 10,
      "completion_tokens": 20,
      "total_tokens": 30
    }
  },
  "trace_id": "trace-xyz-789"
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "Invalid request parameters",
  "trace_id": "trace-xyz-789"
}
```

### 5.2 错误码设计

| Code Range | 类型 | 说明 |
|-----------|------|------|
| 0 | Success | 成功 |
| 400-499 | Client Error | 客户端错误 |
| 500-599 | Server Error | 服务器错误 |
| 1000-1099 | Auth Error | 认证授权错误 |
| 2000-2099 | Agent Error | Agent 执行错误 |
| 3000-3099 | Model Error | 模型调用错误 |

---

## 六、部署架构

### 6.1 单机部署

```
┌────────────────────────────────────────┐
│         Docker Compose                  │
│  ┌──────────┐  ┌──────────────────┐    │
│  │ FastAPI  │  │   PostgreSQL     │    │
│  │   App    │  └──────────────────┘    │
│  └──────────┘  ┌──────────────────┐    │
│                │      Redis       │    │
│                └──────────────────┘    │
│                ┌──────────────────┐    │
│                │     Milvus       │    │
│                └──────────────────┘    │
└────────────────────────────────────────┘
```

### 6.2 分布式部署

```
┌────────────────────────────────────────────────────┐
│                  Load Balancer                      │
└──────────────────────┬─────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ App Pod │   │ App Pod │   │ App Pod │
   └─────────┘   └─────────┘   └─────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
   ┌──────────┐              ┌──────────────┐
   │PostgreSQL│              │    Redis     │
   │ (Master) │              │   Cluster    │
   └────┬─────┘              └──────────────┘
        │
   ┌────┴─────┐
   │PostgreSQL│
   │ (Slave)  │
   └──────────┘

        ┌──────────────┐
        │    Milvus    │
        │   Cluster    │
        └──────────────┘
```

### 6.3 Kubernetes 部署

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: astralagent-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: astralagent-api
  template:
    metadata:
      labels:
        app: astralagent-api
    spec:
      containers:
      - name: api
        image: astralagent:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 七、技术选型

### 7.1 核心依赖

```toml
[project]
dependencies = [
    # Web 框架
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.0.0",
    
    # AI 框架
    "langchain>=0.1.0",
    "langgraph>=0.0.40",
    "openai>=1.3.0",
    
    # 数据库
    "sqlalchemy[asyncio]>=2.0.0",
    "asyncpg>=0.29.0",  # PostgreSQL
    "alembic>=1.12.0",  # 数据库迁移
    
    # 缓存
    "redis>=5.0.0",
    "aioredis>=2.0.0",
    
    # 向量数据库
    "pymilvus>=2.3.0",
    
    # 消息队列
    "aio-pika>=9.3.0",  # RabbitMQ
    
    # 对象存储
    "boto3>=1.29.0",  # S3
    "oss2>=2.18.0",  # 阿里云 OSS
    
    # 配置管理
    "python-dotenv>=1.0.0",
    "toml>=0.10.2",
    
    # 监控和追踪
    "prometheus-client>=0.19.0",
    "opentelemetry-api>=1.21.0",
    "opentelemetry-sdk>=1.21.0",
    "sentry-sdk>=1.38.0",
    
    # 日志
    "structlog>=23.2.0",
    
    # HTTP 客户端
    "httpx>=0.25.0",
    
    # 工具
    "tenacity>=8.2.0",  # 重试
    "python-jose>=3.3.0",  # JWT
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.25.0",
    "black>=23.11.0",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
]
```

### 7.2 技术栈总结

| 分类 | 技术 | 用途 |
|-----|------|------|
| **Web 框架** | FastAPI | REST API |
| **AI 框架** | LangChain, LangGraph | Agent 和 Workflow |
| **数据库** | PostgreSQL | 关系数据存储 |
| **缓存** | Redis | 缓存和会话 |
| **向量库** | Milvus / pgvector | 向量检索 |
| **消息队列** | RabbitMQ | 异步任务 |
| **对象存储** | S3 / OSS | 文件存储 |
| **监控** | Prometheus, OpenTelemetry | 指标和追踪 |
| **日志** | Structlog | 结构化日志 |
| **部署** | Docker, K8s | 容器化部署 |

---

## 八、性能设计

### 8.1 缓存策略

#### 多级缓存

```
L1 Cache (Memory) → L2 Cache (Redis) → L3 Source (DB/Model)
```

#### 缓存场景

| 场景 | 缓存策略 | TTL |
|-----|---------|-----|
| 模型响应 | Redis | 1 hour |
| 向量检索结果 | Redis | 30 min |
| 配置数据 | Memory | 5 min |
| 用户会话 | Redis | 24 hour |

### 8.2 性能优化

1. **异步 IO**：全链路异步，提高并发
2. **连接池**：数据库、Redis 连接池
3. **批处理**：Embedding 批量生成
4. **并行执行**：多 Agent 并行
5. **流式响应**：大语言模型流式输出

### 8.3 性能指标

| 指标 | 目标 |
|-----|------|
| API 响应时间 | P95 < 2s |
| Agent 执行时间 | P95 < 5s |
| RAG 检索时间 | P95 < 500ms |
| 并发用户数 | > 1000 |

---

## 九、安全设计

### 9.1 认证和授权

```
1. 用户请求携带 JWT Token
2. API Gateway 验证 Token
3. 从 Token 中提取用户信息和权限
4. 根据权限控制 Tool 调用
5. 记录审计日志
```

### 9.2 多租户隔离

- **数据隔离**：tenant_id 字段隔离
- **资源隔离**：每个租户独立的向量库 Collection
- **模型隔离**：租户级别的模型配置

### 9.3 安全措施

- ✅ HTTPS 加密传输
- ✅ API Key / JWT 认证
- ✅ RBAC 权限控制
- ✅ 工具调用审计
- ✅ 敏感数据脱敏
- ✅ SQL 注入防护
- ✅ XSS 防护

---

## 十、实施计划

### 10.1 MVP 阶段（4 周）

#### Week 1-2: 基础设施
- [x] 项目脚手架搭建
- [ ] Core Layer（配置、DI、异常、日志）
- [ ] Infrastructure Layer（PostgreSQL、Redis）
- [ ] API Layer（路由、响应格式、Swagger）

#### Week 3: AI 基础
- [ ] Model Provider（OpenAI）
- [ ] Memory Layer（向量存储 + 文档加载）
- [ ] Tools Layer（RAG 工具）

#### Week 4: Agent 和 Workflow
- [ ] Agent Layer（Retrieval Agent + Answer Agent）
- [ ] Workflow Layer（简单 RAG 工作流）
- [ ] Application Layer（Chat Service）

**MVP 交付物**：
- 基础 RAG 问答功能
- 1 个向量库支持
- 1 个模型提供者（OpenAI）
- 基础 API 和文档

### 10.2 Beta 阶段（4 周）

- [ ] 多模型支持（DeepSeek、Ollama）
- [ ] 模型路由和 Fallback
- [ ] 插件系统
- [ ] 多种 Agent 策略（ReAct、Reflection）
- [ ] 复杂工作流（Multi-Agent）
- [ ] 监控和追踪

### 10.3 Production 阶段（4 周）

- [ ] 安全和审计
- [ ] 多租户支持
- [ ] 性能优化
- [ ] 压力测试
- [ ] 部署文档
- [ ] 生产环境上线

---

## 十一、总结

本架构设计融合了**传统分层架构的工程化能力**和 **AI Native 架构的智能化能力**，实现了：

✅ **清晰的分层**：API、Application、AI Native、Infrastructure、Core  
✅ **强大的抽象**：接口驱动，易于扩展和测试  
✅ **企业级就绪**：安全、审计、多租户、可观测性  
✅ **AI 原生**：Agent、Workflow、RAG、多模型  
✅ **高性能**：异步 IO、缓存优化、连接池  

架构已就绪，可以开始实施。

---

**End of Document**

