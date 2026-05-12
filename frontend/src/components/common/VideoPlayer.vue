<template>
  <div class="video-player">
    <video
      ref="videoEl"
      :src="src"
      :poster="poster"
      controls
      preload="metadata"
      class="vp-video"
    ></video>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  src: { type: String, required: true },
  poster: { type: String, default: '' },
})

const videoEl = ref(null)
</script>

<style scoped>
.video-player {
  border-radius: var(--radius-md);
  overflow: hidden;
  background: #000;
  box-shadow: 0 2px 20px rgba(0,0,0,0.15);
}
.vp-video {
  display: block;
  width: 100%;
  max-height: 520px;
}
</style>
