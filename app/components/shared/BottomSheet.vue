<script setup lang="ts">
interface Props {
  modelValue: boolean
  title?: string
  snapPoints?: string[]
}

withDefaults(defineProps<Props>(), {
  title: '',
  snapPoints: () => ['50vh', '90vh'],
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const sheetRef = ref<HTMLElement | null>(null)
const startY = ref(0)
const isDragging = ref(false)
const currentTranslate = ref(0)

function close() {
  emit('update:modelValue', false)
}

function onTouchStart(e: TouchEvent) {
  startY.value = e.touches[0].clientY
  isDragging.value = true
}

function onTouchMove(e: TouchEvent) {
  if (!isDragging.value) return
  const dy = e.touches[0].clientY - startY.value
  if (dy > 0) currentTranslate.value = dy
}

function onTouchEnd() {
  isDragging.value = false
  if (currentTranslate.value > 100) {
    close()
  }
  currentTranslate.value = 0
}
</script>

<template>
  <Teleport to="body">
    <Transition name="sheet-overlay">
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black/30 backdrop-blur-[2px] z-40"
        aria-hidden="true"
        @click="close"
      />
    </Transition>

    <Transition name="sheet">
      <div
        v-if="modelValue"
        ref="sheetRef"
        class="fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-xl rounded-t-3xl shadow-elevated flex flex-col max-h-[90vh]"
        :style="currentTranslate > 0 ? `transform: translateY(${currentTranslate}px)` : ''"
        role="dialog"
        :aria-modal="true"
        :aria-label="title"
        @touchstart="onTouchStart"
        @touchmove="onTouchMove"
        @touchend="onTouchEnd"
      >
        <!-- Drag handle -->
        <div class="flex justify-center pt-3 pb-1 cursor-grab active:cursor-grabbing">
          <div class="w-10 h-1 rounded-full bg-black/20" />
        </div>

        <!-- Header -->
        <div v-if="title" class="flex items-center justify-between px-5 py-3 border-b border-black/[0.06]">
          <h2 class="font-semibold text-text-primary">{{ title }}</h2>
          <button
            class="w-8 h-8 rounded-full bg-black/5 hover:bg-black/10 transition-colors flex items-center justify-center"
            aria-label="Cerrar"
            @click="close"
          >
            <Icon name="lucide:x" class="w-4 h-4" />
          </button>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-y-auto overscroll-contain scrollbar-hide">
          <slot />
        </div>

        <!-- Footer -->
        <div v-if="$slots.footer" class="border-t border-black/[0.06] p-4 pb-safe">
          <slot name="footer" />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.sheet-overlay-enter-active,
.sheet-overlay-leave-active {
  transition: opacity 0.25s ease;
}
.sheet-overlay-enter-from,
.sheet-overlay-leave-to {
  opacity: 0;
}

.sheet-enter-active {
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1);
}
.sheet-leave-active {
  transition: transform 0.25s ease-in;
}
.sheet-enter-from,
.sheet-leave-to {
  transform: translateY(100%);
}
</style>
