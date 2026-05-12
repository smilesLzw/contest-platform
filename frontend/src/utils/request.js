import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
})

// 请求拦截器：自动添加 token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：统一处理响应和错误
request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code === 200) {
      return res
    }
    ElMessage.error(res.message || '请求失败')
    if (res.code === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      window.location.href = '/admin/login'
      return Promise.reject(new Error('未登录'))
    }
    return Promise.reject(new Error(res.message))
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      window.location.href = '/admin/login'
      return Promise.reject(new Error('未登录'))
    }
    // 格式化 FastAPI 422 验证错误
    const detail = error.response?.data?.detail
    const msg = Array.isArray(detail)
      ? detail.map(d => `${d.loc?.join('.')}: ${d.msg}`).join('；')
      : (detail || error.message || '网络错误')
    ElMessage.error(typeof msg === 'string' ? msg : '网络错误')
    return Promise.reject(error)
  }
)

export default request
