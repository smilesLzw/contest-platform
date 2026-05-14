<template>
  <div class="work-form">
    <h1 class="page-title">{{ isEdit ? '编辑作品' : '发布作品' }}</h1>

    <el-card shadow="never">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" v-loading="loading">
        <el-form-item label="作品类型" prop="work_type">
          <el-radio-group v-model="form.work_type">
            <el-radio value="graphic">制图作品</el-radio>
            <el-radio value="music">音乐作品</el-radio>
            <el-radio value="video">视频作品</el-radio>
            <el-radio value="website">网站作品</el-radio>
          </el-radio-group>
        </el-form-item>

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
              <el-select v-model="form.guide_teacher" placeholder="请选择教师" style="width: 100%" clearable filterable>
                <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.name" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="专业" prop="major_id">
              <el-select v-model="form.major_id" placeholder="请选择专业" style="width: 100%">
                <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="班级" prop="class_name">
              <el-select v-model="form.class_name" placeholder="请选择班级" style="width: 100%" clearable>
                <el-option v-for="c in classOptions" :key="c" :label="c" :value="c" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="学年" prop="academic_year">
              <el-select v-model="form.academic_year" placeholder="请选择" style="width: 100%">
                <el-option v-for="y in academicYears" :key="y" :label="y" :value="y" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
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
              <el-select v-model="form.contest_name" placeholder="请选择赛事" style="width: 100%" clearable filterable>
                <el-option v-for="c in competitions" :key="c.id" :label="`${c.name}（${c.academic_year} ${c.semester === 1 ? '上' : '下'}）`" :value="c.name" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="获奖情况" prop="award">
              <el-select v-model="form.award" placeholder="请选择" style="width: 100%" clearable>
                <el-option label="暂无" value="暂无" />
                <el-option label="一等奖" value="一等奖" />
                <el-option label="二等奖" value="二等奖" />
                <el-option label="三等奖" value="三等奖" />
                <el-option label="优秀奖" value="优秀奖" />
                <el-option label="参与奖" value="参与奖" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="封面图" prop="cover_url">
          <div class="cover-field">
            <el-upload
              :show-file-list="false"
              :http-request="handleCoverUpload"
              accept="image/jpeg,image/png,image/webp,image/gif,image/svg+xml"
            >
              <el-image v-if="coverPreviewUrl" :src="coverPreviewUrl" class="cover-upload-preview" fit="cover" />
              <el-button v-else>上传封面</el-button>
            </el-upload>
            <div class="cover-actions" v-if="coverPreviewUrl">
              <el-upload
                :show-file-list="false"
                :http-request="handleCoverUpload"
                accept="image/jpeg,image/png,image/webp,image/gif,image/svg+xml"
              >
                <el-button>重新上传并裁剪</el-button>
              </el-upload>
              <span class="cover-tip">列表、详情和缩略图会使用不同尺寸版本。</span>
            </div>
          </div>
        </el-form-item>

        <!-- 制图：多图上传 -->
        <el-form-item v-if="form.work_type === 'graphic'" label="作品图片">
          <div>
            <el-upload
              :show-file-list="false"
              :http-request="handleGalleryUpload"
              accept="image/jpeg,image/png,image/webp,image/gif,image/svg+xml"
            >
              <el-button>上传图片</el-button>
            </el-upload>
            <div class="gallery-previews" v-if="galleryList.length">
              <div v-for="(url, i) in galleryList" :key="i" class="gallery-item">
                <el-image :src="url" style="width: 100px; height: 70px" fit="cover" />
                <span class="gallery-del" @click="removeGallery(i)">&times;</span>
              </div>
            </div>
          </div>
        </el-form-item>

        <!-- 音乐：音频上传 -->
        <el-form-item v-if="form.work_type === 'music'" label="音频文件">
          <el-upload
            :show-file-list="false"
            :http-request="handleAudioUpload"
            accept="audio/mpeg,audio/wav,audio/ogg,audio/aac,audio/flac,audio/mp4,.mp3,.wav,.ogg,.aac,.flac,.m4a"
          >
            <el-button>上传音频</el-button>
          </el-upload>
          <span v-if="form.audio_url" class="file-name">已上传：{{ form.audio_url.split('/').pop() }}</span>
        </el-form-item>

        <!-- 视频：视频上传 -->
        <el-form-item v-if="form.work_type === 'video'" label="视频文件">
          <div class="video-upload-field">
            <div class="upload-inline">
              <el-upload
                :show-file-list="false"
                :http-request="handleVideoUpload"
                accept="video/mp4,video/webm,video/quicktime"
              >
                <el-button :loading="videoUploading" :disabled="videoUploading">
                  {{ videoUploading ? '上传中' : '上传视频' }}
                </el-button>
              </el-upload>
              <span v-if="form.video_url && !videoUploading" class="file-name">已上传：{{ form.video_url.split('/').pop() }}</span>
            </div>
            <div v-if="videoUploading || videoUploadProgress > 0" class="upload-progress-panel">
              <div class="upload-progress-meta">
                <span>{{ videoUploadName || '视频文件' }}</span>
                <span>{{ videoUploading ? uploadProgressText : '上传完成' }}</span>
              </div>
              <el-progress
                :percentage="videoUploadProgress"
                :status="videoUploadStatus"
                :stroke-width="8"
              />
            </div>
          </div>
        </el-form-item>

        <!-- 网站：上传项目压缩包 -->
        <el-form-item v-if="form.work_type === 'website'" label="项目文件" prop="attachment_url">
          <el-upload
            :show-file-list="false"
            :http-request="handleFileUpload"
            accept=".zip"
          >
            <el-button>上传项目压缩包</el-button>
          </el-upload>
          <span v-if="form.attachment_url" class="file-name">已上传：{{ form.attachment_url.split('/').pop() }}</span>
        </el-form-item>

        <el-form-item label="作品简介" prop="content">
          <div style="width: 100%;">
            <MdEditor v-model="form.content" language="zh-CN" :theme="editorTheme" />
          </div>
        </el-form-item>

        <el-form-item v-if="form.work_type !== 'website'" label="演示链接" prop="demo_url">
          <el-input v-model="form.demo_url" placeholder="https://" />
        </el-form-item>

        <el-form-item v-if="form.work_type !== 'website'" label="附件" prop="attachment_url">
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

    <el-dialog
      v-model="coverCrop.visible"
      title="调整封面展示区域"
      width="860px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <div class="crop-dialog">
        <div class="crop-main">
          <div class="crop-preview crop-preview-main">
            <img :src="coverCrop.previewUrl" :style="cropImageStyle" alt="" />
          </div>
          <div class="crop-controls">
            <div class="crop-control">
              <span>横向位置</span>
              <el-slider v-model="coverCrop.focalX" :min="0" :max="100" />
            </div>
            <div class="crop-control">
              <span>纵向位置</span>
              <el-slider v-model="coverCrop.focalY" :min="0" :max="100" />
            </div>
            <div class="crop-control">
              <span>放大裁剪</span>
              <el-slider v-model="coverCrop.zoom" :min="1" :max="2.5" :step="0.05" />
            </div>
          </div>
        </div>
        <div class="crop-side">
          <div>
            <div class="preview-label">列表卡片</div>
            <div class="crop-preview preview-card">
              <img :src="coverCrop.previewUrl" :style="cropImageStyle" alt="" />
            </div>
          </div>
          <div>
            <div class="preview-label">详情大图</div>
            <div class="crop-preview preview-detail">
              <img :src="coverCrop.previewUrl" :style="cropImageStyle" alt="" />
            </div>
          </div>
          <div>
            <div class="preview-label">缩略图</div>
            <div class="crop-preview preview-thumb">
              <img :src="coverCrop.previewUrl" :style="cropImageStyle" alt="" />
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="cancelCoverCrop">取消</el-button>
        <el-button type="primary" :loading="coverUploading" @click="confirmCoverCrop">确认裁剪并上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getMajors, uploadImage, uploadFile, uploadAudio, uploadVideo, getTeachers, getCompetitions } from '../../api/common'
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
const coverUploading = ref(false)
const videoUploading = ref(false)
const videoUploadProgress = ref(0)
const videoUploadName = ref('')
const majors = ref([])
const teachers = ref([])
const competitions = ref([])

