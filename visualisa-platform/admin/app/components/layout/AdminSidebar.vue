<template>
    <aside class="fixed inset-y-0 left-0 z-50 bg-card border-r border-border flex flex-col transition-all duration-300"
        :class="collapsed ? 'w-16' : 'w-64'">
        <!-- Logo -->
        <div class="h-16 flex items-center px-4 border-b border-border shrink-0">
            <NuxtLink to="/" class="flex items-center gap-3 min-w-0">
                <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center shrink-0">
                    <span class="text-primary-foreground font-bold text-sm">V</span>
                </div>
                <span v-if="!collapsed" class="font-semibold text-foreground truncate">Visualisa Admin</span>
            </NuxtLink>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 overflow-y-auto py-4 space-y-1 px-2">
            <template v-for="group in navGroups" :key="group.label">
                <div v-if="!collapsed"
                    class="px-2 py-1 text-xs font-semibold text-muted-foreground uppercase tracking-wider mt-3 first:mt-0">
                    {{ group.label }}
                </div>
                <NuxtLink v-for="item in group.items" :key="item.to" :to="item.to"
                    class="flex items-center gap-3 px-2 py-2 rounded-md text-sm font-medium transition-colors" :class="[
                        isActive(item.to)
                            ? 'bg-primary text-primary-foreground'
                            : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                        collapsed ? 'justify-center' : '',
                    ]" :title="collapsed ? item.label : undefined">
                    <Icon :name="item.icon" class="shrink-0 w-5 h-5" />
                    <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
                </NuxtLink>
            </template>
        </nav>

        <!-- Collapse toggle -->
        <div class="border-t border-border p-2 shrink-0">
            <button
                class="w-full flex items-center justify-center gap-2 px-2 py-2 rounded-md text-muted-foreground hover:bg-accent hover:text-accent-foreground text-sm"
                @click="$emit('toggle')">
                <Icon :name="collapsed ? 'lucide:panel-right-open' : 'lucide:panel-left-close'" class="w-5 h-5" />
                <span v-if="!collapsed">Collapse</span>
            </button>
        </div>
    </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

defineProps<{ collapsed: boolean }>()
defineEmits<{ toggle: [] }>()

const route = useRoute()

const navGroups = [
    {
        label: 'Overview',
        items: [
            { to: '/', icon: 'lucide:layout-dashboard', label: 'Dashboard' },
            { to: '/analytics', icon: 'lucide:bar-chart-3', label: 'Analytics' },
        ],
    },
    {
        label: 'Catalog',
        items: [
            { to: '/products', icon: 'lucide:package', label: 'Products' },
            { to: '/categories', icon: 'lucide:folder-tree', label: 'Categories' },
            { to: '/brands', icon: 'lucide:tag', label: 'Brands' },
        ],
    },
    {
        label: 'Crawler',
        items: [
            { to: '/crawler', icon: 'lucide:search-code', label: 'Crawler Overview' },
            { to: '/crawler/jobs', icon: 'lucide:circle-play', label: 'Jobs' },
            { to: '/crawler/review', icon: 'lucide:clipboard-check', label: 'Review Queue' },
            { to: '/crawler/sources', icon: 'lucide:globe', label: 'Sources' },
            { to: '/crawler/schedules', icon: 'lucide:clock', label: 'Schedules' },
        ],
    },
    {
        label: 'Users',
        items: [
            { to: '/professionals', icon: 'lucide:users', label: 'Professionals' },
            { to: '/billing/plans', icon: 'lucide:credit-card', label: 'Plans' },
        ],
    },
    {
        label: 'System',
        items: [
            { to: '/settings', icon: 'lucide:settings', label: 'Settings' },
        ],
    },
]

function isActive(to: string) {
    if (to === '/') return route.path === '/'
    return route.path.startsWith(to)
}
</script>
