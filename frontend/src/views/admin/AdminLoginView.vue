<template>
  <div class="admin-login-page">
    <div class="login-box">
      <div class="login-header">
        <span class="login-mark">◆</span>
        <h2>管理后台</h2>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="账号" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" native-type="submit" :loading="loading" style="width:100%">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await authStore.login(form)
    if (authStore.userInfo?.role !== 'admin') {
      ElMessage.error('仅限管理员登录')
      authStore.logout()
      return
    }
    ElMessage.success('登录成功')
    router.push('/admin')
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
}
.login-box {
  width: 380px;
  padding: 44px 40px;
  background: var(--bg-card);
  border-radius: 20px;
  box-shadow: 0 4px 24px var(--shadow-sm);
}
.login-header {
  text-align: center;
  margin-bottom: 36px;
}
.login-mark {
  display: block;
  font-size: 28px;
  color: var(--accent);
  margin-bottom: 8px;
}
.login-header h2 {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}
</style>
