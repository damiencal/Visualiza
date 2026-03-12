<template>
    <div class="min-h-screen bg-background">
        <PortalHeader />
        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <slot />
        </main>
        <PortalFooter />
    </div>
</template>
<script setup lang="ts">
defineOptions({ name: 'DefaultLayout' })
</script>
