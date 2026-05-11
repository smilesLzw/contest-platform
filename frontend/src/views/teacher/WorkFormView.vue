<template>
  <div class="work-form">
    <h1 class="page-title">{{ isEdit ? '编辑作品' : '发布作品' }}</h1>

    <el-card shadow="never">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" v-loading="loading">
        <el-form-item label="作品名称" prop="title">
          <el-input v-model="form.title" maxlength="100" show-word-limit />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="参赛学生" prop="author_names">
              <el-input v-model="form.author_names" placeholder="多个学生用逗号分隔" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="指导教师" prop="guide_teacher">
              <el-input v-model="form.guide_teacher" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="专业" prop="major_id">
              <el-select v-model="form.major_id" placeholder="请选择专业" style="width: 100%">
                <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="学年" prop="academic_year">
              <el-select v-model="form.academic_year" placeholder="请选择" style="width: 100%">
                <el-option v-for="y in academicYears" :key="y" :label="y" :value="y" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="学期" prop="semester">
              <el-radio-group v-model="form.semester">
                <el-radio :value="1">上学期</el-radio>
                <el-radio :value="2">下学期</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="赛事名称" prop="contest_name">
              <el-input v-model="form.contest_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="获奖情况" prop="award">
              <el-select v-model="form.award" placeholder="请选择" style="width: 100%" clearable>
                <el-option label="一等奖" value="一等奖" />
                <el-option label="二等奖" value="二等奖" />
                <el-option label="三等奖" value="三等奖" />
                <el-option label="优秀奖" value="优秀奖" />
                <el-option label="参与奖" value="参与奖" />
                <el-option label="无" value="无" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="封面图" prop="cover_url">
          <el-upload
            :show-file-list="false"
            :http-request="handleCoverUpload"
            accept="image/jpeg,image/png,image/webp"
          >
            <el-image v-if="form.cover_url" :src="form.cover_url" style="width: 200px; height: 120px" fit="cover" />
            <el-button v-else>上传封面</el-button>
          </el-upload>
        </el-form-item>

        <el-form-item label="作品简介" prop="content">
          <div style="width: 100%;">
            <MdEditor v-model="form.content" language="zh-CN" :theme="editorTheme" />
          </div>
        </el-form-item>

        <el-form-item label="演示链接" prop="demo_url">
          <el-input v-model="form.demo_url" placeholder="https://" />
        </el-form-item>

        <el-form-item label="附件" prop="attachment_url">
          <el-upload
            :show-file-list="false"
            :http-request="handleFileUpload"
            accept=".pdf,.zip"
          >
            <el-button>上传附件</el-button>
          </el-upload>
          <span v-if="form.attachment_url" class="file-name">已上传：{{ form.attachment_url.split('/').pop() }}</span>
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
import { getMajors, uploadImage, uploadFile } from '../../api/common'
import { getWork, createWork, updateWork } from '../../api/works'
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
const majors = ref([])

const form = reactive({
  title: '',
  author_names: '',
  guide_teacher: '',
  major_id: null,
  academic_year: '',
  semester: 1,
  contest_name: '',
  award: '',
  cover_url: '',
  content: '',
  demo_url: '',
  attachment_url: '',
})

const rules = {
  title: [{ required: true, message: '请输入作品名称', trigger: 'blur' }],
  author_names: [{ required: true, message: '请输入参赛学生姓名', trigger: 'blur' }],
  major_id: [{ required: true, message: '请选择专业', trigger: 'change' }],
  academic_year: [{ required: true, message: '请选择学年', trigger: 'change' }],
  content: [{ required: true, message: '请输入作品简介', trigger: 'blur' }],
}

const academicYears = []
const year = new Date().getFullYear()
for (let i = 0; i < 5; i++) {
  const start = year - i - 1
  academicYears.push(`${start}-${start + 1}`)
}

async function handleCoverUpload({ file }) {
  try {
    const res = await uploadImage(file)
    form.cover_url = res.data.url
    ElMessage.success('封面上传成功')
  } catch (e) { console.error(e) }
}

async function handleFileUpload({ file }) {
  try {
    const res = await uploadFile(file)
    form.attachment_url = res.data.url
    ElMessage.success('附件上传成功')
  } catch (e) { console.error(e) }
}

async function submitForm(status) {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = { ...form, status }
    if (isEdit) {
      await updateWork(route.params.id, data)
      ElMessage.success('更新成功')
    } else {
      await createWork(data)
      ElMessage.success('提交成功')
    }
    router.push(authStore.isAdmin ? '/admin/works' : '/my/works')
  } catch (e) { console.error(e) }
  finally { submitting.value = false }
}

onMounted(async () => {
  updateEditorTheme()
  themeObserver = new MutationObserver(updateEditorTheme)
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })

  try {
    const majorsRes = await getMajors()
    majors.value = majorsRes.data || []
    if (isEdit) {
      loading.value = true
      const res = await getWork(route.params.id)
      const w = res.data
      Object.assign(form, {
        title: w.title,
        author_names: w.author_names,
        guide_teacher: w.guide_teacher || '',
        major_id: w.major_id,
        academic_year: w.academic_year,
        semester: w.semester,
        contest_name: w.contest_name || '',
        award: w.award || '',
        cover_url: w.cover_url || '',
        content: w.content || '',
        demo_url: w.demo_url || '',
        attachment_url: w.attachment_url || '',
      })
      loading.value = false
    }
  } catch (e) { console.error(e) }
})

onBeforeUnmount(() => {
  if (themeObserver) { themeObserver.disconnect(); themeObserver = null }
})
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 20px; }
.file-name { margin-left: 10px; font-size: 13px; color: #909399; }
</style>
