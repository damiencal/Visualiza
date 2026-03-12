import Link from 'next/link';
import { Sparkles } from 'lucide-react';

export default function HeroSection() {
  return (
    <section className="relative h-[90vh] min-h-[600px] flex items-center justify-center overflow-hidden">
      {/* Background Image with Parallax effect (simulated with fixed attachment or just cover) */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: 'url(https://picsum.photos/seed/hero-room/1920/1080)' }}
      >
        <div className="absolute inset-0 bg-black/30 backdrop-blur-[2px]"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 text-center animate-slide-up">
        <div className="glass-panel p-8 md:p-12 rounded-3xl inline-block">
          <h1 className="text-4xl md:text-6xl font-extrabold text-text-primary tracking-tight mb-6 text-balance">
            Visualiza tu hogar ideal
          </h1>
          <p className="text-lg md:text-xl text-text-secondary mb-8 max-w-2xl mx-auto text-balance">
            Transforma cualquier espacio con productos reales de suplidores dominicanos. Sube una foto y descubre cómo se vería.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/properties" className="btn-soft w-full sm:w-auto">
              Explorar Propiedades
            </Link>
            <Link href="/visualizer" className="btn-primary w-full sm:w-auto flex items-center justify-center gap-2">
              <Sparkles className="w-5 h-5" />
              Abrir Visualizador
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
