<template>
    <div class="flex items-start gap-3">
        <span class="text-sm text-muted-foreground w-32 shrink-0 pt-0.5">{{ label }}</span>
        <span class="text-sm font-medium flex-1">
            <slot>{{ value ?? '—' }}</slot>
        </span>
    </div>
</template>

<script setup lang="ts">
defineProps<{ label: string; value?: string | number | null }>()
</script>
