import { Upload, LayoutGrid, Sparkles } from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      icon: Upload,
      title: 'Sube una foto',
      description: 'Toma una foto de tu habitación o elige una de nuestra galería de propiedades.'
    },
    {
      icon: LayoutGrid,
      title: 'Elige productos',
      description: 'Explora nuestro catálogo con miles de productos de suplidores dominicanos.'
    },
    {
      icon: Sparkles,
      title: 'Visualiza el resultado',
      description: 'Mira cómo se vería tu espacio transformado en tiempo real con realidad aumentada.'
    }
  ];

  return (
    <section className="py-20 bg-white/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-text-primary mb-4">¿Cómo funciona?</h2>
          <p className="text-text-secondary max-w-2xl mx-auto">
            Visualizar tu próximo proyecto de remodelación nunca ha sido tan fácil.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Connecting line for desktop */}
          <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-gradient-to-r from-transparent via-primary/20 to-transparent"></div>

          {steps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <div key={idx} className="glass-card p-8 text-center relative z-10">
                <div className="w-16 h-16 mx-auto bg-primary/10 rounded-2xl flex items-center justify-center mb-6 text-primary shadow-inner-soft">
                  <Icon className="w-8 h-8" />
                </div>
                <div className="absolute -top-4 -right-4 w-8 h-8 bg-white rounded-full shadow-soft flex items-center justify-center font-bold text-text-primary border border-black/5">
                  {idx + 1}
                </div>
                <h3 className="text-xl font-bold text-text-primary mb-3">{step.title}</h3>
                <p className="text-text-secondary">{step.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
