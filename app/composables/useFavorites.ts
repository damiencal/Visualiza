import { useLocalStorage } from "@vueuse/core";

export const useFavorites = () => {
  const favoriteProductIds = useLocalStorage<string[]>("favorite-products", []);

  function toggleProductFavorite(id: string) {
    const idx = favoriteProductIds.value.indexOf(id);
    if (idx >= 0) {
      favoriteProductIds.value.splice(idx, 1);
    } else {
      favoriteProductIds.value.push(id);
    }
    haptic("light");
  }

  function isProductFavorited(id: string): boolean {
    return favoriteProductIds.value.includes(id);
  }

  function haptic(style: "light" | "medium" | "heavy" = "light") {
    if (typeof navigator !== "undefined") {
      const durations = { light: 10, medium: 20, heavy: 40 };
      navigator.vibrate?.(durations[style]);
    }
  }

  const favoriteCount = computed(() => favoriteProductIds.value.length);

  return {
    favoriteProductIds,
    favoriteCount,
    toggleProductFavorite,
    isProductFavorited,
  };
};
