<script setup lang="ts">
import type { Product } from '~/types'

useSeoMeta({ title: 'Mis Favoritos - Visualisa' })

const { favoriteProductIds } = useFavorites()

const { data: allProducts } = await useAsyncData('fav-products', () => $fetch<Product[]>('/api/products'))

const favProducts = computed(() =>
  (allProducts.value ?? []).filter(p => favoriteProductIds.value.includes(p.id)),
)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <h1 class="text-3xl font-bold text-text-primary mb-6">Mis Favoritos</h1>

    <div v-if="favProducts.length" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <CatalogProductCard v-for="product in favProducts" :key="product.id" :product="product" />
    </div>
    <SharedEmptyState v-else icon="lucide:package" title="Sin productos favoritos"
      description="Guarda productos del catálogo para verlos aquí." action-label="Ver catálogo" action-to="/catalog" />
  </div>
</template>
