import { Card, Button, Empty } from 'antd-mobile'
import { AddOutline } from 'antd-mobile-icons'

export default function WorkflowList() {
  return (
    <div className="mobile-page">
      <div className="mobile-title">工作流管理</div>
      <Card>
        <Empty description="暂无工作流" />
        <div style={{ marginTop: 16, textAlign: 'center' }}>
          <Button
            color="primary"
            fill="solid"
            size="large"
            style={{ width: '100%' }}
            onClick={() => {
              // TODO: 跳转到创建工作流页面
            }}
          >
            <AddOutline /> 创建工作流
          </Button>
        </div>
      </Card>
    </div>
  )
}
