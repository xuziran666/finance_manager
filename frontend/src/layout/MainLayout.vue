<template>
  <!-- 主布局：左侧固定侧边栏 + 右侧内容区 -->
  <el-container class="app-container">
    <!-- 侧边栏导航 -->
    <el-aside width="250px" class="app-sidebar">
      <div class="sidebar-header">
        <h5><el-icon :size="20"><Wallet /></el-icon> 财务管家</h5>
      </div>
      <el-divider />
      <!-- 导航菜单，与 vue-router 集成 -->
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
    </el-aside>

    <!-- 主内容区域 -->
    <el-main class="app-main">
      <router-view />
    </el-main>

    <!-- 数据管理对话框：提示数据库备份方式 -->
    <el-dialog v-model="backupDialogVisible" title="数据管理" width="400px">
      <p>可通过 phpMyAdmin 或 mysqldump 工具备份 MySQL 数据库 <code>finance_manager</code>。</p>
    </el-dialog>
  </el-container>
</template>

<script setup>
/**
 * 主布局组件
 * 固定侧边栏导航 + 动态路由内容区
 */
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const backupDialogVisible = ref(false)

// 导航菜单项配置：路由键 / 显示标签 / 图标组件名
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
</script>