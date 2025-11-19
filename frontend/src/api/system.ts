import apiClient from './client'

export interface HealthCheckResponse {
  status: string
  checks: {
    [key: string]: {
      status: string
      message: string | null
      details: any
    }
  }
}

export interface MetricsResponse {
  requests: {
    total: number
    duration: {
      count: number
      min: number
      max: number
      avg: number
      p50: number
      p95: number
      p99: number
    }
  }
  errors: {
    total: number
  }
}

export interface RootResponse {
  name: string
  version: string
  environment: string
  docs: string | null
}

export const systemAPI = {
  /**
   * 获取根信息
   */
  getRoot: () => {
    return apiClient.get<RootResponse>('/')
  },

  /**
   * 健康检查
   */
  healthCheck: () => {
    return apiClient.get<HealthCheckResponse>('/health')
  },

  /**
   * 获取指标
   */
  getMetrics: () => {
    return apiClient.get<MetricsResponse>('/metrics')
  },

  /**
   * Ping
   */
  ping: () => {
    return apiClient.get('/ping')
  },
}

