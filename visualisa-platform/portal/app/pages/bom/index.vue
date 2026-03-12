<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <div>
                <h1 class="text-2xl font-bold">Bill of Materials</h1>
                <p class="text-muted-foreground mt-1">Cost estimates generated for your clients.</p>
            </div>
        </div>

        <div class="bg-card border border-border rounded-xl overflow-hidden">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-border text-left">
                        <th class="py-3 px-4 font-medium text-muted-foreground">Client / Reference</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden md:table-cell">Rooms</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden sm:table-cell">Total (DOP)</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Created</th>
                        <th class="py-3 px-4" />
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loading">
                        <td colspan="5" class="py-10 text-center text-muted-foreground">
                            <Icon name="lucide:loader-circle" class="w-5 h-5 animate-spin inline-block mr-2" />Loading…
                        </td>
                    </tr>
                    <tr v-else-if="!boms.length">
                        <td colspan="5" class="py-12 text-center text-muted-foreground">
                            No BoMs yet. Your clients will generate them through the widget.
                        </td>
                    </tr>
                    <tr v-for="bom in boms" :key="bom.id"
                        class="border-b border-border last:border-0 hover:bg-muted/30">
                        <td class="py-3 px-4">
                            <p class="font-medium">{{ bom.client_name || 'Anonymous' }}</p>
                            <p class="text-xs text-muted-foreground font-mono">{{ bom.id.slice(0, 8) }}</p>
                        </td>
                        <td class="py-3 px-4 text-muted-foreground hidden md:table-cell">{{ bom.line_items_count }}</td>
                        <td class="py-3 px-4 font-mono text-right hidden sm:table-cell">{{ fmtDOP(bom.total_with_tax) }}
                        </td>
                        <td class="py-3 px-4 text-muted-foreground text-xs">{{ fmtDate(bom.created_at) }}</td>
                        <td class="py-3 px-4">
                            <div class="flex items-center justify-end gap-1">
                                <NuxtLink :to="`/bom/${bom.id}`"
                                    class="p-1.5 rounded hover:bg-accent text-muted-foreground" title="View">
                                    <Icon name="lucide:eye" class="w-4 h-4" />
                                </NuxtLink>
                                <button class="p-1.5 rounded hover:bg-accent text-muted-foreground" title="Share link"
                                    @click="shareBoM(bom)">
                                    <Icon name="lucide:share-2" class="w-4 h-4" />
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <!-- Pagination -->
            <div
                class="flex items-center justify-between px-4 py-3 border-t border-border text-sm text-muted-foreground">
                <span>{{ total }} total</span>
                <div class="flex gap-1">
                    <button :disabled="page === 1"
                        class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                        @click="page--; fetch()">
                        <Icon name="lucide:chevron-left" class="w-4 h-4" />
                    </button>
                    <span class="px-2">{{ page }} / {{ pages }}</span>
                    <button :disabled="page >= pages"
                        class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                        @click="page++; fetch()">
                        <Icon name="lucide:chevron-right" class="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'default' })

const api = useApi()
const loading = ref(true)
const boms = ref<BoM[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20

interface BoM {
    id: string; client_name?: string; line_items_count: number
    total_with_tax: number; created_at: string; share_token?: string
}

const pages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function fetch() {
    loading.value = true
    const data = await api.get<{ items: BoM[]; total: number }>(`/api/v1/portal/bom?skip=${(page.value - 1) * pageSize}&limit=${pageSize}`)
    boms.value = data.items
    total.value = data.total
    loading.value = false
}

function fmtDOP(v: number) {
    return new Intl.NumberFormat('es-DO', { style: 'currency', currency: 'DOP', maximumFractionDigits: 0 }).format(v)
}

function fmtDate(d: string) {
    return new Date(d).toLocaleDateString('es-DO')
}

async function shareBoM(bom: BoM) {
    const data = await api.post<{ share_url: string }>(`/api/v1/bom/${bom.id}/share`, {})
    await navigator.clipboard.writeText(data.share_url)
    alert('Share link copied to clipboard!')
}

onMounted(fetch)
</script>
