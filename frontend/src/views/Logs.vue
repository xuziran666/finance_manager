<template>
  <div>
    <h4 class="page-title">操作日志</h4>
    <el-card shadow="never">
      <el-table :data="logs" stripe style="width: 100%" max-height="500" empty-text="暂无">
        <el-table-column label="时间" width="180">
          <template #default="{ row }">
            <small>{{ row.time }}</small>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ row.action }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="详情">
          <template #default="{ row }">
            <small>{{ row.detail }}</small>
          </template>
        </el-table-column>
      </el-table>
      <div class="mt-2">
        <el-button @click="loadLogs" :icon="Refresh">刷新</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
/**
 * 操作日志页面
 * 展示系统操作日志列表，支持手动刷新
 */
import { ref, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { getLogs } from '../api/log'

const logs = ref([])

/** 加载操作日志 */
const loadLogs = async () => {
  const r = await getLogs()
  if (r && r.code === 200) logs.value = r.data
}

onMounted(() => {
  loadLogs()
})
</script>