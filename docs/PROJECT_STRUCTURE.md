# AstralAgent 项目结构说明

## 目录结构

```
AstralAgent/
│
├── backend/                          # 后端应用目录
│   ├── app/                          # 应用主目录
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI 应用入口
│   │   ├── factory.py                # 应用工厂
│   │   ├── factory_lifespan.py       # 生命周期管理
│   │   ├── factory_middleware.py     # 中间件注册
│   │   ├── factory_routes.py         # 路由注册
│   │
│   ├── core/                         # 核心层（横切关注点）
│   │   ├── __init__.py
│   │   ├── config/                   # 配置管理
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 配置提供者接口
│   │   │   ├── loader.py             # 配置加载器
│   │   │   ├── registry.py           # 配置注册中心
│   │   │   ├── models.py             # Pydantic 配置模型
│   │   │   └── providers/            # 配置源实现
│   │   │       ├── __init__.py
│   │   │       ├── env_provider.py   # 环境变量
│   │   │       ├── toml_provider.py  # TOML 文件
│   │   │       ├── nacos_provider.py # Nacos 配置中心
│   │   │       └── consul_provider.py# Consul 配置中心
│   │   │
│   │   ├── di/                       # 依赖注入
│   │   │   ├── __init__.py
│   │   │   ├── container.py          # DI 容器
│   │   │   ├── providers.py          # Provider 定义
│   │   │   └── decorators.py         # 装饰器
│   │   │
│   │   ├── exceptions/               # 异常体系
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 异常基类
│   │   │   ├── api_exceptions.py     # API 异常
│   │   │   ├── agent_exceptions.py   # Agent 异常
│   │   │   ├── model_exceptions.py   # 模型异常
│   │   │   └── handlers.py           # 异常处理器
│   │   │
│   │   ├── logging/                  # 日志系统
│   │   │   ├── __init__.py
│   │   │   ├── logger.py             # 结构化日志
│   │   │   ├── formatters.py         # 日志格式化
│   │   │   └── handlers.py           # 日志处理器
│   │   │
│   │   ├── monitoring/               # 监控和追踪
│   │   │   ├── __init__.py
│   │   │   ├── metrics.py            # Prometheus 指标
│   │   │   ├── tracing.py            # OpenTelemetry 追踪
│   │   │   └── health.py             # 健康检查
│   │   │
│   │   ├── security/                 # 安全
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # 认证
│   │   │   ├── permissions.py        # 权限控制
│   │   │   ├── audit.py              # 审计日志
│   │   │   └── encryption.py         # 加密工具
│   │   │
│   │   └── events/                   # 事件总线
│   │       ├── __init__.py
│   │       ├── bus.py                # 事件总线
│   │       ├── handlers.py           # 事件处理器
│   │       └── decorators.py         # 事件装饰器
│   │
│   ├── infrastructure/               # 基础设施层
│   │   ├── __init__.py
│   │   │
│   │   ├── middleware/               # 中间件
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 中间件接口
│   │   │   ├── manager.py            # 中间件管理器
│   │   │   │
│   │   │   ├── database/             # 数据库
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py           # 数据库接口
│   │   │   │   ├── postgres.py       # PostgreSQL 实现
│   │   │   │   ├── mysql.py          # MySQL 实现
│   │   │   │   ├── sqlite.py         # SQLite 实现
│   │   │   │   ├── connection_pool.py# 连接池
│   │   │   │   └── session.py        # 会话管理
│   │   │   │
│   │   │   ├── cache/                # 缓存
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py           # 缓存接口
│   │   │   │   ├── redis.py          # Redis 实现
│   │   │   │   ├── memory.py         # 内存缓存
│   │   │   │   └── strategies.py     # 缓存策略
│   │   │   │
│   │   │   ├── message_queue/        # 消息队列
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py           # MQ 接口
│   │   │   │   ├── rabbitmq.py       # RabbitMQ 实现
│   │   │   │   └── kafka.py          # Kafka 实现
│   │   │   │
│   │   │   └── storage/              # 对象存储
│   │   │       ├── __init__.py
│   │   │       ├── base.py           # 存储接口
│   │   │       ├── s3.py             # AWS S3
│   │   │       ├── oss.py            # 阿里云 OSS
│   │   │       └── local.py          # 本地存储
│   │   │
│   │   ├── models/                   # 模型提供者
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 模型接口
│   │   │   ├── registry.py           # 模型注册中心
│   │   │   ├── router.py             # 模型路由器
│   │   │   ├── retry.py              # 重试策略
│   │   │   ├── fallback.py           # Fallback 机制
│   │   │   ├── metrics.py            # Token 统计
│   │   │   └── providers/            # 模型实现
│   │   │       ├── __init__.py
│   │   │       ├── openai.py         # OpenAI
│   │   │       ├── deepseek.py       # DeepSeek
│   │   │       ├── ollama.py         # Ollama
│   │   │       └── custom.py         # 自定义
│   │   │
│   │   ├── plugins/                  # 插件系统
│   │   │   ├── __init__.py
│   │   │   ├── loader.py             # 插件加载器
│   │   │   ├── registry.py           # 插件注册中心
│   │   │   ├── lifecycle.py          # 生命周期管理
│   │   │   ├── validator.py          # 插件校验
│   │   │   └── sandbox.py            # 沙箱隔离
│   │   │
│   │   ├── repositories/             # 数据仓储
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 仓储接口
│   │   │   ├── user_repository.py    # 用户仓储
│   │   │   ├── session_repository.py # 会话仓储
│   │   │   └── document_repository.py# 文档仓储
│   │   │
│   │   └── external/                 # 外部服务
│   │       ├── __init__.py
│   │       ├── http_client.py        # HTTP 客户端
│   │       └── webhooks.py           # Webhook 集成
│   │
│   ├── memory/                       # 知识与记忆层
│   │   ├── __init__.py
│   │   │
│   │   ├── vector/                   # 向量存储
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 向量存储接口
│   │   │   ├── milvus.py             # Milvus 实现
│   │   │   ├── pgvector.py           # pgvector 实现
│   │   │   └── chroma.py             # Chroma 实现
│   │   │
│   │   ├── conversation/             # 会话记忆
│   │   │   ├── __init__.py
│   │   │   ├── memory.py             # 会话记忆
│   │   │   ├── short_term.py         # 短期记忆
│   │   │   ├── long_term.py          # 长期记忆
│   │   │   └── summary.py            # 记忆摘要
│   │   │
│   │   ├── document/                 # 文档处理
│   │   │   ├── __init__.py
│   │   │   ├── loader.py             # 文档加载器
│   │   │   ├── chunker.py            # 文档分块
│   │   │   ├── embedder.py           # 嵌入生成
│   │   │   └── indexer.py            # 索引构建
│   │   │
│   │   └── rag/                      # RAG 引擎
│   │       ├── __init__.py
│   │       ├── engine.py             # RAG 引擎
│   │       ├── retriever.py          # 检索器
│   │       ├── reranker.py           # 重排序
│   │       └── fusion.py             # 融合检索
│   │
│   ├── tools/                        # 工具系统
│   │   ├── __init__.py
│   │   ├── base.py                   # 工具接口
│   │   ├── registry.py               # 工具注册中心
│   │   ├── executor.py               # 工具执行器
│   │   │
│   │   ├── builtin/                  # 内置工具
│   │   │   ├── __init__.py
│   │   │   ├── http_tool.py          # HTTP 请求工具
│   │   │   ├── db_tool.py            # 数据库工具
│   │   │   ├── rag_tool.py           # RAG 检索工具
│   │   │   ├── code_tool.py          # 代码执行工具
│   │   │   └── calculator_tool.py    # 计算器工具
│   │   │
│   │   ├── enterprise/               # 企业系统工具
│   │   │   ├── __init__.py
│   │   │   ├── crm_tool.py           # CRM 工具
│   │   │   ├── oa_tool.py            # OA 工具
│   │   │   └── erp_tool.py           # ERP 工具
│   │   │
│   │   ├── plugins/                  # 插件工具
│   │   │   └── __init__.py
│   │   │
│   │   └── permissions/              # 权限控制
│   │       ├── __init__.py
│   │       ├── rbac.py               # 基于角色的访问控制
│   │       └── audit.py              # 工具审计
│   │
│   ├── agents/                       # 智能体层
│   │   ├── __init__.py
│   │   ├── base.py                   # Agent 接口
│   │   ├── registry.py               # Agent 注册中心
│   │   ├── executor.py               # Agent 执行器
│   │   ├── state.py                  # Agent 状态管理
│   │   │
│   │   ├── builtin/                  # 内置 Agent
│   │   │   ├── __init__.py
│   │   │   ├── retrieval_agent.py    # 检索 Agent
│   │   │   ├── answer_agent.py       # 回答 Agent
│   │   │   ├── planner_agent.py      # 规划 Agent
│   │   │   └── reflection_agent.py   # 反思 Agent
│   │   │
│   │   ├── prompts/                  # Prompt 模板
│   │   │   ├── __init__.py
│   │   │   ├── templates/            # 模板文件
│   │   │   │   ├── retrieval.txt
│   │   │   │   ├── answer.txt
│   │   │   │   └── planner.txt
│   │   │   ├── manager.py            # Prompt 管理器
│   │   │   └── optimizer.py          # Prompt 优化
│   │   │
│   │   └── strategies/               # Agent 策略
│   │       ├── __init__.py
│   │       ├── react.py              # ReAct 策略
│   │       ├── tot.py                # Tree of Thoughts
│   │       └── reflexion.py          # Reflexion 策略
│   │
│   ├── workflows/                    # 工作流层
│   │   ├── __init__.py
│   │   ├── base.py                   # Workflow 基类
│   │   ├── graph.py                  # LangGraph 封装
│   │   ├── state.py                  # 状态管理
│   │   ├── checkpoint.py             # Checkpoint 机制
│   │   ├── orchestrator.py           # 工作流编排器
│   │   │
│   │   ├── nodes/                    # 工作流节点
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 节点基类
│   │   │   ├── agent_node.py         # Agent 节点
│   │   │   ├── tool_node.py          # Tool 节点
│   │   │   └── condition_node.py     # 条件节点
│   │   │
│   │   ├── builtin/                  # 内置工作流
│   │   │   ├── __init__.py
│   │   │   ├── rag_flow.py           # RAG 工作流
│   │   │   ├── multi_agent_flow.py   # 多 Agent 工作流
│   │   │   └── reflection_flow.py    # 反思工作流
│   │   │
│   │   └── plugins/                  # 插件工作流
│   │       └── __init__.py
│   │
│   ├── application/                  # 应用层
│   │   ├── __init__.py
│   │   │
│   │   ├── services/                 # 应用服务
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py       # 聊天服务
│   │   │   ├── agent_service.py      # Agent 服务
│   │   │   ├── workflow_service.py   # 工作流服务
│   │   │   └── rag_service.py        # RAG 服务
│   │   │
│   │   ├── use_cases/                # 用例
│   │   │   ├── __init__.py
│   │   │   ├── chat/                 # 聊天用例
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_chat.py
│   │   │   │   └── send_message.py
│   │   │   ├── retrieval/            # 检索用例
│   │   │   │   ├── __init__.py
│   │   │   │   ├── upload_document.py
│   │   │   │   └── search_document.py
│   │   │   └── automation/           # 自动化用例
│   │   │       └── __init__.py
│   │   │
│   │   ├── dto/                      # 数据传输对象
│   │   │   ├── __init__.py
│   │   │   ├── chat_dto.py
│   │   │   ├── agent_dto.py
│   │   │   └── document_dto.py
│   │   │
│   │   └── events/                   # 应用事件
│   │       ├── __init__.py
│   │       ├── chat_events.py
│   │       └── agent_events.py
│   │
│   ├── api/                          # API 层
│   │   ├── __init__.py
│   │   ├── base.py                   # API 基类
│   │   ├── registry.py               # 路由注册中心
│   │   ├── responses.py              # 统一响应格式
│   │   ├── exceptions.py             # API 异常
│   │   ├── dependencies.py           # FastAPI 依赖
│   │   ├── middleware.py             # HTTP 中间件
│   │   │
│   │   ├── v1/                       # API v1
│   │   │   ├── __init__.py
│   │   │   ├── router.py             # 路由聚合
│   │   │   └── endpoints/            # 端点
│   │   │       ├── __init__.py
│   │   │       ├── chat.py           # 聊天接口
│   │   │       ├── agents.py         # Agent 管理
│   │   │       ├── rag.py            # RAG 接口
│   │   │       ├── workflows.py      # 工作流接口
│   │   │       ├── plugins.py        # 插件管理
│   │   │       └── health.py         # 健康检查
│   │   │
│   │   └── streaming/                # 流式响应
│   │       ├── __init__.py
│   │       ├── sse.py                # Server-Sent Events
│   │       └── websocket.py          # WebSocket
│   │
│   ├── domain/                       # 领域层（可选）
│   │   ├── __init__.py
│   │   ├── entities/                 # 实体
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   └── document.py
│   │   ├── value_objects/            # 值对象
│   │   │   ├── __init__.py
│   │   │   └── message.py
│   │   └── services/                 # 领域服务
│   │       ├── __init__.py
│   │       └── session_service.py
│   │
│   └── configs/                      # 配置定义
│       ├── __init__.py
│       ├── app_config.py             # 应用配置
│       ├── model_config.py           # 模型配置
│       ├── db_config.py              # 数据库配置
│       ├── redis_config.py           # Redis 配置
│       └── infra_config.py           # 基础设施配置
│
├── plugins/                          # 外部插件
│   └── example_plugin/
│       ├── manifest.json             # 插件元数据
│       ├── __init__.py
│       ├── agents/                   # 插件 Agent
│       ├── tools/                    # 插件 Tool
│       └── workflows/                # 插件 Workflow
│
├── tests/                            # 测试
│   ├── __init__.py
│   ├── conftest.py                   # Pytest 配置
│   ├── unit/                         # 单元测试
│   │   ├── core/
│   │   ├── agents/
│   │   └── tools/
│   ├── integration/                  # 集成测试
│   │   ├── api/
│   │   └── workflows/
│   └── e2e/                          # 端到端测试
│       └── test_chat_flow.py
│
├── scripts/                          # 脚本
│   ├── init_db.py                    # 初始化数据库
│   ├── migrate.py                    # 数据库迁移
│   ├── load_plugins.py               # 加载插件
│   └── seed_data.py                  # 种子数据
│
├── docs/                             # 文档
│   ├── FINAL_ARCHITECTURE_DESIGN.md  # 最终架构设计
│   ├── ARCHITECTURE_ANALYSIS_AND_OPTIMIZATION.md  # 架构分析
│   ├── AI_Native_Architecture_Design.md  # AI 原生架构
│   ├── PROJECT_STRUCTURE.md          # 项目结构（本文件）
│   ├── API_DOCUMENTATION.md          # API 文档
│   ├── DEVELOPMENT.md                # 开发指南
│   ├── DEPLOYMENT.md                 # 部署指南
│   └── FAQ.md                        # 常见问题
│
├── .cursor/                          # Cursor 配置
│   └── rules/
│       └── Architect.mdc             # 架构规则
│
│   ├── run.py                        # 运行入口
│   ├── pyproject.toml                # 项目配置
│   ├── uv.lock                       # 依赖锁定文件
│   └── env.example                   # 环境变量示例
│
├── frontend/                         # 前端应用
│   ├── src/                          # 源代码
│   ├── package.json                  # 前端依赖
│   └── vite.config.ts                # Vite 配置
│
├── docs/                             # 文档
├── README.md                         # 项目说明
└── .gitignore                        # Git 忽略文件
├── Dockerfile                        # Docker 镜像
├── docker-compose.yml                # Docker Compose 配置
├── .dockerignore                     # Docker 忽略文件
├── .gitignore                        # Git 忽略文件
├── env.example                       # 环境变量示例
└── README.md                         # 项目说明
```