const form = reactive({
  title: '',
  author_names: '',
  guide_teacher: '',
  major_id: null,
  class_name: '',
  academic_year: '',
  semester: 1,
  contest_name: '',
  award: '',
  work_type: '',
  cover_url: '',
  cover_original_url: '',
  cover_card_url: '',
  cover_detail_url: '',
  cover_thumb_url: '',
  cover_crop_data: '',
  content: '',
  demo_url: '',
  attachment_url: '',
  audio_url: '',
  video_url: '',
  gallery_urls: '',
})

const galleryList = computed(() => {
  if (!form.gallery_urls) return []
  try { return JSON.parse(form.gallery_urls) } catch { return [] }
})

const coverPreviewUrl = computed(() => form.cover_card_url || form.cover_url)
const videoUploadStatus = computed(() => {
  if (videoUploading.value) return undefined
  return videoUploadProgress.value >= 100 ? 'success' : undefined
})
const uploadProgressText = computed(() => {
  if (videoUploadProgress.value >= 99) return '正在处理'
  return `${videoUploadProgress.value}%`
})

const coverCrop = reactive({
  visible: false,
  file: null,
  previewUrl: '',
  image: null,
  naturalWidth: 0,
  naturalHeight: 0,
  focalX: 50,
  focalY: 50,
  zoom: 1,
})

