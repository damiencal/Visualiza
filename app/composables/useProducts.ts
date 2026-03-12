import type { Product, ProductCategory, SurfaceType } from '~/types/product'
import { useCatalogStore } from '~/stores/catalog'

export const useProducts = () => {
  const store = useCatalogStore()

  function getProductsBySurface(surfaceType: SurfaceType): Product[] {
    return store.filteredProducts.filter(p => p.surfaceTypes.includes(surfaceType))
  }

  function getProductById(id: string): Product | undefined {
    return store.products.find(p => p.id === id)
  }

  return {
    ...store,
    getProductsBySurface,
    getProductById,
  }
}
