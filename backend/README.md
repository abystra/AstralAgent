# AstralAgent Backend

企业级多智能体平台后端服务

## 技术栈

- **Python 3.12+** - 编程语言
- **FastAPI** - Web 框架
- **SQLAlchemy** - ORM
- **Redis** - 缓存
- **uv** - 依赖管理

## 快速开始

### 1. 安装依赖

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入后端目录
cd backend

# 同步依赖（会自动创建虚拟环境在 backend/.venv/）
uv sync
```

**注意**：`uv` 会在 `backend/` 目录下自动创建 `.venv/` 虚拟环境。

### 2. 配置环境变量

```bash
cp env.example .env
```

编辑 `.env` 文件配置数据库、Redis 等。

### 3. 启动服务

```bash
# 方式 1：直接运行
python run.py

# 方式 2：使用 uvicorn
uvicorn app.main:app --reload

# 方式 3：使用 uv run
uv run python run.py
```

### 4. 访问

#### Swagger 文档（推荐）✨

- **Swagger UI**：http://localhost:8000/docs
  - 交互式 API 文档
  - 在线测试接口
  - 查看请求/响应示例

- **ReDoc**：http://localhost:8000/redoc
  - 更美观的文档展示

- **OpenAPI JSON**：http://localhost:8000/openapi.json
  - 用于导入 Postman 等工具

#### 系统接口

- 健康检查：http://localhost:8000/health
- 性能指标：http://localhost:8000/metrics
- Ping：http://localhost:8000/ping

**注意**：Swagger 文档只有在 `DEBUG=true` 时才会启用。确保 `.env` 文件中设置了 `DEBUG=true`。

## 项目结构

```
backend/
├── app/                    # 应用代码
│   ├── main.py            # 应用入口
│   ├── factory.py          # 应用工厂
│   ├── core/              # 核心层
│   ├── infrastructure/    # 基础设施层
│   ├── api/               # API 层
│   └── locales/          # 多语言配置
├── run.py                 # 启动脚本
├── pyproject.toml         # 项目配置
├── uv.lock                # 依赖锁定
└── env.example            # 环境变量示例
```

## 开发指南

### 添加新 API

1. 在 `app/api/v1/` 创建路由文件
2. 在 `app/factory_routes.py` 注册路由

### 添加新中间件

1. 实现 `Middleware` 接口
2. 在 `app/factory_lifespan.py` 注册

### 添加新配置

1. 在 `app/core/config/models.py` 定义配置类
2. 在 `.env` 添加环境变量

## 许可证

MIT

