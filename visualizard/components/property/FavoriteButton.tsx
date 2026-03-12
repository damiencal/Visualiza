'use client';

import { Heart } from 'lucide-react';
import { useFavorites } from '@/contexts/FavoritesContext';
import { cn } from '@/lib/utils';
import { useState } from 'react';

interface FavoriteButtonProps {
  id: string;
  type: 'property' | 'product';
  className?: string;
}

export default function FavoriteButton({ id, type, className }: FavoriteButtonProps) {
  const { isPropertyFavorited, isProductFavorited, togglePropertyFavorite, toggleProductFavorite } = useFavorites();
  const [isBouncing, setIsBouncing] = useState(false);

  const isFavorited = type === 'property' ? isPropertyFavorited(id) : isProductFavorited(id);

  const handleToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (type === 'property') {
      togglePropertyFavorite(id);
    } else {
      toggleProductFavorite(id);
    }

    if (!isFavorited) {
      setIsBouncing(true);
      setTimeout(() => setIsBouncing(false), 400);
      
      // Optional: Haptic feedback
      if (typeof navigator !== 'undefined' && navigator.vibrate) {
        navigator.vibrate(10);
      }
    }
  };

  return (
    <button
      onClick={handleToggle}
      className={cn(
        'p-2 rounded-full backdrop-blur-md transition-all duration-200',
        isFavorited ? 'bg-white/90 shadow-soft' : 'bg-black/20 hover:bg-black/30',
        isBouncing && 'animate-[heartBounce_0.4s_cubic-bezier(0.175,0.885,0.32,1.275)]',
        className
      )}
      aria-label={isFavorited ? 'Quitar de favoritos' : 'Añadir a favoritos'}
    >
      <Heart
        className={cn(
          'w-5 h-5 transition-colors',
          isFavorited ? 'fill-primary text-primary' : 'text-white'
        )}
      />
      <style jsx>{`
        @keyframes heartBounce {
          0% { transform: scale(1); }
          25% { transform: scale(1.3); }
          50% { transform: scale(0.95); }
          100% { transform: scale(1); }
        }
      `}</style>
    </button>
  );
}
