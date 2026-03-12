<script setup lang="ts">
const footerLinks = {
  company: [
    { to: '/about', label: 'Sobre Nosotros' },
  ],
  services: [
    { to: '/visualizer', label: 'Visualizador' },
    { to: '/catalog', label: 'Catálogo' },
  ],
}
</script>

<template>
  <footer class="bg-white/50 backdrop-blur-sm border-t border-black/[0.05] pb-20 md:pb-0">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand -->
        <div class="md:col-span-2">
          <NuxtLink to="/" class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 bg-primary rounded-xl flex items-center justify-center">
              <Icon name="lucide:home" class="w-4 h-4 text-white" aria-hidden="true" />
            </div>
            <span class="font-bold text-lg">Visualiza</span>
          </NuxtLink>
          <p class="text-text-secondary text-sm max-w-xs">
            Visualiza tu hogar ideal con productos reales de suplidores dominicanos. Transforma cualquier espacio antes de comprar.
          </p>
        </div>

        <!-- Links -->
        <div>
          <h4 class="font-semibold text-sm text-text-primary mb-3">Compañía</h4>
          <ul class="space-y-2">
            <li v-for="link in footerLinks.company" :key="link.to">
              <NuxtLink :to="link.to" class="text-sm text-text-secondary hover:text-text-primary transition-colors">
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <div>
          <h4 class="font-semibold text-sm text-text-primary mb-3">Servicios</h4>
          <ul class="space-y-2">
            <li v-for="link in footerLinks.services" :key="link.to">
              <NuxtLink :to="link.to" class="text-sm text-text-secondary hover:text-text-primary transition-colors">
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-10 pt-6 border-t border-black/[0.05] flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-text-tertiary">
          © {{ new Date().getFullYear() }} Visualiza. Todos los derechos reservados.
        </p>
        <p class="text-xs text-text-tertiary">
          Hecho con ❤️ en República Dominicana
        </p>
      </div>
    </div>
  </footer>
</template>
