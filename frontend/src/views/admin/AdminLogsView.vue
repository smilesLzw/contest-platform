<template>
  <div class="admin-logs">
    <el-card shadow="never" class="table-card">
      <div class="toolbar">
        <h3 class="section-label">操作日志</h3>
      </div>

      <el-table :data="logs" v-loading="loading && !isInitial" stripe style="width:100%"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
      >
        <el-table-column label="ID" prop="id" width="70" align="center" />
        <el-table-column label="用户ID" prop="user_id" width="80" align="center" />
        <el-table-column label="操作" prop="action" width="150" align="center" />
        <el-table-column label="对象类型" prop="target_type" width="100" align="center" />
        <el-table-column label="对象ID" prop="target_id" width="80" align="center" />
        <el-table-column label="详情" prop="detail" min-width="280" show-overflow-tooltip align="center" />
        <el-table-column label="时间" width="170" align="center">
          <template #default="{ row }">{{ row.created_at }}</template>
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
import { getLogs } from '../../api/common'

const logs = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const isInitial = ref(true)

async function loadLogs() {
  loading.value = true
  try {
    const res = await getLogs({ page: page.value, page_size: pageSize.value })
    logs.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

onMounted(loadLogs)
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.section-label { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.02em; }
.pagination { display: flex; justify-content: center; margin-top: 24px; }
</style>
