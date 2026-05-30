/**
 * 分类管理 API 接口模块
 */
import { request } from './request'

/** 获取全部分类（树形结构 + 扁平列表） */
export function getCategories() {
  return request('/api/categories')
}

/** 添加新分类 */
export function createCategory(data) {
  return request('/api/categories', { method: 'POST', body: data })
}

/** 修改分类 */
export function updateCategory(data) {
  return request('/api/categories', { method: 'PUT', body: data })
}
