<script setup lang="ts">
</script>

<template>
  <section class="relative overflow-hidden pt-24 pb-16 sm:pt-32 sm:pb-24">
    <!-- Background gradient -->
    <div class="absolute inset-0 -z-10 bg-gradient-to-br from-rose-50 via-white to-pink-50" />
    <div class="absolute top-0 right-0 -z-10 w-[600px] h-[600px] rounded-full bg-primary/5 blur-3xl -translate-y-1/3 translate-x-1/3" />
    <div class="absolute bottom-0 left-0 -z-10 w-[400px] h-[400px] rounded-full bg-primary/8 blur-2xl translate-y-1/2 -translate-x-1/4" />

    <div class="max-w-4xl mx-auto px-4 sm:px-6 text-center">
      <!-- Badge -->
      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6">
        <Icon name="lucide:sparkles" class="w-4 h-4" />
        Visualizador de interiores para RD
      </div>

      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-text-primary leading-tight tracking-tight mb-6">
        Diseña tu hogar
        <span class="text-primary"> antes de comprar</span>
      </h1>

      <p class="text-lg sm:text-xl text-text-secondary max-w-2xl mx-auto mb-10 leading-relaxed">
        Visualiza cómo lucirán los productos reales de IKEA, Cerámica del Caribe, Pinturas Popular y más en cualquier espacio.
      </p>

      <!-- CTA buttons -->
      <div class="flex flex-wrap items-center justify-center gap-3">
        <NuxtLink to="/visualizer" class="btn-primary flex items-center gap-2">
          <Icon name="lucide:sparkles" class="w-4 h-4" />
          Abrir visualizador
        </NuxtLink>
        <NuxtLink to="/catalog" class="btn-soft flex items-center gap-2">
          <Icon name="lucide:grid-2x2" class="w-4 h-4" />
          Ver catálogo
        </NuxtLink>
      </div>
    </div>

    <!-- Stats row -->
    <div class="max-w-3xl mx-auto px-4 sm:px-6 mt-16">
      <div class="glass-card px-6 py-5 grid grid-cols-3 gap-4 sm:gap-8">
        <div class="text-center">
          <p class="text-2xl sm:text-3xl font-extrabold text-primary">
            <SharedAnimatedCounter :target="500" suffix="+" />
          </p>
          <p class="text-xs text-text-secondary mt-1">Visualizaciones</p>
        </div>
        <div class="text-center">
          <p class="text-2xl sm:text-3xl font-extrabold text-primary">
            <SharedAnimatedCounter :target="40" suffix="+"/>
          </p>
          <p class="text-xs text-text-secondary mt-1">Productos reales</p>
        </div>
        <div class="text-center">
          <p class="text-2xl sm:text-3xl font-extrabold text-primary">
            <SharedAnimatedCounter :target="9" />
          </p>
          <p class="text-xs text-text-secondary mt-1">Suplidores DR</p>
        </div>
      </div>
    </div>
  </section>
</template>
