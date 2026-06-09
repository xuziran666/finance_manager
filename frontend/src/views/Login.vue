<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2><el-icon :size="28"><Wallet /></el-icon> 财务管家</h2>
        <p class="text-muted">个人收支管理系统</p>
      </div>
      <el-form :model="form" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">
            登 录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="auth-footer">
        还没有账号？
        <router-link to="/register">去注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/user'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  loading.value = true
  const r = await login(form.username, form.password)
  loading.value = false
  if (r && r.code === 200) {
    localStorage.setItem('token', r.data.token)
    localStorage.setItem('username', r.data.username)
    ElMessage.success('登录成功')
    await router.push('/')
  } else if (r) {
    ElMessage.error(r.msg || '登录失败')
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e1b4b, #312e81);
}
.auth-card {
  background: #fff;
  border-radius: 16px;
  padding: 40px;
  width: 400px;
  box-shadow: 0 20px 60px rgba(0,0,0,.3);
}
.auth-header {
  text-align: center;
  margin-bottom: 32px;
}
.auth-header h2 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #1e1b4b;
  margin-bottom: 8px;
}
.auth-footer {
  text-align: center;
  font-size: 14px;
  color: #909399;
}
.auth-footer a {
  color: #4f46e5;
  text-decoration: none;
}
</style>
