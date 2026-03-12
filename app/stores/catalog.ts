import { defineStore } from 'pinia'
import type { Product, ProductCategory, Brand } from '~/types/product'

export const useCatalogStore = defineStore('catalog', () => {
  const products = ref<Product[]>([])
  const categories = ref<ProductCategory[]>([])
  const brands = ref<Brand[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const selectedCategory = ref<ProductCategory | null>(null)
  const selectedBrand = ref<string | null>(null)
  const searchQuery = ref('')
  const priceRange = ref<[number, number]>([0, 100000])

  const filteredProducts = computed(() => {
    let result = products.value
    if (selectedCategory.value) {
      result = result.filter(p => p.category === selectedCategory.value)
    }
    if (selectedBrand.value) {
      result = result.filter(p => p.brand.slug === selectedBrand.value)
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter(
        p =>
          p.name.toLowerCase().includes(q) ||
          p.nameEs.toLowerCase().includes(q) ||
          p.brand.name.toLowerCase().includes(q) ||
          p.tags.some(t => t.toLowerCase().includes(q)),
      )
    }
    result = result.filter(
      p => p.price >= priceRange.value[0] && p.price <= priceRange.value[1],
    )
    return result
  })

  async function fetchProducts() {
    if (products.value.length > 0) return
    isLoading.value = true
    error.value = null
    try {
      const data = await $fetch<Product[]>('/api/products')
      products.value = data
    } catch (e) {
      error.value = 'Error cargando productos'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchCategories() {
    if (categories.value.length > 0) return
    try {
      const data = await $fetch<ProductCategory[]>('/api/products/categories')
      categories.value = data
    } catch {
      // fallback silently
    }
  }

  function setCategory(category: ProductCategory | null) {
    selectedCategory.value = category
  }

  function setBrand(brandSlug: string | null) {
    selectedBrand.value = brandSlug
  }

  function setSearch(query: string) {
    searchQuery.value = query
  }

  return {
    products,
    categories,
    brands,
    isLoading,
    error,
    selectedCategory,
    selectedBrand,
    searchQuery,
    priceRange,
    filteredProducts,
    fetchProducts,
    fetchCategories,
    setCategory,
    setBrand,
    setSearch,
  }
})
