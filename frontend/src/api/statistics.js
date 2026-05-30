/**
 * 统计分析 API 接口模块
 */
import { request } from './request'

/** 获取统计数据（总收入/支出/趋势/分类占比） */
export function getStatistics(query) {
  return request('/api/statistics?' + query)
}
