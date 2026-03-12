<template>
    <div>
        <label v-if="label" class="block text-sm font-medium mb-1">{{ label }}</label>
        <slot />
    </div>
</template>

<script setup lang="ts">
defineProps<{ label?: string }>()
</script>
