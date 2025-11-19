import { Card, Empty, Button } from 'antd'
import { PlusOutlined } from '@ant-design/icons'

export default function WorkflowList() {
  return (
    <Card
      title="工作流管理"
      extra={
        <Button type="primary" icon={<PlusOutlined />}>
          创建工作流
        </Button>
      }
    >
      <Empty description="暂无工作流" />
    </Card>
  )
}

