<template>
    <nav class="flex items-center gap-1 text-sm text-muted-foreground" aria-label="Breadcrumb">
        <NuxtLink to="/" class="hover:text-foreground transition-colors">Home</NuxtLink>
        <template v-for="(crumb, i) in crumbs" :key="crumb.path">
            <Icon name="lucide:chevron-right" class="w-4 h-4" />
            <NuxtLink v-if="i < crumbs.length - 1" :to="crumb.path"
                class="hover:text-foreground transition-colors capitalize">
                {{ crumb.label }}
            </NuxtLink>
            <span v-else class="text-foreground font-medium capitalize">{{ crumb.label }}</span>
        </template>
    </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const crumbs = computed(() => {
    const parts = route.path.split('/').filter(Boolean)
    return parts.map((part, i) => ({
        label: part.replace(/-/g, ' '),
        path: '/' + parts.slice(0, i + 1).join('/'),
    }))
})
</script>
