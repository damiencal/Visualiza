import productsData from '../../data/products.json'
import type { Product } from '~/types/product'

export default defineEventHandler((event) => {
  const query = getQuery(event)
  let products = productsData as Product[]

  if (query.category) {
    products = products.filter(p => p.category === query.category)
  }
  if (query.brand) {
    products = products.filter(p => p.brand.slug === query.brand)
  }
  if (query.surface) {
    products = products.filter(p => p.surfaceTypes.includes(query.surface as string))
  }
  if (query.visualizer === 'true') {
    products = products.filter(p => p.visualizerCompatible)
  }
  if (query.q) {
    const q = (query.q as string).toLowerCase()
    products = products.filter(
      p =>
        p.name.toLowerCase().includes(q) ||
        p.nameEs.toLowerCase().includes(q) ||
        p.brand.name.toLowerCase().includes(q),
    )
  }

  return products
})
