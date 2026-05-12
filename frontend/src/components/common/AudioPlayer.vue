<template>
  <div class="audio-player">
    <div class="ap-cover" v-if="coverUrl">
      <img :src="coverUrl" alt="" />
    </div>
    <div class="ap-body">
      <div class="ap-title" v-if="title">{{ title }}</div>
      <div class="ap-artist" v-if="artist">{{ artist }}</div>
      <audio ref="audioEl" :src="src" preload="metadata" @timeupdate="onTimeUpdate" @loadedmetadata="onLoaded" @ended="$emit('ended')"></audio>
      <div class="ap-controls">
        <button class="ap-btn" @click="togglePlay" :title="playing ? '暂停' : '播放'">
          <span v-if="!playing">&#9654;</span>
          <span v-else>&#9646;&#9646;</span>
        </button>
        <div class="ap-progress" @click="seek">
          <div class="ap-track">
            <div class="ap-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <span class="ap-time">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
        </div>
        <div class="ap-volume">
          <span class="ap-vol-icon">&#9834;</span>
          <input type="range" min="0" max="100" :value="volume" @input="setVolume" class="ap-vol-slider" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  title: { type: String, default: '' },
  artist: { type: String, default: '' },
  coverUrl: { type: String, default: '' },
  autoplay: { type: Boolean, default: false },
})

defineEmits(['ended'])

const audioEl = ref(null)
const playing = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(80)

function togglePlay() {
  const a = audioEl.value
  if (!a) return
  if (a.paused) {
    a.play().catch(() => {})
    playing.value = true
  } else {
    a.pause()
    playing.value = false
  }
}

function onTimeUpdate() {
  if (audioEl.value) currentTime.value = audioEl.value.currentTime
}

function onLoaded() {
  if (audioEl.value) {
    duration.value = audioEl.value.duration
    audioEl.value.volume = volume.value / 100
    if (props.autoplay) {
      audioEl.value.play().catch(() => {})
      playing.value = true
    }
  }
}

function seek(e) {
  if (!audioEl.value || !duration.value) return
  const rect = e.currentTarget.querySelector('.ap-track').getBoundingClientRect()
  const ratio = (e.clientX - rect.left) / rect.width
  audioEl.value.currentTime = ratio * duration.value
}

function setVolume(e) {
  volume.value = Number(e.target.value)
  if (audioEl.value) audioEl.value.volume = volume.value / 100
}

function formatTime(s) {
  if (!s || !isFinite(s)) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${sec.toString().padStart(2, '0')}`
}

watch(() => props.src, () => {
  playing.value = false
  currentTime.value = 0
  duration.value = 0
})

onBeforeUnmount(() => {
  if (audioEl.value) {
    audioEl.value.pause()
    audioEl.value.src = ''
  }
})
</script>

<style scoped>
.audio-player {
  display: flex;
  gap: 16px;
  align-items: center;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.ap-cover {
  width: 72px;
  height: 72px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-secondary);
}
.ap-cover img { width: 100%; height: 100%; object-fit: cover; }
.ap-body { flex: 1; min-width: 0; }
.ap-title { font-size: 15px; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ap-artist { font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; }
.ap-controls { display: flex; align-items: center; gap: 12px; }
.ap-btn {
  width: 36px; height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--accent);
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.2s;
}
.ap-btn:hover { background: var(--accent-hover); }
.ap-progress { flex: 1; display: flex; align-items: center; gap: 10px; }
.ap-track {
  flex: 1; height: 4px; background: var(--bg-secondary);
  border-radius: 2px; cursor: pointer; position: relative;
}
.ap-fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.1s linear; }
.ap-time { font-size: 11px; color: var(--text-tertiary); white-space: nowrap; font-variant-numeric: tabular-nums; }
.ap-volume { display: flex; align-items: center; gap: 6px; }
.ap-vol-icon { font-size: 16px; color: var(--text-tertiary); }
.ap-vol-slider { width: 60px; accent-color: var(--accent); }
</style>
