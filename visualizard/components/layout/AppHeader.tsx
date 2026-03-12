'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Heart, Sparkles, Search, Menu } from 'lucide-react';
import { useFavorites } from '@/contexts/FavoritesContext';
import { cn } from '@/lib/utils';

export default function AppHeader() {
  const [isScrolled, setIsScrolled] = useState(false);
  const pathname = usePathname();
  const { favoriteProperties, favoriteProducts } = useFavorites();
  
  const favCount = favoriteProperties.length + favoriteProducts.length;

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { label: 'Inicio', to: '/' },
    { label: 'Propiedades', to: '/properties' },
    { label: 'Catálogo', to: '/catalog' },
  ];

  return (
    <header
      className={cn(
        'fixed top-0 inset-x-0 z-50 transition-all duration-300 glass-header',
        isScrolled ? 'shadow-float bg-white/85' : 'bg-white/75'
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-xl flex items-center justify-center shadow-glow">
            <Home className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight text-text-primary">VisualizaRD</span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => {
            const isActive = pathname === link.to || (link.to !== '/' && pathname.startsWith(link.to));
            return (
              <Link
                key={link.to}
                href={link.to}
                className={cn(
                  'btn-ghost text-sm',
                  isActive && '!text-primary !bg-primary/5'
                )}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button className="btn-ghost p-2 rounded-xl hidden sm:block">
            <Search className="w-5 h-5" />
          </button>
          
          <Link href="/favorites" className="btn-ghost p-2 rounded-xl relative">
            <Heart className="w-5 h-5" />
            {favCount > 0 && (
              <span className="absolute top-1 right-1 w-4 h-4 bg-primary text-white text-[10px] font-bold rounded-full flex items-center justify-center animate-scale-in">
                {favCount}
              </span>
            )}
          </Link>
          
          <Link href="/visualizer" className="btn-primary !px-4 !py-2 text-sm hidden sm:flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            Visualizar
          </Link>

          <button className="btn-ghost p-2 rounded-xl md:hidden">
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}
