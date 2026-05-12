<template>
  <div class="admin-users">
    <div class="toolbar">
      <h3 class="section-label">教师账号</h3>
      <el-button type="primary" size="default" @click="openDialog()">新建教师</el-button>
    </div>

    <el-table :data="users" v-loading="loading && !isInitial">
      <el-table-column prop="name" label="姓名" width="90" />
      <el-table-column prop="username" label="工号" width="110" />
      <el-table-column prop="department" label="院系" width="150" />
      <el-table-column label="状态" width="70">
        <template #default="{ row }">
          <span :class="['status-tag', row.status ? 'on' : 'off']">
            {{ row.status ? '启用' : '禁用' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="130">
        <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-button link size="small" @click="handleToggleStatus(row)" :style="{ color: row.status ? 'var(--amber)' : 'var(--green)' }">
            {{ row.status ? '禁用' : '启用' }}
          </el-button>
          <el-button link size="small" @click="handleResetPwd(row)" style="color:var(--red)">重置密码</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!users.length && !loading" description="暂无教师" />

    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, sizes, total"
        :page-sizes="[20, 50]"
        v-model:page-size="pageSize"
        @current-change="loadUsers"
        @size-change="loadUsers"
      />
    </div>

    <!-- Dialog -->
    <el-dialog v-model="dialog.visible" :title="dialog.isEdit ? '编辑教师' : '新建教师'" width="420px">
      <el-form :model="form" label-width="72px">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="工号">
          <el-input v-model="form.username" :disabled="dialog.isEdit" />
        </el-form-item>
        <el-form-item label="密码" v-if="!dialog.isEdit">
          <el-input v-model="form.password" type="password" show-password placeholder="至少 8 位，包含字母和数字" />
        </el-form-item>
        <el-form-item label="院系">
          <el-input v-model="form.department" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveUser">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getUsers, createUser, updateUser, toggleUserStatus, resetPassword } from '../../api/users'
import { ElMessage, ElMessageBox } from 'element-plus'

const users = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const isInitial = ref(true)
const saving = ref(false)

const dialog = reactive({ visible: false, isEdit: false, editId: null })
const form = reactive({ name: '', username: '', password: '', department: '' })

async function loadUsers() {
  loading.value = true
  try {
    const res = await getUsers({ page: page.value, page_size: pageSize.value })
    users.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

function openDialog(row) {
  if (row) {
    dialog.isEdit = true; dialog.editId = row.id
    form.name = row.name; form.username = row.username; form.password = ''; form.department = row.department || ''
  } else {
    dialog.isEdit = false; dialog.editId = null
    form.name = ''; form.username = ''; form.password = ''; form.department = ''
  }
  dialog.visible = true
}

async function saveUser() {
  if (!form.name || !form.username) { ElMessage.warning('请填写必要信息'); return }
  if (!dialog.isEdit && !form.password) { ElMessage.warning('请设置密码'); return }
  saving.value = true
  try {
    if (dialog.isEdit) {
      await updateUser(dialog.editId, { name: form.name, department: form.department })
      ElMessage.success('更新成功')
    } else {
      await createUser({ username: form.username, password: form.password, name: form.name, department: form.department })
      ElMessage.success('创建成功')
    }
    dialog.visible = false; loadUsers()
  } catch (e) { console.error(e) }
  finally { saving.value = false }
}

async function handleToggleStatus(row) {
  const action = row.status ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确定${action}"${row.name}"？`, '提示', { type: 'warning' })
    await toggleUserStatus(row.id); ElMessage.success(`${action}成功`); loadUsers()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

async function handleResetPwd(row) {
  try {
    await ElMessageBox.confirm(`确定重置"${row.name}"的密码？`, '提示', { type: 'warning' })
    const res = await resetPassword(row.id)
    ElMessage.success(res.message || '密码已重置')
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(loadUsers)
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.section-label {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.status-tag {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 10px;
}
.status-tag.on { background: rgba(52, 199, 89, 0.1); color: var(--green); }
.status-tag.off { background: rgba(255, 59, 48, 0.08); color: var(--red); }

.pagination { display: flex; justify-content: center; margin-top: 24px; }
</style>
