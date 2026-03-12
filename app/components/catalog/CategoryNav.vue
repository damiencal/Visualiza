<script setup lang="ts">
import type { ProductCategory } from '~/types'

interface Props {
  modelValue: ProductCategory | ''
}

defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [v: ProductCategory | ''] }>()

const categories: Array<{ value: ProductCategory | '', label: string, icon: string }> = [
  { value: '', label: 'Todos', icon: 'lucide:layout-grid' },
  { value: 'flooring', label: 'Pisos', icon: 'lucide:square' },
  { value: 'paint', label: 'Pintura', icon: 'lucide:paintbrush' },
  { value: 'tile', label: 'Cerámica', icon: 'lucide:grid-3x3' },
  { value: 'furniture', label: 'Muebles', icon: 'lucide:armchair' },
  { value: 'fixtures', label: 'Accesorios', icon: 'lucide:wrench' },
  { value: 'lighting', label: 'Iluminación', icon: 'lucide:lamp' },
  { value: 'curtains', label: 'Cortinas', icon: 'lucide:columns' },
  { value: 'rugs', label: 'Alfombras', icon: 'lucide:layout' },
  { value: 'wallpaper', label: 'Empapelado', icon: 'lucide:scroll-text' },
  { value: 'countertops', label: 'Encimeras', icon: 'lucide:minus-square' },
]
</script>

<template>
  <nav class="flex gap-2 overflow-x-auto scrollbar-hide pb-1" aria-label="Categorías">
    <button
      v-for="cat in categories"
      :key="cat.value"
      :class="[
        'flex-none flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap',
        modelValue === cat.value
          ? 'chip-active shadow-glow'
          : 'chip hover:bg-black/8',
      ]"
      :aria-current="modelValue === cat.value ? 'true' : undefined"
      @click="emit('update:modelValue', cat.value)"
    >
      <Icon :name="cat.icon" class="w-3.5 h-3.5" />
      {{ cat.label }}
    </button>
  </nav>
</template>
