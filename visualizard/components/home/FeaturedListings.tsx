import Link from 'next/link';
import { mockProperties } from '@/lib/mock-data';
import PropertyCard from '@/components/property/PropertyCard';

export default function FeaturedListings() {
  const featured = mockProperties.filter(p => p.isFeatured);

  return (
    <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6">
      <div className="flex items-end justify-between mb-10">
        <div>
          <h2 className="text-3xl font-bold text-text-primary mb-2">Propiedades Destacadas</h2>
          <p className="text-text-secondary">Descubre los mejores espacios disponibles en el mercado.</p>
        </div>
        <Link href="/properties" className="hidden sm:block text-primary font-medium hover:underline">
          Ver todas
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {featured.map(property => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>
      
      <div className="mt-8 text-center sm:hidden">
        <Link href="/properties" className="btn-soft inline-block w-full">
          Ver todas las propiedades
        </Link>
      </div>
    </section>
  );
}
