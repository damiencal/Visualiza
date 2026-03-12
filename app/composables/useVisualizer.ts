import type { VisualizerSession, Surface, VisualizerLayer } from '~/types/visualizer'
import type { Product } from '~/types/product'
import type { RoomType } from '~/types/property'
import { useVisualizerStore } from '~/stores/visualizer'

export const useVisualizer = () => {
  const store = useVisualizerStore()
  const canvas = ref<HTMLCanvasElement | null>(null)
  const originalImageData = ref<ImageData | null>(null)

  const ctx = computed(() => canvas.value?.getContext('2d') ?? null)

  async function loadRoomImage(imageUrl: string, roomType: RoomType = 'living-room') {
    store.isProcessing = true
    try {
      const img = new Image()
      img.crossOrigin = 'anonymous'
      img.src = imageUrl

      await new Promise<void>((resolve, reject) => {
        img.onload = () => resolve()
        img.onerror = () => reject(new Error('Failed to load image'))
      })

      if (canvas.value && ctx.value) {
        canvas.value.width = img.naturalWidth || img.width
        canvas.value.height = img.naturalHeight || img.height
        ctx.value.drawImage(img, 0, 0)
        originalImageData.value = ctx.value.getImageData(
          0,
          0,
          canvas.value.width,
          canvas.value.height,
        )
      }

      store.createSession(imageUrl, roomType)
    } finally {
      store.isProcessing = false
    }
  }

  async function applyProductToSurface(surface: Surface, product: Product) {
    if (!ctx.value || !canvas.value) return
    store.isProcessing = true

    try {
      const textureImg = new Image()
      textureImg.crossOrigin = 'anonymous'
      textureImg.src = product.images.texture

      await new Promise<void>((resolve, reject) => {
        textureImg.onload = () => resolve()
        textureImg.onerror = () => reject(new Error('Failed to load texture'))
      })

      const scale = product.images.textureScale || 1
      const offscreen = document.createElement('canvas')
      offscreen.width = textureImg.width * scale
      offscreen.height = textureImg.height * scale
      const offCtx = offscreen.getContext('2d')
      if (offCtx) {
        offCtx.drawImage(textureImg, 0, 0, offscreen.width, offscreen.height)
      }

      const pattern = ctx.value.createPattern(offscreen, 'repeat')
      if (!pattern) return

      ctx.value.save()
      ctx.value.globalCompositeOperation = 'multiply'
      ctx.value.globalAlpha = 0.65
      if (pattern) {
        ctx.value.fillStyle = pattern
        ctx.value.fillRect(0, 0, canvas.value.width, canvas.value.height)
      }
      ctx.value.restore()

      store.applyProduct(surface.id, product)

      const thumbnail = canvas.value.toDataURL('image/jpeg', 0.3)
      store.pushSnapshot(thumbnail)
    } finally {
      store.isProcessing = false
    }
  }

  function restoreOriginal() {
    if (!ctx.value || !canvas.value || !originalImageData.value) return
    ctx.value.putImageData(originalImageData.value, 0, 0)
  }

  function exportImage(): string | null {
    return canvas.value?.toDataURL('image/png') ?? null
  }

  async function downloadImage(filename = 'visualiza-result.png') {
    const dataUrl = exportImage()
    if (!dataUrl) return
    const link = document.createElement('a')
    link.download = filename
    link.href = dataUrl
    link.click()
  }

  function undo() {
    store.undo()
  }

  function redo() {
    store.redo()
  }

  function reset() {
    store.reset()
    restoreOriginal()
  }

  return {
    canvas,
    store,
    ctx,
    loadRoomImage,
    applyProductToSurface,
    restoreOriginal,
    exportImage,
    downloadImage,
    undo,
    redo,
    reset,
  }
}
