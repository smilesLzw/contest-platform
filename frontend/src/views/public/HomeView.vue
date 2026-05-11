<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <h1 class="hero-title">
        <span class="hero-line">院赛作品展示</span>
        <span class="hero-line hero-line-alt">AI 工具导航平台</span>
      </h1>
      <p class="hero-sub">汇聚优秀学生作品，探索前沿 AI 工具，让创意与技术在这里交汇</p>
      <div class="hero-actions">
        <button class="btn-primary" @click="$router.push('/works')">浏览作品</button>
        <button class="btn-secondary" @click="$router.push('/ai-tools')">探索 AI 工具</button>
      </div>
      <div class="scroll-indicator" @click="scrollToContent">
        <span class="scroll-arrow"></span>
      </div>
    </section>

    <!-- Stats -->
    <section v-if="stats" ref="statsRef" class="stats reveal">
      <div class="stat-item">
        <span class="stat-num">{{ stats.works_count }}</span>
        <span class="stat-label">作品总数</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-num">{{ stats.news_count }}</span>
        <span class="stat-label">新闻资讯</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-num">{{ stats.tools_count }}</span>
        <span class="stat-label">AI 工具</span>
      </div>
    </section>

    <!-- Latest Works -->
    <section v-if="latestWorks.length" ref="worksRef" class="section reveal">
      <div class="section-head">
        <h2 class="section-title">最新作品</h2>
        <a class="section-more" @click="$router.push('/works')">查看全部 &rarr;</a>
      </div>
      <div class="works-grid">
        <WorkCard v-for="w in latestWorks" :key="w.id" :work="w" />
      </div>
    </section>

    <!-- Latest News -->
    <section v-if="latestNews.length" ref="newsRef" class="section reveal">
      <div class="section-head">
        <h2 class="section-title">最新资讯</h2>
        <a class="section-more" @click="$router.push('/news')">查看全部 &rarr;</a>
      </div>
      <div class="news-grid">
        <div v-for="n in latestNews" :key="n.id" class="news-card" @click="$router.push(`/news/${n.id}`)">
          <div class="news-cover">
            <img v-if="n.cover_url" :src="n.cover_url" alt="" />
            <el-icon v-else :size="28" color="var(--text-tertiary)"><Reading /></el-icon>
          </div>
          <div class="news-body">
            <span class="news-cat">{{ catLabel(n.category) }}</span>
            <h3>{{ n.title }}</h3>
            <p class="news-summary">{{ getSummary(n.content) }}</p>
            <span class="news-time">{{ formatTime(n.published_at) }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Links -->
    <section ref="linksRef" class="section reveal">
      <div class="section-head">
        <h2 class="section-title">快速入口</h2>
      </div>
      <div class="entry-grid">
        <div class="entry-card" @click="$router.push('/works')">
          <span class="entry-icon">◆</span>
          <span class="entry-label">作品展示</span>
        </div>
        <div class="entry-card" @click="$router.push('/ai-tools')">
          <span class="entry-icon">◈</span>
          <span class="entry-label">AI 工具</span>
        </div>
        <div class="entry-card" @click="$router.push('/news')">
          <span class="entry-icon">◇</span>
          <span class="entry-label">资讯中心</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Reading } from '@element-plus/icons-vue'
import { getStats } from '../../api/common'
import { getWorks } from '../../api/works'
import { getNewsList } from '../../api/news'
import WorkCard from '../../components/business/WorkCard.vue'

const stats = ref(null)
const latestWorks = ref([])
const latestNews = ref([])
const statsRef = ref(null)
const worksRef = ref(null)
const newsRef = ref(null)
const linksRef = ref(null)

let observer = null

function catLabel(c) {
  return { tutorial: '教程指南', tech: '科技前沿', lab: '教研室动态' }[c] || c
}

