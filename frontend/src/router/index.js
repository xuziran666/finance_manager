/**
 * Vue Router 路由配置
 * 定义 7 个页面路由，均使用懒加载方式按需加载组件
 */
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 根路径重定向到财务总览
  { path: '/', redirect: '/dash' },
  {
    path: '/dash',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/acc',
    name: 'Accounts',
    component: () => import('../views/Accounts.vue')
  },
  {
    path: '/txn',
    name: 'Transactions',
    component: () => import('../views/Transactions.vue')
  },
  {
    path: '/cat',
    name: 'Categories',
    component: () => import('../views/Categories.vue')
  },
  {
    path: '/budget',
    name: 'Budget',
    component: () => import('../views/Budget.vue')
  },
  {
    path: '/stats',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue')
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('../views/Logs.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router