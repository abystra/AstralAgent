# AstralAgent

> 企业级多智能体平台 | Multi-Agent Orchestration Platform

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

**AstralAgent** 是一个企业级多智能体平台，融合了：

- 🤖 **Multi-Agent 协作**：多智能体编排和协作
- 📚 **RAG 知识库**：企业知识检索和问答
- 💬 **AI 助手**：Chat、Task、Automation
- 🔌 **多模型接入**：OpenAI、DeepSeek、Ollama 等
- 🧩 **插件化扩展**：Agent、Tool、Workflow 可插拔
- 🔄 **LangGraph 编排**：智能工作流引擎

## 核心特性

### 架构特点

- ✅ **Clean Architecture**：依赖倒置，内层不依赖外层
- ✅ **横向分层 + 纵向领域**：工程化能力 + AI 原生能力
- ✅ **接口抽象**：所有组件通过接口交互，易于测试和替换
- ✅ **依赖注入**：统一的 DI 容器管理生命周期
- ✅ **事件驱动**：解耦组件，异步通信
- ✅ **配置驱动**：行为通过配置而非代码控制

### AI 能力

- 🧠 **多种 Agent 策略**：ReAct、Reflection、Tree of Thoughts
- 🔍 **企业级 RAG**：向量检索、Reranking、Hybrid Search
- 🌊 **工作流编排**：基于 LangGraph 的状态机
- 🛠️ **丰富的工具系统**：HTTP、数据库、企业系统集成
- 🔌 **插件系统**：动态加载和管理

### 企业级能力

- 🔒 **安全**：认证、授权、审计
- 👥 **多租户**：数据和资源隔离
- 📊 **可观测性**：Logging + Metrics + Tracing
- ⚡ **高性能**：异步 IO、缓存优化、连接池
- 🚀 **可扩展**：水平扩展，支持 K8s 部署

## 快速开始

### 前置要求

- Python 3.12+
- uv (推荐) 或 pip
- PostgreSQL 15+
- Redis 7+
- Milvus 2.3+ (可选，用于向量检索)

### 安装

```bash
# 克隆项目
git clone https://github.com/your-org/AstralAgent.git
cd AstralAgent

# 安装依赖
uv sync

# 或使用 pip
pip install -e .
```

### 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入必要的配置
vim .env
```

### 运行

#### 开发模式

```bash
# 启动应用
python app.py

# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

### 访问

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **API Base URL**: http://localhost:8000/api/v1

## 项目结构

```
AstralAgent/
├── app/                         # 应用代码
│   ├── core/                    # 核心层（配置、DI、日志等）
│   ├── infrastructure/          # 基础设施层
│   ├── memory/                  # 知识与记忆层
│   ├── tools/                   # 工具系统
│   ├── agents/                  # 智能体层
│   ├── workflows/               # 工作流层
│   ├── application/             # 应用层
│   ├── api/                     # API 层
│   └── main.py                  # 应用入口
│
├── plugins/                     # 插件目录
├── tests/                       # 测试
├── docs/                        # 文档
├── scripts/                     # 脚本
├── pyproject.toml              # 项目配置
├── docker-compose.yml          # Docker Compose 配置
└── README.md                   # 本文件
```

详细架构设计请参阅 [FINAL_ARCHITECTURE_DESIGN.md](docs/最终架构设计方案.md)

## API 使用示例

### 聊天接口

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是人工智能？",
    "session_id": "user-123"
  }'
```

响应：

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "answer": "人工智能是...",
    "session_id": "user-123",
    "token_usage": {
      "total_tokens": 150
    }
  },
  "trace_id": "abc-xyz-123"
}
```

### 流式聊天

```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"message": "介绍一下量子计算"}'
```

### RAG 文档上传

```bash
curl -X POST "http://localhost:8000/api/v1/rag/documents" \
  -F "file=@document.pdf" \
  -F "metadata={\"source\":\"manual\"}"
```

