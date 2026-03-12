<template>
    <div class="max-w-3xl">
        <div class="flex items-center gap-3 mb-6">
            <NuxtLink to="/bom" class="text-muted-foreground hover:text-foreground">
                <Icon name="lucide:arrow-left" class="w-5 h-5" />
            </NuxtLink>
            <h1 class="text-2xl font-bold">Bill of Materials</h1>
        </div>

        <div v-if="loading" class="flex items-center justify-center py-16">
            <Icon name="lucide:loader-circle" class="w-6 h-6 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="bom" class="space-y-6">
            <!-- Header card -->
            <div class="bg-card border border-border rounded-xl p-6">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <p class="text-sm text-muted-foreground">Client</p>
                        <p class="font-semibold">{{ bom.client_name || 'Anonymous' }}</p>
                    </div>
                    <button
                        class="flex items-center gap-2 px-3 py-2 border border-border rounded-md text-sm hover:bg-accent"
                        @click="share">
                        <Icon name="lucide:share-2" class="w-4 h-4" />
                        Share
                    </button>
                </div>
                <div class="grid grid-cols-3 gap-4 pt-4 border-t border-border text-sm">
                    <div>
                        <p class="text-muted-foreground">Subtotal</p>
                        <p class="font-medium">{{ fmtDOP(bom.total_before_tax) }}</p>
                    </div>
                    <div>
                        <p class="text-muted-foreground">ITBIS (18%)</p>
                        <p class="font-medium">{{ fmtDOP(bom.tax_amount) }}</p>
                    </div>
                    <div>
                        <p class="text-muted-foreground font-medium">Total</p>
                        <p class="text-xl font-bold">{{ fmtDOP(bom.total_with_tax) }}</p>
                    </div>
                </div>
            </div>

            <!-- Line items -->
            <div class="bg-card border border-border rounded-xl overflow-hidden">
                <div class="px-5 py-4 border-b border-border">
                    <h2 class="font-semibold">Line Items</h2>
                </div>
                <table class="w-full text-sm">
                    <thead>
                        <tr class="border-b border-border text-left">
                            <th class="py-3 px-4 font-medium text-muted-foreground">Product</th>
                            <th class="py-3 px-4 font-medium text-muted-foreground text-right">Area</th>
                            <th class="py-3 px-4 font-medium text-muted-foreground text-right hidden sm:table-cell">Qty
                            </th>
                            <th class="py-3 px-4 font-medium text-muted-foreground text-right">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in bom.line_items" :key="item.id" class="border-b border-border last:border-0">
                            <td class="py-3 px-4">
                                <p class="font-medium">{{ item.product_name }}</p>
                                <p class="text-xs text-muted-foreground">{{ item.brand_name }}</p>
                            </td>
                            <td class="py-3 px-4 text-right text-muted-foreground">{{ item.area_m2 }} m²</td>
                            <td class="py-3 px-4 text-right text-muted-foreground hidden sm:table-cell">
                                {{ item.quantity_needed }} {{ item.unit }}
                                <span v-if="item.wastage_pct" class="text-xs">(+{{ item.wastage_pct }}%)</span>
                            </td>
                            <td class="py-3 px-4 text-right font-mono">{{ fmtDOP(item.subtotal_dop) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'default' })

const route = useRoute()
const api = useApi()
const id = route.params.id as string
const loading = ref(true)

interface BomLineItem {
    id: string; product_name: string; brand_name?: string
    area_m2: number; quantity_needed: number; unit: string
    wastage_pct?: number; subtotal_dop: number
}
interface BoM {
    id: string; client_name?: string
    total_before_tax: number; tax_amount: number; total_with_tax: number
    line_items: BomLineItem[]
}

const bom = ref<BoM | null>(null)

onMounted(async () => {
    bom.value = await api.get<BoM>(`/api/v1/bom/${id}`)
    loading.value = false
})

function fmtDOP(v: number) {
    return new Intl.NumberFormat('es-DO', { style: 'currency', currency: 'DOP', maximumFractionDigits: 0 }).format(v)
}

async function share() {
    const data = await api.post<{ share_url: string }>(`/api/v1/bom/${id}/share`, {})
    await navigator.clipboard.writeText(data.share_url)
    alert('Share link copied!')
}
</script>
