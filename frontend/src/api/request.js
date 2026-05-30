/**
 * HTTP 请求工具模块
 * 基于 axios 封装统一的请求方法，自动处理 JSON 和错误提示
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'

const http = axios.create({
  headers: { 'Content-Type': 'application/json' }
})

/**
 * 通用请求函数
 * @param {string} url — 请求地址
 * @param {object} opts — 选项（method, body）
 * @returns {object|null} — 响应数据或 null（请求失败时）
 */
export async function request(url, opts = {}) {
  try {
    const r = await http({ method: opts.method || 'GET', url, data: opts.body })
    return r.data
  } catch (e) {
    ElMessage.error(e.message)
    return null
  }
}

export default http
