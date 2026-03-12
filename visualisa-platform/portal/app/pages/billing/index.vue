<template>
    <div class="max-w-2xl">
        <h1 class="text-2xl font-bold mb-6">Billing</h1>

        <!-- Current plan -->
        <div v-if="subscription" class="bg-card border border-border rounded-xl p-6 mb-6">
            <div class="flex items-start justify-between mb-4">
                <div>
                    <p class="text-sm text-muted-foreground">Current Plan</p>
                    <p class="text-2xl font-bold">{{ subscription.plan_name }}</p>
                    <p class="text-sm text-muted-foreground">${{ subscription.price_usd }}/month</p>
                </div>
                <span class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="subscription.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'">
                    {{ subscription.status }}
                </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm mb-4">
                <div>
                    <p class="text-muted-foreground">BoMs this month</p>
                    <p class="font-medium">{{ subscription.boms_used_this_month }} / {{ subscription.max_boms_per_month
                        === -1 ? '∞' : subscription.max_boms_per_month }}</p>
                </div>
                <div>
                    <p class="text-muted-foreground">Widget deployments</p>
                    <p class="font-medium">{{ subscription.widget_deployments_count }} / {{
                        subscription.max_widget_deployments === -1 ? '∞' : subscription.max_widget_deployments }}</p>
                </div>
                <div>
                    <p class="text-muted-foreground">Next billing</p>
                    <p class="font-medium">{{ fmtDate(subscription.current_period_end) }}</p>
                </div>
                <div>
                    <p class="text-muted-foreground">Renewal</p>
                    <p class="font-medium">{{ subscription.cancel_at_period_end ? 'Cancels at period end' :
                        'Auto-renews' }}</p>
                </div>
            </div>
            <button class="px-4 py-2 border border-border rounded-md text-sm hover:bg-accent" :disabled="portalLoading"
                @click="openPortal">
                {{ portalLoading ? 'Loading…' : 'Manage Subscription →' }}
            </button>
        </div>

        <!-- No plan -->
        <div v-else class="space-y-4">
            <p class="text-muted-foreground mb-6">Choose a plan to get started with Visualisa.</p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div v-for="plan in plans" :key="plan.id" class="bg-card border rounded-xl p-5 relative"
                    :class="plan.is_popular ? 'border-primary ring-2 ring-primary/20' : 'border-border'">
                    <span v-if="plan.is_popular"
                        class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 bg-primary text-primary-foreground text-xs font-semibold rounded-full">
                        Most Popular
                    </span>
                    <h3 class="font-bold text-lg mb-1">{{ plan.name }}</h3>
                    <p class="text-2xl font-bold mb-3">${{ plan.price_usd }}<span
                            class="text-sm font-normal text-muted-foreground">/mo</span></p>
                    <ul class="space-y-1.5 text-sm mb-4">
                        <li class="flex items-center gap-2 text-muted-foreground">
                            <Icon name="lucide:check" class="w-4 h-4 text-green-600 shrink-0" />
                            {{ plan.max_boms_per_month === -1 ? 'Unlimited' : plan.max_boms_per_month }} BoMs/month
                        </li>
                        <li class="flex items-center gap-2 text-muted-foreground">
                            <Icon name="lucide:check" class="w-4 h-4 text-green-600 shrink-0" />
                            {{ plan.max_widget_deployments === -1 ? 'Unlimited' : plan.max_widget_deployments }}
                            deployments
                        </li>
                    </ul>
                    <button class="w-full py-2 rounded-md text-sm font-medium transition-colors"
                        :class="plan.is_popular ? 'bg-primary text-primary-foreground hover:bg-primary/90' : 'border border-border hover:bg-accent'"
                        :disabled="checkoutLoading === plan.id" @click="checkout(plan)">
                        {{ checkoutLoading === plan.id ? 'Loading…' : `Start ${plan.name}` }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'default' })

const api = useApi()
const portalLoading = ref(false)
const checkoutLoading = ref<string | null>(null)

interface Subscription {
    plan_name: string; price_usd: number; status: string
    boms_used_this_month: number; max_boms_per_month: number
    widget_deployments_count: number; max_widget_deployments: number
    current_period_end: string; cancel_at_period_end: boolean
}
interface Plan {
    id: string; name: string; price_usd: number
    max_boms_per_month: number; max_widget_deployments: number; is_popular: boolean
}

const subscription = ref<Subscription | null>(null)
const plans = ref<Plan[]>([])

async function load() {
    const [subData, plansData] = await Promise.allSettled([
        api.get<Subscription>('/api/v1/portal/subscription'),
        api.get<{ items: Plan[] }>('/api/v1/billing/plans'),
    ])
    if (subData.status === 'fulfilled') subscription.value = subData.value
    if (plansData.status === 'fulfilled') plans.value = plansData.value.items
}

async function checkout(plan: Plan) {
    checkoutLoading.value = plan.id
    try {
        const config = useRuntimeConfig()
        const data = await api.post<{ checkout_url: string }>('/api/v1/billing/checkout', {
            plan_id: plan.id,
            success_url: `${config.public.appUrl}/billing?success=1`,
            cancel_url: `${config.public.appUrl}/billing`,
        })
        window.location.href = data.checkout_url
    } finally {
        checkoutLoading.value = null
    }
}

async function openPortal() {
    portalLoading.value = true
    try {
        const config = useRuntimeConfig()
        const data = await api.post<{ portal_url: string }>('/api/v1/billing/portal', {
            return_url: `${config.public.appUrl}/billing`,
        })
        window.location.href = data.portal_url
    } finally {
        portalLoading.value = false
    }
}

function fmtDate(d: string) {
    return new Date(d).toLocaleDateString('es-DO')
}

onMounted(load)
</script>
