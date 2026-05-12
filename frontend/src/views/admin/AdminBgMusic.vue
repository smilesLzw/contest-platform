<template>
  <div class="bg-music-admin">
    <div class="page-header">
      <h1 class="page-title">背景音乐管理</h1>
      <el-button type="primary" @click="openDialog()">添加音乐</el-button>
    </div>

    <el-card shadow="never">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="sort_order" label="排序" width="70" align="center" />
        <el-table-column prop="title" label="曲目标题" min-width="180" />
        <el-table-column prop="artist" label="艺术家" width="140" />
        <el-table-column label="来源" width="100" align="center">
          <template #default="{ row }">
            <el-tag size="small" :type="row.source === 'preset' ? 'primary' : 'success'">
              {{ row.source === 'preset' ? '预置' : '学生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-switch :model-value="row.is_active" @change="toggleActive(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" align="center">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-popconfirm title="确认删除？" @confirm="handleDelete(row)">
              <template #reference>
                <el-button text type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑背景音乐' : '添加背景音乐'" width="500px" destroy-on-close>
      <el-form ref="dialogFormRef" :model="dialogForm" :rules="dialogRules" label-width="80px">
        <el-form-item label="曲目标题" prop="title">
          <el-input v-model="dialogForm.title" maxlength="200" />
        </el-form-item>
        <el-form-item label="艺术家" prop="artist">
          <el-input v-model="dialogForm.artist" maxlength="200" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="dialogForm.sort_order" :min="0" :max="9999" />
        </el-form-item>
        <el-form-item label="音频文件">
          <div>
            <el-upload
              :show-file-list="false"
              :http-request="handleDialogUpload"
              accept="audio/mpeg,audio/wav,audio/ogg,audio/aac,audio/flac,audio/mp4,.mp3,.wav,.ogg,.aac,.flac,.m4a"
            >
              <el-button :loading="uploading">上传音频</el-button>
            </el-upload>
            <span v-if="dialogForm.audio_url" class="file-hint">已上传：{{ dialogForm.audio_url.split('/').pop() }}</span>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitDialog">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { uploadAudio, getAdminBgMusic, createBgMusic, updateBgMusic, deleteBgMusic, toggleBgMusic } from '../../api/common'
import { ElMessage } from 'element-plus'

const list = ref([])
const loading = ref(false)
const uploading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)
const dialogFormRef = ref(null)

const dialogForm = reactive({
  title: '',
  artist: '',
  audio_url: '',
  sort_order: 0,
})

const dialogRules = {
  title: [{ required: true, message: '请输入曲目标题', trigger: 'blur' }],
  audio_url: [{ required: true, message: '请上传音频文件', trigger: 'blur' }],
}

async function loadList() {
  loading.value = true
  try {
    const res = await getAdminBgMusic()
    list.value = res.data || []
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

function openDialog(row) {
  editingId.value = row ? row.id : null
  if (row) {
    dialogForm.title = row.title
    dialogForm.artist = row.artist || ''
    dialogForm.audio_url = row.audio_url
    dialogForm.sort_order = row.sort_order
  } else {
    dialogForm.title = ''
    dialogForm.artist = ''
    dialogForm.audio_url = ''
    dialogForm.sort_order = 0
  }
  dialogVisible.value = true
}

async function handleDialogUpload({ file }) {
  uploading.value = true
  try {
    const res = await uploadAudio(file)
    dialogForm.audio_url = res.data.url
    ElMessage.success('上传成功')
  } catch (e) { console.error(e) }
  finally { uploading.value = false }
}

async function submitDialog() {
  const valid = await dialogFormRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    const data = { ...dialogForm }
    if (editingId.value) {
      await updateBgMusic(editingId.value, data)
      ElMessage.success('更新成功')
    } else {
      await createBgMusic(data)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    await loadList()
  } catch (e) { console.error(e) }
  finally { submitting.value = false }
}

async function toggleActive(row) {
  try {
    await toggleBgMusic(row.id)
    await loadList()
  } catch (e) { console.error(e) }
}

async function handleDelete(row) {
  try {
    await deleteBgMusic(row.id)
    ElMessage.success('删除成功')
    await loadList()
  } catch (e) { console.error(e) }
}

onMounted(() => loadList())
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-title { font-size: 24px; }
.file-hint { margin-left: 10px; font-size: 13px; color: #909399; }
</style>
