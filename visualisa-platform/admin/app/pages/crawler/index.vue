<template>
    <div>
        <h1 class="text-2xl font-bold mb-6">Crawler Overview</h1>

        <!-- Source cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div v-for="source in sources" :key="source.id" class="bg-card border border-border rounded-xl p-5">
                <div class="flex items-start justify-between mb-3">
                    <div>
                        <h3 class="font-semibold">{{ source.name }}</h3>
                        <a :href="source.base_url" target="_blank" rel="noopener noreferrer"
                            class="text-xs text-muted-foreground hover:underline truncate max-w-[180px] block">
                            {{ source.base_url }}
                        </a>
                    </div>
                    <span class="px-2 py-0.5 rounded-full text-xs font-medium"
                        :class="source.is_enabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
                        {{ source.is_enabled ? 'Active' : 'Disabled' }}
                    </span>
                </div>

                <div class="space-y-1 text-sm text-muted-foreground mb-4">
                    <div class="flex justify-between">
                        <span>Last run</span>
                        <span>{{ formatDate(source.last_crawl_at) }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Products collected</span>
                        <span>{{ source.total_products_found ?? '—' }}</span>
                    </div>
                </div>

                <button
                    class="w-full py-2 text-sm font-medium border border-border rounded-md hover:bg-accent flex items-center justify-center gap-2"
                    :disabled="triggering === source.id" @click="triggerCrawl(source)">
                    <Icon :name="triggering === source.id ? 'lucide:loader-circle' : 'lucide:play'" class="w-4 h-4"
                        :class="{ 'animate-spin': triggering === source.id }" />
                    {{ triggering === source.id ? 'Starting…' : 'Run Now' }}
                </button>
            </div>
        </div>

        <!-- Recent jobs table -->
        <div class="bg-card border border-border rounded-xl overflow-hidden">
            <div class="flex items-center justify-between px-5 py-4 border-b border-border">
                <h2 class="font-semibold">Recent Jobs</h2>
                <NuxtLink to="/crawler/jobs" class="text-sm text-muted-foreground hover:text-foreground">View all →
                </NuxtLink>
            </div>
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-border text-left">
                        <th class="py-3 px-4 font-medium text-muted-foreground">Source</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden sm:table-cell">Started</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Progress</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Found</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Status</th>
                        <th class="py-3 px-4" />
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loadingJobs">
                        <td colspan="6" class="py-10 text-center text-muted-foreground">
                            <Icon name="lucide:loader-circle" class="w-5 h-5 animate-spin inline-block mr-2" />Loading…
                        </td>
                    </tr>
                    <tr v-for="job in jobs" :key="job.id"
                        class="border-b border-border last:border-0 hover:bg-muted/30">
                        <td class="py-3 px-4 font-medium">{{ job.source_name }}</td>
                        <td class="py-3 px-4 text-muted-foreground hidden sm:table-cell">{{ formatDate(job.started_at)
                            }}</td>
                        <td class="py-3 px-4">
                            <div class="flex items-center gap-2">
                                <div class="w-24 h-1.5 bg-muted rounded-full overflow-hidden">
                                    <div class="h-full bg-primary rounded-full transition-all"
                                        :style="{ width: `${job.progress_pct}%` }" />
                                </div>
                                <span class="text-xs text-muted-foreground">{{ job.progress_pct }}%</span>
                            </div>
                        </td>
                        <td class="py-3 px-4">{{ job.products_found }}</td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="statusClass(job.status)">
                                {{ job.status }}
                            </span>
                        </td>
                        <td class="py-3 px-4">
                            <NuxtLink :to="`/crawler/jobs/${job.id}`"
                                class="text-xs text-muted-foreground hover:text-foreground underline">
                                Details
                            </NuxtLink>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
const sources = ref<Source[]>([])
const jobs = ref<Job[]>([])
const loadingJobs = ref(true)
const triggering = ref<string | null>(null)

interface Source {
    id: string; name: string; base_url: string; is_enabled: boolean
    last_crawl_at?: string; total_products_found?: number
}
interface Job {
    id: string; source_name: string; started_at?: string
    progress_pct: number; products_found: number; status: string
}

async function loadData() {
    const [sourcesRes, jobsRes] = await Promise.all([
        api.get<{ items: Source[] }>('/api/v1/crawler/sources'),
        api.get<{ items: Job[] }>('/api/v1/crawler/jobs?limit=10'),
    ])
    sources.value = sourcesRes.items
    jobs.value = jobsRes.items
    loadingJobs.value = false
}

async function triggerCrawl(source: Source) {
    triggering.value = source.id
    try {
        await api.post(`/api/v1/crawler/sources/${source.id}/trigger`, {})
        await loadData()
    } finally {
        triggering.value = null
    }
}

function formatDate(d?: string) {
    if (!d) return '—'
    return new Date(d).toLocaleString('es-DO')
}

function statusClass(s: string) {
    return {
        completed: 'bg-green-100 text-green-700',
        running: 'bg-blue-100 text-blue-700',
        failed: 'bg-red-100 text-red-700',
        pending: 'bg-gray-100 text-gray-600',
    }[s] ?? 'bg-muted text-muted-foreground'
}

onMounted(loadData)
</script>
