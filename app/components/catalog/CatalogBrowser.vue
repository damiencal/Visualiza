<script setup lang="ts">
import type { Product, ProductCategory } from '~/types'

const { data: productsData, pending } = await useAsyncData('catalog-products', () => $fetch('/api/products'))

const selectedCategory = ref<ProductCategory | ''>('')
const searchQuery = ref('')
const quickViewProduct = ref<Product | null>(null)
const showQuickView = ref(false)

const filtered = computed(() => {
  let list: Product[] = (productsData.value as Product[]) ?? []
  if (selectedCategory.value) list = list.filter(p => p.category === selectedCategory.value)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.name.toLowerCase().includes(q) ||
      (p.nameEs?.toLowerCase().includes(q)) ||
      p.brand.toLowerCase().includes(q),
    )
  }
  return list
})

function openQuickView(product: Product) {
  quickViewProduct.value = product
  showQuickView.value = true
}
</script>

<template>
  <div>
    <!-- Filters bar -->
    <div class="space-y-3 mb-6">
      <CatalogSearchBar v-model="searchQuery" />
      <CatalogCategoryNav v-model="selectedCategory" />
    </div>

    <!-- Results count -->
    <p class="text-xs text-text-tertiary mb-4" aria-live="polite">
      {{ filtered.length }} producto{{ filtered.length !== 1 ? 's' : '' }}
    </p>

    <!-- Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      <template v-if="pending">
        <SharedSkeletonCard v-for="i in 10" :key="i" type="product" />
      </template>
      <template v-else-if="filtered.length">
        <CatalogProductCard
          v-for="product in filtered"
          :key="product.id"
          :product="product"
          @quick-view="openQuickView"
        />
      </template>
      <template v-else>
        <div class="col-span-full">
          <SharedEmptyState
            icon="lucide:package-x"
            title="Sin productos"
            description="No encontramos productos. Intenta cambiar los filtros."
          />
        </div>
      </template>
    </div>

    <!-- Quick view bottom sheet -->
    <CatalogProductQuickView v-model="showQuickView" :product="quickViewProduct" />
  </div>
</template>
