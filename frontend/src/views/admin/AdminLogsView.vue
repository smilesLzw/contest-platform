<template>
  <div class="admin-logs">
    <el-card shadow="never" class="table-card admin-standard-card">
      <div class="toolbar">
        <h3 class="section-label">操作日志</h3>
      </div>

      <el-table :data="logs" v-loading="loading && !isInitial" stripe class="admin-standard-table"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column label="ID" prop="id" width="80" align="center" />
        <el-table-column label="用户ID" prop="user_id" width="90" align="center" />
        <el-table-column label="操作" prop="action" width="170" align="center" show-overflow-tooltip />
        <el-table-column label="对象类型" prop="target_type" width="130" align="center" show-overflow-tooltip />
        <el-table-column label="对象ID" prop="target_id" width="90" align="center" />
        <el-table-column label="详情" prop="detail" width="360" align="center" show-overflow-tooltip />
        <el-table-column label="时间" width="190" align="center">
          <template #default="{ row }">{{ formatDateTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="撤销" width="110" align="center">
          <template #default="{ row }">
            <el-button
              v-if="authStore.isAdmin && row.is_undoable && !row.undone_at"
              link
              type="primary"
              size="small"
              @click="handleUndo(row)"
            >
              撤销
            </el-button>
            <span v-else-if="row.undone_at" class="muted">已撤销</span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!logs.length && !loading" description="暂无日志" />

      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next, sizes, total"
          :page-sizes="[20, 50]"
          v-model:page-size="pageSize"
          @current-change="loadLogs"
          @size-change="loadLogs"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { getLogs, undoLog } from '../../api/common'

const authStore = useAuthStore()

const logs = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const isInitial = ref(true)

function formatDateTime(value) {
  return value ? value.replace('T', ' ').slice(0, 16) : ''
}

async function loadLogs() {
  loading.value = true
  try {
    const res = await getLogs({ page: page.value, page_size: pageSize.value })
    logs.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

async function handleUndo(row) {
  try {
    await ElMessageBox.confirm(`确定撤销这次操作？${row.detail || ''}`, '撤销确认', { type: 'warning' })
    await undoLog(row.id)
    ElMessage.success('撤销成功')
    loadLogs()
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

onMounted(loadLogs)
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.section-label { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.02em; }
.pagination { display: flex; justify-content: center; margin-top: 24px; }
.muted { color: var(--text-tertiary); font-size: 12px; }
</style>
