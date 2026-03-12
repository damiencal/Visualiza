<template>
    <div />
</template>
<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
const authStore = useAuthStore()
navigateTo(authStore.isAuthenticated ? '/dashboard' : '/login')
</script>
