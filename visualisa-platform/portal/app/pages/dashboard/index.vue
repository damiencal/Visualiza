<template>
    <div>
        <div class="mb-8">
            <h1 class="text-3xl font-bold">Welcome back, {{ user?.full_name?.split(' ')[0] }}!</h1>
            <p class="text-muted-foreground mt-1">Here's a summary of your Visualisa account.</p>
        </div>

        <!-- Plan banner -->
        <div v-if="subscription"
            class="bg-accent border border-accent-foreground/10 rounded-xl p-4 mb-6 flex items-center justify-between">
            <div>
                <p class="font-semibold">{{ subscription.plan_name }} Plan</p>
                <p class="text-sm text-muted-foreground">
                    {{ subscription.boms_used_this_month }} / {{ subscription.max_boms_per_month === -1 ? '∞' :
                        subscription.max_boms_per_month }} BoMs this month
                </p>
            </div>
            <NuxtLink to="/billing"
                class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
                Manage Billing
            </NuxtLink>
        </div>

        <div v-else class="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6 flex items-center justify-between">
            <div>
                <p class="font-semibold text-yellow-900">No active plan</p>
                <p class="text-sm text-yellow-700">Choose a plan to unlock the full widget and BoM features.</p>
            </div>
            <NuxtLink to="/pricing"
                class="px-4 py-2 bg-yellow-600 text-white rounded-md text-sm font-medium hover:bg-yellow-700">
                View Plans
            </NuxtLink>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div v-for="s in stats" :key="s.label" class="bg-card border border-border rounded-xl p-5">
                <Icon :name="s.icon" class="w-5 h-5 text-muted-foreground mb-2" />
                <p class="text-2xl font-bold">{{ s.value }}</p>
                <p class="text-sm text-muted-foreground">{{ s.label }}</p>
            </div>
        </div>

        <!-- Quick links -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <QuickLinkCard title="Widget Setup" description="Configure and embed your visualizer widget on any website."
                icon="lucide:code-2" to="/widget" />
            <QuickLinkCard title="Bill of Materials"
                description="View and share renovation cost estimates with your clients." icon="lucide:file-spreadsheet"
                to="/bom" />
            <QuickLinkCard title="Profile Settings" description="Update your professional profile and branding."
                icon="lucide:user-circle" to="/profile" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useApi } from '~/composables/useApi'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: 'default' })

const api = useApi()
const authStore = useAuthStore()
const user = authStore.user

interface Subscription {
    plan_name: string
    boms_used_this_month: number
    max_boms_per_month: number
    widget_deployments_count: number
}

const subscription = ref<Subscription | null>(null)
const stats = computed(() => [
    { label: 'BoMs this month', value: subscription.value?.boms_used_this_month ?? '—', icon: 'lucide:file-text' },
    { label: 'Widget deployments', value: subscription.value?.widget_deployments_count ?? '—', icon: 'lucide:globe' },
    { label: 'Plan limit', value: subscription.value?.max_boms_per_month === -1 ? '∞' : (subscription.value?.max_boms_per_month ?? '—'), icon: 'lucide:shield-check' },
    { label: 'Account age', value: '—', icon: 'lucide:calendar' },
])

onMounted(async () => {
    try {
        subscription.value = await api.get<Subscription>('/api/v1/portal/usage-summary')
    } catch {
        // not yet subscribed
    }
})
</script>
