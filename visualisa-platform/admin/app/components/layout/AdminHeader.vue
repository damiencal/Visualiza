<template>
    <header class="h-16 border-b border-border bg-card flex items-center justify-between px-6 sticky top-0 z-40">
        <div class="flex items-center gap-4">
            <button class="p-2 rounded-md text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                @click="$emit('toggle-sidebar')">
                <Icon name="lucide:menu" class="w-5 h-5" />
            </button>
            <AdminBreadcrumb />
        </div>

        <div class="flex items-center gap-3">
            <!-- Search -->
            <button class="p-2 rounded-md text-muted-foreground hover:bg-accent hover:text-accent-foreground">
                <Icon name="lucide:search" class="w-5 h-5" />
            </button>

            <!-- Notifications -->
            <button class="relative p-2 rounded-md text-muted-foreground hover:bg-accent hover:text-accent-foreground">
                <Icon name="lucide:bell" class="w-5 h-5" />
                <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-destructive rounded-full" />
            </button>

            <!-- User menu -->
            <div class="flex items-center gap-2 pl-3 border-l border-border">
                <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                    <span class="text-primary-foreground text-sm font-medium">A</span>
                </div>
                <div class="hidden sm:block">
                    <p class="text-sm font-medium leading-none">Admin</p>
                    <p class="text-xs text-muted-foreground">superadmin</p>
                </div>
                <button class="p-1 text-muted-foreground hover:text-foreground" title="Sign out"
                    @click="authStore.logout()">
                    <Icon name="lucide:log-out" class="w-4 h-4" />
                </button>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

defineEmits<{ 'toggle-sidebar': [] }>()
const authStore = useAuthStore()
</script>
