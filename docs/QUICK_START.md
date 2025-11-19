# 快速开始指南

## 🚀 启动应用

### 1. 启动后端

```bash
cd backend
python run.py
```

后端运行在：**http://localhost:8000**

---

## 📚 访问 Swagger 文档

### Swagger UI（推荐）✨

```
http://localhost:8000/docs
```

**功能**：
- ✅ 交互式 API 文档
- ✅ 在线测试接口
- ✅ 查看请求/响应示例

### ReDoc

```
http://localhost:8000/redoc
```

### OpenAPI JSON

```
http://localhost:8000/openapi.json
```

---

## ⚙️ 启用 Swagger

确保 `backend/.env` 文件中设置了：

```env
DEBUG=true
```

如果访问 `/docs` 返回 404，说明 debug 模式未启用。

---

## 🧪 测试接口

### 方式 1：Swagger UI（最简单）

1. 访问 http://localhost:8000/docs
2. 找到接口（如 `GET /health`）
3. 点击 **"Try it out"**
4. 点击 **"Execute"**
5. 查看响应结果

### 方式 2：使用 curl

```bash
# 健康检查
curl http://localhost:8000/health

# 获取指标
curl http://localhost:8000/metrics

# 测试 API v1
curl http://localhost:8000/api/v1/
```

### 方式 3：浏览器直接访问

直接在浏览器中访问：
- http://localhost:8000/health
- http://localhost:8000/metrics
- http://localhost:8000/ping

---

## 📋 可用接口

| 接口 | 方法 | 说明 | 地址 |
|------|------|------|------|
| `/docs` | GET | Swagger UI | http://localhost:8000/docs |
| `/health` | GET | 健康检查 | http://localhost:8000/health |
| `/metrics` | GET | 性能指标 | http://localhost:8000/metrics |
| `/ping` | GET | Ping 检查 | http://localhost:8000/ping |
| `/api/v1/` | GET | API v1 | http://localhost:8000/api/v1/ |

---

## 🔧 常见问题

### Q: Swagger 无法访问（404）

**A**: 确保 `DEBUG=true` 在 `.env` 文件中。

### Q: 配置不生效

**A**: 
1. 检查 `backend/.env` 文件是否存在
2. 确保环境变量名称正确（大写，下划线分隔）
3. 重启应用

### Q: 端口被占用

**A**: 修改 `backend/.env` 中的 `API_PORT=8000` 为其他端口。

---

## 📖 详细文档

- [API 使用指南](API_USAGE.md) - 完整的 API 测试方法
- [项目结构](PROJECT_STRUCTURE.md) - 项目结构说明
- [架构设计](FINAL_ARCHITECTURE_DESIGN.md) - 系统架构

---

<p align="center">
  <strong>开始使用 AstralAgent API！</strong>
</p>

