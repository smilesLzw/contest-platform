<template>
  <div class="works-page">
    <h1 class="page-title">作品展示</h1>

    <!-- Filter bar -->
    <div class="filter-bar">
      <el-form :inline="true" :model="filters" size="default">
        <el-form-item label="学年">
          <el-select v-model="filters.academic_year" placeholder="全部学年" clearable style="width: 140px">
            <el-option v-for="y in academicYears" :key="y" :label="y" :value="y" />
          </el-select>
        </el-form-item>
        <el-form-item label="学期">
          <el-select v-model="filters.semester" placeholder="全部学期" clearable style="width: 120px">
            <el-option label="上学期" :value="1" />
            <el-option label="下学期" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select v-model="filters.major_id" placeholder="全部专业" clearable style="width: 160px">
            <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="filters.keyword" placeholder="搜索作品名/作者" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="search">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- View toggle -->
    <div class="view-bar">
      <el-radio-group v-model="viewMode" size="small">
        <el-radio-button value="grid">卡片</el-radio-button>
        <el-radio-button value="list">列表</el-radio-button>
      </el-radio-group>
    </div>

    <!-- Grid view -->
    <div v-if="viewMode === 'grid'" class="works-grid" v-loading="loading && !isInitial">
      <WorkCard v-for="w in works" :key="w.id" :work="w" />
      <el-empty v-if="!works.length && !loading" description="暂无作品" />
    </div>

    <!-- List view -->
    <div v-else class="works-list" v-loading="loading && !isInitial">
      <el-table :data="works" v-if="works.length">
        <el-table-column label="封面" width="100">
          <template #default="{ row }">
            <el-image :src="row.cover_thumb_url || row.cover_card_url || row.cover_url || ''" style="width:60px;height:40px" fit="cover">
              <template #error><div class="img-fb">&mdash;</div></template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="作品名" min-width="180" show-overflow-tooltip />
        <el-table-column prop="major_name" label="专业" width="120" />
        <el-table-column label="学年学期" width="130">
          <template #default="{ row }">{{ row.academic_year }} {{ row.semester === 1 ? '上学期' : '下学期' }}</template>
        </el-table-column>
        <el-table-column prop="award" label="获奖" width="100" />
        <el-table-column label="发布时间" width="100">
          <template #default="{ row }">{{ row.published_at?.slice(0, 10) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button link type="primary" @click="$router.push(`/works/${row.id}`)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无作品" />
    </div>

    <!-- Pagination -->
    <div class="pagination-wrap" v-if="total > 0">
      <el-pagination
        v-model:current-page="filters.page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, sizes, total"
        :page-sizes="[20, 50]"
        v-model:page-size="pageSize"
        @current-change="loadWorks"
        @size-change="loadWorks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getWorks } from '../../api/works'
import { getMajors } from '../../api/common'
import WorkCard from '../../components/business/WorkCard.vue'

const viewMode = ref('grid')
const loading = ref(false)
const isInitial = ref(true)
const works = ref([])
const total = ref(0)
const majors = ref([])
const pageSize = ref(12)

const filters = ref({ page: 1, academic_year: null, semester: null, major_id: null, keyword: null })

const academicYears = []
const year = new Date().getFullYear()
for (let i = 0; i < 5; i++) {
  const start = year - i - 1
  academicYears.push(`${start}-${start + 1}`)
}

async function loadWorks() {
  loading.value = true
  try {
    const res = await getWorks({ ...filters.value, page_size: pageSize.value })
    works.value = res.data.items
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
}

function search() { filters.value.page = 1; loadWorks() }
function resetFilters() {
  filters.value = { page: 1, academic_year: null, semester: null, major_id: null, keyword: null }
  loadWorks()
}

onMounted(async () => {
  try { const r = await getMajors(); majors.value = r.data || [] } catch (e) { console.error(e) }
  loadWorks()
})
</script>

<style scoped>
.page-title {
  font-family: var(--font-display);
  font-size: 40px;
  font-weight: 600;
  margin-bottom: 28px;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}
.filter-bar {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 20px 24px 4px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px var(--shadow-sm);
}
.view-bar { display: flex; justify-content: flex-end; margin-bottom: 16px; }
.works-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.works-list {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: 0 2px 12px var(--shadow-sm);
}
.pagination-wrap { display: flex; justify-content: center; margin-top: 40px; }
.img-fb {
  width: 60px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  font-size: 12px;
}
</style>
