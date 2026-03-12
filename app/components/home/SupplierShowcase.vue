<script setup lang="ts">
const suppliers = [
  { name: 'IKEA', country: 'RD', color: '#0058A3', initials: 'IK' },
  { name: 'Cerámica del Caribe', country: 'RD', color: '#D4A017', initials: 'CC' },
  { name: 'Pinturas Popular', country: 'RD', color: '#E63946', initials: 'PP' },
  { name: 'Ochoa', country: 'RD', color: '#2D6A4F', initials: 'OC' },
  { name: 'Aliss', country: 'RD', color: '#7209B7', initials: 'AL' },
  { name: 'Casa Cuesta', country: 'RD', color: '#F4A261', initials: 'CA' },
  { name: 'La Sirena', country: 'RD', color: '#264653', initials: 'LS' },
  { name: 'Home Gallery RD', country: 'RD', color: '#6D6875', initials: 'HG' },
  { name: 'Ferretería Americana', country: 'RD', color: '#023E8A', initials: 'FA' },
]
</script>

<template>
  <section class="py-12 sm:py-16">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="text-center mb-10">
        <p class="text-xs text-primary font-semibold uppercase tracking-wider mb-2">Suplidores</p>
        <h2 class="text-2xl sm:text-3xl font-bold text-text-primary">Productos reales de marcas dominicanas</h2>
        <p class="text-text-secondary mt-3 max-w-xl mx-auto text-sm">
          Todos los productos del visualisador están disponibles en suplidores locales de la República Dominicana.
        </p>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-4">
        <NuxtLink
          v-for="supplier in suppliers"
          :key="supplier.name"
          to="/catalog"
          class="glass-card px-5 py-3 flex items-center gap-3 hover:shadow-elevated transition-all duration-200 hover:-translate-y-0.5"
        >
          <div
            class="w-9 h-9 rounded-xl flex items-center justify-center text-white text-xs font-black flex-shrink-0"
            :style="{ backgroundColor: supplier.color }"
          >
            {{ supplier.initials }}
          </div>
          <span class="font-semibold text-sm text-text-primary whitespace-nowrap">{{ supplier.name }}</span>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
