'use client';

import { useState } from 'react';
import Image from 'next/image';
import { mockProducts } from '@/lib/mock-data';
import { Search, Filter, Star, Sparkles } from 'lucide-react';
import { formatPrice } from '@/lib/utils';
import FavoriteButton from '@/components/property/FavoriteButton';

export default function CatalogPage() {
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'all', label: 'Todos' },
    { id: 'flooring', label: 'Pisos' },
    { id: 'paint', label: 'Pintura' },
    { id: 'furniture', label: 'Muebles' },
    { id: 'lighting', label: 'Iluminación' },
  ];

  const filteredProducts = mockProducts.filter(p => {
    if (activeCategory !== 'all' && p.category !== activeCategory) return false;
    if (searchQuery && !p.name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-text-primary mb-2">Catálogo de Productos</h1>
          <p className="text-text-secondary">Explora materiales y muebles de los mejores suplidores en RD.</p>
        </div>
        
        <div className="flex items-center gap-4 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <input 
              type="text" 
              placeholder="Buscar productos..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-glass w-full pl-10 py-2.5 text-sm"
            />
          </div>
          <button className="btn-soft p-2.5 md:hidden">
            <Filter className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Categories */}
      <div className="flex items-center gap-2 overflow-x-auto pb-4 mb-6 scrollbar-hide">
        {categories.map(cat => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`chip whitespace-nowrap px-4 py-2 ${activeCategory === cat.id ? 'chip-active' : ''}`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Grid */}
      {filteredProducts.length > 0 ? (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
          {filteredProducts.map(product => (
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
        <div className="text-center py-20 glass-panel rounded-2xl">
          <p className="text-text-secondary text-lg">No se encontraron productos.</p>
          <button 
            onClick={() => { setActiveCategory('all'); setSearchQuery(''); }}
            className="btn-soft mt-4"
          >
            Limpiar filtros
          </button>
        </div>
      )}
    </div>
  );
}
