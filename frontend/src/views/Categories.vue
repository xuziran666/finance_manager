<template>
  <div>
    <div class="page-header-row">
      <h4 class="page-title">分类管理</h4>
      <el-button type="primary" @click="openCat()">
        <el-icon><Plus /></el-icon> 添加
      </el-button>
    </div>
    <el-row :gutter="16">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span class="text-success fw-bold">收入</span>
          </template>
          <div v-if="catTree.income && Object.keys(catTree.income).length === 0" class="text-center text-muted py-3">暂无</div>
          <template v-for="(subs, main) in (catTree.income || {})" :key="main">
            <div class="cat-item cat-item-clickable" @click="toggleExpand('income', main)">
              <span>
                <el-icon class="me-1"><ArrowRight v-if="!isExpanded('income', main)" /><ArrowDown v-else /></el-icon>
                <span class="fw-bold">{{ main }}</span>
              </span>
              <span>
                <el-button size="small" circle @click.stop="openCat('income', main)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" circle type="danger" @click.stop="handleDelete('income', main, '')">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </span>
            </div>
            <div v-for="s in subs" :key="s" v-show="isExpanded('income', main)" class="cat-item ps-4">
              <span>{{ s }}</span>
              <span>
                <el-button size="small" circle @click.stop="openCat('income', main, s)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" circle type="danger" @click.stop="handleDelete('income', main, s)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </span>
            </div>
          </template>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span class="text-danger fw-bold">支出</span>
          </template>
          <div v-if="catTree.expense && Object.keys(catTree.expense).length === 0" class="text-center text-muted py-3">暂无</div>
          <template v-for="(subs, main) in (catTree.expense || {})" :key="main">
            <div class="cat-item cat-item-clickable" @click="toggleExpand('expense', main)">
              <span>
                <el-icon class="me-1"><ArrowRight v-if="!isExpanded('expense', main)" /><ArrowDown v-else /></el-icon>
                <span class="fw-bold">{{ main }}</span>
              </span>
              <span>
                <el-button size="small" circle @click.stop="openCat('expense', main)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" circle type="danger" @click.stop="handleDelete('expense', main, '')">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </span>
            </div>
            <div v-for="s in subs" :key="s" v-show="isExpanded('expense', main)" class="cat-item ps-4">
              <span>{{ s }}</span>
              <span>
                <el-button size="small" circle @click.stop="openCat('expense', main, s)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" circle type="danger" @click.stop="handleDelete('expense', main, s)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </span>
            </div>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" :title="cf.editing ? '修改分类' : '添加分类'" width="400px">
      <el-form label-position="top">
        <el-form-item label="类型">
          <el-select v-model="cf.type" style="width: 100%" :disabled="!!cf.oldSub">
            <el-option label="收入" value="income" />
            <el-option label="支出" value="expense" />
          </el-select>
        </el-form-item>
        <el-form-item label="一级分类">
          <el-input v-model="cf.main" placeholder="一级分类" :disabled="!!cf.oldSub" />
        </el-form-item>
        <el-form-item label="二级分类">
          <el-input v-model="cf.sub" placeholder="二级分类（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCat">{{ cf.editing ? '保存' : '添加' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
/**
 * 分类管理页面
 * 左右分栏展示收入/支出分类树，支持添加和修改一级分类
 */
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowRight, ArrowDown } from '@element-plus/icons-vue'
import { createCategory, updateCategory, deleteCategory } from '../api/category'
import { useStore } from '../composables/useStore'

const { catTree, loadCats } = useStore()

const dialogVisible = ref(false)
const cf = reactive({ editing: false, type: 'expense', main: '', sub: '', oldType: '', oldMain: '', oldSub: '' })

/** 已展开的一级分类 key 集合 */
const expandedKeys = ref(new Set())

const expandKey = (type, main) => `${type}:${main}`
const isExpanded = (type, main) => expandedKeys.value.has(expandKey(type, main))
const toggleExpand = (type, main) => {
  const k = expandKey(type, main)
  if (expandedKeys.value.has(k)) {
    expandedKeys.value.delete(k)
  } else {
    expandedKeys.value.add(k)
  }
  // trigger reactivity
  expandedKeys.value = new Set(expandedKeys.value)
}

/** 打开添加/编辑分类对话框 */
const openCat = (tp, main, sub) => {
  if (main) {
    // 编辑模式：预填原分类信息
    cf.editing = true
    cf.type = tp
    cf.main = main
    cf.sub = sub || ''
    cf.oldType = tp
    cf.oldMain = main
    cf.oldSub = sub || ''
  } else {
    // 添加模式：清空表单
    cf.editing = false
    cf.type = tp || 'expense'
    cf.main = ''
    cf.sub = ''
    cf.oldType = ''
    cf.oldMain = ''
    cf.oldSub = ''
  }
  dialogVisible.value = true
}

/** 保存分类（新增主分类/添加子分类/修改分类） */
const saveCat = async () => {
  if (!cf.main) {
    ElMessage.warning('请填写')
    return
  }
  let r
  if (cf.editing && cf.oldSub) {
    // 编辑子分类名称
    r = await updateCategory({
      old_type: cf.oldType, old_main: cf.oldMain, old_sub: cf.oldSub,
      new_type: cf.type, new_main: cf.main, new_sub: cf.sub
    })
  } else if (cf.editing && cf.sub) {
    // 从主分类按钮进入 + 填了子分类 → 添加子分类
    r = await createCategory({ type: cf.type, main: cf.main, sub: cf.sub })
  } else if (cf.editing) {
    // 从主分类按钮进入 + 未填子分类 → 修改主分类
    r = await updateCategory({
      old_type: cf.oldType, old_main: cf.oldMain, old_sub: '',
      new_type: cf.type, new_main: cf.main, new_sub: ''
    })
  } else {
    // 顶部添加按钮 → 新增主分类
    r = await createCategory({ type: cf.type, main: cf.main, sub: cf.sub })
  }
  if (r && r.code === 200) {
    ElMessage.success(r.msg)
    await loadCats()
    dialogVisible.value = false
  }
}

/** 删除分类 */
const handleDelete = async (type, main, sub) => {
  try {
    await ElMessageBox.confirm(`确定删除「${main}${sub ? ' — ' + sub : ''}」吗？`, '确认删除', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
  } catch {
    return
  }
  const r = await deleteCategory({ type, main, sub })
  if (r && r.code === 200) {
    ElMessage.success(r.msg)
    await loadCats()
  }
}

onMounted(() => {
  loadCats()
})
</script>

<style scoped>
.cat-item-clickable {
  cursor: pointer;
  user-select: none;
}
.cat-item-clickable:hover {
  background: #eef1f6;
}
</style>