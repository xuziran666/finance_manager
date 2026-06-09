import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    redirect: { path: '/dash' },
    children: [
      { path: 'dash', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'acc', name: 'Accounts', component: () => import('../views/Accounts.vue') },
      { path: 'txn', name: 'Transactions', component: () => import('../views/Transactions.vue') },
      { path: 'cat', name: 'Categories', component: () => import('../views/Categories.vue') },
      { path: 'budget', name: 'Budget', component: () => import('../views/Budget.vue') },
      { path: 'stats', name: 'Statistics', component: () => import('../views/Statistics.vue') },
      { path: 'logs', name: 'Logs', component: () => import('../views/Logs.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/login' || to.path === '/register') {
    token ? next('/dash') : next()
  } else if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router
