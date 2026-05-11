<template>
  <div class="work-detail" v-loading="loading">
    <el-empty v-if="!loading && !work" description="作品不存在" />
    <div v-else-if="work" class="detail-content">
      <div class="main-area">
        <el-image :src="work.cover_url || ''" fit="cover" class="cover-image">
          <template #error><div class="placeholder">◆</div></template>
        </el-image>
        <h1 class="title">{{ work.title }}</h1>
        <div class="tags">
          <span class="tag" v-if="work.major_name">{{ work.major_name }}</span>
          <span class="tag">{{ work.academic_year }} {{ work.semester === 1 ? '上学期' : '下学期' }}</span>
          <span class="tag tag-award" v-if="work.award">{{ work.award }}</span>
        </div>
        <div class="content" v-if="work.content">
          <div v-html="renderedContent"></div>
        </div>
        <div v-else class="no-content">暂无简介</div>
      </div>
      <div class="side-area">
        <div class="side-card">
          <h3 class="side-title">参赛信息</h3>
          <p><span class="label">参赛学生：</span>{{ work.author_names }}</p>
          <p v-if="work.guide_teacher"><span class="label">指导教师：</span>{{ work.guide_teacher }}</p>
          <p v-if="work.contest_name"><span class="label">赛事名称：</span>{{ work.contest_name }}</p>
        </div>
        <div class="side-actions" v-if="work.demo_url || work.attachment_url">
          <el-button type="primary" v-if="work.demo_url" @click="openUrl(work.demo_url)" style="width:100%;margin-bottom:8px">查看演示</el-button>
          <el-button v-if="work.attachment_url" @click="openUrl(work.attachment_url)" style="width:100%">下载附件</el-button>
        </div>
        <div class="side-card">
          <h3 class="side-title">发布信息</h3>
          <p v-if="work.publisher_name"><span class="label">发布教师：</span>{{ work.publisher_name }}</p>
          <p v-if="work.published_at"><span class="label">发布时间：</span>{{ work.published_at?.slice(0, 10) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getWork } from '../../api/works'

const route = useRoute()
const work = ref(null)
const loading = ref(true)

const renderedContent = computed(() => {
  if (!work.value?.content) return ''
  return work.value.content
    .replace(/### (.+)/g, '<h3>$1</h3>')
    .replace(/## (.+)/g, '<h2>$1</h2>')
    .replace(/# (.+)/g, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/- (.+)/g, '<li>$1</li>')
    .replace(/\n/g, '<br>')
})

function openUrl(url) { window.open(url, '_blank') }

onMounted(async () => {
  try {
    const res = await getWork(route.params.id)
    work.value = res.data
  } catch (e) { console.error(e) }
  finally { loading.value = false }
})
</script>

<style scoped>
.detail-content { display: flex; gap: 40px; }
.main-area { flex: 1; min-width: 0; }
.side-area { width: 300px; flex-shrink: 0; }
.cover-image {
  width: 100%;
  max-height: 400px;
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: 24px;
}
.placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  color: var(--text-tertiary);
  font-size: 48px;
}
.title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  letter-spacing: -0.03em;
  line-height: 1.2;
}
.tags { display: flex; gap: 8px; margin-bottom: 28px; flex-wrap: wrap; }
.tag {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 12px;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-weight: 500;
}
.tag-award { background: rgba(255, 149, 0, 0.08); color: var(--amber); }
.content { line-height: 1.8; color: var(--text-secondary); font-size: 15px; }
.content :deep(h2) { color: var(--text-primary); margin: 28px 0 14px; font-size: 22px; font-weight: 600; letter-spacing: -0.02em; }
.content :deep(h3) { color: var(--text-primary); margin: 22px 0 10px; font-size: 18px; font-weight: 600; }
.content :deep(strong) { color: var(--text-primary); }
.no-content { color: var(--text-tertiary); text-align: center; padding: 60px; font-size: 15px; }

/* Side cards */
.side-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.side-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 14px;
  letter-spacing: 0.04em;
}
.side-card p { font-size: 14px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5; }
.label { color: var(--text-tertiary); }
.side-actions { margin-bottom: 16px; }
</style>
