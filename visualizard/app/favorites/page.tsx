'use client';

import { useState } from 'react';
import { useFavorites } from '@/contexts/FavoritesContext';
import { mockProperties, mockProducts } from '@/lib/mock-data';
import PropertyCard from '@/components/property/PropertyCard';
import Image from 'next/image';
import { Heart, Star, Sparkles } from 'lucide-react';
import { formatPrice } from '@/lib/utils';
import FavoriteButton from '@/components/property/FavoriteButton';

export default function FavoritesPage() {
  const { favoriteProperties, favoriteProducts } = useFavorites();
  const [activeTab, setActiveTab] = useState<'properties' | 'products'>('properties');

  const favProps = mockProperties.filter(p => favoriteProperties.includes(p.id));
  const favProds = mockProducts.filter(p => favoriteProducts.includes(p.id));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-text-primary mb-2">Tus Favoritos</h1>
        <p className="text-text-secondary">Guarda tus propiedades y productos favoritos para verlos más tarde.</p>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-4 mb-8 border-b border-black/10">
        <button
          onClick={() => setActiveTab('properties')}
          className={`pb-4 px-2 text-sm font-semibold transition-colors relative ${
            activeTab === 'properties' ? 'text-primary' : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          Propiedades ({favProps.length})
          {activeTab === 'properties' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-t-full"></div>
          )}
        </button>
        <button
          onClick={() => setActiveTab('products')}
          className={`pb-4 px-2 text-sm font-semibold transition-colors relative ${
            activeTab === 'products' ? 'text-primary' : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          Productos ({favProds.length})
          {activeTab === 'products' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-t-full"></div>
          )}
        </button>
      </div>

      {/* Content */}
      {activeTab === 'properties' ? (
        favProps.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {favProps.map(property => (
              <PropertyCard key={property.id} property={property} />
            ))}
          </div>
        ) : (
          <EmptyState type="properties" />
        )
      ) : (
        favProds.length > 0 ? (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            {favProds.map(product => (
              <div key={product.id} className="glass-card group overflow-hidden flex flex-col">
                <div className="relative aspect-square bg-gray-100 overflow-hidden">
                  <Image
                    src={product.images.full}
                    alt={product.name}
                    fill
                    className="object-cover transition-transform duration-500 group-hover:scale-105"
                    unoptimized
                  />
                  <FavoriteButton id={product.id} type="product" className="absolute top-2 right-2" />
                  
                  {product.visualizerCompatible && (
                    <div className="absolute top-2 left-2 chip bg-white/80 backdrop-blur-sm text-[10px] px-2 py-1 shadow-sm">
                      <Sparkles className="w-3 h-3 text-primary mr-1" />
                      <span className="hidden sm:inline">Visualizable</span>
                    </div>
                  )}
                </div>
                
                <div className="p-4 flex flex-col flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-xs font-semibold text-text-tertiary uppercase tracking-wider">{product.brand.name}</p>
                    <div className="flex items-center gap-1 text-xs font-medium text-amber-500">
                      <Star className="w-3 h-3 fill-current" />
                      {product.rating}
                    </div>
                  </div>
                  
                  <h3 className="font-bold text-text-primary text-sm md:text-base line-clamp-2 mb-2 flex-1">{product.name}</h3>
                  
                  <div className="flex items-end justify-between mt-auto pt-2 border-t border-black/5">
                    <div>
                      <span className="text-lg font-bold text-primary">{formatPrice(product.price, product.currency)}</span>
                      <span className="text-xs text-text-secondary ml-1">/ {product.unit}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <EmptyState type="products" />
        )
      )}
    </div>
  );
}

function EmptyState({ type }: { type: 'properties' | 'products' }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 glass-panel rounded-3xl text-center px-4">
      <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-6 shadow-inner-soft">
        <Heart className="w-10 h-10 text-primary opacity-50" />
      </div>
      <h3 className="text-xl font-bold text-text-primary mb-2">
        No tienes {type === 'properties' ? 'propiedades' : 'productos'} guardados
      </h3>
      <p className="text-text-secondary max-w-md mb-8">
        Explora nuestro catálogo y guarda los que más te gusten tocando el ícono de corazón.
      </p>
      <a href={type === 'properties' ? '/properties' : '/catalog'} className="btn-primary">
        Explorar {type === 'properties' ? 'Propiedades' : 'Catálogo'}
      </a>
    </div>
  );
}
