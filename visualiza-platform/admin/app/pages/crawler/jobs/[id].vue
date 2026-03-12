<template>
    <div class="max-w-4xl">
        <div class="flex items-center gap-3 mb-6">
            <NuxtLink to="/crawler/jobs" class="text-muted-foreground hover:text-foreground">
                <Icon name="lucide:arrow-left" class="w-5 h-5" />
            </NuxtLink>
            <h1 class="text-2xl font-bold">Job Details</h1>
            <span v-if="job" class="px-2 py-0.5 rounded-full text-xs font-medium" :class="sc(job.status)">{{ job.status
                }}</span>
        </div>

        <div v-if="loading" class="flex items-center justify-center py-16 text-muted-foreground">
            <Icon name="lucide:loader-circle" class="w-6 h-6 animate-spin mr-2" />Loading…
        </div>

        <div v-else-if="job" class="space-y-6">
            <!-- Summary -->
            <div class="bg-card border border-border rounded-xl p-5 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                    <p class="text-xs text-muted-foreground">Source</p>
                    <p class="font-medium">{{ job.source_name }}</p>
                </div>
                <div>
                    <p class="text-xs text-muted-foreground">Products Found</p>
                    <p class="font-medium">{{ job.products_found }}</p>
                </div>
                <div>
                    <p class="text-xs text-muted-foreground">New Products</p>
                    <p class="font-medium text-green-600">+{{ job.products_new ?? 0 }}</p>
                </div>
                <div>
                    <p class="text-xs text-muted-foreground">Pages Crawled</p>
                    <p class="font-medium">{{ job.pages_crawled ?? '—' }}</p>
                </div>
                <div>
                    <p class="text-xs text-muted-foreground">Started</p>
                    <p class="font-medium">{{ fmt(job.started_at) }}</p>
                </div>
                <div>
                    <p class="text-xs text-muted-foreground">Completed</p>
                    <p class="font-medium">{{ fmt(job.completed_at) }}</p>
                </div>
                <div>
                    <p class="text-xs text-muted-foreground">Duration</p>
                    <p class="font-medium">{{ duration }}</p>
                </div>
                <div v-if="job.celery_task_id">
                    <p class="text-xs text-muted-foreground">Task ID</p>
                    <p class="font-mono text-xs">{{ job.celery_task_id }}</p>
                </div>
            </div>

            <!-- Error message -->
            <div v-if="job.error_message" class="bg-destructive/10 border border-destructive/30 rounded-xl p-4">
                <p class="text-sm font-medium text-destructive mb-1">Error</p>
                <pre class="text-xs text-destructive/80 whitespace-pre-wrap">{{ job.error_message }}</pre>
            </div>

            <!-- Progress bar -->
            <div v-if="job.status === 'running'" class="bg-card border border-border rounded-xl p-5">
                <div class="flex items-center justify-between text-sm mb-2">
                    <span>Progress</span>
                    <span class="font-medium">{{ job.progress_pct }}%</span>
                </div>
                <div class="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div class="h-full bg-primary rounded-full transition-all"
                        :style="{ width: `${job.progress_pct}%` }" />
                </div>
            </div>

            <!-- Results link -->
            <div class="bg-card border border-border rounded-xl p-5">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="font-medium">Crawl Results</p>
                        <p class="text-sm text-muted-foreground">Products found need to be reviewed before they appear
                            in the catalog.</p>
                    </div>
                    <NuxtLink to="/crawler/review"
                        class="px-4 py-2 border border-border rounded-md text-sm hover:bg-accent flex items-center gap-2">
                        <Icon name="lucide:clipboard-check" class="w-4 h-4" />
                        Review Queue
                    </NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const route = useRoute()
const api = useApi()
const id = route.params.id as string
const loading = ref(true)

interface Job {
    id: string; source_name: string; started_at?: string; completed_at?: string
    products_found: number; products_new?: number; pages_crawled?: number
    status: string; error_message?: string; progress_pct: number; celery_task_id?: string
}
const job = ref<Job | null>(null)

const duration = computed(() => {
    if (!job.value?.started_at || !job.value?.completed_at) return '—'
    const d = (new Date(job.value.completed_at).getTime() - new Date(job.value.started_at).getTime()) / 1000
    return d < 60 ? `${d.toFixed(0)}s` : `${(d / 60).toFixed(1)}m`
})

async function load() {
    job.value = await api.get<Job>(`/api/v1/crawler/jobs/${id}`)
    loading.value = false
}

function fmt(d?: string) {
    return d ? new Date(d).toLocaleString('es-DO') : '—'
}

function sc(s: string) {
    return {
        completed: 'bg-green-100 text-green-700',
        running: 'bg-blue-100 text-blue-700',
        failed: 'bg-red-100 text-red-700',
        pending: 'bg-gray-100 text-gray-600',
    }[s] ?? 'bg-muted text-muted-foreground'
}

// Poll while running
let poll: ReturnType<typeof setInterval> | null = null
onMounted(() => {
    load()
    poll = setInterval(() => {
        if (job.value?.status === 'running') load()
    }, 5000)
})
onUnmounted(() => { if (poll) clearInterval(poll) })
</script>
