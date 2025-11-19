import axios, { AxiosError } from 'axios'
import { Toast } from 'antd-mobile'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    // 如果返回的是标准格式 { code, message, data }
    const { data } = response
    if (data.code !== undefined) {
      if (data.code === 0 || data.success) {
        return response
      } else {
        Toast.show({
          icon: 'fail',
          content: data.message || '请求失败',
        })
        return Promise.reject(new Error(data.message))
      }
    }
    return response
  },
  (error: AxiosError<any>) => {
    // 处理错误响应
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          Toast.show({
            icon: 'fail',
            content: '未授权，请重新登录',
          })
          // 清除 token 并跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          Toast.show({
            icon: 'fail',
            content: '没有权限访问该资源',
          })
          break
        case 404:
          Toast.show({
            icon: 'fail',
            content: '请求的资源不存在',
          })
          break
        case 500:
          Toast.show({
            icon: 'fail',
            content: data?.message || '服务器错误',
          })
          break
        default:
          Toast.show({
            icon: 'fail',
            content: data?.message || '请求失败',
          })
      }
    } else if (error.request) {
      Toast.show({
        icon: 'fail',
        content: '网络错误，请检查网络连接',
      })
    } else {
      Toast.show({
        icon: 'fail',
        content: '请求配置错误',
      })
    }
    
    return Promise.reject(error)
  }
)

export default apiClient

