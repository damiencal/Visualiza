<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <div>
                <h1 class="text-2xl font-bold">Review Queue</h1>
                <p class="text-muted-foreground text-sm mt-1">Approve or reject crawled products before they appear in
                    the catalog.</p>
            </div>
            <div class="flex items-center gap-2">
                <button v-if="selected.size > 0"
                    class="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md text-sm font-medium hover:bg-green-700"
                    @click="bulkApprove">
                    <Icon name="lucide:check" class="w-4 h-4" />
                    Approve ({{ selected.size }})
                </button>
                <button v-if="selected.size > 0"
                    class="flex items-center gap-2 px-4 py-2 bg-destructive text-destructive-foreground rounded-md text-sm font-medium hover:bg-destructive/90"
                    @click="bulkReject">
                    <Icon name="lucide:x" class="w-4 h-4" />
                    Reject ({{ selected.size }})
                </button>
            </div>
        </div>

        <!-- Filters -->
        <div class="bg-card border border-border rounded-xl p-4 mb-4 flex flex-wrap gap-3">
            <select v-model="sourceFilter" class="px-3 py-2 rounded-md border border-input bg-background text-sm"
                @change="fetch">
                <option value="">All Sources</option>
                <option v-for="s in sources" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <select v-model="surfaceFilter" class="px-3 py-2 rounded-md border border-input bg-background text-sm"
                @change="fetch">
                <option value="">All Surfaces</option>
                <option value="floor">Floor</option>
                <option value="wall">Wall</option>
                <option value="ceiling">Ceiling</option>
                <option value="countertop">Countertop</option>
                <option value="other">Other</option>
            </select>
        </div>

        <!-- Cards grid -->
        <div v-if="loading" class="flex items-center justify-center py-16">
            <Icon name="lucide:loader-circle" class="w-6 h-6 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="!results.length" class="flex flex-col items-center py-16 text-center">
            <Icon name="lucide:inbox" class="w-12 h-12 text-muted-foreground mb-3" />
            <p class="font-medium">Review queue is empty</p>
            <p class="text-muted-foreground text-sm">Run a crawler job to collect products for review.</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            <ProductReviewCard v-for="result in results" :key="result.id" :result="result"
                :selected="selected.has(result.id)" @toggle-select="toggleSelect(result.id)" @approve="approve(result)"
                @reject="reject(result)" />
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between mt-4 text-sm text-muted-foreground">
            <span>{{ total }} pending</span>
            <div class="flex items-center gap-1">
                <button :disabled="page === 1"
                    class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                    @click="page--; fetch()">
                    <Icon name="lucide:chevron-left" class="w-4 h-4" />
                </button>
                <span class="px-2">{{ page }} / {{ totalPages }}</span>
                <button :disabled="page >= totalPages"
                    class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                    @click="page++; fetch()">
                    <Icon name="lucide:chevron-right" class="w-4 h-4" />
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
const loading = ref(true)
const results = ref<CrawlResult[]>([])
const sources = ref<{ id: string; name: string }[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 18
const sourceFilter = ref('')
const surfaceFilter = ref('')
const selected = ref(new Set<string>())

interface CrawlResult {
    id: string; name: string; price_dop: number; surface_type: string
    brand_name?: string; image_url?: string; source_url: string; source_name: string
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function fetch() {
    loading.value = true
    selected.value.clear()
    const params = new URLSearchParams({
        status: 'pending_review',
        skip: String((page.value - 1) * pageSize),
        limit: String(pageSize),
    })
    if (sourceFilter.value) params.set('source_id', sourceFilter.value)
    if (surfaceFilter.value) params.set('surface_type', surfaceFilter.value)

    const [resultsRes, sourcesRes] = await Promise.all([
        api.get<{ items: CrawlResult[]; total: number }>(`/api/v1/crawler/results?${params}`),
        sources.value.length ? Promise.resolve({ items: sources.value }) : api.get<{ items: { id: string; name: string }[] }>('/api/v1/crawler/sources'),
    ])
    results.value = resultsRes.items
    total.value = resultsRes.total
    sources.value = (sourcesRes as { items: { id: string; name: string }[] }).items
    loading.value = false
}

function toggleSelect(id: string) {
    if (selected.value.has(id)) selected.value.delete(id)
    else selected.value.add(id)
    selected.value = new Set(selected.value)
}

async function approve(result: CrawlResult) {
    await api.post(`/api/v1/crawler/results/${result.id}/approve`, {})
    results.value = results.value.filter((r) => r.id !== result.id)
    total.value--
}

async function reject(result: CrawlResult) {
    await api.post(`/api/v1/crawler/results/${result.id}/reject`, {})
    results.value = results.value.filter((r) => r.id !== result.id)
    total.value--
}

async function bulkApprove() {
    await Promise.all([...selected.value].map((id) => api.post(`/api/v1/crawler/results/${id}/approve`, {})))
    fetch()
}

async function bulkReject() {
    await Promise.all([...selected.value].map((id) => api.post(`/api/v1/crawler/results/${id}/reject`, {})))
    fetch()
}

onMounted(fetch)
</script>
