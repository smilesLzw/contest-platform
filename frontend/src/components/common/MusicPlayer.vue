<template>
  <div class="float-music" v-if="tracks.length" @mouseenter="expanded = true" @mouseleave="expanded = false" :class="{ expanded }">
    <!-- 收起状态：圆形按钮 -->
    <div class="fm-trigger">
      <span class="fm-icon" :class="{ playing: playing }">♪</span>
      <span class="fm-wave" v-if="playing">
        <i></i><i></i><i></i>
      </span>
    </div>

    <!-- 展开状态：迷你播放器 -->
    <Transition name="fade">
      <div v-show="expanded" class="fm-panel">
        <span class="fm-title">{{ currentTrack?.title || '未选择' }}</span>
        <div class="fm-controls">
          <button class="fm-btn" @click="prevTrack" title="上一首">&#9664;</button>
          <button class="fm-btn fm-btn-play" @click="togglePlay" :title="playing ? '暂停' : '播放'">
            <span v-if="!playing">&#9654;</span>
            <span v-else>&#9646;&#9646;</span>
          </button>
          <button class="fm-btn" @click="nextTrack" title="下一首">&#9654;</button>
        </div>
        <div class="fm-volume">
          <input type="range" min="0" max="100" :value="volume" @input="setVolume" class="fm-vol-slider" />
        </div>
        <button class="fm-btn fm-list-btn" @click.stop="showList = !showList" title="播放列表">
          &#9776;
        </button>
      </div>
    </Transition>

    <!-- 播放列表弹出 -->
    <Transition name="slide-up">
      <div v-if="showList" class="fm-playlist" @mouseleave="showList = false">
        <div
          v-for="(t, i) in tracks"
          :key="t.id"
          class="fm-pl-item"
          :class="{ active: i === currentIndex }"
          @click="playTrack(i)"
        >
          <span class="fm-pl-title">{{ t.title }}</span>
          <span class="fm-pl-artist" v-if="t.artist">{{ t.artist }}</span>
        </div>
      </div>
    </Transition>

    <audio
      ref="audioEl"
      :src="currentTrack?.audio_url || ''"
      preload="auto"
      @ended="nextTrack"
      @loadedmetadata="onLoaded"
    ></audio>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { getBgMusic } from '../../api/common'

const audioEl = ref(null)
const tracks = ref([])
const currentIndex = ref(0)
const playing = ref(false)
const volume = ref(Number(localStorage.getItem('bgMusicVolume') || 60))
const expanded = ref(false)
const showList = ref(false)

const currentTrack = computed(() => tracks.value[currentIndex.value] || null)

async function loadTracks() {
  try {
    const res = await getBgMusic()
    if (res.data?.length) tracks.value = res.data
  } catch (e) {
    console.error('加载背景音乐失败', e)
  }
}

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

function playTrack(i) {
  currentIndex.value = i
  playing.value = false
  setTimeout(() => {
    const a = audioEl.value
    if (a) {
      a.load()
      a.play().catch(() => {})
      playing.value = true
    }
    showList.value = false
  }, 50)
}

function prevTrack() {
  if (!tracks.value.length) return
  currentIndex.value = (currentIndex.value - 1 + tracks.value.length) % tracks.value.length
  playTrack(currentIndex.value)
}

function nextTrack() {
  if (!tracks.value.length) return
  currentIndex.value = (currentIndex.value + 1) % tracks.value.length
  playTrack(currentIndex.value)
}

function onLoaded() {
  if (audioEl.value) audioEl.value.volume = volume.value / 100
}

function setVolume(e) {
  volume.value = Number(e.target.value)
  localStorage.setItem('bgMusicVolume', volume.value)
  if (audioEl.value) audioEl.value.volume = volume.value / 100
}

let interactionUnlock = null

function registerInteractionUnlock() {
  if (interactionUnlock) return
  interactionUnlock = () => {
    const a = audioEl.value
    if (a && a.paused && tracks.value.length) {
      a.play().then(() => { playing.value = true }).catch(() => {})
    }
    document.removeEventListener('click', interactionUnlock)
    interactionUnlock = null
  }
  document.addEventListener('click', interactionUnlock)
}

