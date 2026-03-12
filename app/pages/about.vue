<script setup lang="ts">
useSeoMeta({
  title: 'Sobre Nosotros - Visualiza',
  description: 'Conoce Visualiza, la plataforma de visualización de interiores para la República Dominicana.',
})
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-12">
    <div class="text-center mb-12">
      <div class="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <Icon name="lucide:home" class="w-8 h-8 text-primary" />
      </div>
      <h1 class="text-3xl font-bold text-text-primary mb-3">Sobre Visualiza</h1>
      <p class="text-text-secondary text-lg leading-relaxed">
        La primera plataforma de visualización de interiores enfocada en el mercado inmobiliario dominicano.
      </p>
    </div>

    <div class="glass-card p-8 space-y-6 text-text-secondary leading-relaxed">
      <p>
        <strong class="text-text-primary">Visualiza</strong> nació con la visión de transformar la manera en que los dominicanos compran y diseñan sus hogares. Creemos que cada persona merece poder ver su espacio ideal antes de comprometerse con una compra.
      </p>
      <p>
        Nuestra plataforma conecta a compradores de bienes raíces con las mejores marcas dominicanas — desde IKEA hasta Pinturas Popular, Cerámica del Caribe y más — permitiéndote visualizar en tiempo real cómo lucirán los productos en tu futuro o actual hogar.
      </p>
      <p>
        Utilizamos tecnología de última generación con Canvas API y texturizado en tiempo real para que puedas explorar combinaciones de pisos, pinturas, cerámicas y mobiliario con total confianza.
      </p>
    </div>

    <div class="text-center mt-10">
      <NuxtLink to="/visualizer" class="btn-primary inline-flex items-center gap-2">
        <Icon name="lucide:wand-2" class="w-4 h-4" />
        Probar el visualizador
      </NuxtLink>
    </div>
  </div>
</template>
