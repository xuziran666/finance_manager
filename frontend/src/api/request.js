import axios from 'axios'
import { ElMessage } from 'element-plus'

const http = axios.create({
  headers: { 'Content-Type': 'application/json' }
})

http.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export async function request(url, opts = {}) {
  try {
    const r = await http({ method: opts.method || 'GET', url, data: opts.body })
    return r.data
  } catch (e) {
    if (e.response) {
      const msg = e.response.data?.detail || e.response.data?.msg || '请求失败'
      ElMessage.error(msg)
    } else if (e.request) {
      ElMessage.error('网络连接失败，请检查网络')
    }
    return null
  }
}

export default http
