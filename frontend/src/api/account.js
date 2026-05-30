/**
 * 账户管理 API 接口模块
 */
import { request } from './request'

/** 获取所有账户列表 */
export function getAccounts() {
  return request('/api/accounts')
}

/** 添加新账户 */
export function createAccount(data) {
  return request('/api/accounts', { method: 'POST', body: data })
}

/** 更新账户信息 */
export function updateAccount(id, data) {
  return request('/api/accounts/' + id, { method: 'PUT', body: data })
}

/** 删除指定账户 */
export function deleteAccount(id) {
  return request('/api/accounts/' + id, { method: 'DELETE' })
}