function getSummary(content) {
  if (!content) return ''
  return content.replace(/[#*`\n]/g, '').slice(0, 80) + (content.length > 80 ? '…' : '')
}

function scrollToContent() {
  const statsEl = statsRef.value
  if (statsEl) {
    statsEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

function formatTime(t) {
  if (!t) return ''
  return t.slice(0, 10)
}

onMounted(async () => {
  try {
    const [statsRes, worksRes, newsRes] = await Promise.all([
      getStats(),
      getWorks({ page: 1, page_size: 6 }),
      getNewsList({ page: 1, page_size: 3 }),
    ])
    stats.value = statsRes.data
    latestWorks.value = worksRes.data.items
    latestNews.value = newsRes.data.items
  } catch (e) {
    console.error(e)
  }

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
        }
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  )
  const refs = [statsRef.value, worksRef.value, newsRef.value, linksRef.value]
  refs.forEach((el) => { if (el) observer.observe(el) })
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})
</script>

<style scoped>
/* ── Hero ── */
.hero {
  position: relative;
  text-align: center;
  padding: 120px 20px 120px;
  background: var(--bg-secondary);
  margin-bottom: 0;
}
.hero-title {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin-bottom: 20px;
  line-height: 1.15;
}
.hero-line { display: block; }
.hero-line-alt { color: var(--accent); }
.hero-sub {
  font-size: 18px;
  color: var(--text-secondary);
  max-width: 500px;
  margin: 0 auto 40px;
  line-height: 1.6;
  font-weight: 400;
}
.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  padding: 12px 28px;
  border-radius: var(--radius-pill);
  font-size: 16px;
  font-weight: 500;
  background: var(--accent);
  color: #ffffff;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: -0.01em;
}
.btn-primary:hover { background: var(--accent-hover); transform: scale(1.02); }
.btn-secondary {
  display: inline-flex;
  align-items: center;
  padding: 12px 28px;
  border-radius: var(--radius-pill);
  font-size: 16px;
  font-weight: 500;
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: -0.01em;
}
.btn-secondary:hover { background: rgba(0,113,227,0.04); }

/* Scroll indicator */
.scroll-indicator {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  animation: float 2s ease-in-out infinite;
}
.scroll-arrow {
  display: block;
  width: 20px;
  height: 20px;
  border-right: 2px solid var(--text-tertiary);
  border-bottom: 2px solid var(--text-tertiary);
  transform: rotate(45deg);
  transition: border-color 0.3s;
}
.scroll-indicator:hover .scroll-arrow {
  border-color: var(--text-secondary);
}
@keyframes float {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* ── Stats ── */
.stats {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 600px;
  margin: -60px auto 80px;
  padding: 28px 40px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 20px var(--shadow-sm);
  position: relative;
  z-index: 2;
}
.stat-item { flex: 1; text-align: center; }
.stat-num {
  display: block;
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}
.stat-label {
  display: block;
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
  letter-spacing: 0.04em;
}
.stat-divider {
  width: 1px;
  height: 36px;
  background: var(--border-subtle);
}

/* ── Section ── */
.section { max-width: 1200px; margin: 0 auto 80px; padding: 0 24px; }
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 24px;
}
.section-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}
.section-more {
  font-size: 14px;
  color: var(--accent);
  cursor: pointer;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}
.section-more:hover { color: var(--accent-hover); }

/* ── News cards ── */
.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
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
.news-cover {
  height: 120px;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.news-cover img { width: 100%; height: 100%; object-fit: cover; }
.news-body { padding: 16px; }
.news-cat {
  font-size: 11px;
  color: var(--accent);
  letter-spacing: 0.04em;
  font-weight: 500;
}
.news-body h3 {
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
.news-summary {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 10px;
}
.news-time { font-size: 12px; color: var(--text-tertiary); }

/* ── Works grid ── */
.works-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* ── Quick links ── */
.entry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.entry-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.entry-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px var(--shadow-lg);
}
.entry-icon {
  display: block;
  font-size: 28px;
  color: var(--accent);
  margin-bottom: 10px;
}
.entry-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

/* ── Scroll reveal ── */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.7s cubic-bezier(0.25, 0.1, 0.25, 1), transform 0.7s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
