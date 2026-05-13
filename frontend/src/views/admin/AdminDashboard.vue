<template>
  <div class="dashboard">
    <!-- Stat cards -->
    <div class="stat-grid">
      <div class="stat-card">
        <span class="stat-num" style="color: var(--accent)">{{ stats.works_count ?? '-' }}</span>
        <span class="stat-label">作品总数</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" style="color: var(--green)">{{ stats.news_count ?? '-' }}</span>
        <span class="stat-label">新闻总数</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" style="color: var(--amber)">{{ stats.tools_count ?? '-' }}</span>
        <span class="stat-label">AI 工具数</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" style="color: var(--red)">{{ usersCount ?? '-' }}</span>
        <span class="stat-label">教师账号数</span>
      </div>
    </div>

    <!-- Recent logs -->
    <el-card shadow="never" class="table-card admin-standard-card">
      <h3 class="section-title">最近操作日志</h3>
      <el-table :data="recentLogs" v-loading="logLoading && !isInitial" stripe class="admin-standard-table"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column label="用户ID" prop="user_id" width="100" align="center" />
        <el-table-column label="操作" prop="action" width="180" align="center" show-overflow-tooltip />
        <el-table-column label="对象类型" prop="target_type" width="140" align="center" show-overflow-tooltip />
        <el-table-column label="详情" prop="detail" width="430" align="center" show-overflow-tooltip />
        <el-table-column label="时间" width="190" align="center">
          <template #default="{ row }">{{ formatDateTime(row.created_at) }}</template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!recentLogs.length && !logLoading" description="暂无日志" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStats, getLogs } from '../../api/common'
import { getUsers } from '../../api/users'

const stats = ref({})
const usersCount = ref(0)
const recentLogs = ref([])
const logLoading = ref(false)
const isInitial = ref(true)

function formatDateTime(value) {
  return value ? value.replace('T', ' ').slice(0, 16) : ''
}

onMounted(async () => {
  try {
    const [statsRes, usersRes] = await Promise.all([
      getStats().catch(() => ({ data: {} })),
      getUsers({ page: 1, page_size: 1 }).catch(() => ({ data: { total: 0 } })),
    ])
    stats.value = statsRes.data || {}
    usersCount.value = usersRes.data?.total || 0

    logLoading.value = true
    const logRes = await getLogs({ page: 1, page_size: 10 })
    recentLogs.value = logRes.data?.items || []
  } catch (e) {
    console.error(e)
  } finally {
    logLoading.value = false
    isInitial.value = false
  }
})
</script>

<style scoped>
/* Stat cards */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}
@media (max-width: 900px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
  .stat-grid { grid-template-columns: 1fr; }
}
.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 24px;
  box-shadow: 0 2px 12px var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.stat-num {
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.03em;
}
.stat-label {
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
}

/* Log section */
.table-card :deep(.el-card__body) { padding: 24px; }
.section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 14px;
  letter-spacing: -0.02em;
}
</style>
