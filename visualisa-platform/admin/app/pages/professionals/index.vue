<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Professionals</h1>
        </div>

        <!-- Search -->
        <div class="mb-4">
            <input v-model="search" type="search" placeholder="Search by name or email…"
                class="px-3 py-2 rounded-md border border-input bg-background text-sm w-72 focus:outline-none focus:ring-2 focus:ring-ring"
                @input="debouncedFetch" />
        </div>

        <div class="bg-card border border-border rounded-xl overflow-hidden">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-border text-left">
                        <th class="py-3 px-4 font-medium text-muted-foreground">Professional</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden md:table-cell">Plan</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden lg:table-cell">BoMs Generated</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden lg:table-cell">Widget Deployments
                        </th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Joined</th>
                        <th class="py-3 px-4" />
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loading">
                        <td colspan="6" class="py-10 text-center text-muted-foreground">
                            <Icon name="lucide:loader-circle" class="w-5 h-5 animate-spin inline-block mr-2" />Loading…
                        </td>
                    </tr>
                    <tr v-for="pro in professionals" :key="pro.id"
                        class="border-b border-border last:border-0 hover:bg-muted/30">
                        <td class="py-3 px-4">
                            <p class="font-medium">{{ pro.user.full_name }}</p>
                            <p class="text-xs text-muted-foreground">{{ pro.user.email }}</p>
                        </td>
                        <td class="py-3 px-4 hidden md:table-cell">
                            <span v-if="pro.subscription"
                                class="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                                {{ pro.subscription.plan_name }}
                            </span>
                            <span v-else class="text-muted-foreground text-xs">No plan</span>
                        </td>
                        <td class="py-3 px-4 hidden lg:table-cell text-muted-foreground">{{ pro.boms_this_month ?? 0 }}
                        </td>
                        <td class="py-3 px-4 hidden lg:table-cell text-muted-foreground">{{ pro.widget_deployments_count
                            ?? 0 }}</td>
                        <td class="py-3 px-4 text-muted-foreground text-xs">{{ fmt(pro.user.created_at) }}</td>
                        <td class="py-3 px-4">
                            <NuxtLink :to="`/professionals/${pro.id}`"
                                class="text-xs underline text-muted-foreground hover:text-foreground">View</NuxtLink>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div
                class="flex items-center justify-between px-4 py-3 border-t border-border text-sm text-muted-foreground">
                <span>{{ total }} professionals</span>
                <div class="flex items-center gap-1">
                    <button :disabled="page === 1"
                        class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                        @click="page--; fetchPros()">
                        <Icon name="lucide:chevron-left" class="w-4 h-4" />
                    </button>
                    <span class="px-2">{{ page }} / {{ totalPages }}</span>
                    <button :disabled="page >= totalPages"
                        class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                        @click="page++; fetchPros()">
                        <Icon name="lucide:chevron-right" class="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
const loading = ref(true)
const search = ref('')
const page = ref(1)
const pageSize = 25
const total = ref(0)

interface Pro {
    id: string
    user: { full_name: string; email: string; created_at: string }
    subscription?: { plan_name: string }
    boms_this_month?: number
    widget_deployments_count?: number
}
const professionals = ref<Pro[]>([])
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function fetchPros() {
    loading.value = true
    const params = new URLSearchParams({ skip: String((page.value - 1) * pageSize), limit: String(pageSize) })
    if (search.value) params.set('search', search.value)
    const data = await api.get<{ items: Pro[]; total: number }>(`/api/v1/admin/professionals?${params}`)
    professionals.value = data.items
    total.value = data.total
    loading.value = false
}

const debouncedFetch = useDebounceFn(() => { page.value = 1; fetchPros() }, 300)

function fmt(d: string) {
    return new Date(d).toLocaleDateString('es-DO')
}

onMounted(fetchPros)
</script>
