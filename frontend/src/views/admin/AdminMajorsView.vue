<template>
  <div class="admin-majors">
    <el-card shadow="never" class="table-card">
      <div class="toolbar">
        <h3 class="section-label">专业管理</h3>
        <el-button type="primary" @click="openDialog()"><el-icon style="margin-right:4px"><Plus /></el-icon>新增专业</el-button>
      </div>

      <el-table :data="list" v-loading="loading" stripe style="width:100%"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
      >
        <el-table-column prop="grade" label="年级" width="100" align="center" />
        <el-table-column prop="duration" label="学制" width="100" align="center" />
        <el-table-column prop="name" label="专业名称" min-width="200" align="center" />
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
      <el-empty v-if="!list.length && !loading" description="暂无专业" />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑专业' : '新增专业'" width="440px">
      <el-form :model="form" label-width="72px">
        <el-form-item label="年级">
          <el-select v-model="form.grade" placeholder="请选择年级" style="width:100%" filterable allow-create>
            <el-option v-for="g in gradeOptions" :key="g" :label="g" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="学制">
          <el-radio-group v-model="form.duration">
            <el-radio value="三年制">三年制</el-radio>
            <el-radio value="五年制">五年制</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="专业名称">
          <el-input v-model="form.name" maxlength="100" placeholder="如：计算机科学与技术" />
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
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { getAdminMajors, createMajor, updateMajor, deleteMajor } from '../../api/common'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)

const form = reactive({ grade: '', duration: '三年制', name: '' })

function generateGradeOptions() {
  const currentYear = new Date().getFullYear()
  const startYear = 2022
  const endYear = currentYear + 2
  const options = []
  for (let y = startYear; y <= endYear; y++) {
    options.push(`${y}级`)
  }
  return options
}

const gradeOptions = generateGradeOptions()

async function load() {
  loading.value = true
  try {
    const res = await getAdminMajors()
    list.value = res.data || []
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

function openDialog(row) {
  editingId.value = row ? row.id : null
  if (row) {
    form.grade = row.grade
    form.duration = row.duration
    form.name = row.name
  } else {
    form.grade = ''
    form.duration = '三年制'
    form.name = ''
  }
  dialogVisible.value = true
}

async function save() {
  if (!form.grade || !form.name) { ElMessage.warning('请填写必要信息'); return }
  saving.value = true
  try {
    if (editingId.value) {
      await updateMajor(editingId.value, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createMajor({ ...form })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    load()
  } catch (e) { console.error(e) }
  finally { saving.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除"${row.grade} ${row.name}"？`, '删除确认', { type: 'warning' })
    await deleteMajor(row.id)
    ElMessage.success('删除成功')
    load()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(load)
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.section-label { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.02em; }
</style>
