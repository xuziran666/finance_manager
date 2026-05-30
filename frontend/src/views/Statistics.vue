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
    <el-row :gutter="16">
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
  </div>
</template>

<script setup>
/**
 * 统计分析页面
 * 按账户/日期筛选，查看总收入/支出/结余统计
 */
import { ref, reactive, onMounted } from 'vue'
import { fmt } from '../api'
import { getStatistics } from '../api/statistics'
import { useStore } from '../composables/useStore'

const { accs } = useStore()

const sd = ref({})     // 统计数据
const sf = reactive({ acc: '', sd: '', ed: '' })  // 筛选条件

/** 加载统计数据 */
const loadStats = async () => {
  const p2 = new URLSearchParams()
  if (sf.acc) p2.set('account_id', sf.acc)
  if (sf.sd) p2.set('start_date', sf.sd)
  if (sf.ed) p2.set('end_date', sf.ed)
  const r = await getStatistics(p2.toString())
  if (r && r.code === 200) sd.value = r.data
}

onMounted(() => {
  loadStats()
})
</script>