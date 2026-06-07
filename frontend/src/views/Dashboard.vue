<template>
  <div>
    <h4 class="page-title">财务总览</h4>
    <el-row :gutter="16" class="mb-4">
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">总收入</div>
          <div class="stat-value text-success">{{ fmt(s.total_income) }}</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">总支出</div>
          <div class="stat-value text-danger">{{ fmt(s.total_expense) }}</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">结余</div>
          <div class="stat-value" :class="s.balance >= 0 ? 'text-primary' : 'text-danger'">{{ fmt(s.balance) }}</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">账户数</div>
          <div class="stat-value text-info">{{ accs.length }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-card shadow="never">
      <template #header>
        <span class="fw-bold">最近交易</span>
      </template>
      <el-table :data="recent" stripe style="width: 100%" empty-text="暂无">
        <el-table-column label="日期" width="175">
          <template #default="{ row }">
            {{ row.date?.replace('T', ' ') || row.date }}
          </template>
        </el-table-column>
        <el-table-column label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.type === 'income' ? 'success' : 'danger'" size="small" effect="plain">
              {{ row.type === 'income' ? '收入' : '支出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" />
        <el-table-column label="金额" width="120">
          <template #default="{ row }">
            <span :class="row.type === 'income' ? 'text-success' : 'text-danger'">
              {{ row.type === 'income' ? '+' : '-' }}{{ fmt(row.amount) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="account_name" label="账户" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
/**
 * 财务总览页面
 * 展示总收入/支出/结余统计卡片，以及最近 10 条交易记录
 */
import { ref, onMounted } from 'vue'
import { fmt } from '../api'
import { getStatistics } from '../api/statistics'
import { getTransactions } from '../api/transaction'
import { useStore } from '../composables/useStore'

const { accs } = useStore()

const s = ref({})      // 统计数据
const recent = ref([]) // 最近交易列表

/** 加载总览数据 */
const loadDash = async () => {
  const r = await getStatistics('group_by=month')
  if (r && r.code === 200) s.value = r.data
  const t = await getTransactions('page=1&page_size=10')
  if (t && t.code === 200) recent.value = t.data.transactions.slice(0, 10)
}

onMounted(() => {
  loadDash()
})
</script>