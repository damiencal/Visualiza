<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const { isProcessing } = storeToRefs(visualizerStore)

const isDragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

async function handleFile(file: File) {
  const { validateImageFile, fileToDataURL } = await import('~/utils/imageHelpers')
  const error = validateImageFile(file, 20)
  if (error) {
    useUiStore().addToast({ type: 'error', title: 'Imagen inválida', message: error })
    return
  }
  const dataUrl = await fileToDataURL(file)
  visualizerStore.createSession(dataUrl, 'living-room')
}

function onDrop(e: DragEvent) {
  isDragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file) handleFile(file)
}

function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) handleFile(file)
}

function useSampleRoom() {
  visualizerStore.createSession(
    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1200&q=80',
    'living-room',
  )
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-20 min-h-full flex flex-col items-center justify-center">
    <!-- Header -->
    <div class="text-center mb-10">
      <h1 class="text-4xl font-bold text-text-primary mb-4">Visualizador Interactivo</h1>
      <p class="text-lg text-text-secondary">Sube una foto de tu espacio para comenzar a visualizar productos.</p>
    </div>

    <!-- Drop zone -->
    <div :class="[
      'w-full max-w-2xl glass-card p-12 border-2 border-dashed text-center relative group transition-colors',
      isDragging ? 'border-primary/60 bg-primary/5 scale-[1.01]' : 'border-primary/30 hover:border-primary/60',
    ]" @dragover.prevent="isDragging = true" @dragleave.prevent="isDragging = false" @drop.prevent="onDrop">
      <input ref="fileInput" type="file" accept="image/jpeg,image/png,image/webp"
        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" aria-label="Subir foto de habitación"
        @change="onFileChange" />
      <div
        class="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-inner-soft">
        <Icon :name="isProcessing ? 'lucide:loader-2' : 'lucide:upload'"
          :class="['w-10 h-10 text-primary', isProcessing && 'animate-spin']" />
      </div>
      <h3 class="text-2xl font-bold text-text-primary mb-2">Arrastra una foto o toca para seleccionar</h3>
      <p class="text-text-secondary">Formatos soportados: JPG, PNG, WebP. Máx 20MB.</p>
    </div>

    <!-- Sample room -->
    <div class="mt-12 text-center">
      <p class="text-text-secondary mb-4">¿No tienes una foto a mano?</p>
      <button class="btn-soft flex items-center gap-2 mx-auto" @click="useSampleRoom">
        <Icon name="lucide:image" class="w-5 h-5" />
        Usar habitación de muestra
      </button>
    </div>
  </div>
</template>
