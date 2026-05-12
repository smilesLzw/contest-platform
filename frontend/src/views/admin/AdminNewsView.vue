<template>
  <div class="admin-news">
    <el-card shadow="never" class="table-card">
      <div class="toolbar">
        <h3 class="section-label">文章列表</h3>
        <el-button type="primary" @click="$router.push('/admin/news/create')"><el-icon style="margin-right:4px"><Plus /></el-icon>新建新闻</el-button>
      </div>

      <el-table :data="newsList" v-loading="loading && !isInitial" stripe style="width:100%"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
      >
        <el-table-column prop="title" label="标题" min-width="220" show-overflow-tooltip />
        <el-table-column label="分类" width="100" align="center">
          <template #default="{ row }">{{ categoryLabel(row.category) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="80" align="center">
          <template #default="{ row }">
            <span :class="['status-tag', row.status]">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="置顶" width="70" align="center">
          <template #default="{ row }">
            <span v-if="row.is_top" class="top-badge">置顶</span>
            <span v-else style="color:var(--text-tertiary)">—</span>
          </template>
        </el-table-column>
        <el-table-column prop="author_name" label="作者" width="90" align="center" />
        <el-table-column label="创建时间" width="130" align="center">
          <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="$router.push(`/admin/news/${row.id}/edit`)">
              <el-icon style="margin-right:1px"><Edit /></el-icon>编辑
            </el-button>
            <el-button v-if="row.status !== 'published'" link type="success" size="small" @click="handlePublish(row.id)">
              <el-icon style="margin-right:1px"><Upload /></el-icon>发布
            </el-button>
            <el-button link size="small" @click="handleToggleTop(row)" :style="{ color: row.is_top ? 'var(--amber)' : '' }">
              <el-icon style="margin-right:1px"><Top /></el-icon>{{ row.is_top ? '取消置顶' : '置顶' }}
            </el-button>
            <el-button link size="small" @click="handleDelete(row)" style="color:var(--red)">
              <el-icon style="margin-right:1px"><Delete /></el-icon>删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!newsList.length && !loading" description="暂无新闻" />

      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="page" :page-size="pageSize" :total="total"
          layout="prev, pager, next, sizes, total" :page-sizes="[20, 50]"
          v-model:page-size="pageSize"
          @current-change="loadNews" @size-change="loadNews"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Upload, Top, Delete } from '@element-plus/icons-vue'
import { getNewsList, deleteNews, publishNews, toggleTopNews } from '../../api/news'
import { ElMessage, ElMessageBox } from 'element-plus'

const newsList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const isInitial = ref(true)

function categoryLabel(c) {
  return { tutorial: '教程指南', tech: '科技前沿', lab: '教研室动态' }[c] || c
}

async function loadNews() {
  loading.value = true
  try {
    const res = await getNewsList({ page: page.value, page_size: pageSize.value })
    newsList.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

async function handlePublish(id) {
  try { await publishNews(id); ElMessage.success('发布成功'); loadNews() }
  catch (e) { console.error(e) }
}

async function handleToggleTop(row) {
  try { await toggleTopNews(row.id); ElMessage.success(row.is_top ? '已取消置顶' : '已置顶'); loadNews() }
  catch (e) { console.error(e) }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除"${row.title}"？`, '删除确认', { type: 'warning' })
    await deleteNews(row.id); ElMessage.success('删除成功'); loadNews()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(loadNews)
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.section-label { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.02em; }
.status-tag { font-size: 11px; font-weight: 500; padding: 2px 8px; border-radius: 10px; white-space: nowrap; }
.status-tag.published { background: rgba(52, 199, 89, 0.1); color: var(--green); }
.status-tag.draft { background: rgba(134, 134, 139, 0.1); color: var(--text-tertiary); }
.top-badge { font-size: 10px; font-weight: 600; padding: 1px 6px; border-radius: 6px; background: rgba(255, 59, 48, 0.08); color: var(--red); white-space: nowrap; }
.pagination { display: flex; justify-content: center; margin-top: 24px; }
</style>
