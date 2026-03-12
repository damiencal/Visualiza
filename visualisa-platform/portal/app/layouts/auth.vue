<template>
    <div class="min-h-screen bg-muted/30 flex flex-col items-center justify-center p-4">
        <slot />
    </div>
</template>
<script setup lang="ts">
defineOptions({ name: 'AuthLayout' })
</script>
