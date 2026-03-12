<template>
    <div class="max-w-4xl">
        <div class="flex items-center gap-3 mb-6">
            <NuxtLink to="/products" class="text-muted-foreground hover:text-foreground">
                <Icon name="lucide:arrow-left" class="w-5 h-5" />
            </NuxtLink>
            <h1 class="text-2xl font-bold line-clamp-1">{{ product?.name ?? 'Product' }}</h1>
            <NuxtLink :to="`/products/${id}/edit`"
                class="ml-auto flex items-center gap-2 px-3 py-2 border border-border rounded-md text-sm hover:bg-accent">
                <Icon name="lucide:pencil" class="w-4 h-4" />
                Edit
            </NuxtLink>
        </div>

        <div v-if="loading" class="flex items-center justify-center py-16 text-muted-foreground">
            <Icon name="lucide:loader-circle" class="w-6 h-6 animate-spin mr-2" />
            Loading…
        </div>

        <div v-else-if="product" class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Image -->
            <div class="md:col-span-1">
                <div class="bg-card border border-border rounded-xl overflow-hidden aspect-square">
                    <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
                        class="w-full h-full object-cover" />
                    <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <Icon name="lucide:image" class="w-12 h-12" />
                    </div>
                </div>
            </div>

            <!-- Details -->
            <div class="md:col-span-2 space-y-4">
                <div class="bg-card border border-border rounded-xl p-5 space-y-3">
                    <DetailRow label="Brand" :value="product.brand?.name" />
                    <DetailRow label="Category" :value="product.category?.name" />
                    <DetailRow label="Surface Type" :value="product.surface_type" />
                    <DetailRow label="Status">
                        <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="statusClass(product.status)">
                            {{ product.status }}
                        </span>
                    </DetailRow>
                    <DetailRow label="Price (DOP)" :value="formatPrice(product.price_dop)" />
                    <DetailRow v-if="product.price_usd" label="Price (USD)" :value="`$${product.price_usd}`" />
                    <DetailRow label="SKU" :value="product.sku" />
                    <DetailRow label="Unit" :value="product.unit" />
                    <DetailRow label="Source" :value="product.source" />
                    <DetailRow label="Source URL">
                        <a v-if="product.source_url" :href="product.source_url" target="_blank"
                            rel="noopener noreferrer" class="text-blue-600 hover:underline truncate max-w-xs block">
                            {{ product.source_url }}
                        </a>
                    </DetailRow>
                </div>

                <div v-if="product.description" class="bg-card border border-border rounded-xl p-5">
                    <p class="text-sm font-medium text-muted-foreground mb-2">Description</p>
                    <p class="text-sm">{{ product.description }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const route = useRoute()
const api = useApi()
const id = route.params.id as string
const loading = ref(true)
const product = ref<Record<string, any> | null>(null)

onMounted(async () => {
    product.value = await api.get(`/api/v1/products/${id}`)
    loading.value = false
})

function formatPrice(v: number) {
    return new Intl.NumberFormat('es-DO', { style: 'currency', currency: 'DOP', maximumFractionDigits: 0 }).format(v)
}

function statusClass(status: string) {
    return {
        active: 'bg-green-100 text-green-700',
        pending_review: 'bg-yellow-100 text-yellow-700',
        inactive: 'bg-gray-100 text-gray-600',
    }[status] ?? 'bg-muted text-muted-foreground'
}
</script>
