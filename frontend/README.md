# AstralAgent Frontend

企业级多智能体平台前端应用

## 技术栈

- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **Ant Design** - UI 组件库
- **Axios** - HTTP 客户端

## 快速开始

### 安装依赖

```bash
pnpm install
```

### 开发模式

```bash
pnpm dev
```

访问：http://localhost:5173

### 生产构建

```bash
pnpm build
```

构建输出到 `dist/` 目录

### 预览构建

```bash
pnpm preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 调用
│   │   ├── client.ts    # Axios 实例
│   │   └── system.ts    # 系统 API
│   ├── components/       # 公共组件
│   │   └── Layout/      # 布局组件
│   ├── pages/           # 页面
│   │   ├── Dashboard/   # 仪表盘
│   │   ├── AgentList/   # 智能体列表
│   │   ├── WorkflowList/ # 工作流列表
│   │   └── Settings/    # 设置
│   ├── stores/          # 状态管理
│   │   └── useSystemStore.ts
│   ├── App.tsx          # 根组件
│   ├── main.tsx         # 入口文件
│   └── index.css        # 全局样式
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 环境变量

创建 `.env.local` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 功能特性

### 已实现

- ✅ 响应式布局
- ✅ 侧边栏导航
- ✅ 系统仪表盘
- ✅ 健康检查显示
- ✅ 性能指标展示
- ✅ API 调用封装
- ✅ 错误处理
- ✅ 请求拦截
- ✅ 响应拦截

### 待实现

- 📋 智能体管理
- 📋 工作流管理
- 📋 用户认证
- 📋 权限管理

## 开发指南

### 添加新页面

1. 在 `src/pages/` 创建页面目录
2. 创建 `index.tsx` 和 `style.css`
3. 在 `App.tsx` 添加路由

### 添加 API

1. 在 `src/api/` 创建新的 API 文件
2. 使用 `apiClient` 发起请求
3. 定义 TypeScript 类型

### 添加状态管理

1. 在 `src/stores/` 创建 store
2. 使用 Zustand 定义状态和方法
3. 在组件中使用 `useStore` hook

## 代码规范

- 使用 TypeScript 严格模式
- 遵循 ESLint 规则
- 组件使用函数式组件
- 状态管理使用 Zustand
- API 调用使用 async/await

## 性能优化

- 使用 React.lazy 懒加载路由
- 合理使用 React.memo
- 避免不必要的重渲染
- 使用 Vite 代码分割

## 部署

### Nginx 配置

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## 许可证

MIT

