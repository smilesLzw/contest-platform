<template>
  <div class="news-detail" v-loading="loading">
    <el-empty v-if="!loading && !news" description="新闻不存在" />
    <div v-else-if="news" class="news-layout">
      <aside class="toc-sidebar" v-if="tocHeadings.length > 0">
        <nav class="toc-nav">
          <h4 class="toc-title">目录</h4>
          <ul class="toc-list">
            <li
              v-for="h in tocHeadings"
              :key="h.id"
              :class="['toc-item', `toc-lv${h.level}`, { active: activeId === h.id }]"
            >
              <a :href="`#${h.id}`" @click.prevent="scrollToHeading(h.id)">{{ h.text }}</a>
            </li>
          </ul>
        </nav>
      </aside>
      <article class="news-main">
        <span class="news-cat">{{ categoryLabel }}</span>
        <h1 class="title">{{ news.title }}</h1>
        <div class="meta">
          <span>{{ news.author_name }}</span>
          <span>&middot;</span>
          <span>{{ formatTime(news.published_at) }}</span>
        </div>
        <div class="content" ref="contentRef">
          <MdPreview
            :modelValue="news.content || ''"
            :mdHeadingId="mdHeadingId"
            language="zh-CN"
            editorId="news-detail"
            previewTheme="github"
          />
        </div>
        <div class="actions">
          <el-button @click="copyLink">复制链接</el-button>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import { getNews } from '../../api/news'
import { ElMessage } from 'element-plus'

const route = useRoute()
const news = ref(null)
const loading = ref(true)
const contentRef = ref(null)
const activeId = ref('')

const categoryLabel = computed(() => {
  const map = { tutorial: '教程指南', tech: '科技前沿', lab: '教研室动态' }
  return map[news.value?.category] || news.value?.category
})

function mdHeadingId(text, level, index) { return `h-${index}` }

