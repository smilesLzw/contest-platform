<template>
  <div class="admin-news">
    <div class="toolbar">
      <h3 class="section-label">文章列表</h3>
      <el-button type="primary" size="default" @click="$router.push('/admin/news/create')">新建新闻</el-button>
    </div>

    <el-table :data="newsList" v-loading="loading && !isInitial">
      <el-table-column prop="title" label="标题" min-width="220" show-overflow-tooltip />
      <el-table-column label="分类" width="100">
        <template #default="{ row }">{{ categoryLabel(row.category) }}</template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <span :class="['status-tag', row.status]">
            {{ row.status === 'published' ? '已发布' : '草稿' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="置顶" width="60">
        <template #default="{ row }">
          <span v-if="row.is_top" class="top-badge">置顶</span>
        </template>
      </el-table-column>
      <el-table-column prop="author_name" label="作者" width="80" />
      <el-table-column label="创建时间" width="130">
        <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="260" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="$router.push(`/admin/news/${row.id}/edit`)">编辑</el-button>
          <el-button v-if="row.status !== 'published'" link type="primary" size="small" @click="handlePublish(row.id)">发布</el-button>
          <el-button link size="small" @click="handleToggleTop(row)" :style="{ color: row.is_top ? 'var(--amber)' : '' }">
            {{ row.is_top ? '取消置顶' : '置顶' }}
          </el-button>
          <el-button link size="small" @click="handleDelete(row)" style="color:var(--red)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!newsList.length && !loading" description="暂无新闻" />

    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, sizes, total"
        :page-sizes="[20, 50]"
        v-model:page-size="pageSize"
        @current-change="loadNews"
        @size-change="loadNews"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
.status-tag.published { background: rgba(52, 199, 89, 0.1); color: var(--green); }
.status-tag.draft { background: rgba(134, 134, 139, 0.1); color: var(--text-tertiary); }

.top-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 6px;
  background: rgba(255, 59, 48, 0.08);
  color: var(--red);
}

.pagination { display: flex; justify-content: center; margin-top: 24px; }
</style>
