<script setup lang="ts">
interface Props {
  modelValue: boolean
  title?: string
  side?: 'left' | 'right'
  width?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  side: 'right',
  width: '380px',
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

function close() {
  emit('update:modelValue', false)
}
</script>

<template>
  <Teleport to="body">
    <Transition name="overlay">
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black/30 backdrop-blur-[2px] z-40"
        aria-hidden="true"
        @click="close"
      />
    </Transition>

    <Transition :name="side === 'right' ? 'panel-right' : 'panel-left'">
      <div
        v-if="modelValue"
        class="fixed top-0 bottom-0 z-50 flex flex-col bg-white/90 backdrop-blur-xl shadow-elevated overflow-hidden"
        :class="side === 'right' ? 'right-0 rounded-l-2xl' : 'left-0 rounded-r-2xl'"
        :style="{ width }"
        role="dialog"
        :aria-modal="true"
        :aria-label="title"
      >
        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-4 border-b border-black/[0.06]">
          <h2 class="font-semibold text-text-primary">{{ title }}</h2>
          <button
            class="w-8 h-8 rounded-full bg-black/5 hover:bg-black/10 transition-colors flex items-center justify-center"
            aria-label="Cerrar panel"
            @click="close"
          >
            <Icon name="lucide:x" class="w-4 h-4" aria-hidden="true" />
          </button>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-y-auto overscroll-contain scrollbar-hide">
          <slot />
        </div>

        <!-- Footer slot (optional) -->
        <div v-if="$slots.footer" class="border-t border-black/[0.06] p-4 pb-safe">
          <slot name="footer" />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.25s ease;
}
.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

.panel-right-enter-active,
.panel-right-leave-active,
.panel-left-enter-active,
.panel-left-leave-active {
  transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}
.panel-right-enter-from,
.panel-right-leave-to {
  transform: translateX(100%);
}
.panel-left-enter-from,
.panel-left-leave-to {
  transform: translateX(-100%);
}
</style>
