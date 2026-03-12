<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const { sliderPosition, showBeforeAfter } = storeToRefs(visualizerStore)

const sliderRef = ref<HTMLDivElement | null>(null)
const trackRef = ref<HTMLDivElement | null>(null)
const isDragging = ref(false)

function startDrag(e: MouseEvent | TouchEvent) {
  isDragging.value = true
  e.preventDefault()
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', stopDrag)
  window.addEventListener('touchmove', onMove, { passive: false })
  window.addEventListener('touchend', stopDrag)
}

function onMove(e: MouseEvent | TouchEvent) {
  if (!isDragging.value || !trackRef.value) return
  const rect = trackRef.value.getBoundingClientRect()
  const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX
  const pos = Math.min(100, Math.max(0, ((clientX - rect.left) / rect.width) * 100))
  visualizerStore.setSliderPosition(pos)
}

function stopDrag() {
  isDragging.value = false
  window.removeEventListener('mousemove', onMove)
  window.removeEventListener('mouseup', stopDrag)
  window.removeEventListener('touchmove', onMove)
  window.removeEventListener('touchend', stopDrag)
}

onUnmounted(stopDrag)
</script>

<template>
  <div ref="trackRef" class="absolute inset-0 z-10 select-none"
    :class="showBeforeAfter ? 'cursor-ew-resize' : 'pointer-events-none'"
    @mousedown="showBeforeAfter && startDrag($event)" @touchstart.prevent="showBeforeAfter && startDrag($event)">
    <!-- Divider line -->
    <div v-if="showBeforeAfter" class="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg"
      :style="{ left: `${sliderPosition}%` }">
      <!-- Handle -->
      <div ref="sliderRef"
        class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-9 h-9 bg-white rounded-full shadow-elevated flex items-center justify-center cursor-ew-resize">
        <Icon name="lucide:move-horizontal" class="w-4 h-4 text-text-primary" />
      </div>

    </div>

    <!-- Labels fixed to container edges -->
    <div
      class="absolute top-3 left-3 text-white text-xs font-semibold bg-black/40 backdrop-blur-sm px-2 py-0.5 rounded-full pointer-events-none">
      Antes
    </div>
    <div
      class="absolute top-3 right-3 text-white text-xs font-semibold bg-black/40 backdrop-blur-sm px-2 py-0.5 rounded-full pointer-events-none">
      Después
    </div>
  </div>
</template>
