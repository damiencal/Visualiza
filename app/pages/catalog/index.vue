<script setup lang="ts">
useSeoMeta({ title: 'Catálogo de Productos - Visualiza' })
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-text-primary mb-1">Catálogo</h1>
      <p class="text-text-secondary text-sm">Productos de suplidores dominicanos para tu hogar</p>
    </div>
    <CatalogBrowser />
  </div>
</template>
