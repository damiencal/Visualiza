<script setup lang="ts">
import type { Product } from '~/types'

interface Props {
  product: Product
}

defineProps<Props>()
const emit = defineEmits<{ 'quick-view': [product: Product] }>()

const { formatPrice } = useFormatPrice()

const categoryLabels: Record<string, string> = {
  flooring: 'Piso', paint: 'Pintura', tile: 'Cerámica', furniture: 'Mueble',
  fixtures: 'Accesorio', lighting: 'Iluminación', curtains: 'Cortina',
  rugs: 'Alfombra', wallpaper: 'Empapelado', countertops: 'Encimera', appliances: 'Electrodoméstico',
}
</script>

<template>
  <div class="glass-card overflow-hidden flex flex-col group">
    <!-- Image -->
    <div class="relative h-44 overflow-hidden bg-surface-100">
      <img :src="product.images.main" :alt="product.nameEs || product.name"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />

      <!-- Quick view button -->
      <button
        class="absolute inset-0 flex items-end justify-center pb-3 opacity-0 group-hover:opacity-100 transition-opacity bg-gradient-to-t from-black/30 to-transparent"
        :aria-label="`Vista rápida: ${product.nameEs || product.name}`" @click="emit('quick-view', product)">
        <span class="text-white text-xs font-medium bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
          Vista rápida
        </span>
      </button>

      <!-- Visualizer badge -->
      <div v-if="product.visualizerCompatible"
        class="absolute top-2 right-2 w-7 h-7 bg-primary rounded-full flex items-center justify-center shadow-glow"
        title="Compatible con visualisador">
        <Icon name="lucide:wand-2" class="w-3.5 h-3.5 text-white" />
      </div>
    </div>

    <!-- Content -->
    <div class="p-3 flex flex-col gap-0.5 flex-1">
      <p class="text-xs text-text-tertiary">{{ product.brand.name }} · {{ categoryLabels[product.category] ??
        product.category }}</p>
      <h3 class="font-medium text-text-primary text-sm leading-tight line-clamp-2">
        {{ product.nameEs || product.name }}
      </h3>
      <div class="flex items-center justify-between mt-auto pt-2">
        <p class="font-bold text-text-primary text-sm">
          {{ formatPrice(product.price, product.currency) }}
        </p>
      </div>
    </div>
  </div>
</template>
