/**
 * 共享状态模块
 * 在多个组件间共享账户列表、分类树、年份范围等全局数据
 */
import { ref } from 'vue'
import { getAccounts } from '../api/account'
import { getCategories } from '../api/category'

// 全局共享的响应式状态（模块级单例）
const accs = ref([])           // 账户列表
const catTree = ref({ income: {}, expense: {} })  // 分类树
const years = ref([])          // 可选年份列表（当前年 ±5 年）

// 生成年份范围
const y = new Date().getFullYear()
for (let i = y - 5; i <= y + 5; i++) years.value.push(i)

export function useStore() {
  /** 从后端加载账户列表 */
  const loadAccs = async () => {
    const r = await getAccounts()
    if (r && r.code === 200) accs.value = r.data
  }

  /** 从后端加载分类树 */
  const loadCats = async () => {
    const r = await getCategories()
    if (r && r.code === 200) catTree.value = r.data.tree
  }

  return {
    accs,      // 响应式账户列表
    catTree,   // 响应式分类树
    years,     // 年份列表
    loadAccs,  // 刷新账户列表
    loadCats   // 刷新分类树
  }
}