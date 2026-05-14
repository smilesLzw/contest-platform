<template>
  <div class="news-page">
    <h1 class="page-title">资讯中心</h1>

    <!-- Category tabs -->
    <div class="category-tabs">
      <span
        v-for="t in tabs" :key="t.value"
        :class="['tab-item', { active: activeCategory === t.value }]"
        @click="activeCategory = t.value; loadNews()"
      >{{ t.label }}</span>
    </div>

    <div v-loading="loading && !isInitial">
      <!-- News grid -->
      <div v-if="newsList.length" class="news-grid">
        <div v-for="n in newsList" :key="n.id" class="news-card" @click="$router.push(`/news/${n.id}`)">
          <div class="card-cover">
            <img v-if="n.cover_url" :src="n.cover_url" alt="" />
            <el-icon v-else :size="28" color="var(--text-tertiary)"><Reading /></el-icon>
          </div>
          <div class="card-body">
            <span class="card-cat">{{ catLabel(n.category) }}</span>
            <h3>{{ n.title }}</h3>
            <p class="card-summary">{{ getSummary(n.content) }}</p>
            <div class="card-meta">
              <span>{{ n.author_name }}</span>
              <span>{{ formatTime(n.published_at) }}</span>
            </div>
          </div>
        </div>
      </div>
      <el-empty v-else-if="!loading" description="暂无新闻" />
    </div>

    <el-pagination
      v-if="total > 0"
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next, sizes, total"
      :page-sizes="[6, 20, 50]"
      v-model:page-size="pageSize"
      @current-change="loadNews"
      @size-change="loadNews"
      class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Reading } from '@element-plus/icons-vue'
import { getNewsList } from '../../api/news'

const tabs = [
  { label: '全部', value: '' },
  { label: '教程指南', value: 'tutorial' },
  { label: '科技前沿', value: 'tech' },
  { label: '教研室动态', value: 'lab' },
]

const activeCategory = ref('')
const newsList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(6)
const loading = ref(false)
const isInitial = ref(true)

function catLabel(c) {
  return { tutorial: '教程指南', tech: '科技前沿', lab: '教研室动态' }[c] || c
}

function getSummary(content) {
  if (!content) return ''
  return content.replace(/[#*`\n>\[\]!]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 100) + (content.length > 100 ? '…' : '')
}

function formatTime(t) { return t ? t.slice(0, 10) : '' }

async function loadNews() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (activeCategory.value) params.category = activeCategory.value
    const res = await getNewsList(params)
    newsList.value = res.data.items || []
    total.value = res.data.total
  } catch (e) { console.error(e) }
  finally {
    loading.value = false
    isInitial.value = false
  }
}

onMounted(loadNews)
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

/* Category tabs */
.category-tabs { display: flex; gap: 4px; margin-bottom: 32px; }
.tab-item {
  padding: 7px 20px;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}
.tab-item:hover { color: var(--text-primary); background: var(--bg-secondary); }
.tab-item.active { background: var(--accent); color: #ffffff; }

/* News cards */
.news-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.news-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.news-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px var(--shadow-lg);
}
.card-cover {
  height: 140px;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.card-cover img { width: 100%; height: 100%; object-fit: cover; }
.card-body { padding: 16px; }
.card-cat {
  font-size: 11px;
  color: var(--accent);
  letter-spacing: 0.04em;
  font-weight: 500;
}
.card-body h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 6px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  letter-spacing: -0.01em;
}
.card-summary {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 10px;
}
.card-meta { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-tertiary); }

.pagination { display: flex; justify-content: center; margin-top: 40px; }

@media (max-width: 1100px) {
  .news-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .page-title {
    font-size: 32px;
    margin-bottom: 20px;
  }

  .category-tabs {
    overflow-x: auto;
    margin: 0 -14px 24px;
    padding: 0 14px 2px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }

  .category-tabs::-webkit-scrollbar {
    display: none;
  }

  .tab-item {
    flex: 0 0 auto;
    padding: 7px 16px;
  }

  .news-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .news-card:hover {
    transform: none;
  }

  .card-cover {
    height: auto;
    aspect-ratio: 16 / 9;
  }

  .card-meta {
    gap: 12px;
    flex-wrap: wrap;
  }

  .pagination {
    margin-top: 28px;
  }

  .pagination :deep(.el-pagination) {
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
  }
}
</style>
