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
          <div v-for="(subs, main) in (catTree.income || {})" :key="main" class="cat-item">
            <span>{{ main }}</span>
            <el-button size="small" circle @click="openCat('income', main)">
              <el-icon><Edit /></el-icon>
            </el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span class="text-danger fw-bold">支出</span>
          </template>
          <div v-if="catTree.expense && Object.keys(catTree.expense).length === 0" class="text-center text-muted py-3">暂无</div>
          <div v-for="(subs, main) in (catTree.expense || {})" :key="main" class="cat-item">
            <span>{{ main }}</span>
            <el-button size="small" circle @click="openCat('expense', main)">
              <el-icon><Edit /></el-icon>
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" :title="cf.editing ? '修改分类' : '添加分类'" width="400px">
      <el-form label-position="top">
        <el-form-item label="类型">
          <el-select v-model="cf.type" style="width: 100%">
            <el-option label="收入" value="income" />
            <el-option label="支出" value="expense" />
          </el-select>
        </el-form-item>
        <el-form-item label="一级分类">
          <el-input v-model="cf.main" placeholder="一级分类" />
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
import { ElMessage } from 'element-plus'
import { createCategory, updateCategory } from '../api/category'
import { useStore } from '../composables/useStore'

const { catTree, loadCats } = useStore()

const dialogVisible = ref(false)
const cf = reactive({ editing: false, type: 'expense', main: '', sub: '', oldType: '', oldMain: '', oldSub: '' })

/** 打开添加/编辑分类对话框 */
const openCat = (tp, main) => {
  if (main) {
    // 编辑模式：预填原分类信息
    cf.editing = true
    cf.type = tp
    cf.main = main
    cf.sub = ''
    cf.oldType = tp
    cf.oldMain = main
    cf.oldSub = ''
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

/** 保存分类（新增或更新） */
const saveCat = async () => {
  if (!cf.main) {
    ElMessage.warning('请填写')
    return
  }
  let r
  if (cf.editing) {
    r = await updateCategory({
      old_type: cf.oldType, old_main: cf.oldMain, old_sub: cf.oldSub,
      new_type: cf.type, new_main: cf.main, new_sub: cf.sub
    })
  } else {
    r = await createCategory({ type: cf.type, main: cf.main, sub: cf.sub })
  }
  if (r && r.code === 200) {
    ElMessage.success(r.msg)
    await loadCats()
    dialogVisible.value = false
  }
}

onMounted(() => {
  loadCats()
})
</script>