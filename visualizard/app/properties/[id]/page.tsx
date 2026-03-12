'use client';

import { use } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { MapPin, BedDouble, Bath, Ruler, Sparkles, Phone, Mail } from 'lucide-react';
import { mockProperties } from '@/lib/mock-data';
import { formatPrice } from '@/lib/utils';
import FavoriteButton from '@/components/property/FavoriteButton';

export default function PropertyDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const property = mockProperties.find(p => p.slug === id || p.id === id);

  if (!property) {
    notFound();
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="chip chip-active capitalize">{property.type}</span>
            <span className="chip">{property.status === 'available' ? 'Disponible' : 'Vendido'}</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">{property.title}</h1>
          <p className="text-text-secondary flex items-center gap-1">
            <MapPin className="w-4 h-4" />
            {property.location.address}, {property.location.neighborhood}, {property.location.city}
          </p>
        </div>
        <div className="flex flex-col items-start md:items-end">
          <span className="text-3xl font-bold text-primary">
            {formatPrice(property.price, property.currency)}
          </span>
          {property.priceUSD && (
            <span className="text-text-secondary">
              ≈ {formatPrice(property.priceUSD, 'USD')}
            </span>
          )}
        </div>
      </div>

      {/* Gallery */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        <div className="md:col-span-2 relative aspect-[16/9] md:aspect-auto md:h-[500px] rounded-2xl overflow-hidden group">
          <Image
            src={property.images[0]?.url || 'https://picsum.photos/1200/800'}
            alt={property.title}
            fill
            className="object-cover"
            unoptimized
          />
          <FavoriteButton id={property.id} type="property" className="absolute top-4 right-4" />
          
          {property.images[0]?.isVisualizerReady && (
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
              <Link href={`/visualizer?image=${encodeURIComponent(property.images[0].url)}`} className="btn-primary flex items-center gap-2">
                <Sparkles className="w-5 h-5" />
                Visualizar esta habitación
              </Link>
            </div>
          )}
        </div>
        <div className="hidden md:flex flex-col gap-4 h-[500px]">
          {property.images.slice(1, 3).map((img, idx) => (
            <div key={idx} className="relative flex-1 rounded-2xl overflow-hidden group">
              <Image
                src={img.url}
                alt={img.alt}
                fill
                className="object-cover"
                unoptimized
              />
              {img.isVisualizerReady && (
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
                  <Link href={`/visualizer?image=${encodeURIComponent(img.url)}`} className="btn-primary text-sm px-4 py-2 flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Visualizar
                  </Link>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div className="lg:col-span-2 space-y-8">
          {/* Specs */}
          <div className="glass-panel p-6 rounded-2xl flex items-center justify-around">
            <div className="text-center">
              <BedDouble className="w-6 h-6 mx-auto mb-2 text-primary" />
              <p className="font-semibold text-text-primary">{property.specs.bedrooms}</p>
              <p className="text-xs text-text-secondary uppercase tracking-wider">Habitaciones</p>
            </div>
            <div className="w-px h-12 bg-black/10"></div>
            <div className="text-center">
              <Bath className="w-6 h-6 mx-auto mb-2 text-primary" />
              <p className="font-semibold text-text-primary">{property.specs.bathrooms}</p>
              <p className="text-xs text-text-secondary uppercase tracking-wider">Baños</p>
            </div>
            <div className="w-px h-12 bg-black/10"></div>
            <div className="text-center">
              <Ruler className="w-6 h-6 mx-auto mb-2 text-primary" />
              <p className="font-semibold text-text-primary">{property.specs.area} m²</p>
              <p className="text-xs text-text-secondary uppercase tracking-wider">Área</p>
            </div>
          </div>

          {/* Description */}
          <div>
            <h2 className="text-2xl font-bold text-text-primary mb-4">Descripción</h2>
            <p className="text-text-secondary leading-relaxed whitespace-pre-line">
              {property.description}
            </p>
          </div>

          {/* Features */}
          <div>
            <h2 className="text-2xl font-bold text-text-primary mb-4">Características</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {property.features.map((feature, idx) => (
                <div key={idx} className="flex items-center gap-2 text-text-secondary">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                  {feature}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Agent Card */}
          <div className="glass-card p-6 sticky top-24">
            <h3 className="text-lg font-bold text-text-primary mb-4">Agente Inmobiliario</h3>
            <div className="flex items-center gap-4 mb-6">
              <div className="relative w-16 h-16 rounded-full overflow-hidden border-2 border-white shadow-sm">
                <Image
                  src={property.agent.avatar}
                  alt={property.agent.name}
                  fill
                  className="object-cover"
                  unoptimized
                />
              </div>
              <div>
                <p className="font-semibold text-text-primary">{property.agent.name}</p>
                <p className="text-sm text-text-secondary">Asesor Inmobiliario</p>
              </div>
            </div>
            <div className="space-y-3">
              <button className="btn-primary w-full flex items-center justify-center gap-2">
                <Phone className="w-4 h-4" />
                Llamar
              </button>
              <button className="btn-soft w-full flex items-center justify-center gap-2">
                <Mail className="w-4 h-4" />
                Mensaje
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