## 模块说明

### Core Layer（核心层）

所有层都依赖的基础横切层，提供：
- **配置管理**：多源配置支持
- **依赖注入**：统一的 DI 容器
- **异常处理**：统一异常体系
- **日志系统**：结构化日志
- **监控追踪**：指标收集和分布式追踪
- **安全**：认证、授权、审计
- **事件总线**：事件驱动架构支持

### Infrastructure Layer（基础设施层）

外部服务和中间件抽象：
- **Middleware**：数据库、缓存、消息队列、对象存储
- **Model Provider**：多模型接入和路由
- **Plugin System**：插件加载和管理
- **Repositories**：数据仓储
- **External**：外部服务集成

### Memory Layer（记忆层）

知识和记忆管理：
- **Vector Store**：向量数据库
- **Conversation Memory**：会话记忆
- **Document Processing**：文档处理
- **RAG Engine**：检索增强生成

### Tools Layer（工具层）

智能体可调用的工具：
- **Builtin Tools**：内置工具
- **Enterprise Tools**：企业系统集成
- **Plugin Tools**：插件工具
- **Permissions**：权限控制和审计

### Agents Layer（智能体层）

AI Agent 定义和执行：
- **Builtin Agents**：内置 Agent
- **Prompts**：Prompt 模板管理
- **Strategies**：Agent 策略（ReAct、ToT、Reflexion）

