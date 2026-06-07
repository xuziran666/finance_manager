<template>
  <div>
    <div class="page-header-row">
      <h4 class="page-title">收支记录</h4>
      <div>
        <el-button @click="showTransfer()">
          <el-icon><RightLeft /></el-icon> 转账
        </el-button>
        <el-button type="primary" @click="openTxn()">
          <el-icon><Plus /></el-icon> 添加
        </el-button>
      </div>
    </div>
    <el-card shadow="never" class="mb-3">
      <el-row :gutter="8">
        <el-col :span="6">
          <el-select v-model="f.acc" placeholder="全部账户" clearable style="width: 100%">
            <el-option label="全部" value="" />
            <el-option v-for="a in accs" :key="a.id" :label="a.name" :value="a.id" />
          </el-select>
        </el-col>
        <el-col :span="5">
          <el-date-picker v-model="f.sd" type="date" placeholder="开始日期" style="width: 100%" value-format="YYYY-MM-DD" />
        </el-col>
        <el-col :span="5">
          <el-date-picker v-model="f.ed" type="date" placeholder="结束日期" style="width: 100%" value-format="YYYY-MM-DD" />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" style="width: 100%" @click="loadTxns(1)">查询</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="success" style="width: 100%" @click="exportData">导出</el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-card shadow="never">
      <el-table :data="txns" stripe style="width: 100%" empty-text="暂无">
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
        <el-table-column label="金额" width="130">
          <template #default="{ row }">
            <span :class="[row.type === 'income' ? 'text-success' : 'text-danger', 'fw-bold']">
              {{ row.type === 'income' ? '+' : '-' }}{{ fmt(row.amount) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="account_name" label="账户" />
        <el-table-column label="操作" width="70" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" size="small" plain @click="delTxn(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="flex-center mt-3" v-if="tp > 1">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="tp * 20"
          :page-size="20"
          :current-page="cp"
          @current-change="loadTxns"
        />
      </div>
    </el-card>

    <!-- Dialog: 添加收支 -->
    <el-dialog v-model="txnDialogVisible" title="添加收支" width="400px">
      <el-form label-position="top">
        <el-form-item>
          <el-radio-group v-model="tf.type">
            <el-radio-button value="expense">支出</el-radio-button>
            <el-radio-button value="income">收入</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="账户">
          <el-select v-model="tf.acc" placeholder="选择账户" style="width: 100%">
            <el-option v-for="a in accs" :key="a.id" :label="`${a.name}（余额：${fmt(a.balance)}）`" :value="a.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="tf.cat" placeholder="选择分类" style="width: 100%" filterable @change="onCatChange">
            <el-option v-for="c in mainCats" :key="c" :label="c" :value="c" />
            <el-option label="✚ 新建分类" value="__new__" />
          </el-select>
        </el-form-item>
        <el-form-item label="子分类" v-if="tf.cat">
          <el-select v-model="tf.subcat" placeholder="选择子分类（可选）" style="width: 100%" clearable @change="onSubcatChange">
            <el-option v-for="s in subCats" :key="s" :label="s" :value="s" />
            <el-option label="✚ 新建子分类" value="__new_sub__" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额">
          <el-input-number v-model="tf.amt" :precision="2" :min="0.01" style="width: 100%" />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="tf.date" type="datetime" style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="txnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTxn">添加</el-button>
      </template>
    </el-dialog>

    <!-- Dialog: 转账 -->
    <el-dialog v-model="transferDialogVisible" title="转账" width="400px">
      <el-form label-position="top">
        <el-form-item label="转出">
          <el-select v-model="trf.from" placeholder="选择转出账户" style="width: 100%">
            <el-option v-for="a in accs" :key="a.id" :label="`${a.name}(${fmt(a.balance)})`" :value="a.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="转入">
          <el-select v-model="trf.to" placeholder="选择转入账户" style="width: 100%">
            <el-option v-for="a in accs" :key="a.id" :label="a.name" :value="a.id" :disabled="a.id === trf.from" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额">
          <el-input-number v-model="trf.amt" :precision="2" :min="0.01" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="transferDialogVisible = false">取消</el-button>
        <el-button type="warning" @click="doTransfer">转账</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
/**
 * 收支记录页面
 * 支持按账户/日期筛选、添加收支、转账、CSV 导出、分页展示
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fmt } from '../api'
import { createCategory } from '../api/category'
import { getTransactions, createTransaction, transfer, deleteTransaction } from '../api/transaction'
import { useStore } from '../composables/useStore'

const { accs, catTree, loadAccs, loadCats } = useStore()
const txns = ref([])   // 交易记录列表
const cp = ref(1)      // 当前页码
const tp = ref(1)      // 总页数
const f = reactive({ acc: '', sd: '', ed: '' })  // 筛选条件

// 新增交易表单
const defNow = () => new Date().toISOString().slice(0, 19).replace('T', ' ')
const tf = reactive({ acc: '', type: 'expense', cat: '', subcat: '', amt: '', date: defNow() })

// 根据选择的类型动态获取主分类和子分类
const mainCats = computed(() => Object.keys(catTree.value[tf.type] || {}))
const subCats = computed(() => (catTree.value[tf.type]?.[tf.cat]) || [])

/** 分类选择变更处理：检测"新建分类"时弹出输入框 */
const onCatChange = async (val) => {
  if (val !== '__new__') {
    tf.subcat = ''
    return
  }
  // 恢复原值，等创建成功后再更新
  tf.cat = ''
  try {
    const { value } = await ElMessageBox.prompt('请输入新分类名称', '新建分类', {
      confirmButtonText: '确定', cancelButtonText: '取消', inputPattern: /\S+/, inputErrorMessage: '名称不能为空'
    })
    const r = await createCategory({ type: tf.type, main: value })
    if (r && r.code === 200) {
      await loadCats()
      tf.cat = value
    }
  } catch { /* cancelled */ }
}

/** 子分类选择变更处理 */
const onSubcatChange = async (val) => {
  if (val !== '__new_sub__') return
  tf.subcat = ''
  try {
    const { value } = await ElMessageBox.prompt('请输入子分类名称', '新建子分类', {
      confirmButtonText: '确定', cancelButtonText: '取消', inputPattern: /\S+/, inputErrorMessage: '名称不能为空'
    })
    const r = await createCategory({ type: tf.type, main: tf.cat, sub: value })
    if (r && r.code === 200) {
      await loadCats()
      tf.subcat = value
    }
  } catch { /* cancelled */ }
}

// 转账表单
const trf = reactive({ from: '', to: '', amt: '' })
const txnDialogVisible = ref(false)
const transferDialogVisible = ref(false)

/** 加载交易列表（支持分页） */
const loadTxns = async (p) => {
  if (p === undefined) p = cp.value
  else cp.value = p
  const p2 = new URLSearchParams({ page: p, page_size: 20 })
  if (f.acc) p2.set('account_id', f.acc)
  if (f.sd) p2.set('start_date', f.sd)
  if (f.ed) p2.set('end_date', f.ed)
  const r = await getTransactions(p2.toString())
  if (r && r.code === 200) {
    txns.value = r.data.transactions
    tp.value = r.data.total_pages
  }
}

/** 打开添加交易对话框 */
const openTxn = () => {
  tf.acc = accs.value[0]?.id || ''
  tf.type = 'expense'
  tf.cat = ''
  tf.subcat = ''
  tf.amt = ''
  tf.date = defNow()
  txnDialogVisible.value = true
}

/** 保存新交易记录 */
const saveTxn = async () => {
  if (!tf.acc || !tf.cat || !tf.amt) {
    ElMessage.warning('请填写完整')
    return
  }
  const acc = accs.value.find(a => a.id === tf.acc)
  if (tf.type === 'expense' && acc && acc.balance < tf.amt) {
    ElMessage.warning(`余额不足：${acc.name} 仅剩 ${fmt(acc.balance)}`)
    return
  }
  const r = await createTransaction({ account_id: tf.acc, type: tf.type, category: tf.cat, subcategory: tf.subcat, amount: tf.amt, date: tf.date })
  if (r && r.code === 200) {
    ElMessage.success('成功')
    await loadTxns()
    await loadAccs()
    txnDialogVisible.value = false
  }
}

/** 打开转账对话框 */
const showTransfer = () => {
  transferDialogVisible.value = true
}

/** 执行转账操作 */
const doTransfer = async () => {
  if (!trf.from || !trf.to || !trf.amt) {
    ElMessage.warning('请填写完整')
    return
  }
  if (trf.from === trf.to) {
    ElMessage.warning('不能转给自己')
    return
  }
  const fromAcc = accs.value.find(a => a.id === trf.from)
  if (fromAcc && fromAcc.balance < trf.amt) {
    ElMessage.warning(`余额不足：${fromAcc.name} 仅剩 ${fmt(fromAcc.balance)}`)
    return
  }
  const r = await transfer({ from_account: trf.from, to_account: trf.to, amount: trf.amt })
  if (r && r.code === 200) {
    ElMessage.success('转账成功')
    await loadAccs()
    await loadTxns()
    transferDialogVisible.value = false
  }
}

/** 删除交易记录 */
const delTxn = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除这笔 ${row.type === 'income' ? '收入' : '支出'} ${fmt(row.amount)} 的记录？`, '确认删除', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning',
    })
  } catch { return }
  const r = await deleteTransaction(row.id)
  if (r && r.code === 200) {
    ElMessage.success('已删除')
    await loadTxns()
    await loadAccs()
  }
}

/** 导出筛选后的交易记录为 CSV */
const exportData = () => {
  const p = new URLSearchParams()
  if (f.acc) p.set('account_id', f.acc)
  if (f.sd) p.set('start_date', f.sd)
  if (f.ed) p.set('end_date', f.ed)
  window.open('/api/transactions/export?' + p, '_blank')
}

onMounted(() => {
  loadTxns()
  loadCats()
})
</script>