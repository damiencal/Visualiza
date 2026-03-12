<template>
    <header class="border-b border-border bg-card sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <!-- Logo -->
            <NuxtLink to="/dashboard" class="flex items-center gap-2 font-bold text-lg">
                <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                    <span class="text-primary-foreground text-sm font-bold">V</span>
                </div>
                Visualiza
            </NuxtLink>

            <!-- Nav -->
            <nav class="hidden md:flex items-center gap-6 text-sm font-medium">
                <NuxtLink to="/dashboard" class="text-muted-foreground hover:text-foreground transition-colors"
                    active-class="text-foreground">
                    Dashboard
                </NuxtLink>
                <NuxtLink to="/widget" class="text-muted-foreground hover:text-foreground transition-colors"
                    active-class="text-foreground">
                    Widget
                </NuxtLink>
                <NuxtLink to="/bom" class="text-muted-foreground hover:text-foreground transition-colors"
                    active-class="text-foreground">
                    Bill of Materials
                </NuxtLink>
                <NuxtLink to="/billing" class="text-muted-foreground hover:text-foreground transition-colors"
                    active-class="text-foreground">
                    Billing
                </NuxtLink>
            </nav>

            <!-- User -->
            <div class="flex items-center gap-3">
                <span class="text-sm text-muted-foreground hidden sm:block">{{ user?.full_name }}</span>
                <button class="p-2 rounded-md text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    title="Sign out" @click="authStore.logout()">
                    <Icon name="lucide:log-out" class="w-4 h-4" />
                </button>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
const authStore = useAuthStore()
const user = authStore.user
</script>
