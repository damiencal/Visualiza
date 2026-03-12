<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const uiStore = useUiStore()
const emit = defineEmits<{ 'image-loaded': [] }>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const containerRef = ref<HTMLDivElement | null>(null)

const { session, isProcessing, showBeforeAfter, sliderPosition, generatedImage, isGenerating, canUndo, canRedo } = storeToRefs(visualizerStore)

// Drawing mode state
const isDrawingMode = ref(false)
const isDrawing = ref(false)
const maskPath = ref<{ x: number; y: number }[]>([])

// Draw room image + layers whenever session changes
watchEffect(() => {
  if (!canvasRef.value || !session.value?.roomImage) return
  drawCanvas()
})

async function drawCanvas() {
  const canvas = canvasRef.value
  if (!canvas || !session.value) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const img = new Image()
  img.crossOrigin = 'anonymous'
  img.src = session.value.roomImage
  await new Promise<void>(resolve => { img.onload = () => resolve() })

  canvas.width = img.naturalWidth
  canvas.height = img.naturalHeight

  ctx.drawImage(img, 0, 0)

  // Draw each layer
  for (const layer of session.value.layers) {
    if (!layer.product?.images?.texture) continue
    const texImg = new Image()
    texImg.crossOrigin = 'anonymous'
    texImg.src = layer.product.images.texture
    await new Promise<void>(resolve => { texImg.onload = () => resolve() })
    const pattern = ctx.createPattern(texImg, 'repeat')
    if (!pattern) continue
    ctx.save()
    ctx.globalAlpha = layer.opacity ?? 0.85
    ctx.globalCompositeOperation = (layer.blendMode ?? 'multiply') as GlobalCompositeOperation
    ctx.fillStyle = pattern
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.restore()
  }
  emit('image-loaded')
}

// Draw freehand mask overlay on canvas
function drawMaskOverlay() {
  const canvas = canvasRef.value
  if (!canvas || maskPath.value.length < 2) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const first = maskPath.value[0]
  if (!first) return

  ctx.save()
  ctx.beginPath()
  ctx.moveTo(first.x, first.y)
  for (let i = 1; i < maskPath.value.length; i++) {
    const pt = maskPath.value[i]
    if (pt) ctx.lineTo(pt.x, pt.y)
  }
  if (!isDrawing.value && maskPath.value.length > 2) {
    ctx.closePath()
    ctx.fillStyle = 'rgba(244, 63, 94, 0.2)'
    ctx.fill()
  }
  ctx.strokeStyle = '#F43F5E'
  ctx.lineWidth = 3
  ctx.setLineDash([5, 5])
  ctx.stroke()
  ctx.restore()
}

// Pointer event handlers for drawing mode
function handlePointerDown(e: PointerEvent) {
  if (!isDrawingMode.value || !canvasRef.value) return
  const canvas = canvasRef.value
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  isDrawing.value = true
  maskPath.value = [{ x: (e.clientX - rect.left) * scaleX, y: (e.clientY - rect.top) * scaleY }]
}

function handlePointerMove(e: PointerEvent) {
  if (!isDrawingMode.value || !isDrawing.value || !canvasRef.value) return
  const canvas = canvasRef.value
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  maskPath.value = [...maskPath.value, { x: (e.clientX - rect.left) * scaleX, y: (e.clientY - rect.top) * scaleY }]
  drawCanvas().then(() => drawMaskOverlay())
}

async function handlePointerUp() {
  if (!isDrawingMode.value || !isDrawing.value) return
  isDrawing.value = false
  await drawCanvas()
  drawMaskOverlay()
}

function clearMask() {
  maskPath.value = []
  drawCanvas()
}

function toggleDrawingMode() {
  isDrawingMode.value = !isDrawingMode.value
  if (!isDrawingMode.value) {
    maskPath.value = []
    drawCanvas()
  }
}

// Before/After slider
const beforeCanvasRef = ref<HTMLCanvasElement | null>(null)

async function drawBeforeCanvas() {
  if (!beforeCanvasRef.value || !session.value?.roomImage) return
  const canvas = beforeCanvasRef.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  const img = new Image()
  img.crossOrigin = 'anonymous'
  img.src = session.value.roomImage
  await new Promise<void>(resolve => { img.onload = () => resolve() })
  canvas.width = img.naturalWidth
  canvas.height = img.naturalHeight
  ctx.drawImage(img, 0, 0)
}

watch(() => session.value?.roomImage, () => {
  if (session.value?.roomImage) drawBeforeCanvas()
})

// Toolbar actions
async function exportAndDownload() {
  const { downloadImage } = useVisualizer()
  await downloadImage()
}

async function handleGenerate() {
  try {
    let base64 = undefined;
    if (canvasRef.value) {
      // Get the current canvas drawing as base64 without the 'data:image/jpeg;base64,' prefix
      base64 = canvasRef.value.toDataURL('image/jpeg', 0.8).split(',')[1];
    }
    await visualizerStore.generateWithAI(undefined, base64)
    uiStore.visualizerSidebarTab = 'analysis'
  }
  catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Error al generar imagen'
    uiStore.addToast({ type: 'error', title: 'Error de generación', message: msg })
  }
}

defineExpose({ canvasRef })
</script>

