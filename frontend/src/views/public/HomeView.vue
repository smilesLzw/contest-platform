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
    <section v-if="stats" ref="statsRef" class="stats-band">
      <div class="stat-item">
        <strong>{{ stats.works_count }}</strong>
        <span>作品总数</span>
      </div>
      <div class="stat-item">
        <strong>{{ stats.news_count }}</strong>
        <span>新闻资讯</span>
      </div>
      <div class="stat-item">
        <strong>{{ stats.tools_count }}</strong>
        <span>AI 工具</span>
      </div>
    </section>

    <!-- Featured Works -->
    <section ref="showcaseRef" class="section works-section reveal">
      <div class="section-head">
        <div>
          <span class="section-kicker">Student Works</span>
          <h2 class="section-title">推荐学生作品</h2>
        </div>
        <button class="link-button" @click="$router.push('/works')">查看全部作品</button>
      </div>

      <div v-if="visibleWorks.length" class="works-shelf" :class="{ 'is-single': visibleWorks.length === 1 }">
        <article
          v-for="w in visibleWorks"
          :key="w.id"
          class="work-tile"
          @click="$router.push(`/works/${w.id}`)"
        >
          <div class="work-cover">
            <el-image :src="coverFor(w, 'card')" fit="cover" style="width:100%;height:100%">
              <template #error>
                <div class="cover-fallback">{{ typeIcon(w.work_type) }}</div>
              </template>
            </el-image>
            <span v-if="hasAward(w)" class="award-badge">{{ w.award }}</span>
          </div>
          <div class="work-body">
            <div class="work-tags">
              <span v-if="w.major_name">{{ w.major_name }}</span>
              <span v-if="w.work_type">{{ typeLabel(w.work_type) }}</span>
            </div>
            <h3>{{ w.title }}</h3>
            <p>{{ workSummary(w) }}</p>
            <div class="work-meta">
              <span>{{ w.author_names || '学生作品' }}</span>
              <span v-if="w.academic_year">{{ w.academic_year }} 学年</span>
            </div>
          </div>
        </article>
      </div>

      <div v-else class="showcase-empty">
        <div>
          <span class="empty-mark">◆</span>
          <h3>优秀作品正在整理中</h3>
          <p>可以先进入作品展示页查看全部内容。</p>
        </div>
        <button class="btn-primary" @click="$router.push('/works')">进入作品展示</button>
      </div>
    </section>

    <!-- Quick Links -->
    <section ref="linksRef" class="section quick-section reveal">
      <div class="section-head">
        <h2 class="section-title">快速入口</h2>
      </div>
      <div class="entry-grid">
        <div class="entry-card" @click="$router.push('/works')">
          <el-icon><Collection /></el-icon>
          <span class="entry-label">作品展示</span>
          <small>浏览学生创作成果</small>
        </div>
        <div class="entry-card" @click="$router.push('/ai-tools')">
          <el-icon><MagicStick /></el-icon>
          <span class="entry-label">AI 工具</span>
          <small>查找实用创作工具</small>
        </div>
        <div class="entry-card" @click="$router.push('/news')">
          <el-icon><Reading /></el-icon>
          <span class="entry-label">资讯中心</span>
          <small>查看教学与平台动态</small>
        </div>
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

  </div>
</template>

<script setup>
import { computed, nextTick, ref, onMounted, onBeforeUnmount } from 'vue'
import { Collection, MagicStick, Reading } from '@element-plus/icons-vue'
import { getStats } from '../../api/common'
import { getWorks } from '../../api/works'
import { getNewsList } from '../../api/news'

