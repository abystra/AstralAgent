# AstralAgent Frontend

企业级多智能体平台前端应用（移动端 H5）

## 技术栈

- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **Ant Design Mobile** - 移动端 UI 组件库 ⭐
- **Axios** - HTTP 客户端

## 移动端特性

- ✅ 响应式设计，适配各种移动设备
- ✅ 底部 TabBar 导航
- ✅ 下拉刷新（PullToRefresh）
- ✅ 触摸友好的交互
- ✅ 安全区域适配（iPhone X 等）
- ✅ rem 自适应布局
- ✅ PWA 支持（可配置）

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
│   │   └── Layout/      # 移动端布局（TabBar）
│   ├── pages/           # 页面
│   │   ├── Dashboard/   # 仪表盘（移动端优化）
│   │   ├── AgentList/   # 智能体列表
│   │   ├── WorkflowList/ # 工作流列表
│   │   └── Settings/    # 设置
│   ├── stores/          # 状态管理
│   │   └── useSystemStore.ts
│   ├── utils/           # 工具函数
│   │   └── rem.ts       # rem 适配
│   ├── App.tsx          # 根组件
│   ├── main.tsx         # 入口文件
│   └── index.css        # 全局样式（移动端优化）
├── index.html           # HTML 模板（移动端 meta）
├── vite.config.ts       # Vite 配置（移动端优化）
├── tsconfig.json
└── package.json
```

## 环境变量

创建 `.env.local` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 功能特性

### 已实现（移动端 H5）

- ✅ 移动端响应式布局
- ✅ 底部 TabBar 导航
- ✅ 下拉刷新（PullToRefresh）
- ✅ 系统仪表盘（移动端优化）
- ✅ 健康检查显示
- ✅ 性能指标展示
- ✅ API 调用封装
- ✅ 错误处理
- ✅ 请求拦截
- ✅ 响应拦截
- ✅ 安全区域适配
- ✅ rem 自适应布局

### 待实现

- 📋 智能体管理
- 📋 工作流管理
- 📋 用户认证
- 📋 权限管理
- 📋 PWA 支持

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

## 移动端适配说明

### 1. rem 适配

使用 `rem` 单位实现自适应布局，基准宽度 375px。

### 2. 安全区域适配

自动适配 iPhone X 等设备的安全区域（刘海屏、底部指示条）。

### 3. 触摸优化

- 禁用文本选择（输入框除外）
- 优化滚动体验
- 触摸反馈

### 4. 性能优化

- 代码分割
- 懒加载
- 压缩优化

## 部署

### Nginx 配置（移动端 H5）

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/frontend/dist;
    index index.html;

    # 移动端优化
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### CDN 部署

移动端 H5 适合部署到 CDN，提升访问速度。

## 许可证

MIT

