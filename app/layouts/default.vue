<template>
  <div class="min-h-screen flex flex-col bg-background">
    <LayoutAppHeader />
    <main class="flex-1 pt-16">
      <slot />
    </main>
    <LayoutAppFooter />
    <LayoutMobileNav />
    <SharedToast />
  </div>
</template>