const tocHeadings = computed(() => {
  if (!news.value?.content) return []
  const lines = news.value.content.split('\n')
  const result = []
  let inCodeBlock = false
  let idx = 1
  for (const line of lines) {
    if (line.startsWith('```')) { inCodeBlock = !inCodeBlock; continue }
    if (inCodeBlock) continue
    let m = line.match(/^### (.+)/)
    if (m) { result.push({ level: 3, text: m[1].trim(), id: `h-${idx++}` }); continue }
    m = line.match(/^## (.+)/)
    if (m) { result.push({ level: 2, text: m[1].trim(), id: `h-${idx++}` }); continue }
    m = line.match(/^# (.+)/)
    if (m) { result.push({ level: 1, text: m[1].trim(), id: `h-${idx++}` }) }
  }
  return result
})

function scrollToHeading(id) {
  const el = document.getElementById(id)
  if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); activeId.value = id }
}

let scrollTimer = null
function onScroll() {
  if (scrollTimer) return
  scrollTimer = setTimeout(() => { scrollTimer = null; updateActiveHeading() }, 100)
}

function updateActiveHeading() {
  if (!contentRef.value) return
  const els = contentRef.value.querySelectorAll('h1[id], h2[id], h3[id]')
  if (!els.length) return
  let current = els[0].id
  for (const el of els) { if (el.getBoundingClientRect().top <= 100) current = el.id }
  activeId.value = current
}

function formatTime(t) { return t ? t.slice(0, 10) : '' }

function copyLink() {
  navigator.clipboard.writeText(window.location.href)
  ElMessage.success('链接已复制')
}

onMounted(async () => {
  window.addEventListener('scroll', onScroll, { passive: true })
  try {
    const res = await getNews(route.params.id)
    news.value = res.data
  } catch (e) { console.error(e) }
  finally { loading.value = false }
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  if (scrollTimer) clearTimeout(scrollTimer)
})
</script>

<style>
/* Global styles for MdPreview images */
.news-detail .content img {
  display: block !important;
  max-width: 100%;
  max-height: 400px;
  margin: 16px auto !important;
  border-radius: 12px;
}
.news-detail .content figure {
  display: flex !important;
  flex-direction: column;
  align-items: center;
  margin: 16px auto !important;
}
</style>

<style scoped>
.news-detail { max-width: 1200px; margin: 0 auto; }

.news-layout { display: flex; gap: 40px; align-items: flex-start; }

/* TOC */
.toc-sidebar { width: 200px; flex-shrink: 0; position: sticky; top: 80px; max-height: calc(100vh - 120px); overflow-y: auto; }
.toc-nav { padding-right: 12px; border-right: 1px solid var(--border-subtle); }
.toc-title { font-size: 13px; font-weight: 600; color: var(--text-primary); margin: 0 0 12px 0; letter-spacing: 0.02em; }
.toc-list { list-style: none; margin: 0; padding: 0; }
.toc-item { line-height: 1.6; }
.toc-item a {
  display: block;
  padding: 3px 8px;
  font-size: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
}
.toc-item a:hover { color: var(--text-primary); background: var(--bg-secondary); }
.toc-item.active a { color: var(--accent); font-weight: 500; background: rgba(0,113,227,0.06); }
.toc-lv1 a { font-weight: 600; color: var(--text-primary); font-size: 13px; }
.toc-lv2 a { padding-left: 18px; }
.toc-lv3 a { padding-left: 28px; font-size: 11px; color: var(--text-tertiary); }

/* Main content */
.news-main { flex: 1; min-width: 0; }
.news-cat {
  display: inline-block;
  font-size: 12px;
  color: var(--accent);
  letter-spacing: 0.04em;
  font-weight: 500;
  margin-bottom: 8px;
}
.title {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  letter-spacing: -0.03em;
  line-height: 1.2;
}
.meta { display: flex; align-items: center; gap: 8px; color: var(--text-tertiary); font-size: 14px; margin-bottom: 36px; }

.content {
  line-height: 1.8;
  color: var(--text-secondary);
  font-size: 16px;
  max-width: 750px;
  overflow-x: auto;
}

/* MdPreview dark overrides — light theme adjustments */
.content :deep(h1) { color: var(--text-primary); font-size: 28px; font-weight: 600; margin: 36px 0 18px; letter-spacing: -0.02em; }
.content :deep(h2) { color: var(--text-primary); border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px; margin-top: 36px; font-size: 22px; font-weight: 600; letter-spacing: -0.02em; }
.content :deep(h3) { color: var(--text-primary); margin-top: 28px; font-size: 18px; font-weight: 600; }
.content :deep(p) { color: var(--text-secondary); }
.content :deep(strong) { color: var(--text-primary); }
.content :deep(a) { color: var(--link); }
.content :deep(blockquote) { border-left: 3px solid var(--accent); padding-left: 18px; color: var(--text-secondary); margin: 20px 0; font-style: italic; }
.content :deep(pre) { background: var(--bg-secondary); padding: 16px; border-radius: 12px; overflow-x: auto; border: 1px solid var(--border-subtle); }
.content :deep(code) { font-family: 'SF Mono', 'JetBrains Mono', 'Fira Code', monospace; font-size: 13px; color: var(--text-primary); }
.content :deep(table) { border-collapse: collapse; width: 100%; margin: 20px 0; }
.content :deep(th) { background: var(--bg-secondary); font-weight: 600; color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px 14px; text-align: left; font-size: 14px; }
.content :deep(td) { border: 1px solid var(--border-subtle); padding: 10px 14px; color: var(--text-secondary); font-size: 14px; }
.content :deep(ul), .content :deep(ol) { color: var(--text-secondary); }
.content :deep(hr) { border-color: var(--border-subtle); margin: 28px 0; }

.actions { max-width: 750px; margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border-subtle); }

@media (max-width: 768px) {
  .toc-sidebar { display: none; }
  .content { max-width: 100%; }
  .actions { max-width: 100%; }
}
</style>
