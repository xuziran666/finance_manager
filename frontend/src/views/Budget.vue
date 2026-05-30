<template>
  <div>
    <div class="page-header-row">
      <h4 class="page-title">预算管理</h4>
      <el-button type="primary" @click="openBudget()">
        <el-icon><Plus /></el-icon> 设置
      </el-button>
    </div>
    <el-card shadow="never" class="mb-3">
      <el-row :gutter="8">
        <el-col :span="6">
          <el-select v-model="by" style="width: 100%">
            <el-option v-for="y in years" :key="y" :label="y + '年'" :value="y" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="bm" style="width: 100%">
            <el-option v-for="m in 12" :key="m" :label="m + '月'" :value="m" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="loadBudget">查看</el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-card shadow="never">
      <el-alert
        v-if="bw.length"
        :title="bw.join('；')"
        type="warning"
        :closable="false"
        class="mb-3"
      />
      <el-table :data="bsum" stripe style="width: 100%" empty-text="暂无">
        <el-table-column prop="category" label="分类" />
        <el-table-column label="预算" width="120">
          <template #default="{ row }">{{ fmt(row.budget) }}</template>
        </el-table-column>
        <el-table-column label="已用" width="120">
          <template #default="{ row }">{{ fmt(row.spent) }}</template>
        </el-table-column>
        <el-table-column label="剩余" width="120">
          <template #default="{ row }">
            <span :class="row.remaining < 0 ? 'text-danger' : 'text-success'">{{ fmt(row.remaining) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="使用率" width="180">
          <template #default="{ row }">
            <div class="d-flex align-items-center gap-2">
              <el-progress
                :percentage="Math.min(row.percentage, 100)"
                :color="row.percentage > 100 ? '#ef4444' : row.percentage > 80 ? '#e6a23c' : '#10b981'"
                :stroke-width="8"
                style="width: 100px"
              />
              <span>{{ row.percentage }}%</span>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="设置预算" width="400px">
      <el-form label-position="top">
        <el-row :gutter="8">
          <el-col :span="12">
            <el-form-item label="年份">
              <el-select v-model="bf.y" style="width: 100%">
                <el-option v-for="y in years" :key="y" :label="y + '年'" :value="y" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="月份">
              <el-select v-model="bf.m" style="width: 100%">
                <el-option v-for="m in 12" :key="m" :label="m + '月'" :value="m" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="分类">
          <el-input v-model="bf.cat" placeholder="分类名称" />
        </el-form-item>
        <el-form-item label="金额">
          <el-input-number v-model="bf.amt" :precision="2" :min="0.01" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveBudget">设置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
/**
 * 预算管理页面
 * 按年月查看预算汇总（含进度条和超支预警），支持添加新预算
 */
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { fmt } from '../api'
import { getBudgetSummary, createBudget } from '../api/budget'
import { useStore } from '../composables/useStore'

const { years } = useStore()

const by = ref(new Date().getFullYear())  // 选中年份
const bm = ref(new Date().getMonth() + 1) // 选中月份
const bsum = ref([])   // 预算汇总数据
const bw = ref([])      // 预警列表
const dialogVisible = ref(false)
const bf = reactive({ y: new Date().getFullYear(), m: new Date().getMonth() + 1, cat: '', amt: '' })

/** 加载指定年月的预算汇总 */
const loadBudget = async () => {
  const r = await getBudgetSummary(by.value, bm.value)
  if (r && r.code === 200) {
    bsum.value = r.data.summary
    bw.value = r.data.warnings
  }
}

/** 打开设置预算对话框 */
const openBudget = () => {
  bf.y = new Date().getFullYear()
  bf.m = new Date().getMonth() + 1
  bf.cat = ''
  bf.amt = ''
  dialogVisible.value = true
}

/** 保存预算设置 */
const saveBudget = async () => {
  if (!bf.cat || !bf.amt) {
    ElMessage.warning('请填写完整')
    return
  }
  const r = await createBudget({ year: bf.y, month: bf.m, category: bf.cat, amount: bf.amt })
  if (r && r.code === 200) {
    ElMessage.success('成功')
    await loadBudget()
    dialogVisible.value = false
  }
}

onMounted(() => {
  loadBudget()
})
</script>