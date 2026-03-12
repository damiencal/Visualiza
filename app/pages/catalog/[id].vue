<script setup lang="ts">
import type { Product } from '~/types'

const route = useRoute()
const router = useRouter()

const { data: product, error } = await useAsyncData(
  `product-${route.params.id}`,
  () => $fetch<Product>(`/api/products/${route.params.id}`),
)

if (error.value) throw createError({ statusCode: 404, statusMessage: 'Producto no encontrado' })

useSeoMeta({
  title: computed(() => `${product.value?.nameEs ?? product.value?.name ?? 'Producto'} - Visualiza`),
  ogImage: computed(() => product.value?.images?.main ?? ''),
})

const { formatPrice } = useFormatPrice()

function visualize() {
  router.push({ path: '/visualizer', query: { productId: product.value?.id } })
}
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm text-text-secondary mb-6">
      <NuxtLink to="/" class="hover:text-text-primary">Inicio</NuxtLink>
      <Icon name="lucide:chevron-right" class="w-3.5 h-3.5" />
      <NuxtLink to="/catalog" class="hover:text-text-primary">Catálogo</NuxtLink>
      <Icon name="lucide:chevron-right" class="w-3.5 h-3.5" />
      <span class="text-text-primary">{{ product?.nameEs ?? product?.name }}</span>
    </nav>

    <div v-if="product" class="grid md:grid-cols-2 gap-10">
      <!-- Image -->
      <div class="aspect-square rounded-3xl overflow-hidden bg-surface-100 shadow-card">
        <img :src="product.images.main" :alt="product.nameEs ?? product.name" class="w-full h-full object-cover" />
      </div>

      <!-- Info -->
      <div class="flex flex-col gap-4">
        <div>
          <p class="text-xs text-text-tertiary font-medium uppercase tracking-wide mb-1">{{ product.brand.name }}</p>
          <h1 class="text-3xl font-bold text-text-primary">{{ product.nameEs ?? product.name }}</h1>
        </div>

        <p class="text-primary font-black text-3xl">
          {{ formatPrice(product.price, product.currency) }}
        </p>

        <p v-if="product.description" class="text-text-secondary leading-relaxed text-sm">{{ product.description }}</p>

        <!-- Texture -->
        <div v-if="product.images.texture" class="flex items-center gap-3 glass-card p-3">
          <div class="w-12 h-12 rounded-xl overflow-hidden">
            <img :src="product.images.texture" alt="Textura" class="w-full h-full object-cover" />
          </div>
          <div>
            <p class="text-xs text-text-tertiary">Vista de textura</p>
            <p class="text-sm font-medium">Escala {{ product.textureScale ?? 1 }}x</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 mt-2">
          <button v-if="product.visualizerCompatible" class="btn-primary flex-1 flex items-center justify-center gap-2"
            @click="visualize">
            <Icon name="lucide:wand-2" class="w-4 h-4" />
            Visualizar en tu hogar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