<template>
  <div ref="containerRef"
    class="relative w-full h-full flex flex-col items-center justify-center bg-black/5 rounded-2xl overflow-hidden shadow-inner-soft">
    <!-- Loading overlay -->
    <Transition name="fade">
      <div v-if="isProcessing || isGenerating"
        class="absolute inset-0 z-20 bg-white/50 backdrop-blur-md flex items-center justify-center transition-all duration-300">
        <div class="flex flex-col items-center gap-4 bg-white/80 p-6 rounded-2xl shadow-elevated">
          <Icon name="lucide:sparkles" class="w-10 h-10 text-primary animate-pulse" />
          <span class="text-primary font-bold text-lg">Generando con IA...</span>
          <p class="text-sm text-text-secondary">Adaptando iluminación y perspectiva</p>
        </div>
      </div>
    </Transition>

    <!-- Before / After mode -->
    <template v-if="showBeforeAfter && session?.roomImage">
      <div class="relative select-none w-full h-full" style="touch-action: none;">
        <!-- After (full) -->
        <canvas ref="canvasRef" class="w-full h-full object-contain block" />
        <!-- Before clip -->
        <div class="absolute inset-0 overflow-hidden" :style="{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }">
          <canvas ref="beforeCanvasRef" class="w-full h-full object-contain block" />
        </div>
        <!-- Divider -->
        <VisualizerBeforeAfterSlider />
      </div>
    </template>

    <!-- Normal mode -->
    <template v-else>
      <!-- AI Generated image overlay -->
      <Transition name="fade">
        <div v-if="generatedImage" class="absolute inset-0 z-10 rounded-2xl overflow-hidden">
          <img :src="generatedImage" alt="Diseño generado por IA" class="w-full h-full object-cover" />
          <div
            class="absolute bottom-3 left-3 flex items-center gap-1.5 bg-black/60 text-white text-xs font-medium px-2.5 py-1 rounded-full backdrop-blur-sm">
            <Icon name="lucide:sparkles" class="w-3.5 h-3.5 text-violet-300" />
            Generado con Imagen AI
          </div>
        </div>
      </Transition>

      <div class="relative w-full h-full flex items-center justify-center p-4">
        <canvas v-if="session?.roomImage" ref="canvasRef" :class="[
          'max-w-full max-h-full object-contain rounded-xl shadow-card transition-all duration-300',
          isDrawingMode ? 'cursor-crosshair' : 'cursor-default',
          isProcessing ? 'blur-md scale-[1.02]' : '',
        ]" style="touch-action: none;" @pointerdown="handlePointerDown" @pointermove="handlePointerMove"
          @pointerup="handlePointerUp" @pointerleave="handlePointerUp" />
        <div v-else class="flex flex-col items-center justify-center text-text-tertiary gap-3">
          <Icon name="lucide:image-plus" class="w-10 h-10 opacity-50" />
          <p class="text-sm">Sube una foto de tu habitación para comenzar</p>
        </div>
      </div>
    </template>

    <!-- Bottom Floating Toolbar -->
    <div v-if="session?.roomImage"
      class="absolute bottom-6 left-1/2 -translate-x-1/2 glass-panel px-6 py-3 rounded-full flex items-center gap-4 shadow-elevated z-10">
      <!-- Draw mode toggle -->
      <button :class="[
        'p-2 transition-colors',
        isDrawingMode ? 'text-primary bg-primary/10 rounded-full' : 'text-text-secondary hover:text-primary',
      ]" :title="isDrawingMode ? 'Dibujando Área' : 'Seleccionar Área'" @click="toggleDrawingMode">
        <Icon name="lucide:pen-tool" class="w-5 h-5" />
      </button>

      <!-- Clear mask -->
      <button v-if="maskPath.length > 0" class="p-2 text-text-secondary hover:text-primary transition-colors"
        title="Borrar Área" @click="clearMask">
        <Icon name="lucide:eraser" class="w-5 h-5" />
      </button>

      <div class="w-px h-6 bg-black/10" />

      <!-- Before/After -->
      <button :class="[
        'p-2 transition-colors',
        showBeforeAfter ? 'text-primary bg-primary/10 rounded-full' : 'text-text-secondary hover:text-primary',
      ]" title="Antes / Después" @click="visualizerStore.toggleBeforeAfter()">
        <Icon name="lucide:split-square-horizontal" class="w-5 h-5" />
      </button>

      <div class="w-px h-6 bg-black/10" />

      <!-- Undo -->
      <button :disabled="!canUndo || isProcessing || isGenerating"
        class="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors" title="Deshacer"
        @click="visualizerStore.undo()">
        <Icon name="lucide:undo-2" class="w-5 h-5" />
      </button>

      <!-- Redo -->
      <button :disabled="!canRedo || isProcessing || isGenerating"
        class="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors" title="Rehacer"
        @click="visualizerStore.redo()">
        <Icon name="lucide:redo-2" class="w-5 h-5" />
      </button>

      <div class="w-px h-6 bg-black/10" />

      <!-- Reset -->
      <button :disabled="isProcessing || isGenerating"
        class="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors" title="Reiniciar"
        @click="visualizerStore.reset()">
        <Icon name="lucide:rotate-ccw" class="w-5 h-5" />
      </button>

      <div class="w-px h-6 bg-black/10" />

      <!-- Download -->
      <button :disabled="isProcessing || isGenerating"
        class="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors" title="Descargar"
        @click="exportAndDownload">
        <Icon name="lucide:download" class="w-5 h-5" />
      </button>

      <!-- Generate with AI -->
      <button :disabled="isGenerating || isProcessing" :class="[
        'p-2 transition-colors disabled:opacity-30',
        generatedImage ? 'text-violet-500 hover:text-violet-700' : 'text-fuchsia-500 hover:text-fuchsia-600',
      ]" title="Generar con IA" @click="handleGenerate">
        <Icon :name="isGenerating ? 'lucide:loader-2' : 'lucide:sparkles'"
          :class="['w-5 h-5', isGenerating && 'animate-spin']" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
