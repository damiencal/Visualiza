<script setup lang="ts">
interface Props {
  icon?: string
  title?: string
  description?: string
  actionLabel?: string
  actionTo?: string
}

withDefaults(defineProps<Props>(), {
  icon: 'lucide:search-x',
  title: 'Sin resultados',
  description: 'No encontramos lo que buscas. Intenta con otros filtros.',
  actionLabel: '',
  actionTo: '',
})
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-6 text-center">
    <div class="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-4">
      <Icon :name="icon" class="w-8 h-8 text-primary" />
    </div>
    <h3 class="text-text-primary font-semibold text-lg mb-2">{{ title }}</h3>
    <p class="text-text-secondary text-sm max-w-xs">{{ description }}</p>
    <NuxtLink
      v-if="actionLabel && actionTo"
      :to="actionTo"
      class="btn-primary mt-6"
    >
      {{ actionLabel }}
    </NuxtLink>
    <slot />
  </div>
</template>
