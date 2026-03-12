<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Crawl Jobs</h1>
        </div>

        <div class="bg-card border border-border rounded-xl overflow-hidden">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-border text-left">
                        <th class="py-3 px-4 font-medium text-muted-foreground">Job ID</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Source</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden sm:table-cell">Triggered</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Duration</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Products</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Status</th>
                        <th class="py-3 px-4" />
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loading">
                        <td colspan="7" class="py-10 text-center text-muted-foreground">
                            <Icon name="lucide:loader-circle" class="w-5 h-5 animate-spin inline-block mr-2" />Loading…
                        </td>
                    </tr>
                    <tr v-for="job in jobs" :key="job.id"
                        class="border-b border-border last:border-0 hover:bg-muted/30">
                        <td class="py-3 px-4 font-mono text-xs text-muted-foreground">{{ job.id.slice(0, 8) }}</td>
                        <td class="py-3 px-4 font-medium">{{ job.source_name }}</td>
                        <td class="py-3 px-4 text-muted-foreground hidden sm:table-cell">{{ fmt(job.started_at) }}</td>
                        <td class="py-3 px-4 text-muted-foreground">{{ duration(job) }}</td>
                        <td class="py-3 px-4">
                            <span class="font-medium">{{ job.products_found }}</span>
                            <span v-if="job.products_new" class="text-xs text-green-600 ml-1">(+{{ job.products_new }}
                                new)</span>
                        </td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="sc(job.status)">{{
                                job.status }}</span>
                        </td>
                        <td class="py-3 px-4">
                            <NuxtLink :to="`/crawler/jobs/${job.id}`"
                                class="text-xs underline text-muted-foreground hover:text-foreground">View</NuxtLink>
                        </td>
                    </tr>
                </tbody>
            </table>
            <!-- Pagination -->
            <div
                class="flex items-center justify-between px-4 py-3 border-t border-border text-sm text-muted-foreground">
                <span>{{ total }} total jobs</span>
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
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
const jobs = ref<Job[]>([])
const loading = ref(true)
const page = ref(1)
const total = ref(0)
const pageSize = 25

interface Job {
    id: string; source_name: string; started_at?: string; completed_at?: string
    products_found: number; products_new?: number; status: string; error_message?: string
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function fetch() {
    loading.value = true
    const data = await api.get<{ items: Job[]; total: number }>(`/api/v1/crawler/jobs?skip=${(page.value - 1) * pageSize}&limit=${pageSize}`)
    jobs.value = data.items
    total.value = data.total
    loading.value = false
}

function fmt(d?: string) {
    return d ? new Date(d).toLocaleString('es-DO') : '—'
}

function duration(j: Job) {
    if (!j.started_at || !j.completed_at) return '—'
    const diff = (new Date(j.completed_at).getTime() - new Date(j.started_at).getTime()) / 1000
    return diff < 60 ? `${diff.toFixed(0)}s` : `${(diff / 60).toFixed(1)}m`
}

function sc(s: string) {
    return {
        completed: 'bg-green-100 text-green-700',
        running: 'bg-blue-100 text-blue-700',
        failed: 'bg-red-100 text-red-700',
        pending: 'bg-gray-100 text-gray-600',
    }[s] ?? 'bg-muted text-muted-foreground'
}

onMounted(fetch)
</script>
