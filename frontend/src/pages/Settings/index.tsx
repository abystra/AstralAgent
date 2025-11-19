import { Card, Form, Input, Switch, Button, Toast } from 'antd-mobile'
import { CheckCircleOutline } from 'antd-mobile-icons'

export default function Settings() {
  const [form] = Form.useForm()

  const handleSave = async (values: any) => {
    console.log('Settings:', values)
    Toast.show({
      icon: 'success',
      content: '设置已保存',
    })
  }

  return (
    <div className="mobile-page">
      <div className="mobile-title">系统设置</div>
      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            apiUrl: 'http://localhost:8000',
            timeout: 30000,
            enableDebug: false,
          }}
          footer={
            <Button
              block
              type="submit"
              color="primary"
              size="large"
              style={{ marginTop: 16 }}
            >
              <CheckCircleOutline /> 保存设置
            </Button>
          }
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

          <Form.Item
            label="启用调试模式"
            name="enableDebug"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}
