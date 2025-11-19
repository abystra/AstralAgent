import { Card, Empty, Button } from 'antd'
import { PlusOutlined } from '@ant-design/icons'

export default function AgentList() {
  return (
    <Card
      title="智能体管理"
      extra={
        <Button type="primary" icon={<PlusOutlined />}>
          创建智能体
        </Button>
      }
    >
      <Empty description="暂无智能体" />
    </Card>
  )
}

