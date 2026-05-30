<template>
  <div>
    <div class="page-header-row">
      <h4 class="page-title">账户管理</h4>
      <el-button type="primary" @click="openAcct()">
        <el-icon><Plus /></el-icon> 添加
      </el-button>
    </div>
    <el-row :gutter="16">
      <el-col :xs="24" :sm="12" :md="8" v-for="a in accs" :key="a.id" class="mb-3">
        <el-card shadow="never">
          <div class="acc-card-header">
            <div>
              <h6 class="fw-bold mb-1">{{ a.name }}</h6>
              <small class="text-muted">{{ a.type }}</small>
            </div>
            <el-dropdown trigger="click" @command="(cmd) => handleCmd(cmd, a)">
              <el-button size="small" circle>
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit"><el-icon><Edit /></el-icon> 编辑</el-dropdown-item>
                  <el-dropdown-item command="delete" divided><el-icon><Delete /></el-icon> 删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <el-divider />
          <div class="acc-balance">
            <small>余额</small>
            <div class="fw-bold fs-4" :class="parseFloat(a.balance) >= 0 ? 'text-success' : 'text-danger'">
              {{ fmt(a.balance) }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Dialog -->
    <el-dialog v-model="dialogVisible" :title="af.id ? '编辑账户' : '添加账户'" width="400px">
      <el-form label-position="top">
        <el-form-item label="名称">
          <el-input v-model="af.name" placeholder="账户名称" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="af.type" placeholder="选择类型" style="width: 100%">
            <el-option label="现金" value="现金" />
            <el-option label="银行卡" value="银行卡" />
            <el-option label="微信" value="微信" />
            <el-option label="支付宝" value="支付宝" />
          </el-select>
        </el-form-item>
        <el-form-item label="初始余额" v-if="!af.id">
          <el-input-number v-model="af.balance" :precision="2" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveAcct">{{ af.id ? '保存' : '添加' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
/**
 * 账户管理页面
 * 卡片式展示所有账户，支持添加/编辑/删除操作
 */
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fmt } from '../api'
import { createAccount, updateAccount, deleteAccount } from '../api/account'
import { useStore } from '../composables/useStore'

const { accs, loadAccs } = useStore()

const dialogVisible = ref(false)
const af = reactive({ id: null, name: '', type: '', balance: 0 })

/** 打开添加/编辑对话框 */
const openAcct = (a) => {
  if (a) {
    af.id = a.id
    af.name = a.name
    af.type = a.type
    af.balance = a.balance
  } else {
    af.id = null
    af.name = ''
    af.type = ''
    af.balance = 0
  }
  dialogVisible.value = true
}

/** 保存账户（新增或更新） */
const saveAcct = async () => {
  if (!af.name || !af.type) {
    ElMessage.warning('请填写完整')
    return
  }
  const data = { name: af.name, type: af.type, balance: af.balance }
  const r = af.id ? await updateAccount(af.id, data) : await createAccount(data)
  if (r && r.code === 200) {
    ElMessage.success('成功')
    await loadAccs()
    dialogVisible.value = false
  }
}

/** 删除账户（确认后执行） */
const delAcct = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' })
    const r = await deleteAccount(id)
    if (r && r.code === 200) {
      ElMessage.success('删除成功')
      await loadAccs()
    }
  } catch (e) { /* 用户取消操作，不做任何处理 */ }
}

/** 处理卡片菜单命令 */
const handleCmd = (cmd, a) => {
  if (cmd === 'edit') openAcct(a)
  else if (cmd === 'delete') delAcct(a.id)
}

onMounted(() => {
  loadAccs()
})
</script>