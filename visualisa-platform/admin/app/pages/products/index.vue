<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Products</h1>
            <div class="flex items-center gap-2">
                <NuxtLink to="/products/import"
                    class="flex items-center gap-2 px-3 py-2 border border-border rounded-md text-sm hover:bg-accent transition-colors">
                    <Icon name="lucide:upload" class="w-4 h-4" />
                    Import
                </NuxtLink>
                <NuxtLink to="/products/create"
                    class="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
                    <Icon name="lucide:plus" class="w-4 h-4" />
                    Add Product
                </NuxtLink>
            </div>
        </div>

        <!-- Filters -->
        <div class="bg-card border border-border rounded-xl p-4 mb-4 flex flex-wrap gap-3">
            <input v-model="search" type="search" placeholder="Search products…"
                class="px-3 py-2 rounded-md border border-input bg-background text-sm w-64 focus:outline-none focus:ring-2 focus:ring-ring"
                @input="debouncedFetch" />
            <select v-model="filters.status"
                class="px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none"
                @change="fetchProducts">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="pending_review">Pending Review</option>
                <option value="inactive">Inactive</option>
            </select>
            <select v-model="filters.surface_type"
                class="px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none"
                @change="fetchProducts">
                <option value="">All Surfaces</option>
                <option value="floor">Floor</option>
                <option value="wall">Wall</option>
                <option value="ceiling">Ceiling</option>
                <option value="countertop">Countertop</option>
                <option value="door">Door</option>
                <option value="window">Window</option>
                <option value="exterior">Exterior</option>
                <option value="other">Other</option>
            </select>
        </div>

        <!-- Table -->
        <div class="bg-card border border-border rounded-xl overflow-hidden">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-border">
                        <th class="text-left py-3 px-4 font-medium text-muted-foreground">Product</th>
                        <th class="text-left py-3 px-4 font-medium text-muted-foreground hidden md:table-cell">Brand
                        </th>
                        <th class="text-left py-3 px-4 font-medium text-muted-foreground hidden lg:table-cell">Surface
                        </th>
                        <th class="text-right py-3 px-4 font-medium text-muted-foreground">Price (DOP)</th>
                        <th class="text-left py-3 px-4 font-medium text-muted-foreground hidden sm:table-cell">Status
                        </th>
                        <th class="py-3 px-4" />
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loading">
                        <td colspan="6" class="py-12 text-center text-muted-foreground">
                            <Icon name="lucide:loader-circle" class="w-5 h-5 animate-spin inline-block mr-2" />
                            Loading…
                        </td>
                    </tr>
                    <tr v-else-if="!products.length">
                        <td colspan="6" class="py-12 text-center text-muted-foreground">No products found</td>
                    </tr>
                    <tr v-for="product in products" v-else :key="product.id"
                        class="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                        <td class="py-3 px-4">
                            <div class="flex items-center gap-3">
                                <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
                                    class="w-10 h-10 rounded object-cover shrink-0 bg-muted" />
                                <div v-else class="w-10 h-10 rounded bg-muted shrink-0" />
                                <span class="font-medium line-clamp-1">{{ product.name }}</span>
                            </div>
                        </td>
                        <td class="py-3 px-4 text-muted-foreground hidden md:table-cell">{{ product.brand?.name ?? '—'
                            }}</td>
                        <td class="py-3 px-4 text-muted-foreground hidden lg:table-cell capitalize">{{
                            product.surface_type }}</td>
                        <td class="py-3 px-4 text-right font-mono">{{ formatPrice(product.price_dop) }}</td>
                        <td class="py-3 px-4 hidden sm:table-cell">
                            <span class="px-2 py-0.5 rounded-full text-xs font-medium"
                                :class="statusClass(product.status)">
                                {{ product.status }}
                            </span>
                        </td>
                        <td class="py-3 px-4">
                            <div class="flex items-center justify-end gap-1">
                                <NuxtLink :to="`/products/${product.id}`"
                                    class="p-1.5 rounded hover:bg-accent text-muted-foreground hover:text-foreground"
                                    title="View">
                                    <Icon name="lucide:eye" class="w-4 h-4" />
                                </NuxtLink>
                                <NuxtLink :to="`/products/${product.id}/edit`"
                                    class="p-1.5 rounded hover:bg-accent text-muted-foreground hover:text-foreground"
                                    title="Edit">
                                    <Icon name="lucide:pencil" class="w-4 h-4" />
                                </NuxtLink>
                                <button
                                    class="p-1.5 rounded hover:bg-destructive/10 text-muted-foreground hover:text-destructive"
                                    title="Delete" @click="confirmDelete(product)">
                                    <Icon name="lucide:trash-2" class="w-4 h-4" />
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- Pagination -->
            <div
                class="flex items-center justify-between px-4 py-3 border-t border-border text-sm text-muted-foreground">
                <span>{{ total }} total products</span>
                <div class="flex items-center gap-1">
                    <button :disabled="page === 1"
                        class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                        @click="changePage(page - 1)">
                        <Icon name="lucide:chevron-left" class="w-4 h-4" />
                    </button>
                    <span class="px-3">Page {{ page }} / {{ totalPages }}</span>
                    <button :disabled="page >= totalPages"
                        class="px-2 py-1 rounded border border-border hover:bg-accent disabled:opacity-40"
                        @click="changePage(page + 1)">
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
const loading = ref(false)
const products = ref<Product[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const search = ref('')
const filters = ref({ status: '', surface_type: '' })

interface Product {
    id: string
    name: string
    price_dop: number
    status: string
    surface_type: string
    image_url?: string
    brand?: { name: string }
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function fetchProducts() {
    loading.value = true
    try {
        const params = new URLSearchParams({
            skip: String((page.value - 1) * pageSize),
            limit: String(pageSize),
        })
        if (search.value) params.set('search', search.value)
        if (filters.value.status) params.set('status', filters.value.status)
        if (filters.value.surface_type) params.set('surface_type', filters.value.surface_type)

        const data = await api.get<{ items: Product[]; total: number }>(`/api/v1/products?${params}`)
        products.value = data.items
        total.value = data.total
    } finally {
        loading.value = false
    }
}

const debouncedFetch = useDebounceFn(() => {
    page.value = 1
    fetchProducts()
}, 300)

function changePage(p: number) {
    page.value = p
    fetchProducts()
}

function formatPrice(v: number) {
    return new Intl.NumberFormat('es-DO', { style: 'currency', currency: 'DOP', maximumFractionDigits: 0 }).format(v)
}

function statusClass(status: string) {
    return {
        active: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
        pending_review: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
        inactive: 'bg-gray-100 text-gray-600 dark:bg-gray-800',
    }[status] ?? 'bg-muted text-muted-foreground'
}

async function confirmDelete(product: Product) {
    if (!confirm(`Delete "${product.name}"? This cannot be undone.`)) return
    await api.delete(`/api/v1/products/${product.id}`)
    fetchProducts()
}

onMounted(fetchProducts)
</script>
