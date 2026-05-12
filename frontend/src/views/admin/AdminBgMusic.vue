<template>
  <div class="bg-music-admin">
    <el-card shadow="never" class="table-card">
      <div class="toolbar">
        <h3 class="section-label">背景音乐管理</h3>
        <el-button type="primary" @click="openDialog()"><el-icon style="margin-right:4px"><Plus /></el-icon>添加音乐</el-button>
      </div>

      <el-table :data="list" v-loading="loading" stripe style="width:100%"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
      >
        <el-table-column prop="sort_order" label="排序" width="70" align="center" />
        <el-table-column prop="title" label="曲目标题" min-width="240" show-overflow-tooltip align="center" />
        <el-table-column prop="artist" label="艺术家" width="150" align="center" />
        <el-table-column label="来源" width="90" align="center">
          <template #default="{ row }">
            <span :class="['source-tag', row.source]">
              {{ row.source === 'preset' ? '预置' : '学生' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-switch :model-value="row.is_active" size="small" @change="toggleActive(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">
              <el-icon style="margin-right:1px"><Edit /></el-icon>编辑
            </el-button>
            <el-button link size="small" @click="handleDelete(row)" style="color:var(--red)">
              <el-icon style="margin-right:1px"><Delete /></el-icon>删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!list.length && !loading" description="暂无背景音乐" />
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
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { uploadAudio, getAdminBgMusic, createBgMusic, updateBgMusic, deleteBgMusic, toggleBgMusic } from '../../api/common'
import { ElMessage, ElMessageBox } from 'element-plus'

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
    await ElMessageBox.confirm(`确定删除"${row.title}"？`, '删除确认', { type: 'warning' })
    await deleteBgMusic(row.id)
    ElMessage.success('删除成功')
    await loadList()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(() => loadList())
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.section-label { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.02em; }
.file-hint { margin-left: 10px; font-size: 13px; color: var(--text-tertiary); }

.source-tag {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 10px;
}
.source-tag.preset { background: rgba(0, 113, 227, 0.08); color: var(--accent); }
.source-tag.student { background: rgba(52, 199, 89, 0.1); color: var(--green); }
</style>
