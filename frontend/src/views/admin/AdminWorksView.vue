<template>
  <div class="admin-works">
    <el-card shadow="never" class="table-card admin-standard-card">
      <!-- Toolbar -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-select v-model="filters.status" placeholder="全部状态" clearable size="default" style="width:120px" @change="search">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="已下架" value="archived" />
          </el-select>
          <el-select v-model="filters.academic_year" placeholder="全部学年" clearable size="default" style="width:140px" @change="search">
            <el-option v-for="y in academicYears" :key="y" :label="y" :value="y" />
          </el-select>
          <el-input v-model="filters.keyword" placeholder="搜索作品名或作者" clearable size="default" style="width:200px" @keyup.enter="search" />
          <el-button type="primary" @click="search">搜索</el-button>
        </div>
        <div class="toolbar-right">
          <el-button @click="batchPublish" :disabled="!selectedIds.length" size="default"><el-icon style="margin-right:4px"><Upload /></el-icon>批量发布</el-button>
          <el-button @click="batchArchive" :disabled="!selectedIds.length" size="default"><el-icon style="margin-right:4px"><Folder /></el-icon>批量下架</el-button>
          <el-button type="primary" size="default" @click="$router.push('/admin/works/create')"><el-icon style="margin-right:4px"><Plus /></el-icon>新建作品</el-button>
        </div>
      </div>

      <!-- Table -->
      <el-table
        :data="works"
        v-loading="loading && !isInitial"
        stripe
        class="admin-standard-table"
        :header-cell-style="{ background:'var(--bg-secondary)', color:'var(--text-secondary)', fontWeight:600, fontSize:'12px', textAlign:'center' }"
        @selection-change="(val) => selectedIds = val.map(v => v.id)"
      >
        <el-table-column type="selection" width="46" align="center" />
        <el-table-column type="index" label="序号" width="64" align="center" />
        <el-table-column label="封面" width="72" align="center">
          <template #default="{ row }">
            <el-image :src="row.cover_thumb_url || row.cover_card_url || row.cover_url || ''" style="width:40px;height:28px;border-radius:4px" fit="cover">
              <template #error><div class="img-ph">—</div></template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="作品名" width="250" align="center" show-overflow-tooltip />
        <el-table-column prop="major_name" label="专业" width="140" align="center" show-overflow-tooltip />
        <el-table-column label="学年学期" width="140" align="center">
          <template #default="{ row }">{{ row.academic_year }} {{ row.semester === 1 ? '上' : '下' }}</template>
        </el-table-column>
        <el-table-column label="状态" width="90" align="center">
          <template #default="{ row }">
            <span :class="['status-tag', row.status]">
              {{ { draft: '草稿', published: '已发布', archived: '已下架' }[row.status] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="publisher_name" label="发布者" width="100" align="center" show-overflow-tooltip />
        <el-table-column label="操作" width="218" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="$router.push(`/admin/works/${row.id}/edit`)">
              <el-icon style="margin-right:1px"><Edit /></el-icon>编辑
            </el-button>
            <el-button v-if="row.status !== 'published'" link type="success" size="small" @click="handlePublish(row.id)">
              <el-icon style="margin-right:1px"><Upload /></el-icon>发布
            </el-button>
            <el-button v-if="row.status === 'published'" link size="small" @click="handleArchive(row.id)" style="color:var(--amber)">
              <el-icon style="margin-right:1px"><Folder /></el-icon>下架
            </el-button>
            <el-button link size="small" @click="handleDelete(row)" style="color:var(--red)">
              <el-icon style="margin-right:1px"><Delete /></el-icon>删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!works.length && !loading" description="暂无作品" />

      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next, sizes, total"
          :page-sizes="[20, 50]"
          v-model:page-size="pageSize"
          @current-change="loadWorks"
          @size-change="loadWorks"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Edit, Upload, Folder, Delete } from '@element-plus/icons-vue'
import { getAdminWorks, deleteWork, publishWork, archiveWork } from '../../api/works'
import { ElMessage, ElMessageBox } from 'element-plus'

const works = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const isInitial = ref(true)
const selectedIds = ref([])

const filters = reactive({ status: null, academic_year: null, keyword: null })

const academicYears = []
const y = new Date().getFullYear()
for (let i = 0; i < 5; i++) { const s = y - i - 1; academicYears.push(`${s}-${s + 1}`) }

async function loadWorks() {
  loading.value = true
  try {
    const res = await getAdminWorks({ ...filters, page: page.value, page_size: pageSize.value })
    works.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

function search() { page.value = 1; loadWorks() }

async function handlePublish(id) {
  try { await publishWork(id); ElMessage.success('发布成功'); loadWorks() }
  catch (e) { console.error(e) }
}

async function handleArchive(id) {
  try { await archiveWork(id); ElMessage.success('已下架'); loadWorks() }
  catch (e) { console.error(e) }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除"${row.title}"？`, '删除确认', { type: 'warning' })
    await deleteWork(row.id); ElMessage.success('删除成功'); loadWorks()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

async function batchPublish() {
  try {
    for (const id of selectedIds.value) await publishWork(id).catch(() => {})
    ElMessage.success('批量发布完成'); loadWorks()
  } catch (e) { console.error(e) }
}

async function batchArchive() {
  try {
    for (const id of selectedIds.value) await archiveWork(id).catch(() => {})
    ElMessage.success('批量下架完成'); loadWorks()
  } catch (e) { console.error(e) }
}

onMounted(loadWorks)
</script>

<style scoped>
.table-card :deep(.el-card__body) { padding: 24px; }
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  flex-wrap: wrap;
  gap: 12px;
}
.toolbar-left { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.toolbar-right { display: flex; gap: 8px; }

.status-tag {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 10px;
}
.status-tag.published { background: rgba(52, 199, 89, 0.1); color: var(--green); }
.status-tag.draft { background: rgba(134, 134, 139, 0.1); color: var(--text-tertiary); }
.status-tag.archived { background: rgba(255, 149, 0, 0.1); color: var(--amber); }

.pagination { display: flex; justify-content: center; margin-top: 24px; }
.img-ph { width:40px; height:28px; display:flex; align-items:center; justify-content:center; background:var(--bg-secondary); color:var(--text-tertiary); font-size:10px; border-radius:4px; }
</style>
