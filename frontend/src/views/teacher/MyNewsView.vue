<template>
  <div class="my-news">
    <div class="page-header">
      <h1>我的新闻</h1>
      <el-button type="primary" @click="$router.push('/my/news/create')">发布新闻</el-button>
    </div>

    <el-table :data="newsList" v-loading="loading" stripe>
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
      <el-table-column label="分类" width="100">
        <template #default="{ row }">{{ categoryLabel(row.category) }}</template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : 'info'" size="small">
            {{ row.status === 'published' ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="100">
        <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/my/news/${row.id}/edit`)">编辑</el-button>
          <el-button v-if="row.status === 'draft'" link type="primary" @click="handlePublish(row.id)">发布</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!newsList.length && !loading" description="暂无新闻" />

    <el-pagination
      v-if="total > 0"
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next, total"
      @current-change="loadNews"
      class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyNews, deleteNews, publishNews } from '../../api/news'
import { ElMessage, ElMessageBox } from 'element-plus'

const newsList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

function categoryLabel(c) {
  return { contest: '赛事报道', notice: '活动通知', honor: '荣誉展示', other: '其他' }[c] || c
}

async function loadNews() {
  loading.value = true
  try {
    const res = await getMyNews({ page: page.value, page_size: pageSize })
    newsList.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

async function handlePublish(id) {
  try {
    await publishNews(id)
    ElMessage.success('发布成功')
    loadNews()
  } catch (e) { console.error(e) }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除新闻"${row.title}"？`, '提示', { type: 'warning' })
    await deleteNews(row.id)
    ElMessage.success('删除成功')
    loadNews()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(loadNews)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { font-size: 24px; }
.pagination { display: flex; justify-content: center; margin-top: 20px; }
</style>
