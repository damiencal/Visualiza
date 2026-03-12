<script setup lang="ts">
definePageMeta({ layout: 'visualizer' })
useSeoMeta({ title: 'Visualizador de Interiores - Visualiza', description: 'Visualiza cómo lucirán los productos en tu hogar.' })

const visualizerStore = useVisualizerStore()
const { session } = storeToRefs(visualizerStore)
</script>

<template>
  <!-- Upload state -->
  <template v-if="!session?.roomImage">
    <VisualizerRoomUploader />
  </template>

  <!-- Main split layout when image is loaded -->
  <div v-else class="flex flex-col md:flex-row h-full overflow-hidden">
    <!-- Canvas area -->
    <div class="flex-1 relative p-4 md:p-6 h-[60vh] md:h-full overflow-hidden">
      <VisualizerCanvas class="h-full" />
    </div>

    <!-- Sidebar -->
    <div class="w-full md:w-[400px] h-[40vh] md:h-full flex-shrink-0 z-20">
      <VisualizerSidebar class="h-full" />
    </div>
  </div>
</template>
