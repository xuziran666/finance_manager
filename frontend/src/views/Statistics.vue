<template>
  <div>
    <h4 class="page-title">统计分析</h4>
    <el-card shadow="never" class="mb-3">
      <el-row :gutter="8">
        <el-col :span="6">
          <el-select v-model="sf.acc" placeholder="全部账户" clearable style="width: 100%">
            <el-option label="全部" value="" />
            <el-option v-for="a in accs" :key="a.id" :label="a.name" :value="a.id" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker v-model="sf.sd" type="date" placeholder="开始日期" style="width: 100%" value-format="YYYY-MM-DD" />
        </el-col>
        <el-col :span="6">
          <el-date-picker v-model="sf.ed" type="date" placeholder="结束日期" style="width: 100%" value-format="YYYY-MM-DD" />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="loadStats">分析</el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-row :gutter="16" class="mb-4">
      <el-col :span="8">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">总收入</div>
          <div class="stat-value text-success">{{ fmt(sd.total_income) }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">总支出</div>
          <div class="stat-value text-danger">{{ fmt(sd.total_expense) }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never" class="stat-card">
          <div class="stat-label">结余</div>
          <div class="stat-value" :class="sd.balance >= 0 ? 'text-primary' : 'text-danger'">{{ fmt(sd.balance) }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" class="mb-3" v-if="sd.trend && sd.trend.length">
      <template #header><span class="fw-bold">收支趋势</span></template>
      <div ref="trendRef" style="width:100%;height:280px"></div>
    </el-card>

    <el-row :gutter="16">
      <el-col :span="12">
        <el-card shadow="never" v-if="sd.expense_by_category && sd.expense_by_category.length">
          <template #header><span class="fw-bold text-danger">支出分类</span></template>
          <div ref="expensePieRef" style="width:100%;height:300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never" v-if="sd.income_by_category && sd.income_by_category.length">
          <template #header><span class="fw-bold text-success">收入分类</span></template>
          <div ref="incomePieRef" style="width:100%;height:300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { fmt } from '../api'
import { getStatistics } from '../api/statistics'
import { useStore } from '../composables/useStore'

const { accs } = useStore()

const sd = ref({})
const sf = reactive({ acc: '', sd: '', ed: '' })
const trendRef = ref(null)
const expensePieRef = ref(null)
const incomePieRef = ref(null)

const PIE_COLORS = ['#409eff','#67c23a','#f56c6c','#e6a23c','#909399','#b37feb','#36cfc9','#ff85c0','#ffd666','#5cdbd3','#69b1ff','#bae637','#d3adf7','#ff9c6e','#a0d911']

const getOrInit = (refVal, disposer) => {
  if (!refVal) return null
  return echarts.init(refVal)
}

const renderCharts = () => {
  const tc = trendRef.value && echarts.getInstanceByDom(trendRef.value) || echarts.init(trendRef.value)
  const ep = expensePieRef.value && echarts.getInstanceByDom(expensePieRef.value) || echarts.init(expensePieRef.value)
  const ip = incomePieRef.value && echarts.getInstanceByDom(incomePieRef.value) || echarts.init(incomePieRef.value)

  if (sd.value.trend?.length) {
    const periods = sd.value.trend.map(t => t.period)
    tc.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['收入', '支出', '结余'] },
      grid: { left: 60, right: 20, bottom: 30, top: 10 },
      xAxis: { type: 'category', data: periods, boundaryGap: false },
      yAxis: { type: 'value', axisLabel: { formatter: v => '¥' + v.toLocaleString() } },
      series: [
        { name: '收入', type: 'line', smooth: true, data: sd.value.trend.map(t => t.income), lineStyle: { color: '#67c23a' }, itemStyle: { color: '#67c23a' }, areaStyle: { color: 'rgba(103,194,58,0.1)' } },
        { name: '支出', type: 'line', smooth: true, data: sd.value.trend.map(t => t.expense), lineStyle: { color: '#f56c6c' }, itemStyle: { color: '#f56c6c' }, areaStyle: { color: 'rgba(245,108,108,0.1)' } },
        { name: '结余', type: 'line', smooth: true, data: sd.value.trend.map(t => t.balance), lineStyle: { color: '#409eff' }, itemStyle: { color: '#409eff' }, areaStyle: { color: 'rgba(64,158,255,0.1)' } }
      ]
    })
  }
  if (sd.value.expense_by_category?.length) {
    ep.setOption({
      tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
      legend: { orient: 'vertical', right: 10, top: 'center' },
      series: [{
        type: 'pie', radius: ['40%', '65%'], center: ['35%', '50%'], avoidLabelOverlap: true,
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
        data: sd.value.expense_by_category.map((c, i) => ({ value: c.amount, name: c.name, itemStyle: { color: PIE_COLORS[i % PIE_COLORS.length] } }))
      }]
    })
  }
  if (sd.value.income_by_category?.length) {
    ip.setOption({
      tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
      legend: { orient: 'vertical', right: 10, top: 'center' },
      series: [{
        type: 'pie', radius: ['40%', '65%'], center: ['35%', '50%'], avoidLabelOverlap: true,
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
        data: sd.value.income_by_category.map((c, i) => ({ value: c.amount, name: c.name, itemStyle: { color: PIE_COLORS[i % PIE_COLORS.length] } }))
      }]
    })
  }
}

const resize = () => {
  ;[trendRef, expensePieRef, incomePieRef].forEach(r => {
    const dom = r.value
    if (dom) {
      const inst = echarts.getInstanceByDom(dom)
      inst && inst.resize()
    }
  })
}

const loadStats = async () => {
  const p2 = new URLSearchParams()
  if (sf.acc) p2.set('account_id', sf.acc)
  if (sf.sd) p2.set('start_date', sf.sd)
  if (sf.ed) p2.set('end_date', sf.ed)
  const r = await getStatistics(p2.toString())
  if (r && r.code === 200) {
    sd.value = r.data
    await nextTick()
    renderCharts()
  }
}

onMounted(() => {
  loadStats()
  window.addEventListener('resize', resize)
})

onBeforeUnmount(() => {
  ;[trendRef, expensePieRef, incomePieRef].forEach(r => {
    const dom = r.value
    if (dom) {
      const inst = echarts.getInstanceByDom(dom)
      inst && inst.dispose()
    }
  })
  window.removeEventListener('resize', resize)
})
</script>