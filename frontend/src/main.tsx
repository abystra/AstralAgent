import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd-mobile'
import zhCN from 'antd-mobile/es/locales/zh-CN'
import 'dayjs/locale/zh-cn'
import App from './App'
import 'antd-mobile/es/global'
import './utils/rem' // 移动端 rem 适配
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  </React.StrictMode>,
)

// 移动端适配：设置 viewport
const setViewport = () => {
  const meta = document.querySelector('meta[name="viewport"]')
  if (!meta) {
    const viewport = document.createElement('meta')
    viewport.name = 'viewport'
    viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover'
    document.head.appendChild(viewport)
  }
}
setViewport()

