'use client';

import { useState } from 'react';
import { mockProperties } from '@/lib/mock-data';
import PropertyCard from '@/components/property/PropertyCard';
import { Filter } from 'lucide-react';

export default function PropertiesPage() {
  const [activeType, setActiveType] = useState<string>('all');
  const [activeCity, setActiveCity] = useState<string>('all');

  const types = ['all', 'apartment', 'house', 'villa', 'studio', 'penthouse'];
  const cities = ['all', 'Santo Domingo', 'Punta Cana', 'Santiago de los Caballeros'];

  const filteredProperties = mockProperties.filter(p => {
    if (activeType !== 'all' && p.type !== activeType) return false;
    if (activeCity !== 'all' && p.location.city !== activeCity) return false;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-text-primary mb-2">Propiedades en Venta</h1>
          <p className="text-text-secondary">Encuentra el espacio perfecto para tu próximo proyecto.</p>
        </div>
        
        <button className="btn-soft flex items-center gap-2 md:hidden">
          <Filter className="w-4 h-4" />
          Filtros
        </button>
      </div>

      {/* Filters */}
      <div className="hidden md:flex flex-col gap-4 mb-8">
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
          <span className="text-sm font-medium text-text-secondary mr-2">Tipo:</span>
          {types.map(type => (
            <button
              key={type}
              onClick={() => setActiveType(type)}
              className={`chip whitespace-nowrap capitalize ${activeType === type ? 'chip-active' : ''}`}
            >
              {type === 'all' ? 'Todos' : type}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
          <span className="text-sm font-medium text-text-secondary mr-2">Ciudad:</span>
          {cities.map(city => (
            <button
              key={city}
              onClick={() => setActiveCity(city)}
              className={`chip whitespace-nowrap ${activeCity === city ? 'chip-active' : ''}`}
            >
              {city === 'all' ? 'Todas' : city}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      {filteredProperties.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProperties.map(property => (
            <PropertyCard key={property.id} property={property} />
          ))}
        </div>
      ) : (
        <div className="text-center py-20 glass-panel rounded-2xl">
          <p className="text-text-secondary text-lg">No se encontraron propiedades con estos filtros.</p>
          <button 
            onClick={() => { setActiveType('all'); setActiveCity('all'); }}
            className="btn-soft mt-4"
          >
            Limpiar filtros
          </button>
        </div>
      )}
    </div>
  );
}
