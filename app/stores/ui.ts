import { defineStore } from 'pinia'

export interface Toast {
  id: string
  type: 'success' | 'error' | 'info' | 'warning'
  title: string
  message?: string
  duration?: number
}

export const useUiStore = defineStore('ui', () => {
  const toasts = ref<Toast[]>([])
  const isBottomSheetOpen = ref(false)
  const bottomSheetContent = ref<string | null>(null)
  const isMobileMenuOpen = ref(false)
  const isSearchOpen = ref(false)
  const visualizerSidebarTab = ref<'products' | 'bom' | 'analysis'>('products')

  function addToast(toast: Omit<Toast, 'id'>) {
    const id = crypto.randomUUID()
    toasts.value.push({ ...toast, id })
    setTimeout(() => removeToast(id), toast.duration ?? 4000)
  }

  function removeToast(id: string) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  function openBottomSheet(content: string) {
    bottomSheetContent.value = content
    isBottomSheetOpen.value = true
  }

  function closeBottomSheet() {
    isBottomSheetOpen.value = false
    bottomSheetContent.value = null
  }

  return {
    toasts,
    isBottomSheetOpen,
    bottomSheetContent,
    isMobileMenuOpen,
    isSearchOpen,
    visualizerSidebarTab,
    addToast,
    removeToast,
    openBottomSheet,
    closeBottomSheet,
  }
})
