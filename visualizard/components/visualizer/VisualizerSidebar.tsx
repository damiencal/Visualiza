'use client';

import { useState } from 'react';
import Image from 'next/image';
import { Product } from '@/types';
import { mockProducts } from '@/lib/mock-data';
import { Search, ChevronDown, Check } from 'lucide-react';
import { formatPrice } from '@/lib/utils';

interface VisualizerSidebarProps {
  onSelectProduct: (product: Product) => void;
  selectedProductId?: string;
}

export default function VisualizerSidebar({ 
  onSelectProduct, 
  selectedProductId
}: VisualizerSidebarProps) {
  const [activeCategory, setActiveCategory] = useState<string>('flooring');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'flooring', label: 'Pisos' },
    { id: 'paint', label: 'Pintura' },
    { id: 'furniture', label: 'Muebles' },
  ];

  const filteredProducts = mockProducts.filter(p => {
    if (p.category !== activeCategory) return false;
    if (searchQuery && !p.name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="w-full h-full flex flex-col bg-white/80 backdrop-blur-xl border-l border-white/40 shadow-[-10px_0_30px_-15px_rgba(0,0,0,0.1)]">
      {/* Header */}
      <div className="p-4 border-b border-black/5">
        <h2 className="text-lg font-bold text-text-primary mb-4">Catálogo de Productos</h2>
        
        {/* Search */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
          <input 
            type="text" 
            placeholder="Buscar productos..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-glass w-full pl-10 py-2 text-sm"
          />
        </div>

        {/* Categories */}
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`chip whitespace-nowrap text-xs ${activeCategory === cat.id ? 'chip-active' : ''}`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Product List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {filteredProducts.length > 0 ? (
          filteredProducts.map(product => {
            const isSelected = selectedProductId === product.id;
            return (
              <div 
                key={product.id}
                onClick={() => onSelectProduct(product)}
                className={`glass-card p-3 flex gap-4 cursor-pointer transition-all ${isSelected ? 'ring-2 ring-primary bg-primary/5' : 'hover:bg-white/90'}`}
              >
                <div className="relative w-20 h-20 rounded-xl overflow-hidden flex-shrink-0 bg-gray-100">
                  <Image
                    src={product.images.thumbnail}
                    alt={product.name}
                    fill
                    className="object-cover"
                    unoptimized
                  />
                  {isSelected && (
                    <div className="absolute inset-0 bg-primary/20 flex items-center justify-center backdrop-blur-[1px]">
                      <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center shadow-glow">
                        <Check className="w-4 h-4 text-white" />
                      </div>
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0 flex flex-col justify-center">
                  <p className="text-xs font-medium text-text-tertiary uppercase tracking-wider mb-1">{product.brand.name}</p>
                  <h3 className="text-sm font-bold text-text-primary truncate mb-1">{product.name}</h3>
                  <p className="text-sm font-semibold text-primary">{formatPrice(product.price, product.currency)} <span className="text-xs text-text-secondary font-normal">/ {product.unit}</span></p>
                </div>
              </div>
            );
          })
        ) : (
          <div className="text-center py-10">
            <p className="text-text-secondary text-sm">No se encontraron productos.</p>
          </div>
        )}
      </div>
    </div>
  );
}
