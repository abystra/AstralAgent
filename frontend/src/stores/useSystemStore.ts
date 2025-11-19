import { create } from 'zustand'
import { systemAPI, HealthCheckResponse, MetricsResponse } from '@/api/system'

interface SystemState {
  health: HealthCheckResponse | null
  metrics: MetricsResponse | null
  loading: boolean
  
  // Actions
  fetchHealth: () => Promise<void>
  fetchMetrics: () => Promise<void>
}

export const useSystemStore = create<SystemState>((set) => ({
  health: null,
  metrics: null,
  loading: false,

  fetchHealth: async () => {
    set({ loading: true })
    try {
      const response = await systemAPI.healthCheck()
      set({ health: response.data, loading: false })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch health:', error)
    }
  },

  fetchMetrics: async () => {
    set({ loading: true })
    try {
      const response = await systemAPI.getMetrics()
      set({ metrics: response.data, loading: false })
    } catch (error) {
      set({ loading: false })
      console.error('Failed to fetch metrics:', error)
    }
  },
}))

