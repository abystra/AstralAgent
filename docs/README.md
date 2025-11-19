# 文档目录

## 核心文档

### 1. [架构设计](最终架构设计方案.md)
完整的系统架构设计方案，包括：
- 架构概览
- 系统架构
- 模块设计
- 数据流设计
- 接口规范
- 技术选型
- 性能设计
- 安全设计

### 2. [项目结构](项目结构说明.md)
项目目录结构说明，包括：
- 目录结构
- 模块职责
- 依赖关系
- 扩展说明

### 3. [API 使用指南](API 使用指南.md) ✨
API 使用和测试指南，包括：
- Swagger 文档访问
- 接口测试方法
- curl/Postman 示例
- 调试技巧

---

## 快速导航

### 开发相关
- 配置管理：`backend/app/core/config/`
- 异常处理：`backend/app/core/exceptions/`
- 日志系统：`backend/app/core/logging/`
- 监控系统：`backend/app/core/monitoring/`

### 基础设施
- 数据库：`backend/app/infrastructure/database/`
- 缓存：`backend/app/infrastructure/cache/`
- 中间件：`backend/app/infrastructure/middleware/`

### API
- 系统路由：`backend/app/api/system.py`
- API v1：`backend/app/api/v1/`

### 多语言
- 中文：`backend/app/locales/zh-CN/`
- 英文：`backend/app/locales/en-US/`
- 日文：`backend/app/locales/ja-JP/`

---

## 相关资源

- [主 README](../README_ZH.md)
- [后端 README](../backend/README.md)
- [前端 README](../frontend/README.md)
- [环境变量示例](../backend/env.example)
- [项目配置](../backend/pyproject.toml)

---

## 快速开始

### 1. 启动后端
```bash
cd backend
python app.py
```

### 2. 访问 Swagger
```
http://localhost:8000/docs
```

### 3. 测试接口
在 Swagger UI 中点击 "Try it out" 即可测试接口。

详见：[API 使用指南](API 使用指南.md)