const cropImageStyle = computed(() => ({
  objectPosition: `${coverCrop.focalX}% ${coverCrop.focalY}%`,
  transform: `scale(${coverCrop.zoom})`,
  transformOrigin: `${coverCrop.focalX}% ${coverCrop.focalY}%`,
}))

const rules = {
  title: [{ required: true, message: '请输入作品名称', trigger: 'blur' }],
  author_names: [{ required: true, message: '请输入参赛学生姓名', trigger: 'blur' }],
  major_id: [{ required: true, message: '请选择专业', trigger: 'change' }],
  academic_year: [{ required: true, message: '请选择学年', trigger: 'change' }],
  content: [{ required: true, message: '请输入作品简介', trigger: 'blur' }],
}

const classOptions = ['一班', '二班', '三班', '四班', '五班', '六班', '七班']

const academicYears = []
const year = new Date().getFullYear()
for (let i = 0; i < 5; i++) {
  const start = year - i - 1
  academicYears.push(`${start}-${start + 1}`)
}

function workUploadMeta(suffix = '') {
  return {
    title: form.title,
    academic_year: form.academic_year,
    semester: form.semester,
    suffix,
  }
}

function ensureWorkUploadMeta() {
  if (!form.title || !form.academic_year || !form.semester) {
    ElMessage.warning('请先填写作品名称、学年和学期，再上传媒体文件')
    return false
  }
  return true
}

async function handleCoverUpload({ file }) {
  if (!ensureWorkUploadMeta()) return
  if (coverCrop.previewUrl) URL.revokeObjectURL(coverCrop.previewUrl)
  const previewUrl = URL.createObjectURL(file)
  coverCrop.file = file
  coverCrop.previewUrl = previewUrl
  coverCrop.focalX = 50
  coverCrop.focalY = 50
  coverCrop.zoom = 1

  try {
    const image = await loadImage(previewUrl)
    coverCrop.image = image
    coverCrop.naturalWidth = image.naturalWidth
    coverCrop.naturalHeight = image.naturalHeight
    coverCrop.visible = true
  } catch (e) { console.error(e) }
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => resolve(image)
    image.onerror = reject
    image.src = src
  })
}

function getCropRect(image, aspect) {
  const sourceAspect = image.naturalWidth / image.naturalHeight
  let width
  let height
  if (sourceAspect > aspect) {
    height = image.naturalHeight
    width = height * aspect
  } else {
    width = image.naturalWidth
    height = width / aspect
  }

  width /= coverCrop.zoom
  height /= coverCrop.zoom

  const centerX = image.naturalWidth * (coverCrop.focalX / 100)
  const centerY = image.naturalHeight * (coverCrop.focalY / 100)
  const x = Math.min(Math.max(centerX - width / 2, 0), image.naturalWidth - width)
  const y = Math.min(Math.max(centerY - height / 2, 0), image.naturalHeight - height)

  return { x, y, width, height }
}

