import { Card, Form, Input, Switch, Button, Space, message } from 'antd'
import { SaveOutlined } from '@ant-design/icons'

export default function Settings() {
  const [form] = Form.useForm()

  const handleSave = (values: any) => {
    console.log('Settings:', values)
    message.success('设置已保存')
  }

  return (
    <Card title="系统设置">
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSave}
        initialValues={{
          apiUrl: 'http://localhost:8000',
          timeout: 30000,
          enableDebug: false,
        }}
      >
        <Form.Item
          label="API 地址"
          name="apiUrl"
          rules={[{ required: true, message: '请输入 API 地址' }]}
        >
          <Input placeholder="http://localhost:8000" />
        </Form.Item>

        <Form.Item
          label="请求超时（毫秒）"
          name="timeout"
          rules={[{ required: true, message: '请输入超时时间' }]}
        >
          <Input type="number" placeholder="30000" />
        </Form.Item>

        <Form.Item label="启用调试模式" name="enableDebug" valuePropName="checked">
          <Switch />
        </Form.Item>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
              保存设置
            </Button>
            <Button onClick={() => form.resetFields()}>重置</Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  )
}

