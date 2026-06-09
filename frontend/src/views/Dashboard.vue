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
    <el-card shadow="never" class="mb-3">
      <template #header>
        <div class="d-flex align-items-center justify-content-between">
          <span class="fw-bold">收支趋势</span>
          <el-radio-group v-model="groupBy" size="small" @change="loadTrend">
            <el-radio-button value="month">月度</el-radio-button>
            <el-radio-button value="year">年度</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div ref="trendRef" style="width:100%;height:320px"></div>
    </el-card>
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
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { fmt } from '../api'
import { getStatistics } from '../api/statistics'
import { getTransactions } from '../api/transaction'
import { useStore } from '../composables/useStore'

const { accs } = useStore()

const s = ref({})
const recent = ref([])
const groupBy = ref('month')
const trendRef = ref(null)
let trendChart = null

const renderTrend = () => {
  if (!trendChart || !s.value.trend?.length) return
  const periods = s.value.trend.map(t => t.period)
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入', '支出', '结余'] },
    grid: { left: 60, right: 20, bottom: 30, top: 10 },
    xAxis: { type: 'category', data: periods, boundaryGap: false },
    yAxis: { type: 'value', axisLabel: { formatter: v => '¥' + v.toLocaleString() } },
    series: [
      {
        name: '收入', type: 'line', smooth: true, data: s.value.trend.map(t => t.income),
        lineStyle: { color: '#67c23a' }, itemStyle: { color: '#67c23a' }, areaStyle: { color: 'rgba(103,194,58,0.1)' }
      },
      {
        name: '支出', type: 'line', smooth: true, data: s.value.trend.map(t => t.expense),
        lineStyle: { color: '#f56c6c' }, itemStyle: { color: '#f56c6c' }, areaStyle: { color: 'rgba(245,108,108,0.1)' }
      },
      {
        name: '结余', type: 'line', smooth: true, data: s.value.trend.map(t => t.balance),
        lineStyle: { color: '#409eff' }, itemStyle: { color: '#409eff' }, areaStyle: { color: 'rgba(64,158,255,0.1)' }
      }
    ]
  })
}

const loadTrend = async () => {
  const r = await getStatistics(`group_by=${groupBy.value}`)
  if (r && r.code === 200) {
    s.value = r.data
    await nextTick()
    renderTrend()
  }
}

onMounted(async () => {
  trendChart = echarts.init(trendRef.value)
  await loadTrend()
  const t = await getTransactions('page=1&page_size=10')
  if (t && t.code === 200) recent.value = t.data.transactions.slice(0, 10)
  window.addEventListener('resize', trendChart.resize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', trendChart?.resize)
  trendChart?.dispose()
})
</script>