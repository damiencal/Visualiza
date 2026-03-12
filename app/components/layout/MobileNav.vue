<script setup lang="ts">
const route = useRoute()

const tabs = [
  { to: '/', icon: 'lucide:home', label: 'Inicio' },
  { to: '/catalog', icon: 'lucide:grid-2x2', label: 'Catálogo' },
  { to: '/visualizer', icon: 'lucide:sparkles', label: 'Visualizar', isCenter: true },
  { to: '/about', icon: 'lucide:info', label: 'Nosotros' },
]

function isActive(to: string): boolean {
  if (to === '/') return route.path === '/'
  return route.path.startsWith(to)
}
</script>

<template>
  <nav class="md:hidden fixed bottom-0 inset-x-0 z-50 glass-panel border-t border-white/20 pb-safe"
    aria-label="Navegación móvil">
    <div class="flex items-end justify-around px-2 pt-2 pb-1">
      <template v-for="tab in tabs" :key="tab.to">
        <!-- Center elevated Visualizer button -->
        <NuxtLink v-if="tab.isCenter" :to="tab.to" class="flex flex-col items-center -mt-6" :aria-label="tab.label"
          :aria-current="isActive(tab.to) ? 'page' : undefined">
          <div :class="[
            'w-14 h-14 rounded-2xl flex items-center justify-center shadow-elevated transition-all duration-200',
            isActive(tab.to)
              ? 'bg-primary-dark scale-105'
              : 'bg-primary hover:bg-primary-dark active:scale-95',
          ]">
            <Icon :name="tab.icon" class="w-6 h-6 text-white" aria-hidden="true" />
          </div>
          <span class="text-[10px] mt-1 font-medium text-text-secondary">{{ tab.label }}</span>
        </NuxtLink>

        <!-- Regular tab buttons -->
        <NuxtLink v-else :to="tab.to"
          class="flex flex-col items-center gap-0.5 px-2 py-1 rounded-xl transition-all duration-150"
          :aria-label="tab.label" :aria-current="isActive(tab.to) ? 'page' : undefined">
          <Icon :name="tab.icon" :class="[
            'w-5 h-5 transition-colors',
            isActive(tab.to) ? 'text-primary' : 'text-text-tertiary',
          ]" aria-hidden="true" />
          <span :class="[
            'text-[10px] font-medium transition-colors',
            isActive(tab.to) ? 'text-primary' : 'text-text-tertiary',
          ]">
            {{ tab.label }}
          </span>
        </NuxtLink>
      </template>
    </div>
  </nav>
</template>
