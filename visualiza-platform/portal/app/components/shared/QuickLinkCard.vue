<template>
    <NuxtLink :to="to"
        class="bg-card border border-border rounded-xl p-5 hover:border-primary/40 hover:bg-accent/30 transition-all group block">
        <Icon :name="icon" class="w-8 h-8 text-primary mb-3 group-hover:scale-110 transition-transform" />
        <p class="font-semibold mb-1">{{ title }}</p>
        <p class="text-sm text-muted-foreground">{{ description }}</p>
    </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{ title: string; description: string; icon: string; to: string }>()
</script>