更多 API 示例请参阅 [API 文档](http://localhost:8000/docs)

## 配置说明

### 环境变量

主要配置项：

```bash
# 应用配置
APP_NAME=AstralAgent
DEBUG=false
API_V1_PREFIX=/api/v1

# 数据库
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/astralagent

# Redis
REDIS_URL=redis://localhost:6379/0

# 向量数据库
MILVUS_HOST=localhost
MILVUS_PORT=19530

# 模型配置
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-4

# 安全
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
```

完整配置项请参阅 [.env.example](.env.example)

### 多配置源

支持多种配置源（优先级从高到低）：

1. 环境变量
2. Nacos/Consul 配置中心
3. TOML 文件 (`config.toml`)
4. `.env` 文件（默认值）

## 开发指南

### 添加新的 Agent

```python
# app/agents/custom/my_agent.py
from app.agents.base import IAgent, AgentInput, AgentOutput

class MyAgent(IAgent):
    @property
    def name(self) -> str:
        return "my_agent"
    
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        # 实现你的 Agent 逻辑
        return AgentOutput(
            answer="...",
            reasoning="..."
        )

# 注册 Agent
from app.agents.registry import agent_registry
agent_registry.register(MyAgent())
```

### 添加新的 Tool

```python
# app/tools/custom/my_tool.py
from app.tools.base import ITool, ToolInput, ToolOutput

class MyToolInput(ToolInput):
    param1: str
    param2: int

class MyTool(ITool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    @property
    def description(self) -> str:
        return "工具描述"
    
    async def execute(self, input_data: MyToolInput) -> ToolOutput:
        # 实现工具逻辑
        return ToolOutput(success=True, result="...")

# 注册 Tool
from app.tools.registry import tool_registry
tool_registry.register(MyTool())
```

### 创建插件

```bash
# 创建插件目录
mkdir -p plugins/my_plugin

# 创建插件文件
plugins/my_plugin/
├── manifest.json    # 插件元数据
├── __init__.py
├── agents/         # 插件 Agent
├── tools/          # 插件 Tool
└── workflows/      # 插件 Workflow
```

详细开发指南请参阅 [开发文档](docs/DEVELOPMENT.md)

## 测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit

# 运行集成测试
pytest tests/integration

# 查看覆盖率
pytest --cov=app --cov-report=html
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t astralagent:latest .

# 运行容器
docker run -d \
  --name astralagent \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  astralagent:latest
```

### Kubernetes 部署

```bash
# 应用配置
kubectl apply -f k8s/

# 查看状态
kubectl get pods -l app=astralagent

# 查看日志
kubectl logs -f deployment/astralagent-api
```

详细部署文档请参阅 [DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 监控和运维

### 健康检查

```bash
curl http://localhost:8000/health
```

### Prometheus 指标

```bash
curl http://localhost:8000/metrics
```

### 日志查看

```bash
# Docker Compose
docker-compose logs -f app

# Kubernetes
kubectl logs -f deployment/astralagent-api
```

## 性能指标

| 指标 | 目标值 |
|-----|-------|
| API 响应时间 (P95) | < 2s |
| Agent 执行时间 (P95) | < 5s |
| RAG 检索时间 (P95) | < 500ms |
| 支持并发用户数 | > 1000 |

## 文档

- [架构设计](docs/最终架构设计方案.md)
- [架构分析与优化](docs/ARCHITECTURE_ANALYSIS_AND_OPTIMIZATION.md)
- [AI Native 设计](docs/AI_Native_Architecture_Design.md)
- [API 文档](http://localhost:8000/docs)
- [开发指南](docs/DEVELOPMENT.md)
- [部署指南](docs/DEPLOYMENT.md)

## 常见问题

### Q: 如何切换模型提供者？

在 `.env` 文件中修改：

```bash
DEFAULT_MODEL_PROVIDER=deepseek  # 或 ollama
```

### Q: 如何启用 Nacos 配置中心？

```bash
# .env
ENABLE_NACOS=true
NACOS_SERVER_ADDR=localhost:8848
NACOS_NAMESPACE=astralagent
```

### Q: 如何添加自定义向量库？

实现 `IVectorStore` 接口并注册到 DI 容器。

更多问题请参阅 [FAQ](docs/FAQ.md)

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

请确保：
- 代码通过所有测试
- 添加必要的测试用例
- 更新相关文档
- 遵循代码风格规范

## 路线图

### MVP (已完成)
- [x] 基础架构搭建
- [ ] Core Layer 实现
- [ ] RAG 基础功能
- [ ] 单模型支持（OpenAI）

### v0.2 (开发中)
- [ ] 多模型支持
- [ ] 插件系统
- [ ] 复杂工作流

### v1.0 (计划中)
- [ ] 生产级安全
- [ ] 多租户支持
- [ ] 完整监控体系
- [ ] 性能优化

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目主页: https://github.com/your-org/AstralAgent
- 文档: https://docs.astralagent.dev
- 问题反馈: https://github.com/your-org/AstralAgent/issues

## 致谢

特别感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Milvus](https://milvus.io/)

---

**Made with ❤️ by AstralAgent Team**

