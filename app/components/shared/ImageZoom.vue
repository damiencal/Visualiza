<script setup lang="ts">
interface Props {
  src: string
  alt?: string
  maxScale?: number
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  maxScale: 4,
})

const containerRef = ref<HTMLDivElement | null>(null)
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const isZoomed = computed(() => scale.value > 1)

// Pinch-to-zoom state
let initialDistance = 0
let initialScale = 1

function getDistance(touches: TouchList): number {
  const dx = touches[0].clientX - touches[1].clientX
  const dy = touches[0].clientY - touches[1].clientY
  return Math.sqrt(dx * dx + dy * dy)
}

function onTouchStart(e: TouchEvent) {
  if (e.touches.length === 2) {
    initialDistance = getDistance(e.touches)
    initialScale = scale.value
  }
}

function onTouchMove(e: TouchEvent) {
  if (e.touches.length === 2) {
    e.preventDefault()
    const dist = getDistance(e.touches)
    const newScale = Math.min(props.maxScale, Math.max(1, initialScale * (dist / initialDistance)))
    scale.value = newScale
    if (newScale === 1) {
      translateX.value = 0
      translateY.value = 0
    }
  }
}

function onDoubleClick(e: MouseEvent) {
  if (scale.value > 1) {
    scale.value = 1
    translateX.value = 0
    translateY.value = 0
  } else {
    scale.value = 2
    const rect = containerRef.value!.getBoundingClientRect()
    translateX.value = (rect.width / 2 - (e.clientX - rect.left)) * 0.5
    translateY.value = (rect.height / 2 - (e.clientY - rect.top)) * 0.5
  }
}

// Mouse drag when zoomed
let dragStartX = 0
let dragStartY = 0
let dragStartTX = 0
let dragStartTY = 0
const isDragging = ref(false)

function onMouseDown(e: MouseEvent) {
  if (!isZoomed.value) return
  isDragging.value = true
  dragStartX = e.clientX
  dragStartY = e.clientY
  dragStartTX = translateX.value
  dragStartTY = translateY.value
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

function onMouseMove(e: MouseEvent) {
  if (!isDragging.value) return
  translateX.value = dragStartTX + (e.clientX - dragStartX)
  translateY.value = dragStartTY + (e.clientY - dragStartY)
}

function onMouseUp() {
  isDragging.value = false
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
}

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
})
</script>

<template>
  <div
    ref="containerRef"
    class="overflow-hidden select-none"
    :class="isZoomed ? 'cursor-grab active:cursor-grabbing' : 'cursor-zoom-in'"
    @touchstart="onTouchStart"
    @touchmove.prevent="onTouchMove"
    @dblclick="onDoubleClick"
    @mousedown="onMouseDown"
  >
    <img
      :src="src"
      :alt="alt"
      class="w-full h-full object-cover transition-transform duration-200 will-change-transform"
      :style="{
        transform: `scale(${scale}) translate(${translateX / scale}px, ${translateY / scale}px)`,
        transitionDuration: isDragging ? '0ms' : '200ms',
      }"
      draggable="false"
    />

    <!-- Zoom hint -->
    <div
      v-if="!isZoomed"
      class="absolute bottom-2 right-2 bg-black/40 text-white text-[10px] px-2 py-0.5 rounded-full pointer-events-none"
    >
      Doble clic para ampliar
    </div>

    <!-- Reset button when zoomed -->
    <button
      v-if="isZoomed"
      class="absolute top-2 right-2 w-8 h-8 bg-black/50 text-white rounded-full flex items-center justify-center hover:bg-black/70 transition-colors"
      aria-label="Restablecer zoom"
      @click.stop="scale = 1; translateX = 0; translateY = 0"
    >
      <Icon name="lucide:minimize-2" class="w-3.5 h-3.5" />
    </button>
  </div>
</template>
