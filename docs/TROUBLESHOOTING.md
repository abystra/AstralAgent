# 故障排查指南

## 🔍 常见问题

### 1. Swagger 无法访问（404）

#### 问题
访问 `http://localhost:8000/docs` 返回 404

#### 原因
- `DEBUG=false` 时 Swagger 被禁用
- 访问路径错误（应该是 `/docs` 而不是 `/api/docs`）

#### 解决方案

**方法 1：启用 Debug 模式**

编辑 `backend/.env`：
```env
DEBUG=true
```

**方法 2：确认访问路径**

正确的访问路径：
- ✅ `http://localhost:8000/docs` （Swagger UI）
- ✅ `http://localhost:8000/redoc` （ReDoc）
- ❌ `http://localhost:8000/api/docs` （错误路径）

---

### 2. 数据库连接错误

#### 错误信息
```
TypeError: unsupported operand type(s) for -: 'int' and 'str'
```

#### 原因
配置中的 `pool_size` 等参数从环境变量读取时是字符串，但 SQLAlchemy 需要整数。

#### 解决方案

**已自动修复**：代码已添加类型转换。

如果仍有问题，检查 `backend/.env`：
```env
DATABASE_POOL_SIZE=10        # 确保是数字
DATABASE_MAX_OVERFLOW=20     # 确保是数字
```

---

### 3. Redis 连接失败

#### 错误信息
```
ConnectionRefusedError: [Errno 61] Connection refused
```

#### 原因
Redis 服务未启动或未安装。

#### 解决方案

**选项 1：安装并启动 Redis**

```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# 验证
redis-cli ping
# 应该返回: PONG
```

**选项 2：不使用 Redis（可选依赖）**

如果不需要 Redis，可以不配置 `REDIS_URL`，应用会正常启动，只是缓存功能不可用。

---

### 4. 数据库连接失败

#### 错误信息
```
Failed to connect database: ...
```

#### 原因
- PostgreSQL 未安装或未启动
- 连接字符串错误
- 数据库不存在

#### 解决方案

**选项 1：安装 PostgreSQL**

```bash
# macOS
brew install postgresql
brew services start postgresql

# 创建数据库
createdb astralagent
```

**选项 2：不使用数据库（开发环境）**

如果不需要数据库，可以不配置 `DATABASE_URL`，应用会正常启动，只是数据库功能不可用。

---

### 5. 中间件连接失败但应用仍启动

#### 现象
日志显示中间件连接失败，但应用仍然启动成功。

#### 说明
这是**正常行为**！应用设计为：
- ✅ 中间件是**可选依赖**
- ✅ 连接失败不会阻止应用启动
- ✅ 只有使用该中间件时才会报错

#### 验证
即使数据库和 Redis 都未启动，以下接口仍然可用：
- `GET /` - 根路径
- `GET /health` - 健康检查
- `GET /docs` - Swagger 文档
- `GET /api/v1/` - API v1

---

## 🛠️ 调试步骤

### 1. 检查配置

```bash
cd backend
cat .env | grep DEBUG
# 应该显示: DEBUG=true
```

### 2. 检查服务状态

```bash
# 检查 Redis
redis-cli ping

# 检查 PostgreSQL
psql -U postgres -c "SELECT version();"
```

### 3. 查看日志

应用启动时的日志会显示：
- ✅ 哪些中间件注册成功
- ⚠️ 哪些中间件连接失败
- ✅ 应用是否成功启动

---

## 📋 最小化启动（无需数据库和 Redis）

如果只想测试 API，可以：

1. **不配置数据库和 Redis**
   ```env
   # 注释掉或删除这些行
   # DATABASE_URL=...
   # REDIS_URL=...
   ```

2. **启动应用**
   ```bash
   cd backend
   python run.py
   ```

3. **访问 Swagger**
   ```
   http://localhost:8000/docs
   ```

应用会正常启动，只是数据库和缓存功能不可用。

---

## ✅ 验证清单

启动前检查：

- [ ] `backend/.env` 文件存在
- [ ] `DEBUG=true` 已设置（用于 Swagger）
- [ ] 端口 8000 未被占用
- [ ] Python 3.12+ 已安装
- [ ] 依赖已安装（`uv sync`）

可选检查：

- [ ] PostgreSQL 已启动（如果需要数据库）
- [ ] Redis 已启动（如果需要缓存）

---

## 🚀 快速测试

### 测试应用是否正常

```bash
# 1. 启动应用
cd backend
python run.py

# 2. 测试健康检查（不需要数据库/Redis）
curl http://localhost:8000/health

# 3. 访问 Swagger
open http://localhost:8000/docs
```

如果健康检查返回 JSON，说明应用正常运行！

---

## 📞 获取帮助

如果问题仍未解决：

1. 查看完整日志输出
2. 检查 `.env` 配置
3. 确认依赖服务状态
4. 查看 [API 使用指南](API_USAGE.md)

---

<p align="center">
  <strong>问题排查完成</strong>
</p>

