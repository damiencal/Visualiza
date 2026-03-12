<script setup lang="ts">
definePageMeta({ layout: 'visualizer' })

const route = useRoute()
const sessionId = route.params.sessionId as string

const visualizerStore = useVisualizerStore()
const { session } = storeToRefs(visualizerStore)

// Restore session from sessionId if needed (future: persist to server)
// For now, if no active session, redirect to fresh visualizer
onMounted(() => {
  if (!session.value || session.value.id !== sessionId) {
    // Attempt to load from localStorage persistence (best-effort)
    const saved = localStorage.getItem(`viz-session-${sessionId}`)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        Object.assign(visualizerStore, { session: parsed })
      } catch {}
    }
  }
})

useSeoMeta({
  title: computed(() => `Sesión de Visualizador - Visualiza`),
})

const showSidebar = ref(false)
</script>

<template>
  <div class="flex h-full">
    <!-- Main canvas area -->
    <div class="flex-1 flex flex-col min-w-0 p-4 gap-4">
      <div class="glass-card px-4 py-2.5 flex items-center justify-between gap-4">
        <div class="flex items-center gap-2 min-w-0">
          <h1 class="font-bold text-text-primary hidden sm:block truncate">Visualizador</h1>
          <span class="text-xs text-text-tertiary hidden sm:block font-mono">{{ sessionId.slice(0, 8) }}…</span>
        </div>
        <VisualizerToolbar />
        <button
          class="lg:hidden btn-soft flex items-center gap-1.5 text-sm"
          @click="showSidebar = !showSidebar"
        >
          <Icon name="lucide:panel-right" class="w-4 h-4" />
          Panel
        </button>
      </div>

      <div class="flex-1 min-h-0">
        <VisualizerRoomUploader v-if="!session?.roomImage" />
        <VisualizerCanvas v-else class="h-full" />
      </div>
    </div>

    <!-- Desktop sidebar -->
    <div class="hidden lg:flex flex-col w-80 shrink-0 p-4 pl-0">
      <VisualizerSidebar class="h-full" />
    </div>

    <LayoutSidePanel v-model="showSidebar" title="Productos" side="right" width="320px">
      <VisualizerSidebar />
    </LayoutSidePanel>
  </div>
</template>
