<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const { session, selectedSurfaceId } = storeToRefs(visualizerStore)

const surfaceTypeLabels: Record<string, string> = {
  floor: 'Piso',
  wall: 'Pared',
  ceiling: 'Techo',
  'counter-top': 'Encimera',
  backsplash: 'Salpicadero',
}

function addSurface(type: 'floor' | 'wall' | 'ceiling' | 'counter-top' | 'backsplash') {
  visualizerStore.addSurface(type)
}
</script>

<template>
  <div class="space-y-3">
    <h3 class="text-sm font-semibold text-text-primary px-1">Superficies</h3>

    <!-- Existing surfaces -->
    <div class="space-y-1.5">
      <button
        v-for="surface in session?.surfaces ?? []"
        :key="surface.id"
        :class="[
          'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-all',
          selectedSurfaceId === surface.id
            ? 'bg-primary text-white shadow-glow'
            : 'bg-black/[0.04] hover:bg-black/[0.07] text-text-primary',
        ]"
        :aria-pressed="selectedSurfaceId === surface.id"
        @click="visualizerStore.selectSurface(surface.id)"
      >
        <Icon
          name="lucide:layers"
          :class="['w-4 h-4', selectedSurfaceId === surface.id ? 'text-white' : 'text-primary']"
        />
        <span class="flex-1 text-sm font-medium">{{ surfaceTypeLabels[surface.type] ?? surface.type }}</span>
        <Icon
          v-if="selectedSurfaceId === surface.id"
          name="lucide:check"
          class="w-4 h-4 text-white"
        />
      </button>
    </div>

    <!-- Add surface buttons -->
    <div class="grid grid-cols-3 gap-1.5">
      <button
        v-for="type in ['floor', 'wall', 'ceiling'] as const"
        :key="type"
        class="flex flex-col items-center gap-1 p-2 rounded-xl bg-black/[0.04] hover:bg-primary/10 hover:text-primary transition-all text-xs text-text-secondary"
        :aria-label="`Agregar ${surfaceTypeLabels[type]}`"
        @click="addSurface(type)"
      >
        <Icon name="lucide:plus" class="w-4 h-4" />
        {{ surfaceTypeLabels[type] }}
      </button>
    </div>

    <p v-if="!session?.surfaces?.length" class="text-xs text-text-tertiary text-center py-2">
      Agrega una superficie para aplicar productos
    </p>
  </div>
</template>
