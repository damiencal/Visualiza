<template>
  <div class="flex flex-col h-screen bg-background overflow-hidden">
    <!-- Compact visualizer header -->
    <header
      class="shrink-0 h-14 glass-header flex items-center justify-between px-4 gap-4 border-b border-black/[0.06]">
      <NuxtLink to="/" class="flex items-center gap-2">
        <div class="w-7 h-7 bg-primary rounded-xl flex items-center justify-center">
          <Icon name="lucide:home" class="w-3.5 h-3.5 text-white" />
        </div>
        <span class="font-bold text-sm hidden sm:block">Visualiza</span>
      </NuxtLink>

      <NuxtLink to="/" class="text-sm text-text-secondary hover:text-text-primary transition-colors">
        ← Inicio
      </NuxtLink>
    </header>

    <main class="flex-1 overflow-hidden">
      <slot />
    </main>

    <SharedToast />
  </div>
</template>
