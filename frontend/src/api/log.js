/**
 * 操作日志 API 接口模块
 */
import { request } from './request'

/** 获取操作日志列表（最近 200 条） */
export function getLogs() {
  return request('/api/logs?limit=200')
}
