<script setup lang="ts">
import type { Product } from '~/types'

interface Props {
  modelValue: boolean
  product: Product | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [v: boolean] }>()

const { formatPrice } = useFormatPrice()
const router = useRouter()

function visualize() {
  emit('update:modelValue', false)
  router.push({ path: '/visualizer', query: { productId: props.product?.id } })
}
</script>

<template>
  <SharedBottomSheet
    :model-value="modelValue"
    :title="product?.nameEs || product?.name || ''"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <div v-if="product" class="p-5 space-y-5">
      <!-- Image -->
      <div class="aspect-square rounded-2xl overflow-hidden bg-surface-100">
        <img
          :src="product.images.main"
          :alt="product.nameEs || product.name"
          class="w-full h-full object-cover"
        />
      </div>

      <!-- Info -->
      <div>
        <p class="text-xs text-text-tertiary mb-1">{{ product.brand.name }}</p>
        <h2 class="font-bold text-xl text-text-primary mb-2">{{ product.nameEs || product.name }}</h2>
        <p class="text-primary font-bold text-2xl">
          {{ formatPrice(product.price, product.currency) }}
        </p>
      </div>

      <p v-if="product.description" class="text-sm text-text-secondary leading-relaxed">
        {{ product.description }}
      </p>

      <!-- Texture preview -->
      <div v-if="product.images.texture" class="flex items-center gap-3">
        <div class="w-14 h-14 rounded-xl overflow-hidden border border-black/10">
          <img :src="product.images.texture" alt="Textura" class="w-full h-full object-cover" />
        </div>
        <div>
          <p class="text-xs text-text-tertiary">Textura del producto</p>
          <p class="text-sm font-medium">Escala {{ product.textureScale ?? 1 }}x</p>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex gap-3">
        <button
          v-if="product?.visualizerCompatible"
          class="btn-primary flex-1 flex items-center justify-center gap-2"
          @click="visualize"
        >
          <Icon name="lucide:wand-2" class="w-4 h-4" />
          Visualizar
        </button>
        <NuxtLink
          v-if="product"
          :to="`/catalog/${product.slug}`"
          class="btn-soft flex-1 text-center"
          @click="emit('update:modelValue', false)"
        >
          Ver detalles
        </NuxtLink>
      </div>
    </template>
  </SharedBottomSheet>
</template>
