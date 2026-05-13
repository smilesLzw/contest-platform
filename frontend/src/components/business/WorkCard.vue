<template>
  <div class="work-card" @click="$router.push(`/works/${work.id}`)">
    <div class="cover">
      <el-image :src="work.cover_card_url || work.cover_url || ''" fit="cover" style="width:100%;height:100%">
        <template #error>
          <div class="cover-fallback">{{ typeIcon }}</div>
        </template>
      </el-image>
      <span class="type-badge" v-if="work.work_type">{{ typeLabel }}</span>
    </div>
    <div class="info">
      <div class="tags">
        <span class="tag-major" v-if="work.major_name">{{ work.major_name }}</span>
        <span class="tag-award" v-if="work.award">{{ work.award }}</span>
      </div>
      <h3 class="title" :title="work.title">{{ work.title }}</h3>
      <p class="authors" v-if="work.author_names">{{ work.author_names }}</p>
      <p class="year" v-if="work.academic_year">{{ work.academic_year }} 学年</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ work: { type: Object, required: true } })

const typeMap = {
  music: { label: '音乐', icon: '♪' },
  graphic: { label: '制图', icon: '◆' },
  video: { label: '视频', icon: '▶' },
  website: { label: '网站', icon: '◇' },
}

const typeLabel = computed(() => typeMap[props.work.work_type]?.label || '')
const typeIcon = computed(() => typeMap[props.work.work_type]?.icon || '◆')
</script>

<style scoped>
.work-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.work-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px var(--shadow-lg);
}
.cover {
  height: 180px;
  overflow: hidden;
  background: var(--bg-secondary);
  position: relative;
}
.type-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 12px;
  background: rgba(0,0,0,0.5);
  color: #fff;
  font-weight: 500;
  letter-spacing: 0.02em;
}
.cover-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: var(--text-tertiary);
}
.info { padding: 16px; }
.tags { display: flex; gap: 6px; margin-bottom: 8px; flex-wrap: wrap; }
.tag-major {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 12px;
  background: rgba(0, 113, 227, 0.08);
  color: var(--accent);
  letter-spacing: 0.02em;
  font-weight: 500;
}
.tag-award {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 12px;
  background: rgba(255, 149, 0, 0.08);
  color: var(--amber);
  font-weight: 500;
}
.title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}
.authors { font-size: 13px; color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.year { font-size: 12px; color: var(--text-tertiary); margin-top: 2px; }
</style>
