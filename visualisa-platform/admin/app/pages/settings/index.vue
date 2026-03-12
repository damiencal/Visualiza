<template>
    <div>
        <h1 class="text-2xl font-bold mb-6">Settings</h1>
        <div class="bg-card border border-border rounded-xl p-6 max-w-2xl space-y-4">
            <p class="text-muted-foreground text-sm">Platform-wide settings. These values are managed via environment
                variables and the backend config. Edit <code class="bg-muted px-1 rounded">.env</code> and restart the
                backend service to apply changes.</p>
            <div class="grid grid-cols-2 gap-3 text-sm">
                <div class="text-muted-foreground">API Base URL</div>
                <div class="font-mono">{{ apiBase }}</div>
                <div class="text-muted-foreground">ITBIS Rate</div>
                <div>18%</div>
                <div class="text-muted-foreground">Currency</div>
                <div>DOP (RD$)</div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
definePageMeta({ layout: 'admin' })
const config = useRuntimeConfig()
const apiBase = config.public.apiBaseUrl
</script>
