import productsData from '../../data/products.json'
import type { Product } from '~/types/product'

export default defineEventHandler((event) => {
  const id = getRouterParam(event, 'id')
  const products = productsData as Product[]
  const product = products.find(p => p.id === id || p.slug === id)
  if (!product) {
    throw createError({ statusCode: 404, statusMessage: 'Product not found' })
  }
  return product
})
