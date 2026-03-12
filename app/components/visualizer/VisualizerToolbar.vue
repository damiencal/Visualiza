<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const { session, canUndo, canRedo, showBeforeAfter, isGenerating, generatedImage, bom } = storeToRefs(visualizerStore)
const uiStore = useUiStore()

async function exportAndDownload() {
  const { downloadImage } = useVisualizer()
  await downloadImage()
}

async function handleGenerate() {
  try {
    await visualizerStore.generateWithAI()
    uiStore.visualizerSidebarTab = 'products'
  }
  catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Error al generar imagen'
    useUiStore().addToast({ type: 'error', title: 'Error de generación', message: msg })
  }
}

function openBom() {
  uiStore.visualizerSidebarTab = 'bom'
}
</script>

<template>
  <div class="flex items-center gap-1.5 flex-wrap">
    <!-- Undo -->
    <button :disabled="!canUndo"
      class="w-9 h-9 rounded-xl bg-white/80 shadow-soft flex items-center justify-center disabled:opacity-40 hover:shadow-card transition-all"
      title="Deshacer" @click="visualizerStore.undo()">
      <Icon name="lucide:undo-2" class="w-4 h-4" />
    </button>

    <!-- Redo -->
    <button :disabled="!canRedo"
      class="w-9 h-9 rounded-xl bg-white/80 shadow-soft flex items-center justify-center disabled:opacity-40 hover:shadow-card transition-all"
      title="Rehacer" @click="visualizerStore.redo()">
      <Icon name="lucide:redo-2" class="w-4 h-4" />
    </button>

    <div class="w-px h-6 bg-black/10 mx-1" />

    <!-- Before/After toggle -->
    <button :class="[
      'flex items-center gap-1.5 h-9 px-3 rounded-xl text-sm font-medium transition-all',
      showBeforeAfter
        ? 'bg-primary text-white shadow-glow'
        : 'bg-white/80 shadow-soft hover:shadow-card text-text-primary',
    ]" :disabled="!session?.roomImage" :aria-pressed="showBeforeAfter" title="Antes / Después"
      @click="visualizerStore.toggleBeforeAfter()">
      <Icon name="lucide:split-square-horizontal" class="w-4 h-4" />
      <span class="hidden sm:inline">Antes/Después</span>
    </button>

    <div class="w-px h-6 bg-black/10 mx-1" />

    <!-- Reset -->
    <button :disabled="!canUndo"
      class="w-9 h-9 rounded-xl bg-white/80 shadow-soft flex items-center justify-center disabled:opacity-40 hover:shadow-card transition-all text-text-secondary hover:text-red-500"
      title="Reiniciar" @click="visualizerStore.reset()">
      <Icon name="lucide:trash-2" class="w-4 h-4" />
    </button>

    <!-- Export -->
    <button :disabled="!session?.roomImage"
      class="flex items-center gap-1.5 h-9 px-3 rounded-xl bg-white/80 shadow-soft text-sm font-medium hover:shadow-card transition-all disabled:opacity-40"
      title="Descargar imagen" @click="exportAndDownload">
      <Icon name="lucide:download" class="w-4 h-4" />
      <span class="hidden sm:inline">Exportar</span>
    </button>

    <div class="w-px h-6 bg-black/10 mx-1" />

    <!-- Bill of Materials -->
    <button :disabled="!bom.length" :class="[
      'relative flex items-center gap-1.5 h-9 px-3 rounded-xl text-sm font-medium transition-all disabled:opacity-40',
      uiStore.visualizerSidebarTab === 'bom'
        ? 'bg-emerald-500 text-white shadow-md'
        : 'bg-white/80 shadow-soft hover:shadow-card text-text-primary',
    ]" title="Lista de materiales y presupuesto" @click="openBom">
      <Icon name="lucide:clipboard-list" class="w-4 h-4" />
      <span class="hidden sm:inline">Presupuesto</span>
      <span v-if="bom.length"
        class="ml-0.5 min-w-[18px] h-4.5 flex items-center justify-center bg-white/30 text-[10px] font-bold rounded-full px-1">{{
          bom.length }}</span>
    </button>

    <div class="w-px h-6 bg-black/10 mx-1" />
    <button :disabled="!session?.roomImage || isGenerating" :class="[
      'flex items-center gap-1.5 h-9 px-3 rounded-xl text-sm font-semibold transition-all disabled:opacity-40',
      generatedImage
        ? 'bg-violet-100 text-violet-700 hover:bg-violet-200'
        : 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white shadow-md hover:opacity-90',
    ]" title="Generar diseño con Imagen AI" @click="handleGenerate">
      <Icon :name="isGenerating ? 'lucide:loader-2' : 'lucide:sparkles'"
        :class="['w-4 h-4', isGenerating && 'animate-spin']" />
      <span class="hidden sm:inline">{{ isGenerating ? 'Generando…' : 'Generar con IA' }}</span>
    </button>

    <!-- Clear generated image -->
    <button v-if="generatedImage"
      class="w-9 h-9 rounded-xl bg-white/80 shadow-soft flex items-center justify-center hover:shadow-card transition-all text-violet-500 hover:text-red-500"
      title="Descartar imagen generada" @click="visualizerStore.clearGeneratedImage()">
      <Icon name="lucide:x" class="w-4 h-4" />
    </button>
  </div>
</template>
