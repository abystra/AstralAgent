import { useEffect } from 'react'
import { Card, Row, Col, Statistic, Tag, Space, Button } from 'antd'
import {
  ApiOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import { useSystemStore } from '@/stores/useSystemStore'
import './style.css'

export default function Dashboard() {
  const { health, metrics, loading, fetchHealth, fetchMetrics } = useSystemStore()

  useEffect(() => {
    fetchHealth()
    fetchMetrics()
  }, [fetchHealth, fetchMetrics])

  const handleRefresh = () => {
    fetchHealth()
    fetchMetrics()
  }

  return (
    <div className="dashboard">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 标题栏 */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>系统仪表盘</h1>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={loading}>
            刷新
          </Button>
        </div>

        {/* 统计卡片 */}
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="请求总数"
                value={metrics?.requests.total || 0}
                prefix={<ApiOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="平均响应时间"
                value={metrics?.requests.duration.avg || 0}
                precision={2}
                suffix="ms"
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="错误总数"
                value={metrics?.errors.total || 0}
                valueStyle={{ color: metrics?.errors.total ? '#cf1322' : '#3f8600' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="系统状态"
                value={health?.status || 'unknown'}
                valueStyle={{
                  color: health?.status === 'healthy' ? '#3f8600' : '#cf1322',
                }}
                prefix={
                  health?.status === 'healthy' ? (
                    <CheckCircleOutlined />
                  ) : (
                    <CloseCircleOutlined />
                  )
                }
              />
            </Card>
          </Col>
        </Row>

        {/* 健康检查详情 */}
        <Card title="健康检查详情" loading={loading}>
          {health?.checks && (
            <Space direction="vertical" style={{ width: '100%' }}>
              {Object.entries(health.checks).map(([name, check]) => (
                <div key={name} className="health-check-item">
                  <Space>
                    <strong>{name}:</strong>
                    <Tag
                      color={
                        check.status === 'healthy'
                          ? 'success'
                          : check.status === 'degraded'
                          ? 'warning'
                          : 'error'
                      }
                    >
                      {check.status}
                    </Tag>
                    {check.message && <span>{check.message}</span>}
                  </Space>
                  {check.details && (
                    <pre style={{ marginTop: 8, fontSize: 12 }}>
                      {JSON.stringify(check.details, null, 2)}
                    </pre>
                  )}
                </div>
              ))}
            </Space>
          )}
        </Card>

        {/* 性能指标 */}
        <Card title="性能指标" loading={loading}>
          {metrics?.requests.duration && (
            <Row gutter={[16, 16]}>
              <Col span={8}>
                <Statistic
                  title="最小响应时间"
                  value={metrics.requests.duration.min}
                  precision={2}
                  suffix="ms"
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="P95 响应时间"
                  value={metrics.requests.duration.p95}
                  precision={2}
                  suffix="ms"
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="最大响应时间"
                  value={metrics.requests.duration.max}
                  precision={2}
                  suffix="ms"
                />
              </Col>
            </Row>
          )}
        </Card>
      </Space>
    </div>
  )
}

