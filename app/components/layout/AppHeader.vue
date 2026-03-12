<script setup lang="ts">
import { useWindowScroll } from '@vueuse/core'

const { y: scrollY } = useWindowScroll()
const isScrolled = computed(() => scrollY.value > 20)

const navLinks = [
  { to: '/', label: 'Inicio' },
  { to: '/visualizer', label: 'Visualisador' },
  { to: '/catalog', label: 'Catálogo' },
]
</script>

<template>
  <header :class="[
    'fixed top-0 inset-x-0 z-50 transition-all duration-300',
    'glass-header',
    isScrolled ? 'shadow-float bg-white/85' : 'bg-white/75',
  ]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center gap-2.5 group">
        <div
          class="w-8 h-8 bg-primary rounded-xl flex items-center justify-center shadow-glow/50 group-hover:scale-105 transition-transform">
          <Icon name="lucide:home" class="w-4 h-4 text-white" aria-hidden="true" />
        </div>
        <span class="font-bold text-lg tracking-tight text-text-primary">Visualisa</span>
      </NuxtLink>

      <!-- Desktop Nav -->
      <nav class="hidden md:flex items-center gap-1" aria-label="Navegación principal">
        <NuxtLink v-for="link in navLinks" :key="link.to" :to="link.to" class="btn-ghost text-sm"
          active-class="!text-primary !bg-primary/5">
          {{ link.label }}
        </NuxtLink>
      </nav>

      <!-- Actions -->
      <div class="flex items-center gap-2">
        <NuxtLink to="/visualizer" class="btn-primary !px-4 !py-2 text-sm hidden sm:inline-flex items-center gap-2">
          <Icon name="lucide:sparkles" class="w-4 h-4" aria-hidden="true" />
          Visualizar
        </NuxtLink>
      </div>
    </div>
  </header>
</template>
