import HeroSection from '@/components/home/HeroSection';
import SupplierShowcase from '@/components/home/SupplierShowcase';
import FeaturedListings from '@/components/home/FeaturedListings';
import HowItWorks from '@/components/home/HowItWorks';
import BeforeAfterSlider from '@/components/visualizer/BeforeAfterSlider';
import Link from 'next/link';
import { Sparkles } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col gap-0">
      <HeroSection />
      <SupplierShowcase />
      <FeaturedListings />
      <HowItWorks />
      
      {/* Interactive Demo Section */}
      <section className="py-20 max-w-5xl mx-auto px-4 sm:px-6 w-full">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-text-primary mb-4">Pruébalo tú mismo</h2>
          <p className="text-text-secondary">
            Desliza para ver cómo un cambio de piso puede transformar completamente un espacio.
          </p>
        </div>
        
        <BeforeAfterSlider 
          beforeImage="https://placehold.co/1200x800/e2e8f0/64748b?text=Piso+Original"
          afterImage="https://placehold.co/1200x800/8B5A2B/ffffff?text=Piso+Maderado+Roble"
        />
        
        <div className="mt-10 text-center">
          <Link href="/visualizer" className="btn-primary inline-flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            Abrir Visualizador
          </Link>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 bg-primary/5 border-t border-primary/10">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-text-primary mb-6">¿Listo para transformar tu espacio?</h2>
          <p className="text-lg text-text-secondary mb-10">
            Únete a miles de dominicanos que ya están visualizando y creando el hogar de sus sueños.
          </p>
          <Link href="/visualizer" className="btn-primary inline-flex items-center gap-2 text-lg px-8 py-4">
            <Sparkles className="w-6 h-6" />
            Comenzar ahora
          </Link>
        </div>
      </section>
    </div>
  );
}