function tryAutoplay() {
  const a = audioEl.value
  if (!a) return
  a.volume = volume.value / 100
  a.play().then(() => {
    playing.value = true
    if (interactionUnlock) {
      document.removeEventListener('click', interactionUnlock)
      interactionUnlock = null
    }
  }).catch(() => {
    playing.value = false
    registerInteractionUnlock()
  })
}

onMounted(() => {
  // 先注册交互监听，避免 API 加载期间错过用户点击
  registerInteractionUnlock()
  loadTracks().then(() => {
    if (tracks.value.length && audioEl.value) {
      tryAutoplay()
    }
  })
})

onBeforeUnmount(() => {
  if (interactionUnlock) {
    document.removeEventListener('click', interactionUnlock)
    interactionUnlock = null
  }
  if (audioEl.value) {
    audioEl.value.pause()
    audioEl.value.src = ''
  }
})
</script>

<style scoped>
.float-music {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 0;
}

/* ── 收起：圆形按钮 ── */
.fm-trigger {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  box-shadow: 0 2px 16px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
  flex-shrink: 0;
  position: relative;
  z-index: 2;
  transition: box-shadow 0.3s;
}
.expanded .fm-trigger {
  box-shadow: none;
  border-right: none;
  border-radius: 22px 0 0 22px;
}
.fm-icon {
  font-size: 20px;
  color: var(--text-tertiary);
  transition: color 0.3s;
}
.fm-icon.playing { color: var(--accent); }

/* 音波动画 */
.fm-wave {
  position: absolute;
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 12px;
  bottom: 8px;
}
.fm-wave i {
  width: 2px;
  background: var(--accent);
  border-radius: 1px;
  animation: wave 0.8s ease-in-out infinite;
}
.fm-wave i:nth-child(1) { height: 6px; animation-delay: 0s; }
.fm-wave i:nth-child(2) { height: 12px; animation-delay: 0.15s; }
.fm-wave i:nth-child(3) { height: 8px; animation-delay: 0.3s; }
@keyframes wave {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(0.4); }
}

/* ── 展开面板 ── */
.fm-panel {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-left: none;
  border-radius: 0 12px 12px 0;
  padding: 6px 14px 6px 10px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.1);
  white-space: nowrap;
}
.fm-title {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.fm-controls {
  display: flex;
  align-items: center;
  gap: 2px;
}
.fm-btn {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  transition: all 0.15s;
}
.fm-btn:hover { color: var(--text-primary); background: var(--bg-secondary); }
.fm-btn-play {
  background: var(--accent);
  color: #fff;
  width: 30px;
  height: 30px;
  font-size: 11px;
}
.fm-btn-play:hover { background: var(--accent-hover); color: #fff; }
.fm-volume { display: flex; align-items: center; }
.fm-vol-slider { width: 48px; accent-color: var(--accent); height: 3px; }
.fm-list-btn { font-size: 12px; }

/* ── 播放列表 ── */
.fm-playlist {
  position: fixed;
  bottom: 80px;
  right: 24px;
  width: 220px;
  max-height: 240px;
  overflow-y: auto;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 20px rgba(0,0,0,0.12);
}
.fm-pl-item {
  padding: 8px 14px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.15s;
}
.fm-pl-item:last-child { border-bottom: none; }
.fm-pl-item:hover { background: var(--bg-card-hover); }
.fm-pl-item.active { background: var(--bg-secondary); }
.fm-pl-item.active .fm-pl-title { color: var(--accent); }
.fm-pl-title { font-size: 12px; font-weight: 500; color: var(--text-primary); display: block; }
.fm-pl-artist { font-size: 11px; color: var(--text-tertiary); }

/* ── 过渡动画 ── */
.fade-enter-active, .fade-leave-active { transition: all 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; max-width: 0; padding: 6px 0; overflow: hidden; }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.2s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translateY(8px); }
</style>
