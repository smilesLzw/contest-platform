<template>
  <div class="my-works">
    <div class="page-header">
      <h1>我的作品</h1>
      <el-button type="primary" @click="$router.push('/my/works/create')">发布作品</el-button>
    </div>

    <el-table :data="works" v-loading="loading" stripe>
      <el-table-column label="封面" width="80">
        <template #default="{ row }">
          <el-image :src="row.cover_thumb_url || row.cover_card_url || row.cover_url || ''" style="width: 50px; height: 35px" fit="cover">
            <template #error><div class="img-ph">无</div></template>
          </el-image>
        </template>
      </el-table-column>
      <el-table-column prop="title" label="作品名" min-width="160" show-overflow-tooltip />
      <el-table-column prop="major_name" label="专业" width="120" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="100">
        <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/my/works/${row.id}/edit`)">编辑</el-button>
          <el-button v-if="row.status === 'draft'" link type="primary" @click="handlePublish(row.id)">发布</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!works.length && !loading" description="暂无作品" />

    <el-pagination
      v-if="total > 0"
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next, total"
      @current-change="loadWorks"
      class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyWorks, deleteWork, publishWork } from '../../api/works'
import { ElMessage, ElMessageBox } from 'element-plus'

const works = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 12
const loading = ref(false)

function statusType(s) {
  return { draft: 'info', published: 'success', archived: 'warning' }[s] || 'info'
}
function statusLabel(s) {
  return { draft: '草稿', published: '已发布', archived: '已下架' }[s] || s
}

async function loadWorks() {
  loading.value = true
  try {
    const res = await getMyWorks({ page: page.value, page_size: pageSize })
    works.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

async function handlePublish(id) {
  try {
    await publishWork(id)
    ElMessage.success('发布成功')
    loadWorks()
  } catch (e) { console.error(e) }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除作品"${row.title}"？`, '提示', { type: 'warning' })
    await deleteWork(row.id)
    ElMessage.success('删除成功')
    loadWorks()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

onMounted(loadWorks)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { font-size: 24px; }
.pagination { display: flex; justify-content: center; margin-top: 20px; }
.img-ph { width: 50px; height: 35px; display: flex; align-items: center; justify-content: center; background: #f5f7fa; color: #c0c4cc; font-size: 12px; }
</style>
