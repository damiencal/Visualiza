<script setup lang="ts">
import { useUiStore } from '~/stores/ui'

const ui = useUiStore()

const typeConfig = {
  success: { icon: 'lucide:check-circle-2', colorClass: 'text-emerald-600', bgClass: 'bg-emerald-50' },
  error: { icon: 'lucide:x-circle', colorClass: 'text-red-600', bgClass: 'bg-red-50' },
  info: { icon: 'lucide:info', colorClass: 'text-blue-600', bgClass: 'bg-blue-50' },
  warning: { icon: 'lucide:alert-triangle', colorClass: 'text-amber-600', bgClass: 'bg-amber-50' },
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed top-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none"
      aria-live="polite"
      aria-label="Notificaciones"
    >
      <TransitionGroup
        name="toast"
        tag="div"
        class="flex flex-col gap-2"
      >
        <div
          v-for="toast in ui.toasts"
          :key="toast.id"
          class="pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-2xl bg-white/90 backdrop-blur-xl shadow-elevated border border-black/[0.06] max-w-sm min-w-[280px]"
          role="alert"
        >
          <div
            :class="[
              'w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0',
              typeConfig[toast.type].bgClass,
            ]"
          >
            <Icon
              :name="typeConfig[toast.type].icon"
              :class="['w-4 h-4', typeConfig[toast.type].colorClass]"
            />
          </div>
          <div class="flex-1 min-w-0 pt-0.5">
            <p class="text-sm font-semibold text-text-primary leading-tight">{{ toast.title }}</p>
            <p v-if="toast.message" class="text-xs text-text-secondary mt-0.5 leading-snug">{{ toast.message }}</p>
          </div>
          <button
            class="w-6 h-6 rounded-full hover:bg-black/5 flex items-center justify-center text-text-tertiary transition-colors"
            :aria-label="`Cerrar: ${toast.title}`"
            @click="ui.removeToast(toast.id)"
          >
            <Icon name="lucide:x" class="w-3 h-3" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-leave-active {
  transition: all 0.2s ease-in;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}
.toast-move {
  transition: transform 0.3s ease;
}
</style>
