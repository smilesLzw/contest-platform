<template>
  <div class="ai-tools-page">
    <h1 class="page-title">AI 工具导航</h1>
    <p class="page-desc">精选国内外优质 AI 工具，助力学习与工作效率提升</p>

    <!-- Filter bar -->
    <div class="filter-bar">
      <div class="region-tabs">
        <span
          v-for="r in regionOptions" :key="r.value"
          :class="['filter-btn', { active: activeRegion === r.value }]"
          @click="activeRegion = r.value"
        >{{ r.label }}</span>
      </div>
      <span class="filter-divider"></span>
      <div class="price-tabs">
        <span
          v-for="p in priceOptions" :key="p.value"
          :class="['filter-btn', { active: activePrice === p.value }]"
          @click="activePrice = p.value"
        >{{ p.label }}</span>
      </div>
    </div>

    <div v-loading="loading && !isInitial">
      <template v-for="cat in categories" :key="cat.id">
        <div v-if="getToolsByCategory(cat.id).length" class="category-section">
          <h2 class="category-title">
            {{ cat.name }}
            <span class="cat-count">{{ getToolsByCategory(cat.id).length }} 个</span>
          </h2>
          <div class="tools-grid">
            <div
              v-for="tool in getToolsByCategory(cat.id)"
              :key="tool.id"
              class="tool-card"
              @click="openUrl(tool.url)"
            >
              <div class="card-logo">
                <el-image :src="tool.logo_url || ''" class="logo-img" fit="contain">
                  <template #error>
                    <div class="logo-fallback">{{ tool.name.charAt(0) }}</div>
                  </template>
                </el-image>
              </div>
              <div class="card-body">
                <h3 class="tool-name">{{ tool.name }}</h3>
                <p class="tool-desc">{{ tool.description || '暂无简介' }}</p>
              </div>
              <div class="card-footer">
                <span :class="['tag-free', { paid: !tool.is_free }]">
                  {{ tool.is_free ? '免费' : '付费' }}
                </span>
                <span class="tool-rating">★ {{ tool.rating }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
      <el-empty v-if="!loading && !hasTools" description="暂无工具" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getCategories, getTools } from '../../api/aiTools'

const regionOptions = [
  { label: '全部', value: '' },
  { label: '国内', value: 'domestic' },
  { label: '国外', value: 'international' },
]
const priceOptions = [
  { label: '全部', value: '' },
  { label: '免费', value: '1' },
  { label: '付费', value: '0' },
]

const categories = ref([])
const tools = ref([])
const loading = ref(false)
const isInitial = ref(true)
const activeRegion = ref('')
const activePrice = ref('')

const filteredTools = computed(() => {
  return tools.value.filter(t => {
    if (activeRegion.value && t.region !== activeRegion.value) return false
    if (activePrice.value !== '' && t.is_free !== Number(activePrice.value)) return false
    return true
  })
})

const hasTools = computed(() => filteredTools.value.length > 0)

function getToolsByCategory(categoryId) {
  return filteredTools.value.filter(t => t.category_id === categoryId)
}

function openUrl(url) { window.open(url, '_blank') }

onMounted(async () => {
  loading.value = true
  try {
    const [catRes, toolsRes] = await Promise.all([getCategories(), getTools({ page_size: 200 })])
    categories.value = catRes.data || []
    tools.value = toolsRes.data?.items || []
  } catch (e) { console.error(e) }
  finally { loading.value = false; isInitial.value = false }
})
</script>

<style scoped>
.page-title {
  font-family: var(--font-display);
  font-size: 40px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}
.page-desc { color: var(--text-secondary); margin-bottom: 32px; font-size: 17px; }

/* Filter bar */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 40px;
  padding: 8px;
  background: var(--bg-card);
  border-radius: var(--radius-pill);
  box-shadow: 0 2px 12px var(--shadow-sm);
  display: inline-flex;
}
.region-tabs, .price-tabs { display: flex; gap: 4px; padding: 0 8px; }
.filter-divider { width: 1px; height: 20px; background: var(--border-subtle); }
.filter-btn {
  padding: 6px 18px;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}
.filter-btn:hover { color: var(--text-primary); }
.filter-btn.active { background: var(--accent); color: #ffffff; }

/* Category */
.category-section { margin-bottom: 56px; }
.category-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  letter-spacing: -0.02em;
}
.cat-count { font-size: 13px; color: var(--text-tertiary); font-weight: 400; }

/* Tool cards */
.tools-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.tool-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 24px 16px 16px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.tool-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px var(--shadow-lg);
}

.card-logo { width: 48px; height: 48px; margin-bottom: 12px; border-radius: 12px; overflow: hidden; background: var(--bg-secondary); display: flex; align-items: center; justify-content: center; }
.logo-img { width: 48px; height: 48px; }
.logo-fallback {
  width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, rgba(0,113,227,0.12), rgba(52,199,89,0.12));
  color: var(--accent); font-size: 20px; font-weight: 600; border-radius: 12px;
}
.card-body { flex: 1; min-width: 0; width: 100%; }
.tool-name { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.01em; }
.tool-desc { font-size: 12px; color: var(--text-secondary); line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 10px; }
.card-footer { display: flex; align-items: center; justify-content: space-between; width: 100%; margin-top: auto; }
.tag-free { font-size: 11px; padding: 2px 8px; border-radius: 10px; background: rgba(52,199,89,0.1); color: var(--green); font-weight: 500; }
.tag-free.paid { background: rgba(255,149,0,0.1); color: var(--amber); }
.tool-rating { font-size: 12px; color: var(--amber); font-weight: 600; }

@media (max-width: 1100px) {
  .tools-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .page-title {
    font-size: 32px;
  }

  .page-desc {
    font-size: 15px;
    margin-bottom: 22px;
  }

  .filter-bar {
    display: flex;
    width: 100%;
    align-items: stretch;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 32px;
    border-radius: 18px;
  }

  .region-tabs,
  .price-tabs {
    padding: 0;
    overflow-x: auto;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }

  .region-tabs::-webkit-scrollbar,
  .price-tabs::-webkit-scrollbar {
    display: none;
  }

  .filter-divider {
    display: none;
  }

  .filter-btn {
    flex: 0 0 auto;
    padding: 7px 14px;
  }

  .category-section {
    margin-bottom: 42px;
  }

  .category-title {
    font-size: 18px;
    margin-bottom: 14px;
  }

  .tools-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .tool-card {
    padding: 18px 12px 14px;
    border-radius: 16px;
  }

  .tool-card:hover {
    transform: none;
  }

  .card-footer {
    gap: 8px;
  }
}

@media (max-width: 420px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style>
