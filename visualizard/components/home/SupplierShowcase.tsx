import Image from 'next/image';

const suppliers = [
  { name: 'IKEA', logo: 'https://placehold.co/200x80/0051ba/ffda1a?text=IKEA' },
  { name: 'Ochoa', logo: 'https://placehold.co/200x80/ffffff/000000?text=Ochoa' },
  { name: 'Aliss', logo: 'https://placehold.co/200x80/ffffff/e3000f?text=Aliss' },
  { name: 'Ferretería Americana', logo: 'https://placehold.co/200x80/ffffff/0033a0?text=Americana' },
  { name: 'Casa Cuesta', logo: 'https://placehold.co/200x80/ffffff/000000?text=Casa+Cuesta' },
  { name: 'La Sirena', logo: 'https://placehold.co/200x80/ffe600/000000?text=La+Sirena' },
];

export default function SupplierShowcase() {
  return (
    <section className="py-12 bg-white/50 border-y border-black/[0.04]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <p className="text-center text-sm font-semibold text-text-tertiary uppercase tracking-wider mb-8">
          Con la confianza de las mejores marcas en RD
        </p>
        
        <div className="relative overflow-hidden">
          {/* Marquee container */}
          <div className="flex space-x-12 animate-[shimmer_20s_linear_infinite] w-max">
            {/* Double the list for seamless loop */}
            {[...suppliers, ...suppliers].map((supplier, idx) => (
              <div 
                key={idx} 
                className="w-32 h-12 relative grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300"
              >
                <Image
                  src={supplier.logo}
                  alt={supplier.name}
                  fill
                  className="object-contain"
                  unoptimized
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
