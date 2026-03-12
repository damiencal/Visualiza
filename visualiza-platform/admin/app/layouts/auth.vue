<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-muted/30">
        <slot />
    </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'AuthLayout' })
</script>
