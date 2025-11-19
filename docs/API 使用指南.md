# API 使用指南

## 📚 Swagger 文档访问

### 访问地址

启动后端服务后，访问以下地址：

#### 1. Swagger UI（推荐）✨

```
http://localhost:8000/docs
```

**功能**：
- ✅ 交互式 API 文档
- ✅ 在线测试接口
- ✅ 查看请求/响应示例
- ✅ 自动生成请求代码

#### 2. ReDoc（备用）

```
http://localhost:8000/redoc
```

**功能**：
- ✅ 更美观的文档展示
- ✅ 只读模式（不能测试）

#### 3. OpenAPI JSON

```
http://localhost:8000/openapi.json
```

**功能**：
- ✅ 获取 OpenAPI 规范 JSON
- ✅ 用于导入到 Postman、Insomnia 等工具

---

## ⚙️ 启用 Swagger

### 检查配置

Swagger 文档只有在 **debug 模式**下才会启用。

检查 `backend/.env` 文件：

```env
DEBUG=true
```

或者检查 `backend/app/core/config/models.py` 中的默认值。

### 如果 Swagger 无法访问

如果访问 `/docs` 返回 404，说明 debug 模式未启用：

1. **方法 1：设置环境变量**
```bash
cd backend
export DEBUG=true
python app.py
```

2. **方法 2：修改 .env 文件**
```bash
cd backend
echo "DEBUG=true" >> .env
python app.py
```

3. **方法 3：强制启用（开发环境）**

修改 `backend/app/factory.py`：
```python
docs_url="/docs",  # 移除 if config.debug else None
```

---

## 🧪 测试接口

### 方式 1：使用 Swagger UI（最简单）✨

1. 访问 http://localhost:8000/docs
2. 找到要测试的接口（如 `/health`）
3. 点击 "Try it out"
4. 点击 "Execute"
5. 查看响应结果

**示例**：
- 测试健康检查：`GET /health`
- 测试指标：`GET /metrics`
- 测试 Ping：`GET /ping`

---

### 方式 2：使用 curl

#### 健康检查
```bash
curl http://localhost:8000/health
```

#### 获取指标
```bash
curl http://localhost:8000/metrics
```

#### 测试 API v1
```bash
curl http://localhost:8000/api/v1/
```

#### 带参数的请求（POST 示例）
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "email": "test@example.com"}'
```

---

### 方式 3：使用 Postman

1. **导入 OpenAPI 规范**
   - 打开 Postman
   - 点击 "Import"
   - 输入 URL：`http://localhost:8000/openapi.json`
   - 自动导入所有接口

2. **手动创建请求**
   - 新建 Request
   - 方法：GET/POST/PUT/DELETE
   - URL：`http://localhost:8000/health`
   - 点击 Send

---

### 方式 4：使用 Python requests

```python
import requests

# 健康检查
response = requests.get("http://localhost:8000/health")
print(response.json())

# 获取指标
response = requests.get("http://localhost:8000/metrics")
print(response.json())

# POST 请求示例
response = requests.post(
    "http://localhost:8000/api/v1/users",
    json={"name": "test", "email": "test@example.com"}
)
print(response.json())
```

---

### 方式 5：使用前端（已集成）

前端应用已集成 API 调用，可以直接在浏览器中测试：

1. 启动前端：`cd frontend && pnpm dev`
2. 访问：http://localhost:5173
3. 在仪表盘中查看系统状态和指标

---

## 📋 可用接口列表

### 系统接口

| 接口 | 方法 | 说明 | 示例 |
|------|------|------|------|
| `/` | GET | 根路径 | http://localhost:8000/ |
| `/health` | GET | 健康检查 | http://localhost:8000/health |
| `/metrics` | GET | 性能指标 | http://localhost:8000/metrics |
| `/ping` | GET | Ping 检查 | http://localhost:8000/ping |
| `/docs` | GET | Swagger UI | http://localhost:8000/docs |
| `/redoc` | GET | ReDoc | http://localhost:8000/redoc |
| `/openapi.json` | GET | OpenAPI 规范 | http://localhost:8000/openapi.json |

### API v1 接口

| 接口 | 方法 | 说明 | 示例 |
|------|------|------|------|
| `/api/v1/` | GET | API 根路径 | http://localhost:8000/api/v1/ |

---

## 🔍 接口测试示例

### 1. 测试健康检查

**Swagger UI**：
1. 访问 http://localhost:8000/docs
2. 找到 `GET /health`
3. 点击 "Try it out" → "Execute"

**curl**：
```bash
curl http://localhost:8000/health
```

**响应示例**：
```json
{
  "status": "healthy",
  "checks": {
    "system": {
      "status": "healthy",
      "message": null,
      "details": {
        "cpu_percent": 15.2,
        "memory_percent": 45.8,
        "memory_available_mb": 8192
      }
    }
  }
}
```

---

### 2. 测试指标

**curl**：
```bash
curl http://localhost:8000/metrics
```

**响应示例**：
```json
{
  "requests": {
    "total": 42,
    "duration": {
      "count": 42,
      "min": 0.001,
      "max": 0.123,
      "avg": 0.045,
      "p50": 0.042,
      "p95": 0.098,
      "p99": 0.115
    }
  },
  "errors": {
    "total": 0
  }
}
```

---

### 3. 测试 API v1

**curl**：
```bash
curl http://localhost:8000/api/v1/
```

**响应示例**：
```json
{
  "message": "API v1"
}
```

---

## 🛠️ 调试技巧

### 1. 查看请求日志

后端会记录所有请求，查看控制台输出。

### 2. 查看错误信息

如果接口返回错误，Swagger UI 会显示详细的错误信息。

### 3. 检查 CORS

如果前端调用失败，检查 CORS 配置：
- 后端允许的源：`http://localhost:5173`
- 前端代理配置：`frontend/vite.config.ts`

---

## 📝 注意事项

1. **确保后端已启动**
   ```bash
   cd backend
   python app.py
   ```

2. **确保 debug 模式开启**（才能访问 Swagger）
   ```env
   DEBUG=true
   ```

3. **端口冲突**
   - 后端默认：8000
   - 前端默认：5173
   - 如果端口被占用，修改配置

4. **CORS 配置**
   - 开发环境：已配置允许所有源
   - 生产环境：需要配置具体域名

---

## 🚀 快速开始

1. **启动后端**
   ```bash
   cd backend
   python app.py
   ```

2. **访问 Swagger**
   ```
   http://localhost:8000/docs
   ```

3. **测试接口**
   - 在 Swagger UI 中点击 "Try it out"
   - 或使用 curl/Postman

---

<p align="center">
  <strong>🎉 开始测试你的 API 吧！</strong>
</p>

