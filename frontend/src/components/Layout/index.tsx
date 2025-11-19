/**
 * 移动端布局组件
 * 
 * 使用 Ant Design Mobile 的 TabBar 实现底部导航
 */

import { useState, useEffect } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { TabBar } from 'antd-mobile'
import {
  AppOutline,
  UnorderedListOutline,
  SetOutline,
} from 'antd-mobile-icons'
import './style.css'

const tabs = [
  {
    key: '/',
    title: '首页',
    icon: <AppOutline />,
  },
  {
    key: '/agents',
    title: '智能体',
    icon: <UnorderedListOutline />,
  },
  {
    key: '/workflows',
    title: '工作流',
    icon: <UnorderedListOutline />,
  },
  {
    key: '/settings',
    title: '设置',
    icon: <SetOutline />,
  },
]

export default function Layout() {
  const navigate = useNavigate()
  const location = useLocation()
  const [activeKey, setActiveKey] = useState(location.pathname)

  // 监听路由变化，同步 TabBar 状态
  useEffect(() => {
    setActiveKey(location.pathname)
  }, [location.pathname])

  const handleTabChange = (key: string) => {
    setActiveKey(key)
    navigate(key)
  }

  return (
    <div className="mobile-layout">
      {/* 主内容区 */}
      <div className="mobile-content">
        <Outlet />
      </div>

      {/* 底部导航栏 */}
      <TabBar
        activeKey={activeKey}
        onChange={handleTabChange}
        className="mobile-tabbar"
      >
        {tabs.map((item) => (
          <TabBar.Item key={item.key} icon={item.icon} title={item.title} />
        ))}
      </TabBar>
    </div>
  )
}
