/**
 * 预算管理 API 接口模块
 */
import { request } from './request'

/** 获取预算汇总（含花费统计和预警） */
export function getBudgetSummary(year, month) {
  return request(`/api/budgets/summary?year=${year}&month=${month}`)
}

/** 设置预算 */
export function createBudget(data) {
  return request('/api/budgets', { method: 'POST', body: data })
}
