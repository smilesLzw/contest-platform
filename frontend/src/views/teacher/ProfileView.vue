<template>
  <div class="profile-page">
    <h1 class="page-title">个人中心</h1>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header><span>基本信息</span></template>
          <el-form :model="profileForm" label-width="80px">
            <el-form-item label="头像">
              <el-upload
                :show-file-list="false"
                :http-request="handleAvatarUpload"
                accept="image/jpeg,image/png"
              >
                <el-avatar :size="80" :src="profileForm.avatar_url || ''">
                  {{ profileForm.name?.charAt(0) }}
                </el-avatar>
              </el-upload>
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="profileForm.name" />
            </el-form-item>
            <el-form-item label="工号">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="院系">
              <el-input v-model="profileForm.department" />
            </el-form-item>
            <el-form-item label="角色">
              <el-tag>{{ profileForm.role === 'admin' ? '管理员' : '教师' }}</el-tag>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveProfile">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card shadow="never">
          <template #header><span>修改密码</span></template>
          <el-form :model="pwdForm" ref="pwdFormRef" :rules="pwdRules" label-width="100px">
            <el-form-item label="原密码" prop="old_password">
              <el-input v-model="pwdForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="pwdForm.new_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input v-model="pwdForm.confirm_password" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="pwdSaving" @click="changePwd">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { updateProfile, changePassword } from '../../api/auth'
import { uploadImage } from '../../api/common'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()

const profileForm = reactive({
  username: '',
  name: '',
  department: '',
  role: '',
  avatar_url: '',
})
const saving = ref(false)

const pwdForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})
const pwdSaving = ref(false)
const pwdFormRef = ref(null)
const pwdRules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码至少8位', trigger: 'blur' },
  ],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== pwdForm.new_password) callback(new Error('两次密码不一致'))
        else callback()
      },
      trigger: 'blur',
    },
  ],
}

function loadUserInfo() {
  const u = authStore.userInfo
  if (u) {
    profileForm.username = u.username || ''
    profileForm.name = u.name || ''
    profileForm.department = u.department || ''
    profileForm.role = u.role || ''
    profileForm.avatar_url = u.avatar_url || ''
  }
}

async function handleAvatarUpload({ file }) {
  try {
    const res = await uploadImage(file)
    profileForm.avatar_url = res.data.url
    ElMessage.success('头像上传成功')
  } catch (e) {
    console.error(e)
  }
}

async function saveProfile() {
  saving.value = true
  try {
    const res = await updateProfile({
      name: profileForm.name,
      department: profileForm.department,
      avatar_url: profileForm.avatar_url,
    })
    authStore.setUserInfo(res.data)
    ElMessage.success('保存成功')
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}

async function changePwd() {
  const valid = await pwdFormRef.value.validate().catch(() => false)
  if (!valid) return
  pwdSaving.value = true
  try {
    await changePassword({
      old_password: pwdForm.old_password,
      new_password: pwdForm.new_password,
    })
    ElMessage.success('密码修改成功')
    pwdForm.old_password = ''
    pwdForm.new_password = ''
    pwdForm.confirm_password = ''
  } catch (e) {
    console.error(e)
  } finally {
    pwdSaving.value = false
  }
}

onMounted(loadUserInfo)
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 20px; }
</style>