function cropToBlob(image, aspect, outputWidth, outputHeight) {
  const rect = getCropRect(image, aspect)
  const canvas = document.createElement('canvas')
  canvas.width = outputWidth
  canvas.height = outputHeight
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, outputWidth, outputHeight)
  ctx.drawImage(image, rect.x, rect.y, rect.width, rect.height, 0, 0, outputWidth, outputHeight)

  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (blob) resolve(blob)
      else reject(new Error('封面裁剪失败'))
    }, 'image/jpeg', 0.9)
  })
}

function variantFile(blob, name) {
  const baseName = (name || 'cover').replace(/\.[^.]+$/, '').replace(/[^\w\u4e00-\u9fa5-]+/g, '_')
  return {
    card: new File([blob.card], `${baseName}_card.jpg`, { type: 'image/jpeg' }),
    detail: new File([blob.detail], `${baseName}_detail.jpg`, { type: 'image/jpeg' }),
    thumb: new File([blob.thumb], `${baseName}_thumb.jpg`, { type: 'image/jpeg' }),
  }
}

async function confirmCoverCrop() {
  if (!coverCrop.file || !coverCrop.image) return
  coverUploading.value = true
  try {
    const variants = {
      card: await cropToBlob(coverCrop.image, 16 / 9, 1200, 675),
      detail: await cropToBlob(coverCrop.image, 16 / 9, 1600, 900),
      thumb: await cropToBlob(coverCrop.image, 3 / 2, 480, 320),
    }
    const files = variantFile(variants, coverCrop.file.name)
    const [originalRes, cardRes, detailRes, thumbRes] = await Promise.all([
      uploadImage(coverCrop.file, workUploadMeta('cover_original')),
      uploadImage(files.card, workUploadMeta('cover_card')),
      uploadImage(files.detail, workUploadMeta('cover_detail')),
      uploadImage(files.thumb, workUploadMeta('cover_thumb')),
    ])

    const cropData = {
      focalX: coverCrop.focalX,
      focalY: coverCrop.focalY,
      zoom: coverCrop.zoom,
      originalWidth: coverCrop.naturalWidth,
      originalHeight: coverCrop.naturalHeight,
    }
    form.cover_original_url = originalRes.data.url
    form.cover_card_url = cardRes.data.url
    form.cover_detail_url = detailRes.data.url
    form.cover_thumb_url = thumbRes.data.url
    form.cover_url = cardRes.data.url
    form.cover_crop_data = JSON.stringify(cropData)
    coverCrop.visible = false
    ElMessage.success('封面裁剪上传成功')
  } catch (e) {
    console.error(e)
    ElMessage.error('封面处理失败，请重新上传')
  } finally {
    coverUploading.value = false
  }
}

function cancelCoverCrop() {
  coverCrop.visible = false
}

async function handleFileUpload({ file }) {
  if (!ensureWorkUploadMeta()) return
  try {
    const res = await uploadFile(file, workUploadMeta(form.work_type === 'website' ? 'project' : 'attachment'))
    form.attachment_url = res.data.url
    ElMessage.success('附件上传成功')
  } catch (e) { console.error(e) }
}

async function handleAudioUpload({ file }) {
  if (!ensureWorkUploadMeta()) return
  try {
    const res = await uploadAudio(file, workUploadMeta('audio'))
    form.audio_url = res.data.url
    ElMessage.success('音频上传成功')
  } catch (e) { console.error(e) }
}

async function handleVideoUpload({ file }) {
  if (!ensureWorkUploadMeta()) return
  videoUploading.value = true
  videoUploadProgress.value = 0
  videoUploadName.value = file.name
  try {
    const res = await uploadVideo(file, workUploadMeta('video'), {
      onUploadProgress: (event) => {
        if (!event.total) return
        const percent = Math.round((event.loaded * 100) / event.total)
        videoUploadProgress.value = Math.min(99, Math.max(1, percent))
      },
    })
    form.video_url = res.data.url
    videoUploadProgress.value = 100
    ElMessage.success('视频上传成功')
  } catch (e) {
    console.error(e)
    videoUploadProgress.value = 0
  } finally {
    videoUploading.value = false
  }
}