### Workflows Layer（工作流层）

基于 LangGraph 的工作流编排：
- **Nodes**：工作流节点
- **Builtin Workflows**：内置工作流
- **Orchestrator**：工作流编排器
- **Checkpoint**：状态检查点

### Application Layer（应用层）

业务逻辑编排：
- **Services**：应用服务
- **Use Cases**：用例
- **DTOs**：数据传输对象
- **Events**：应用事件

### API Layer（API 层）

对外接口：
- **REST API**：RESTful 接口
- **Streaming**：SSE 和 WebSocket
- **Middleware**：HTTP 中间件
- **Documentation**：Swagger/OpenAPI

## 依赖关系

```
API Layer
    ↓
Application Layer
    ↓
┌───────────────┴───────────────┐
│                               │
Agents/Workflows Layer    Infrastructure Layer
    ↓                           ↓
Memory/Tools Layer              │
    ↓                           │
    └───────────┬───────────────┘
                ↓
          Core Layer
```

**关键原则**：
- 内层不依赖外层
- 所有层都可以依赖 Core Layer
- 通过接口抽象实现解耦

## 配置文件

| 文件 | 用途 |
|-----|------|
| `pyproject.toml` | 项目配置和依赖 |
| `env.example` | 环境变量示例 |
| `docker-compose.yml` | 本地开发环境 |
| `Dockerfile` | 容器镜像 |

