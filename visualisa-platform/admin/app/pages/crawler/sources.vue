<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Crawl Sources</h1>
        </div>

        <div class="space-y-4">
            <div v-for="source in sources" :key="source.id" class="bg-card border border-border rounded-xl p-5">
                <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-3 mb-1">
                            <h3 class="font-semibold text-lg">{{ source.name }}</h3>
                            <span class="px-2 py-0.5 rounded-full text-xs font-medium"
                                :class="source.is_enabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
                                {{ source.is_enabled ? 'Enabled' : 'Disabled' }}
                            </span>
                        </div>
                        <a :href="source.base_url" target="_blank" rel="noopener noreferrer"
                            class="text-sm text-blue-600 hover:underline">
                            {{ source.base_url }}
                        </a>
                        <p class="text-xs text-muted-foreground mt-1">Crawler class: <code
                                class="bg-muted px-1 rounded">{{ source.crawler_class }}</code></p>
                    </div>
                    <button class="ml-4 px-3 py-1.5 text-sm border border-border rounded-md hover:bg-accent"
                        @click="toggleEnabled(source)">
                        {{ source.is_enabled ? 'Disable' : 'Enable' }}
                    </button>
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
interface Source { id: string; name: string; base_url: string; is_enabled: boolean; crawler_class: string }
const sources = ref<Source[]>([])

async function load() {
    const data = await api.get<{ items: Source[] }>('/api/v1/crawler/sources')
    sources.value = data.items
}

async function toggleEnabled(source: Source) {
    await api.put(`/api/v1/crawler/sources/${source.id}`, { is_enabled: !source.is_enabled })
    source.is_enabled = !source.is_enabled
}

onMounted(load)
</script>
