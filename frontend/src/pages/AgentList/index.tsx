import { Card, Button, Empty } from 'antd-mobile'
import { AddOutline } from 'antd-mobile-icons'

export default function AgentList() {
  return (
    <div className="mobile-page">
      <div className="mobile-title">智能体管理</div>
      <Card>
        <Empty description="暂无智能体" />
        <div style={{ marginTop: 16, textAlign: 'center' }}>
          <Button
            color="primary"
            fill="solid"
            size="large"
            style={{ width: '100%' }}
            onClick={() => {
              // TODO: 跳转到创建智能体页面
            }}
          >
            <AddOutline /> 创建智能体
          </Button>
        </div>
      </Card>
    </div>
  )
}