const stats = ref(null)
const latestWorks = ref([])
const latestNews = ref([])
const statsRef = ref(null)
const showcaseRef = ref(null)
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
  const statsEl = statsRef.value || showcaseRef.value
  if (statsEl) {
    statsEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function formatTime(t) {
  if (!t) return ''
  return t.slice(0, 10)
}

const recommendedWorks = computed(() => {
  return [...latestWorks.value].sort((a, b) => {
    const awardWeight = Number(hasAward(b)) - Number(hasAward(a))
    if (awardWeight !== 0) return awardWeight
    return new Date(b.published_at || b.created_at || 0) - new Date(a.published_at || a.created_at || 0)
  })
})

const visibleWorks = computed(() => recommendedWorks.value.slice(0, 6))

const typeMap = {
  music: { label: '音乐作品', icon: '♪' },
  graphic: { label: '平面作品', icon: '◆' },
  video: { label: '视频作品', icon: '▶' },
  website: { label: '网站作品', icon: '◇' },
}

function typeLabel(type) {
  return typeMap[type]?.label || '学生作品'
}

function typeIcon(type) {
  return typeMap[type]?.icon || '◆'
}

function hasAward(work) {
  const award = String(work?.award || '').trim()
  return Boolean(award && !['暂无', '无', '无奖', '未获奖'].includes(award))
}

function coverFor(work, variant = 'card') {
  if (!work) return ''
  if (variant === 'detail') {
    return work.cover_detail_url || work.cover_card_url || work.cover_url || ''
  }
  if (variant === 'thumb') {
    return work.cover_thumb_url || work.cover_card_url || work.cover_url || ''
  }
  return work.cover_card_url || work.cover_url || ''
}

function workSummary(work) {
  if (work.content) return getSummary(work.content)
  const parts = [work.contest_name, work.guide_teacher ? `指导教师：${work.guide_teacher}` : '', work.major_name]
  return parts.filter(Boolean).join(' / ') || '从课堂实践到竞赛创作，这里展示学生的阶段性成果。'
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

  await nextTick()

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
  const refs = [showcaseRef.value, linksRef.value, newsRef.value]
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
  background: var(--bg-secondary) url('../../assets/images/hero-banner.png') center/cover no-repeat;
  margin-bottom: 0;
}
.hero-title {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0;
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
  letter-spacing: 0;
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
  letter-spacing: 0;
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

/* ── Section ── */
.section { max-width: 1200px; margin: 0 auto 56px; padding: 0 24px; }
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 20px;
  margin-bottom: 22px;
}
.section-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0;
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

/* ── Stats ── */
.stats-band {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  max-width: 760px;
  margin: 40px auto 56px;
  border: 1px solid rgba(210, 210, 215, 0.72);
  border-radius: 26px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(18px);
}
.stat-item {
  min-width: 0;
  padding: 20px 18px;
  text-align: center;
}
.stat-item + .stat-item {
  border-left: 1px solid rgba(210, 210, 215, 0.72);
}
.stat-item strong {
  display: block;
  font-family: var(--font-display);
  font-size: 30px;
  line-height: 1.1;
  color: var(--text-primary);
}
.stat-item span {
  display: block;
  margin-top: 5px;
  color: var(--text-tertiary);
  font-size: 13px;
}

/* ── Featured works ── */
.works-section { margin-bottom: 48px; }
.section-kicker {
  display: block;
  margin-bottom: 4px;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0;
}
.link-button {
  border: 1px solid var(--border-subtle);
  background: var(--bg-card);
  color: var(--accent);
  border-radius: var(--radius-pill);
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}
.link-button:hover {
  border-color: var(--accent);
  background: rgba(0, 113, 227, 0.04);
}
.works-shelf {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
}
.works-shelf.is-single {
  grid-template-columns: minmax(280px, 390px);
  justify-content: center;
}
.work-tile {
  background: var(--bg-card);
  border: 1px solid rgba(210, 210, 215, 0.62);
  border-radius: 24px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 12px 34px rgba(0, 0, 0, 0.05);
  transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
}
.work-tile:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 113, 227, 0.32);
  box-shadow: 0 18px 46px rgba(0, 0, 0, 0.09);
}
.work-cover {
  position: relative;
  aspect-ratio: 16 / 10;
  background: var(--bg-secondary);
}
.cover-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44px;
  color: var(--text-tertiary);
}
.award-badge {
  position: absolute;
  left: 16px;
  top: 16px;
  max-width: calc(100% - 32px);
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  background: rgba(255, 149, 0, 0.92);
  color: #ffffff;
  font-size: 12px;
  font-weight: 600;
}
.work-body {
  display: flex;
  flex-direction: column;
  min-height: 210px;
  padding: 22px;
}
.work-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}
.work-tags span {
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  background: rgba(0, 113, 227, 0.08);
  color: var(--accent);
  font-size: 12px;
  font-weight: 600;
}
.work-body h3 {
  font-size: 21px;
  line-height: 1.3;
  color: var(--text-primary);
  margin-bottom: 10px;
  letter-spacing: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.work-body p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.65;
  margin-bottom: 18px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.work-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  margin-top: auto;
  color: var(--text-tertiary);
  font-size: 13px;
}
.showcase-empty {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 40px;
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
}
.empty-mark {
  display: inline-flex;
  margin-bottom: 12px;
  color: var(--accent);
  font-size: 24px;
}
.showcase-empty h3 {
  font-size: 22px;
  margin-bottom: 6px;
  letter-spacing: 0;
}
.showcase-empty p {
  color: var(--text-secondary);
  font-size: 14px;
}

/* ── Quick links ── */
.quick-section { margin-bottom: 52px; }
.entry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.entry-card {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  grid-template-rows: auto auto;
  align-items: center;
  column-gap: 14px;
  min-height: 92px;
  background: var(--bg-card);
  border: 1px solid rgba(210, 210, 215, 0.62);
  border-radius: 22px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.28s ease;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.045);
}
.entry-card:hover {
  transform: translateY(-3px);
  border-color: rgba(0, 113, 227, 0.34);
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.08);
}
.entry-card .el-icon {
  grid-row: 1 / 3;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(0, 113, 227, 0.08);
  color: var(--accent);
  font-size: 21px;
}
.entry-label {
  min-width: 0;
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0;
}
.entry-card small {
  min-width: 0;
  color: var(--text-secondary);
  font-size: 13px;
}

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
  letter-spacing: 0;
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

@media (max-width: 1100px) {
  .works-shelf {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .hero {
    padding: 88px 18px 104px;
  }
  .hero-title {
    font-size: 34px;
  }
  .hero-sub {
    font-size: 16px;
  }
  .stats-band {
    grid-template-columns: 1fr;
    margin: 28px 16px 42px;
    border-radius: 20px;
  }
  .stat-item + .stat-item {
    border-left: none;
    border-top: 1px solid rgba(210, 210, 215, 0.72);
  }
  .section {
    max-width: none;
    margin-bottom: 44px;
    padding: 0 16px;
  }
  .section-head,
  .showcase-empty {
    align-items: stretch;
    flex-direction: column;
  }
  .works-shelf,
  .works-shelf.is-single,
  .news-grid,
  .entry-grid {
    grid-template-columns: 1fr;
  }
  .work-body {
    min-height: auto;
  }
  .entry-card {
    min-height: 84px;
  }
}
</style>
