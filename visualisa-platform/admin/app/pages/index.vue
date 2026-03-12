<template>
    <div>
        <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

        <!-- Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
            <StatCard v-for="stat in stats" :key="stat.label" :label="stat.label" :value="stat.value"
                :delta="stat.delta" :icon="stat.icon" :loading="statsLoading" />
        </div>

        <!-- Charts row -->
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8">
            <!-- Products over time -->
            <div class="bg-card rounded-xl border border-border p-5">
                <h2 class="font-semibold mb-4">Products Collected (last 7 crawl jobs)</h2>
                <ClientOnly>
                    <Line v-if="!statsLoading" :data="chartData" :options="chartOptions" class="max-h-64" />
                </ClientOnly>
            </div>

            <!-- Crawl job status breakdown -->
            <div class="bg-card rounded-xl border border-border p-5">
                <h2 class="font-semibold mb-4">Last Crawl Jobs</h2>
                <div class="space-y-3">
                    <div v-for="job in recentJobs" :key="job.id" class="flex items-center justify-between text-sm">
                        <span class="font-medium">{{ job.source_name }}</span>
                        <div class="flex items-center gap-3">
                            <span class="text-muted-foreground">{{ job.products_found }} products</span>
                            <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="statusClass(job.status)">
                                {{ job.status }}
                            </span>
                        </div>
                    </div>
                    <p v-if="!recentJobs.length && !statsLoading" class="text-muted-foreground text-sm">No recent jobs
                    </p>
                </div>
            </div>
        </div>

        <!-- Review queue notice -->
        <div v-if="pendingReview > 0"
            class="flex items-center gap-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-4">
            <Icon name="lucide:alert-circle" class="w-5 h-5 text-yellow-600 shrink-0" />
            <div class="flex-1">
                <p class="font-medium text-yellow-900 dark:text-yellow-200">{{ pendingReview }} products awaiting review
                </p>
                <p class="text-sm text-yellow-700 dark:text-yellow-400">Crawled products need approval before appearing
                    in the catalog.</p>
            </div>
            <NuxtLink to="/crawler/review"
                class="px-4 py-2 bg-yellow-600 text-white rounded-md text-sm font-medium hover:bg-yellow-700">
                Review now
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js'
import { useApi } from '~/composables/useApi'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

definePageMeta({ layout: 'admin' })

const api = useApi()
const statsLoading = ref(true)
const stats = ref([
    { label: 'Total Products', value: '—', delta: '', icon: 'lucide:package' },
    { label: 'Active Professionals', value: '—', delta: '', icon: 'lucide:users' },
    { label: 'Pending Review', value: '—', delta: '', icon: 'lucide:clipboard-list' },
    { label: 'Monthly Revenue', value: '—', delta: '', icon: 'lucide:dollar-sign' },
])
const recentJobs = ref<Array<{ id: string; source_name: string; products_found: number; status: string }>>([])
const pendingReview = ref(0)

const chartData = ref({
    labels: [] as string[],
    datasets: [
        {
            label: 'Products Found',
            data: [] as number[],
            borderColor: 'hsl(240 5.9% 10%)',
            backgroundColor: 'hsl(240 5.9% 10% / 0.1)',
            fill: true,
            tension: 0.3,
        },
    ],
})

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
}

async function loadStats() {
    try {
        const [jobsRes, productsRes] = await Promise.all([
            api.get<{ items: typeof recentJobs.value; total: number }>('/api/v1/crawler/jobs?limit=7'),
            api.get<{ pending_review: number; total: number }>('/api/v1/products?limit=1'),
        ])
        recentJobs.value = jobsRes.items
        pendingReview.value = 0 // Would come from stats endpoint

        chartData.value.labels = jobsRes.items.map((j) => j.source_name)
        chartData.value.datasets[0].data = jobsRes.items.map((j) => j.products_found)

        stats.value[0].value = String(productsRes.total ?? '—')
    } catch {
        // silently fail — admin login may redirect
    } finally {
        statsLoading.value = false
    }
}

function statusClass(status: string) {
    return {
        completed: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
        running: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
        failed: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
        pending: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    }[status] ?? 'bg-muted text-muted-foreground'
}

onMounted(loadStats)
</script>
