<script setup lang="ts">
import type { Product } from '~/types'

const visualizerStore = useVisualizerStore()
const uiStore = useUiStore()
const { session, selectedSurfaceId, bom, generatedImage } = storeToRefs(visualizerStore)
const { visualizerSidebarTab: activeTab } = storeToRefs(uiStore)

const { data: products } = await useAsyncData('viz-products', () =>
  $fetch<Product[]>('/api/products'),
)

// Category tabs matching visualizard
const categories = [
  { id: 'flooring', label: 'Pisos' },
  { id: 'paint', label: 'Pintura' },
  { id: 'furniture', label: 'Muebles' },
]

const activeCategory = ref('flooring')
const searchQuery = ref('')

const filteredProducts = computed(() => {
  if (!products.value) return []
  return products.value.filter(p => {
    if (p.category !== activeCategory.value) return false
    if (searchQuery.value && !p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) && !p.nameEs?.toLowerCase().includes(searchQuery.value.toLowerCase())) return false
    return true
  })
})

const selectedProductId = ref<string | null>(null)

function handleSelectProduct(product: Product) {
  selectedProductId.value = product.id
  // Auto-add surface if none selected
  if (!selectedSurfaceId.value && session.value) {
    const typeMap: Record<string, 'floor' | 'wall' | 'ceiling'> = {
      flooring: 'floor',
      paint: 'wall',
      furniture: 'floor',
    }
    visualizerStore.addSurface(typeMap[activeCategory.value] ?? 'floor')
  }
  if (selectedSurfaceId.value) {
    visualizerStore.applyProduct(selectedSurfaceId.value, product)
  } else {
    uiStore.addToast({ type: 'info', title: 'Selecciona una superficie', message: 'Elige piso, pared o techo primero.' })
  }
}

const { formatPrice } = useFormatPrice()
</script>

<template>
  <div
    class="w-full h-full flex flex-col bg-white/80 backdrop-blur-xl border-l border-white/40 shadow-[-10px_0_30px_-15px_rgba(0,0,0,0.1)]">
    <!-- Header -->
    <div class="p-4 border-b border-black/5">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-bold text-text-primary">Catálogo de Productos</h2>
        <!-- BoM and AI icon buttons -->
        <div class="flex items-center gap-1">
          <button :class="[
            'w-8 h-8 rounded-xl flex items-center justify-center transition-colors',
            activeTab === 'bom' ? 'bg-primary/10 text-primary' : 'text-text-secondary hover:text-primary hover:bg-black/[0.04]',
          ]" title="Presupuesto" @click="uiStore.visualizerSidebarTab = 'bom'">
            <div class="relative">
              <Icon name="lucide:clipboard-list" class="w-4 h-4" />
              <span v-if="bom.length"
                class="absolute -top-1.5 -right-1.5 min-w-[14px] h-3.5 flex items-center justify-center bg-primary text-white text-[9px] font-bold rounded-full px-0.5">{{
                bom.length }}</span>
            </div>
          </button>
          <button v-if="activeTab !== 'products'"
            class="w-8 h-8 rounded-xl flex items-center justify-center text-text-secondary hover:text-primary hover:bg-black/[0.04] transition-colors"
            title="Volver a productos" @click="uiStore.visualizerSidebarTab = 'products'">
            <Icon name="lucide:x" class="w-4 h-4" />
          </button>
        </div>
      </div>

      <template v-if="activeTab === 'products'">
        <!-- Search -->
        <div class="relative mb-4">
          <Icon name="lucide:search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
          <input v-model="searchQuery" type="text" placeholder="Buscar productos..."
            class="input-glass w-full pl-9 py-2 text-sm" />
        </div>

        <!-- Category chips -->
        <div class="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
          <button v-for="cat in categories" :key="cat.id"
            :class="['chip whitespace-nowrap text-xs', activeCategory === cat.id ? 'chip-active' : '']"
            @click="activeCategory = cat.id">
            {{ cat.label }}
          </button>
        </div>
      </template>
    </div>

    <!-- Products tab -->
    <template v-if="activeTab === 'products'">
      <div class="flex-1 overflow-y-auto overscroll-contain scrollbar-hide p-4 space-y-4">
        <template v-if="filteredProducts.length">
          <div v-for="product in filteredProducts" :key="product.id" :class="[
            'glass-card p-3 flex gap-4 cursor-pointer transition-all',
            selectedProductId === product.id ? 'ring-2 ring-primary bg-primary/5' : 'hover:bg-white/90',
          ]" @click="handleSelectProduct(product)">
            <!-- Thumbnail -->
            <div class="relative w-20 h-20 rounded-xl overflow-hidden flex-shrink-0 bg-gray-100">
              <img :src="product.images.texture || product.images.thumbnail" :alt="product.nameEs || product.name"
                class="w-full h-full object-cover" />
              <div v-if="selectedProductId === product.id"
                class="absolute inset-0 bg-primary/20 flex items-center justify-center backdrop-blur-[1px]">
                <div class="w-6 h-6 bg-primary rounded-full flex items-center justify-center shadow-glow">
                  <Icon name="lucide:check" class="w-4 h-4 text-white" />
                </div>
              </div>
            </div>
            <!-- Info -->
            <div class="flex-1 min-w-0 flex flex-col justify-center">
              <p class="text-xs font-medium text-text-tertiary uppercase tracking-wider mb-1">{{ product.brand.name }}
              </p>
              <h3 class="text-sm font-bold text-text-primary truncate mb-1">{{ product.nameEs || product.name }}</h3>
              <p class="text-sm font-semibold text-primary">
                {{ formatPrice(product.price, product.currency) }}
                <span class="text-xs text-text-secondary font-normal">/ {{ product.unit }}</span>
              </p>
            </div>
          </div>
        </template>

        <SharedEmptyState v-else icon="lucide:package-x" title="Sin productos"
          description="No se encontraron productos para esta categoría." />
      </div>
    </template>

    <!-- BoM tab -->
    <div v-else-if="activeTab === 'bom'" class="flex-1 overflow-hidden">
      <VisualizerBillOfMaterials class="h-full" />
    </div>

    <!-- AI Analysis tab -->
    <div v-else-if="activeTab === 'analysis'" class="flex-1 overflow-hidden">
      <VisualizerAIDesignAnalysis class="h-full" />
    </div>
  </div>
</template>
