<template>
    <div class="min-h-screen bg-background">
        <AdminSidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />
        <div class="transition-all duration-300" :class="sidebarCollapsed ? 'ml-16' : 'ml-64'">
            <AdminHeader @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
            <main class="p-6">
                <slot />
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const sidebarCollapsed = ref(false)

defineOptions({ name: 'AdminLayout' })
</script>
