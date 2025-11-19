import { useEffect } from 'react'
import { Card, Grid, Tag, SpinLoading, PullToRefresh } from 'antd-mobile'
import { useSystemStore } from '@/stores/useSystemStore'
import './style.css'

export default function Dashboard() {
  const { health, metrics, loading, fetchHealth, fetchMetrics } = useSystemStore()

  useEffect(() => {
    fetchHealth()
    fetchMetrics()
  }, [fetchHealth, fetchMetrics])

  const handleRefresh = async () => {
    await Promise.all([fetchHealth(), fetchMetrics()])
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'success'
      case 'degraded':
        return 'warning'
      case 'unhealthy':
        return 'danger'
      default:
        return 'default'
    }
  }

  return (
    <div className="mobile-page">
      <PullToRefresh onRefresh={handleRefresh}>
        <div className="mobile-title">系统仪表盘</div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px 0' }}>
            <SpinLoading style={{ '--size': '48px' }} />
          </div>
        ) : (
          <>
            {/* 统计卡片 */}
            <Grid columns={2} gap={8} style={{ marginBottom: 16 }}>
              <Card>
                <div className="stat-item">
                  <div className="stat-label">请求总数</div>
                  <div className="stat-value">{metrics?.requests.total || 0}</div>
                </div>
              </Card>
              <Card>
                <div className="stat-item">
                  <div className="stat-label">平均响应</div>
                  <div className="stat-value">
                    {metrics?.requests.duration.avg
                      ? `${(metrics.requests.duration.avg * 1000).toFixed(0)}ms`
                      : '0ms'}
                  </div>
                </div>
              </Card>
              <Card>
                <div className="stat-item">
                  <div className="stat-label">错误总数</div>
                  <div className="stat-value error">
                    {metrics?.errors.total || 0}
                  </div>
                </div>
              </Card>
              <Card>
                <div className="stat-item">
                  <div className="stat-label">系统状态</div>
                  <div className="stat-value">
                    <Tag color={getStatusColor(health?.status || '')}>
                      {health?.status || 'unknown'}
                    </Tag>
                  </div>
                </div>
              </Card>
            </Grid>

            {/* 健康检查详情 */}
            <Card title="健康检查" style={{ marginBottom: 16 }}>
              {health?.checks && Object.entries(health.checks).length > 0 ? (
                <div className="health-list">
                  {Object.entries(health.checks).map(([name, check]) => (
                    <div key={name} className="health-item">
                      <div className="health-header">
                        <span className="health-name">{name}</span>
                        <Tag color={getStatusColor(check.status)}>
                          {check.status}
                        </Tag>
                      </div>
                      {check.message && (
                        <div className="health-message">{check.message}</div>
                      )}
                      {check.details && (
                        <div className="health-details">
                          {Object.entries(check.details).map(([key, value]) => (
                            <div key={key} className="health-detail-item">
                              <span className="detail-key">{key}:</span>
                              <span className="detail-value">{String(value)}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ textAlign: 'center', color: '#999', padding: '20px 0' }}>
                  暂无健康检查数据
                </div>
              )}
            </Card>

            {/* 性能指标 */}
            {metrics?.requests.duration && (
              <Card title="性能指标">
                <div className="metrics-list">
                  <div className="metric-item">
                    <span className="metric-label">最小响应时间</span>
                    <span className="metric-value">
                      {(metrics.requests.duration.min * 1000).toFixed(2)}ms
                    </span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">P95 响应时间</span>
                    <span className="metric-value">
                      {(metrics.requests.duration.p95 * 1000).toFixed(2)}ms
                    </span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">最大响应时间</span>
                    <span className="metric-value">
                      {(metrics.requests.duration.max * 1000).toFixed(2)}ms
                    </span>
                  </div>
                </div>
              </Card>
            )}
          </>
        )}
      </PullToRefresh>
    </div>
  )
}
