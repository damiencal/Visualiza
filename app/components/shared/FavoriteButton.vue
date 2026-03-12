<script setup lang="ts">
interface Props {
  productId?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
})

const { isProductFavorited, toggleProductFavorite } = useFavorites()

const isFavorited = computed(() =>
  props.productId ? isProductFavorited(props.productId) : false,
)

function toggle() {
  if (props.productId) toggleProductFavorite(props.productId)
}

const sizeClasses = {
  sm: 'w-7 h-7',
  md: 'w-9 h-9',
  lg: 'w-11 h-11',
}

const iconSizes = {
  sm: 'w-3.5 h-3.5',
  md: 'w-4 h-4',
  lg: 'w-5 h-5',
}
</script>

<template>
  <button :class="[
    'flex items-center justify-center rounded-full transition-all duration-200 active:scale-90',
    sizeClasses[size],
    isFavorited
      ? 'bg-primary text-white shadow-glow'
      : 'bg-white/80 text-text-secondary hover:bg-white hover:text-primary shadow-soft',
  ]" :aria-label="isFavorited ? 'Quitar de favoritos' : 'Agregar a favoritos'" :aria-pressed="isFavorited"
    @click.prevent="toggle">
    <Icon :name="isFavorited ? 'lucide:heart' : 'lucide:heart'" :class="[
      iconSizes[size],
      'transition-all duration-200',
      isFavorited ? 'fill-current animate-heartBounce' : '',
    ]" />
  </button>
</template>
