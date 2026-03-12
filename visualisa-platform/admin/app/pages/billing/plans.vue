<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Billing Plans</h1>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div v-for="plan in plans" :key="plan.id" class="bg-card border rounded-xl p-6 relative"
                :class="plan.is_popular ? 'border-primary ring-2 ring-primary/20' : 'border-border'">
                <span v-if="plan.is_popular"
                    class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 bg-primary text-primary-foreground text-xs font-semibold rounded-full">
                    Popular
                </span>
                <h3 class="font-bold text-xl mb-1">{{ plan.name }}</h3>
                <p class="text-3xl font-bold mb-1">${{ plan.price_usd }}<span
                        class="text-base font-normal text-muted-foreground">/mo</span></p>
                <p class="text-sm text-muted-foreground mb-4">{{ plan.description }}</p>
                <ul class="space-y-2 text-sm mb-6">
                    <li class="flex items-center gap-2">
                        <Icon name="lucide:check" class="w-4 h-4 text-green-600 shrink-0" />
                        {{ plan.max_boms_per_month === -1 ? 'Unlimited' : plan.max_boms_per_month }} BoMs/mo
                    </li>
                    <li class="flex items-center gap-2">
                        <Icon name="lucide:check" class="w-4 h-4 text-green-600 shrink-0" />
                        {{ plan.max_widget_deployments === -1 ? 'Unlimited' : plan.max_widget_deployments }} widget
                        deployments
                    </li>
                    <li v-if="plan.custom_branding" class="flex items-center gap-2">
                        <Icon name="lucide:check" class="w-4 h-4 text-green-600 shrink-0" />
                        Custom branding
                    </li>
                    <li v-if="plan.api_access" class="flex items-center gap-2">
                        <Icon name="lucide:check" class="w-4 h-4 text-green-600 shrink-0" />
                        API access
                    </li>
                </ul>
                <div class="text-xs text-muted-foreground border-t border-border pt-3">
                    <p>Stripe Price ID: <code class="bg-muted px-1 rounded">{{ plan.stripe_price_id || '—' }}</code></p>
                    <p class="mt-1">{{ plan.subscriber_count ?? 0 }} active subscribers</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
interface Plan {
    id: string; name: string; price_usd: number; description: string
    max_boms_per_month: number; max_widget_deployments: number
    custom_branding: boolean; api_access: boolean; is_popular: boolean
    stripe_price_id?: string; subscriber_count?: number
}
const plans = ref<Plan[]>([])

onMounted(async () => {
    const data = await api.get<{ items: Plan[] }>('/api/v1/billing/plans')
    plans.value = data.items
})
</script>
