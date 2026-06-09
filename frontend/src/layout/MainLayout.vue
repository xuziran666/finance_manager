<template>
  <el-container class="app-container">
    <el-aside width="250px" class="app-sidebar">
      <div class="sidebar-header">
        <h5><el-icon :size="20"><Wallet /></el-icon> 财务管家</h5>
      </div>
      <el-divider />
      <el-menu
        :default-active="route.path"
        background-color="transparent"
        text-color="#a5b4fc"
        active-text-color="#ffffff"
        router
      >
        <el-menu-item v-for="m in menu" :key="m.k" :index="'/' + m.k">
          <el-icon><component :is="m.ic" /></el-icon>
          <span>{{ m.l }}</span>
        </el-menu-item>
        <el-divider />
        <el-menu-item index="backup" @click="showBackup">
          <el-icon><Upload /></el-icon>
          <span>数据管理</span>
        </el-menu-item>
      </el-menu>
      <div class="sidebar-footer">
        <el-divider />
        <div class="user-info">
          <el-icon><User /></el-icon>
          <span class="username">{{ username }}</span>
          <el-button text size="small" class="logout-btn" @click="handleLogout">
            退出
          </el-button>
        </div>
      </div>
    </el-aside>

    <el-main class="app-main">
      <router-view />
    </el-main>

    <el-dialog v-model="backupDialogVisible" title="数据管理" width="400px">
      <p>可通过 phpMyAdmin 或 mysqldump 工具备份 MySQL 数据库 <code>finance_manager</code>。</p>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const backupDialogVisible = ref(false)
const username = localStorage.getItem('username') || '用户'

const menu = [
  { k: 'dash', l: '财务总览', ic: 'House' },
  { k: 'acc', l: '账户管理', ic: 'OfficeBuilding' },
  { k: 'txn', l: '收支记录', ic: 'List' },
  { k: 'cat', l: '分类管理', ic: 'PriceTag' },
  { k: 'budget', l: '预算管理', ic: 'Coin' },
  { k: 'stats', l: '统计分析', ic: 'DataAnalysis' },
  { k: 'logs', l: '操作日志', ic: 'Document' }
]

const showBackup = () => {
  backupDialogVisible.value = true
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/login')
}
</script>

<style scoped>
.sidebar-footer {
  margin-top: auto;
  padding: 0 16px 16px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #a5b4fc;
  font-size: 14px;
}
.username {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.logout-btn {
  color: #a5b4fc !important;
}
.logout-btn:hover {
  color: #ef4444 !important;
}
</style>
