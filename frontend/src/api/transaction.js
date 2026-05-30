/**
 * 交易记录 API 接口模块
 */
import { request } from './request'

/** 分页查询交易记录 */
export function getTransactions(query) {
  return request('/api/transactions?' + query)
}

/** 添加交易记录 */
export function createTransaction(data) {
  return request('/api/transactions', { method: 'POST', body: data })
}

/** 账户间转账 */
export function transfer(data) {
  return request('/api/transactions/transfer', { method: 'POST', body: data })
}
