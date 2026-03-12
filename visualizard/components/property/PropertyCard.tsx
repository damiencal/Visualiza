import Link from 'next/link';
import Image from 'next/image';
import { MapPin, BedDouble, Bath, Ruler, Sparkles } from 'lucide-react';
import { Property } from '@/types';
import { formatPrice } from '@/lib/utils';
import FavoriteButton from './FavoriteButton';

export default function PropertyCard({ property }: { property: Property }) {
  const hasVisualizerReadyImage = property.images.some(i => i.isVisualizerReady);

  return (
    <Link href={`/properties/${property.slug}`} className="glass-card group overflow-hidden block">
      {/* Image Container */}
      <div className="relative aspect-[4/3] overflow-hidden rounded-t-2xl bg-gray-100">
        <Image
          src={property.images[0]?.url || 'https://picsum.photos/800/600'}
          alt={property.title}
          fill
          className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          referrerPolicy="no-referrer"
        />
        
        {/* Type Badge */}
        <span className="absolute top-3 left-3 chip chip-active text-xs backdrop-blur-sm capitalize">
          {property.type}
        </span>
        
        {/* Visualizer-Ready Badge */}
        {hasVisualizerReadyImage && (
          <span className="absolute top-3 right-14 chip bg-white/80 backdrop-blur-sm text-xs shadow-sm">
            <Sparkles className="w-3 h-3 text-primary" />
            <span className="hidden sm:inline">Visualizable</span>
          </span>
        )}
        
        {/* Favorite */}
        <FavoriteButton id={property.id} type="property" className="absolute top-3 right-3" />
      </div>

      {/* Content */}
      <div className="p-4 space-y-2">
        <div className="flex items-baseline justify-between">
          <span className="text-xl font-bold text-text-primary">
            {formatPrice(property.price, property.currency)}
          </span>
          {property.priceUSD && (
            <span className="text-sm text-text-tertiary">
              ≈ {formatPrice(property.priceUSD, 'USD')}
            </span>
          )}
        </div>
        
        <h3 className="font-semibold text-text-primary line-clamp-1">{property.title}</h3>
        
        <p className="text-sm text-text-secondary flex items-center gap-1">
          <MapPin className="w-3.5 h-3.5 flex-shrink-0" />
          <span className="truncate">{property.location.neighborhood}, {property.location.city}</span>
        </p>
        
        {/* Specs Row */}
        <div className="flex items-center gap-4 pt-3 mt-1 border-t border-black/[0.04]">
          <span className="flex items-center gap-1.5 text-sm text-text-secondary">
            <BedDouble className="w-4 h-4 text-text-tertiary" /> {property.specs.bedrooms}
          </span>
          <span className="flex items-center gap-1.5 text-sm text-text-secondary">
            <Bath className="w-4 h-4 text-text-tertiary" /> {property.specs.bathrooms}
          </span>
          <span className="flex items-center gap-1.5 text-sm text-text-secondary">
            <Ruler className="w-4 h-4 text-text-tertiary" /> {property.specs.area}m²
          </span>
        </div>
      </div>
    </Link>
  );
}