async function handleGalleryUpload({ file }) {
  if (!ensureWorkUploadMeta()) return
  try {
    const nextIndex = galleryList.value.length + 1
    const res = await uploadImage(file, workUploadMeta(`gallery_${nextIndex}`))
    const list = [...galleryList.value, res.data.url]
    form.gallery_urls = JSON.stringify(list)
    ElMessage.success('图片上传成功')
  } catch (e) { console.error(e) }
}

function removeGallery(i) {
  const list = [...galleryList.value]
  list.splice(i, 1)
  form.gallery_urls = list.length ? JSON.stringify(list) : ''
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
    const [majorsRes, teachersRes, competitionsRes] = await Promise.all([
      getMajors(),
      getTeachers().catch(() => ({ data: [] })),
      getCompetitions().catch(() => ({ data: [] })),
    ])
    majors.value = majorsRes.data || []
    teachers.value = teachersRes.data || []
    competitions.value = competitionsRes.data || []

    if (isEdit) {
      loading.value = true
      const res = await getWork(route.params.id)
      const w = res.data
      Object.assign(form, {
        title: w.title,
        author_names: w.author_names,
        guide_teacher: w.guide_teacher || '',
        major_id: w.major_id,
        class_name: w.class_name || '',
        academic_year: w.academic_year,
        semester: w.semester,
        contest_name: w.contest_name || '',
        award: w.award || '',
        work_type: w.work_type || '',
        cover_url: w.cover_url || '',
        cover_original_url: w.cover_original_url || '',
        cover_card_url: w.cover_card_url || '',
        cover_detail_url: w.cover_detail_url || '',
        cover_thumb_url: w.cover_thumb_url || '',
        cover_crop_data: w.cover_crop_data || '',
        content: w.content || '',
        demo_url: w.demo_url || '',
        attachment_url: w.attachment_url || '',
        audio_url: w.audio_url || '',
        video_url: w.video_url || '',
        gallery_urls: w.gallery_urls || '',
      })
      loading.value = false
    }
  } catch (e) { console.error(e) }
})

onBeforeUnmount(() => {
  if (themeObserver) { themeObserver.disconnect(); themeObserver = null }
  if (coverCrop.previewUrl) URL.revokeObjectURL(coverCrop.previewUrl)
})
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 20px; }
.file-name { margin-left: 10px; font-size: 13px; color: #909399; }
.video-upload-field {
  width: min(520px, 100%);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.upload-inline {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.upload-inline .file-name { margin-left: 0; }
.upload-progress-panel {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  background: var(--bg-secondary);
}
.upload-progress-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}
.upload-progress-meta span:first-child {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.upload-progress-meta span:last-child {
  flex-shrink: 0;
  color: var(--text-tertiary);
}
.cover-field { display: flex; align-items: flex-start; gap: 16px; flex-wrap: wrap; }
.cover-upload-preview {
  width: 200px;
  height: 112px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-secondary);
}
.cover-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}
.cover-tip { font-size: 12px; color: var(--text-tertiary); }
.crop-dialog {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 220px;
  gap: 24px;
}
.crop-main { min-width: 0; }
.crop-preview {
  position: relative;
  overflow: hidden;
  background: var(--bg-secondary);
  border-radius: 10px;
}
.crop-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.crop-preview-main {
  aspect-ratio: 16 / 9;
  width: 100%;
}
.crop-controls { margin-top: 16px; }
.crop-control {
  display: grid;
  grid-template-columns: 76px 1fr;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: var(--text-secondary);
}
.crop-side {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.preview-label {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 6px;
}
.preview-card,
.preview-detail { aspect-ratio: 16 / 9; }
.preview-thumb { aspect-ratio: 3 / 2; }
.gallery-previews { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
.gallery-item { position: relative; display: inline-block; }
.gallery-del {
  position: absolute; top: -6px; right: -6px;
  width: 20px; height: 20px;
  border-radius: 50%;
  background: var(--red);
  color: #fff;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  line-height: 1;
}
</style>
