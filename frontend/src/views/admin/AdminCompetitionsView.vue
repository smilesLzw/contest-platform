<template>
  <div class="admin-competitions">
    <el-card shadow="never" class="table-card admin-standard-card">
      <div class="toolbar">
        <h3 class="section-label">赛事管理</h3>
        <div class="toolbar-actions">
          <el-button @click="batchDelete" :disabled="!selectedIds.length">批量删除</el-button>
          <el-button type="primary" @click="openDialog()"><el-icon style="margin-right:4px"><Plus /></el-icon>新增赛事</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading && !isInitial" stripe class="admin-standard-table"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
        @selection-change="(val) => selectedIds = val.map(v => v.id)"
      >
        <el-table-column type="selection" width="46" align="center" />
        <el-table-column type="index" label="序号" width="64" align="center" />
        <el-table-column prop="name" label="赛事名称" width="430" align="center" show-overflow-tooltip />
        <el-table-column label="学年学期" width="190" align="center">
          <template #default="{ row }">{{ row.academic_year }} {{ row.semester === 1 ? '上学期' : '下学期' }}</template>
        </el-table-column>
        <el-table-column label="状态" width="110" align="center">
          <template #default="{ row }">
            <span :class="['status-tag', row.is_active ? 'on' : 'off']">
              {{ row.is_active ? '启用' : '禁用' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">
              <el-icon style="margin-right:1px"><Edit /></el-icon>编辑
            </el-button>
            <el-button link size="small" @click="handleToggle(row)" :style="{ color: row.is_active ? 'var(--amber)' : 'var(--green)' }">
              <el-icon style="margin-right:1px"><SwitchButton /></el-icon>{{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button link size="small" @click="handleDelete(row)" style="color:var(--red)">
              <el-icon style="margin-right:1px"><Delete /></el-icon>删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!isInitial && !list.length && !loading" description="暂无赛事" />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑赛事' : '新增赛事'" width="440px">
      <el-form :model="form" label-width="72px">
        <el-form-item label="赛事名称">
          <el-input v-model="form.name" maxlength="200" />
        </el-form-item>
        <el-form-item label="学年">
          <el-select v-model="form.academic_year" placeholder="请选择" style="width:100%">
            <el-option v-for="y in academicYears" :key="y" :label="y" :value="y" />
          </el-select>
        </el-form-item>
        <el-form-item label="学期">
          <el-radio-group v-model="form.semester">
            <el-radio :value="1">上学期</el-radio>
            <el-radio :value="2">下学期</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Edit, Delete, SwitchButton } from '@element-plus/icons-vue'
import { getAdminCompetitions, createCompetition, updateCompetition, deleteCompetition, toggleCompetition } from '../../api/common'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const loading = ref(false)
const isInitial = ref(true)
const selectedIds = ref([])
const saving = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)

const form = reactive({ name: '', academic_year: '', semester: 1 })

const academicYears = []
const y = new Date().getFullYear()
for (let i = 0; i < 5; i++) {
  const s = y - i + (new Date().getMonth() >= 8 ? 0 : -1)
  academicYears.push(`${s}-${s + 1}`)
}
// dedupe and ensure current year
const y2 = new Date().getFullYear()
const curYear = `${y2}-${y2 + 1}`
const nextYear = `${y2 + 1}-${y2 + 2}`
if (!academicYears.includes(curYear)) academicYears.unshift(curYear)
if (!academicYears.includes(nextYear)) academicYears.push(nextYear)

async function load() {
  loading.value = true
  try {
    const res = await getAdminCompetitions()
    list.value = res.data || []
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

function openDialog(row) {
  editingId.value = row ? row.id : null
  if (row) {
    form.name = row.name
    form.academic_year = row.academic_year
    form.semester = row.semester
  } else {
    form.name = ''
    form.academic_year = ''
    form.semester = 1
  }
  dialogVisible.value = true
}

async function save() {
  if (!form.name || !form.academic_year) { ElMessage.warning('请填写必要信息'); return }
  saving.value = true
  try {
    if (editingId.value) {
      await updateCompetition(editingId.value, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createCompetition({ ...form })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    load()
  } catch (e) { console.error(e) }
  finally { saving.value = false }
}

async function handleToggle(row) {
  try {
    await toggleCompetition(row.id)
    load()
  } catch (e) { console.error(e) }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除赛事"${row.name}"？`, '删除确认', { type: 'warning' })
    await deleteCompetition(row.id)
    ElMessage.success('删除成功')
    load()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

async function batchDelete() {
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 个赛事？`, '批量删除确认', { type: 'warning' })
    for (const id of selectedIds.value) await deleteCompetition(id).catch(() => {})
    ElMessage.success('批量删除完成')
    selectedIds.value = []
    load()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(load)
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.toolbar-actions { display: flex; align-items: center; gap: 8px; }
.section-label { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.02em; }
.status-tag { font-size: 11px; font-weight: 500; padding: 2px 8px; border-radius: 10px; }
.status-tag.on { background: rgba(52, 199, 89, 0.1); color: var(--green); }
.status-tag.off { background: rgba(255, 59, 48, 0.08); color: var(--red); }
</style>
