<script setup lang="ts">
const steps = [
  {
    number: '01',
    icon: 'lucide:image-plus',
    title: 'Sube tu foto',
    description: 'Carga una foto de tu habitación o usa imágenes de las propiedades.',
  },
  {
    number: '02',
    icon: 'lucide:wand-2',
    title: 'Visualisa productos',
    description: 'Aplica pisos, pinturas y más de suplidores dominicanos en tiempo real.',
  },
  {
    number: '03',
    icon: 'lucide:download',
    title: 'Comparte o descarga',
    description: 'Exporta el diseño y compártelo con tu familia o decorador.',
  },
]
</script>

<template>
  <section class="py-12 sm:py-20 bg-gradient-to-b from-white to-rose-50/50">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="text-center mb-12">
        <p class="text-xs text-primary font-semibold uppercase tracking-wider mb-2">Cómo funciona</p>
        <h2 class="text-2xl sm:text-3xl font-bold text-text-primary">Diseña en 3 pasos simples</h2>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center">
        <div v-for="step in steps" :key="step.number"
          class="glass-card p-6 flex flex-col items-center text-center hover:shadow-elevated transition-shadow duration-300">
          <div class="relative mb-4">
            <div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center">
              <Icon :name="step.icon" class="w-7 h-7 text-primary" />
            </div>
            <span class="absolute -top-2 -right-2 text-xs font-black text-primary/40">{{ step.number }}</span>
          </div>
          <h3 class="font-bold text-text-primary mb-2">{{ step.title }}</h3>
          <p class="text-sm text-text-secondary leading-relaxed">{{ step.description }}</p>
        </div>
      </div>

      <div class="text-center mt-10">
        <NuxtLink to="/visualizer" class="btn-primary inline-flex items-center gap-2">
          <Icon name="lucide:play-circle" class="w-4 h-4" />
          Comenzar ahora
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
