<template>
  <div class="audio-player">
    <div class="ap-cover" v-if="coverUrl">
      <img :src="coverUrl" alt="" />
    </div>
    <div class="ap-body">
      <div class="ap-title" v-if="title">{{ title }}</div>
      <div class="ap-artist" v-if="artist">{{ artist }}</div>
      <audio
        ref="audioEl"
        :src="src"
        preload="metadata"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoaded"
        @play="playing = true"
        @pause="playing = false"
        @ended="onEnded"
      ></audio>
      <div class="ap-controls">
        <button class="ap-btn" @click="togglePlay" :title="playing ? '暂停' : '播放'">
          <span v-if="!playing">&#9654;</span>
          <span v-else>&#9646;&#9646;</span>
        </button>
        <div class="ap-progress">
          <div
            ref="trackEl"
            class="ap-track"
            :class="{ dragging: seeking }"
            @click="seek"
            @pointerdown="startSeek"
          >
            <div class="ap-fill" :style="{ width: progress + '%' }"></div>
            <div class="ap-thumb" :style="{ left: progress + '%' }"></div>
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
import { computed, ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  title: { type: String, default: '' },
  artist: { type: String, default: '' },
  coverUrl: { type: String, default: '' },
  autoplay: { type: Boolean, default: false },
})

const emit = defineEmits(['ended'])

const audioEl = ref(null)
const trackEl = ref(null)
const playing = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(80)
const seeking = ref(false)
let wasPlayingBeforeSeek = false

const progress = computed(() => {
  if (!duration.value || !isFinite(duration.value)) return 0
  return Math.min(100, Math.max(0, (currentTime.value / duration.value) * 100))
})

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
  if (audioEl.value && !seeking.value) currentTime.value = audioEl.value.currentTime
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
  updateSeekPosition(e)
}

function startSeek(e) {
  if (!audioEl.value || !duration.value) return
  e.preventDefault()
  seeking.value = true
  wasPlayingBeforeSeek = !audioEl.value.paused
  updateSeekPosition(e)
  window.addEventListener('pointermove', updateSeekPosition)
  window.addEventListener('pointerup', stopSeek, { once: true })
  window.addEventListener('pointercancel', stopSeek, { once: true })
}

function updateSeekPosition(e) {
  if (!audioEl.value || !duration.value) return
  const track = e.currentTarget?.classList?.contains('ap-track')
    ? e.currentTarget
    : trackEl.value
  if (!track) return
  const rect = track.getBoundingClientRect()
  const ratio = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width))
  const nextTime = ratio * duration.value
  currentTime.value = nextTime
  audioEl.value.currentTime = nextTime
}

function stopSeek() {
  seeking.value = false
  window.removeEventListener('pointermove', updateSeekPosition)
  window.removeEventListener('pointercancel', stopSeek)
  if (wasPlayingBeforeSeek && audioEl.value) {
    audioEl.value.play().catch(() => {})
  }
}

function onEnded() {
  playing.value = false
  emit('ended')
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
  window.removeEventListener('pointermove', updateSeekPosition)
  window.removeEventListener('pointercancel', stopSeek)
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
  flex: 1;
  height: 6px;
  background: var(--bg-secondary);
  border-radius: 999px;
  cursor: pointer;
  position: relative;
  touch-action: none;
}
.ap-fill {
  height: 100%;
  background: var(--accent);
  border-radius: inherit;
  transition: width 0.1s linear;
}
.ap-thumb {
  position: absolute;
  top: 50%;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #ffffff;
  border: 2px solid var(--accent);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
  transform: translate(-50%, -50%) scale(0.85);
  opacity: 0;
  transition: opacity 0.16s ease, transform 0.16s ease;
  pointer-events: none;
}
.ap-track:hover .ap-thumb,
.ap-track.dragging .ap-thumb {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}
.ap-track.dragging .ap-fill {
  transition: none;
}
.ap-time { font-size: 11px; color: var(--text-tertiary); white-space: nowrap; font-variant-numeric: tabular-nums; }
.ap-volume { display: flex; align-items: center; gap: 6px; }
.ap-vol-icon { font-size: 16px; color: var(--text-tertiary); }
.ap-vol-slider { width: 60px; accent-color: var(--accent); }
</style>
