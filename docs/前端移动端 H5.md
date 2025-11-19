# 前端移动端 H5 实现指南

## 概述

AstralAgent 前端已重构为移动端 H5 应用，使用 **Ant Design Mobile** 作为 UI 组件库，提供完整的移动端体验。

## 技术栈

### 核心框架
- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具

### UI 组件库
- **Ant Design Mobile 5.34.0** - 移动端 UI 组件库
  - TabBar 底部导航
  - Card 卡片
  - PullToRefresh 下拉刷新
  - Toast 提示
  - Form 表单
  - 等移动端优化组件

### 其他依赖
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **Axios** - HTTP 客户端

## 移动端特性

### 1. 响应式布局
- 使用 `rem` 单位实现自适应布局
- 基准宽度：375px（iPhone 标准宽度）
- 自动适配不同屏幕尺寸

### 2. 底部导航栏
- 使用 Ant Design Mobile 的 `TabBar` 组件
- 固定底部，适配安全区域（iPhone X 等）
- 四个主要页面：首页、智能体、工作流、设置

### 3. 触摸优化
- 禁用文本选择（输入框除外）
- 优化滚动体验（`-webkit-overflow-scrolling: touch`）
- 触摸反馈优化

### 4. 安全区域适配
- 自动适配 iPhone X 等设备的安全区域
- 使用 `env(safe-area-inset-*)` CSS 变量
- 底部导航栏自动适配底部指示条

### 5. 性能优化
- 代码分割
- 懒加载
- 生产环境压缩优化（移除 console、debugger）

## 项目结构

```
frontend/
├── src/
│   ├── api/                    # API 调用
│   │   ├── client.ts          # Axios 实例（移动端 Toast）
│   │   └── system.ts          # 系统 API
│   ├── components/             # 公共组件
│   │   └── Layout/            # 移动端布局（TabBar）
│   │       ├── index.tsx
│   │       └── style.css
│   ├── pages/                  # 页面
│   │   ├── Dashboard/         # 仪表盘（移动端优化）
│   │   ├── AgentList/         # 智能体列表
│   │   ├── WorkflowList/      # 工作流列表
│   │   └── Settings/          # 设置
│   ├── stores/                 # 状态管理
│   │   └── useSystemStore.ts
│   ├── utils/                  # 工具函数
│   │   └── rem.ts             # rem 适配工具
│   ├── App.tsx                 # 根组件
│   ├── main.tsx                # 入口文件
│   └── index.css               # 全局样式（移动端优化）
├── index.html                  # HTML 模板（移动端 meta）
├── vite.config.ts              # Vite 配置（移动端优化）
└── package.json                # 依赖配置
```

## 关键文件说明

### 1. `src/utils/rem.ts`
rem 适配工具，根据设备宽度动态设置根元素字体大小。

```typescript
// 基准宽度：375px
// 基准字体：16px
// 自动适配不同屏幕
```

### 2. `src/components/Layout/index.tsx`
移动端布局组件，使用 TabBar 实现底部导航。

### 3. `src/index.css`
移动端全局样式：
- 禁用文本选择
- 优化滚动
- 安全区域适配
- 触摸优化

### 4. `index.html`
移动端 HTML 配置：
- viewport 设置
- PWA 支持（可配置）
- 主题色设置

## 开发指南

### 安装依赖

```bash
cd frontend
pnpm install
```

### 启动开发服务器

```bash
pnpm dev
```

访问：http://localhost:5173

### 构建生产版本

```bash
pnpm build
```

输出目录：`frontend/dist/`

### 预览生产版本

```bash
pnpm preview
```

## 移动端适配最佳实践

### 1. 使用 rem 单位
```css
/* 推荐 */
width: 10rem;
font-size: 1rem;

/* 不推荐 */
width: 150px;
font-size: 14px;
```

### 2. 使用 Ant Design Mobile 组件
```tsx
import { Card, Button, Toast } from 'antd-mobile'

// 使用移动端优化组件
<Card>
  <Button color="primary">按钮</Button>
</Card>
```

### 3. 触摸友好的交互
- 按钮最小点击区域：44x44px
- 使用 `PullToRefresh` 实现下拉刷新
- 使用 `Toast` 替代 `message` 提示

### 4. 性能优化
- 使用 `React.lazy` 实现路由懒加载
- 图片使用 `loading="lazy"` 延迟加载
- 避免在移动端使用过大的动画

## 与桌面端的区别

| 特性 | 桌面端 | 移动端 H5 |
|------|--------|-----------|
| UI 组件库 | Ant Design | Ant Design Mobile |
| 布局方式 | 侧边栏导航 | 底部 TabBar |
| 响应式 | 固定宽度 | rem 自适应 |
| 交互方式 | 鼠标点击 | 触摸操作 |
| 提示组件 | message | Toast |
| 表单组件 | Form (桌面) | Form (移动端优化) |

## 浏览器兼容性

- ✅ iOS Safari 12+
- ✅ Android Chrome 80+
- ✅ 微信内置浏览器
- ✅ 支付宝内置浏览器

## 部署

### Nginx 配置

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

## 常见问题

### Q: 如何调试移动端？
A: 使用 Chrome DevTools 的设备模拟器，或使用手机访问开发服务器（确保在同一网络）。

### Q: 如何适配不同屏幕尺寸？
A: 使用 rem 单位，系统会自动适配。如需特殊处理，使用媒体查询。

### Q: 如何实现下拉刷新？
A: 使用 `PullToRefresh` 组件包裹内容区域。

### Q: 如何显示提示信息？
A: 使用 `Toast.show()` 替代 `message.error()`。

## 后续优化方向

- [ ] PWA 支持（离线访问、安装到桌面）
- [ ] 手势操作（滑动、长按等）
- [ ] 暗色模式支持
- [ ] 国际化（i18n）
- [ ] 性能监控和优化