## 数据存储

| 存储类型 | 技术 | 用途 |
|---------|------|------|
| 关系数据库 | PostgreSQL | 用户、会话、文档元数据 |
| 缓存 | Redis | 缓存、会话状态 |
| 向量数据库 | Milvus | 文档向量、语义检索 |
| 对象存储 | S3/OSS | 文件存储 |
| 消息队列 | RabbitMQ | 异步任务 |

## 开发工具

| 工具 | 用途 |
|-----|------|
| `uv` | 依赖管理 |
| `pytest` | 测试 |
| `black` | 代码格式化 |
| `ruff` | 代码检查 |
| `mypy` | 类型检查 |

## 部署方式

1. **开发环境**：本地运行或 Docker Compose
2. **测试环境**：Docker 容器
3. **生产环境**：Kubernetes 集群

## 扩展点

项目提供以下扩展点：

1. **Config Provider**：添加新的配置源
2. **Model Provider**：接入新的模型
3. **Vector Store**：切换向量数据库
4. **Agent**：创建自定义 Agent
5. **Tool**：添加新工具
6. **Workflow**：定义新工作流
7. **Plugin**：开发插件

## 下一步

1. 实施 Core Layer（配置、DI、异常、日志）
2. 实施 Infrastructure Layer（数据库、Redis、模型）
3. 实施 Memory Layer（向量存储、RAG）
4. 实施 Agents 和 Workflows
5. 实施 API Layer

详细实施计划请参阅 [FINAL_ARCHITECTURE_DESIGN.md](FINAL_ARCHITECTURE_DESIGN.md)

