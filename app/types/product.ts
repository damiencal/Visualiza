export type SurfaceType = 'floor' | 'wall' | 'ceiling' | 'countertop' | 'exterior'

export type ProductCategory =
  | 'flooring'
  | 'paint'
  | 'tile'
  | 'wallpaper'
  | 'furniture'
  | 'fixtures'
  | 'lighting'
  | 'countertops'
  | 'rugs'
  | 'curtains'
  | 'appliances'

export interface Brand {
  id: string
  name: string
  slug: string
  logo: string
  country: string
  description: string
  website?: string
}

export interface Product {
  id: string
  name: string
  nameEs: string
  slug: string
  brand: Brand
  category: ProductCategory
  subcategory: string
  description: string
  descriptionEs: string
  price: number
  currency: 'DOP' | 'USD'
  unit: string
  sku: string
  images: {
    thumbnail: string
    full: string
    texture: string
    textureScale: number
  }
  specs: Record<string, string>
  colors: string[]
  inStock: boolean
  rating: number
  reviewCount: number
  tags: string[]
  visualizerCompatible: boolean
  surfaceTypes: SurfaceType[]
}
