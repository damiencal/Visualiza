import productsData from '../../data/products.json'
import type { Product, ProductCategory } from '~/types/product'

export default defineEventHandler(() => {
  const products = productsData as Product[]
  const categories = [...new Set(products.map(p => p.category))] as ProductCategory[]
  return categories
})
