<template>
    <div class="bg-card rounded-xl border border-border p-5 flex items-start justify-between">
        <div>
            <p class="text-sm text-muted-foreground font-medium">{{ label }}</p>
            <p class="text-2xl font-bold mt-1">
                <span v-if="loading" class="inline-block w-16 h-7 bg-muted animate-pulse rounded" />
                <span v-else>{{ value }}</span>
            </p>
            <p v-if="delta && !loading" class="text-xs text-muted-foreground mt-1">{{ delta }}</p>
        </div>
        <div class="w-10 h-10 rounded-lg bg-muted flex items-center justify-center shrink-0">
            <Icon :name="icon" class="w-5 h-5 text-muted-foreground" />
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    label: string
    value: string
    delta?: string
    icon: string
    loading?: boolean
}>()
</script>
