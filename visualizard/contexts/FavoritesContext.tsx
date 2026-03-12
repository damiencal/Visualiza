'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface FavoritesContextType {
  favoriteProperties: string[];
  favoriteProducts: string[];
  togglePropertyFavorite: (id: string) => void;
  toggleProductFavorite: (id: string) => void;
  isPropertyFavorited: (id: string) => boolean;
  isProductFavorited: (id: string) => boolean;
}

const FavoritesContext = createContext<FavoritesContextType | undefined>(undefined);

export function FavoritesProvider({ children }: { children: React.ReactNode }) {
  const [favoriteProperties, setFavoriteProperties] = useState<string[]>([]);
  const [favoriteProducts, setFavoriteProducts] = useState<string[]>([]);

  useEffect(() => {
    const storedProps = localStorage.getItem('fav_properties');
    const storedProds = localStorage.getItem('fav_products');
    setTimeout(() => {
      if (storedProps) setFavoriteProperties(JSON.parse(storedProps));
      if (storedProds) setFavoriteProducts(JSON.parse(storedProds));
    }, 0);
  }, []);

  const togglePropertyFavorite = (id: string) => {
    setFavoriteProperties(prev => {
      const next = prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id];
      localStorage.setItem('fav_properties', JSON.stringify(next));
      return next;
    });
  };

  const toggleProductFavorite = (id: string) => {
    setFavoriteProducts(prev => {
      const next = prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id];
      localStorage.setItem('fav_products', JSON.stringify(next));
      return next;
    });
  };

  const isPropertyFavorited = (id: string) => favoriteProperties.includes(id);
  const isProductFavorited = (id: string) => favoriteProducts.includes(id);

  return (
    <FavoritesContext.Provider value={{
      favoriteProperties,
      favoriteProducts,
      togglePropertyFavorite,
      toggleProductFavorite,
      isPropertyFavorited,
      isProductFavorited
    }}>
      {children}
    </FavoritesContext.Provider>
  );
}

export function useFavorites() {
  const context = useContext(FavoritesContext);
  if (context === undefined) {
    throw new Error('useFavorites must be used within a FavoritesProvider');
  }
  return context;
}
