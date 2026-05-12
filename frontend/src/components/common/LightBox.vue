<template>
  <Teleport to="body">
    <div v-if="visible" class="lightbox-overlay" @click.self="close">
      <div class="lightbox-container">
        <button class="lb-close" @click="close">&times;</button>
        <button v-if="images.length > 1" class="lb-nav lb-prev" @click.stop="prev">&lsaquo;</button>
        <div class="lb-image-wrap">
          <img :src="currentSrc" alt="" />
        </div>
        <button v-if="images.length > 1" class="lb-nav lb-next" @click.stop="next">&rsaquo;</button>
        <div v-if="images.length > 1" class="lb-counter">{{ index + 1 }} / {{ images.length }}</div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  images: { type: Array, default: () => [] },
  modelValue: { type: Boolean, default: false },
  initialIndex: { type: Number, default: 0 },
})

const emit = defineEmits(['update:modelValue'])

const index = ref(0)
const visible = ref(false)

const currentSrc = computed(() => props.images[index.value] || '')

watch(() => props.modelValue, (v) => {
  visible.value = v
  if (v) index.value = props.initialIndex
})
watch(visible, (v) => emit('update:modelValue', v))

function close() { visible.value = false }
function prev() { if (index.value > 0) index.value-- }
function next() { if (index.value < props.images.length - 1) index.value++ }

function onKey(e) {
  if (!visible.value) return
  if (e.key === 'Escape') close()
  if (e.key === 'ArrowLeft') prev()
  if (e.key === 'ArrowRight') next()
}

watch(visible, (v) => {
  if (v) document.addEventListener('keydown', onKey)
  else document.removeEventListener('keydown', onKey)
})
</script>

<style scoped>
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0,0,0,0.92);
  display: flex;
  align-items: center;
  justify-content: center;
}
.lightbox-container {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 90vw;
  max-height: 90vh;
}
.lb-image-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
}
.lb-image-wrap img {
  max-width: 85vw;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 4px;
}
.lb-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: #fff;
  font-size: 36px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.lb-close:hover { opacity: 1; }
.lb-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.1);
  border: none;
  color: #fff;
  font-size: 48px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  z-index: 1;
}
.lb-nav:hover { background: rgba(255,255,255,0.2); }
.lb-prev { left: -28px; }
.lb-next { right: -28px; }
.lb-counter {
  position: absolute;
  bottom: -32px;
  left: 50%;
  transform: translateX(-50%);
  color: #fff;
  font-size: 13px;
  opacity: 0.7;
}
</style>
