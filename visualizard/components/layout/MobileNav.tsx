'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Building, Sparkles, LayoutGrid, Heart } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function MobileNav() {
  const pathname = usePathname();

  const tabs = [
    { icon: Home, label: 'Inicio', to: '/' },
    { icon: Building, label: 'Propiedades', to: '/properties' },
    { icon: Sparkles, label: 'Visualizar', to: '/visualizer', isPrimary: true },
    { icon: LayoutGrid, label: 'Catálogo', to: '/catalog' },
    { icon: Heart, label: 'Favoritos', to: '/favorites' },
  ];

  return (
    <nav className="md:hidden fixed bottom-0 inset-x-0 z-50 glass-header pb-safe border-t border-white/20">
      <div className="flex items-center justify-around h-16 px-2">
        {tabs.map((tab) => {
          const isActive = pathname === tab.to || (tab.to !== '/' && pathname.startsWith(tab.to));
          const Icon = tab.icon;

          if (tab.isPrimary) {
            return (
              <Link
                key={tab.to}
                href={tab.to}
                className="relative -top-4 flex flex-col items-center justify-center"
              >
                <div className="w-14 h-14 bg-primary rounded-full flex items-center justify-center shadow-glow text-white border-4 border-background">
                  <Icon className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-medium text-text-primary mt-1">
                  {tab.label}
                </span>
              </Link>
            );
          }

          return (
            <Link
              key={tab.to}
              href={tab.to}
              className={cn(
                'flex flex-col items-center justify-center w-16 h-full gap-1 transition-colors',
                isActive ? 'text-primary' : 'text-text-secondary'
              )}
            >
              <Icon className={cn("w-5 h-5", isActive && "fill-primary/20")} />
              <span className="text-[10px] font-medium">{tab.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
