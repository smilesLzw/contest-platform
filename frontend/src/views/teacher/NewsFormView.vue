<template>
  <div class="news-form">
    <h1 class="page-title">{{ isEdit ? '编辑新闻' : '发布新闻' }}</h1>

    <el-card shadow="never">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" v-loading="loading">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" maxlength="200" show-word-limit />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类" prop="category">
              <el-select v-model="form.category" style="width: 100%">
                <el-option label="教程指南" value="tutorial" />
                <el-option label="科技前沿" value="tech" />
                <el-option label="教研室动态" value="lab" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="封面图">
              <el-upload
                :show-file-list="false"
                :http-request="handleCoverUpload"
                accept="image/jpeg,image/png"
              >
                <el-button>上传封面</el-button>
              </el-upload>
              <el-image
                v-if="form.cover_url"
                :src="form.cover_url"
                style="width: 120px; height: 70px; margin-left: 10px"
                fit="cover"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="正文" prop="content">
          <div style="width: 100%;">
            <MdEditor v-model="form.content" language="zh-CN" :theme="editorTheme" />
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submitForm('draft')">保存草稿</el-button>
          <el-button type="success" :loading="submitting" @click="submitForm('published')">直接发布</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { uploadImage } from '../../api/common'
import { getNews, createNews, updateNews } from '../../api/news'
import { useAuthStore } from '../../stores/auth'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isEdit = !!route.params.id
const editorTheme = ref('light')

function updateEditorTheme() {
  editorTheme.value = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'
}

let themeObserver = null

const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)

const form = reactive({
  title: '',
  category: 'tutorial',
  cover_url: '',
  content: '',
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入正文内容', trigger: 'blur' }],
}

async function handleCoverUpload({ file }) {
  try {
    const res = await uploadImage(file)
    form.cover_url = res.data.url
    ElMessage.success('封面上传成功')
  } catch (e) { console.error(e) }
}

async function submitForm(status) {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = { ...form, status }
    if (isEdit) {
      await updateNews(route.params.id, data)
      ElMessage.success('更新成功')
    } else {
      await createNews(data)
      ElMessage.success('提交成功')
    }
    router.push(authStore.isAdmin ? '/admin/news' : '/my/news')
  } catch (e) { console.error(e) }
  finally { submitting.value = false }
}

onMounted(async () => {
  updateEditorTheme()
  themeObserver = new MutationObserver(updateEditorTheme)
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })

  if (isEdit) {
    loading.value = true
    try {
      const res = await getNews(route.params.id)
      const n = res.data
      form.title = n.title
      form.category = n.category
      form.cover_url = n.cover_url || ''
      form.content = n.content || ''
    } catch (e) { console.error(e) }
    finally { loading.value = false }
  }
})

onBeforeUnmount(() => {
  if (themeObserver) { themeObserver.disconnect(); themeObserver = null }
})
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 20px; }
</style>
