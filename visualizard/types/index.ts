export interface Property {
  id: string;
  title: string;
  slug: string;
  description: string;
  price: number;
  priceUSD?: number;
  currency: 'DOP' | 'USD';
  location: {
    address: string;
    city: string;
    province: string;
    neighborhood: string;
    coordinates: { lat: number; lng: number };
  };
  specs: {
    bedrooms: number;
    bathrooms: number;
    area: number;
    parking: number;
    yearBuilt?: number;
  };
  images: PropertyImage[];
  features: string[];
  type: 'apartment' | 'house' | 'penthouse' | 'villa' | 'studio' | 'commercial';
  status: 'available' | 'reserved' | 'sold';
  agent: {
    name: string;
    phone: string;
    avatar: string;
  };
  createdAt: string;
  isFeatured: boolean;
}

export interface PropertyImage {
  id: string;
  url: string;
  alt: string;
  room: RoomType;
  isVisualizerReady: boolean;
  segmentationMask?: string;
  width: number;
  height: number;
}

export type RoomType =
  | 'living-room' | 'bedroom' | 'kitchen'
  | 'bathroom' | 'dining-room' | 'office'
  | 'balcony' | 'exterior' | 'other';

export interface Product {
  id: string;
  name: string;
  nameEs: string;
  slug: string;
  brand: Brand;
  category: ProductCategory;
  subcategory: string;
  description: string;
  descriptionEs: string;
  price: number;
  currency: 'DOP' | 'USD';
  unit: string;
  sku: string;
  images: {
    thumbnail: string;
    full: string;
    texture: string;
    textureScale: number;
  };
  specs: Record<string, string>;
  colors: string[];
  inStock: boolean;
  rating: number;
  reviewCount: number;
  tags: string[];
  visualizerCompatible: boolean;
  surfaceTypes: SurfaceType[];
}

export type SurfaceType = 'floor' | 'wall' | 'ceiling' | 'countertop' | 'exterior';

export type ProductCategory =
  | 'flooring' | 'paint' | 'tile'
  | 'wallpaper' | 'furniture' | 'fixtures'
  | 'lighting' | 'countertops' | 'rugs'
  | 'curtains' | 'appliances';

export interface Brand {
  id: string;
  name: string;
  slug: string;
  logo: string;
  country: string;
  description: string;
  website?: string;
}
