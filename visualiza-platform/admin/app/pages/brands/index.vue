<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Brands</h1>
            <button
                class="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                @click="openCreate">
                <Icon name="lucide:plus" class="w-4 h-4" />
                Add Brand
            </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            <div v-for="brand in brands" :key="brand.id"
                class="bg-card border border-border rounded-xl p-5 flex items-center gap-4">
                <div class="w-12 h-12 rounded-lg bg-muted flex items-center justify-center shrink-0 overflow-hidden">
                    <img v-if="brand.logo_url" :src="brand.logo_url" :alt="brand.name"
                        class="w-full h-full object-contain" />
                    <Icon v-else name="lucide:tag" class="w-6 h-6 text-muted-foreground" />
                </div>
                <div class="flex-1 min-w-0">
                    <p class="font-medium">{{ brand.name }}</p>
                    <a v-if="brand.website_url" :href="brand.website_url" target="_blank" rel="noopener noreferrer"
                        class="text-xs text-blue-600 hover:underline truncate block">
                        {{ brand.website_url }}
                    </a>
                    <p class="text-xs text-muted-foreground">{{ brand.product_count ?? 0 }} products</p>
                </div>
                <div class="flex flex-col gap-1">
                    <button class="p-1.5 rounded hover:bg-accent text-muted-foreground" @click="openEdit(brand)">
                        <Icon name="lucide:pencil" class="w-4 h-4" />
                    </button>
                    <button class="p-1.5 rounded hover:bg-destructive/10 text-muted-foreground hover:text-destructive"
                        @click="del(brand)">
                        <Icon name="lucide:trash-2" class="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div v-if="modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
            @click.self="modal = false">
            <div class="bg-card border border-border rounded-xl p-6 w-full max-w-md shadow-xl">
                <h2 class="font-semibold text-lg mb-4">{{ editing ? 'Edit' : 'New' }} Brand</h2>
                <form class="space-y-4" @submit.prevent="save">
                    <FieldGroup label="Name *">
                        <input v-model="form.name" required
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </FieldGroup>
                    <FieldGroup label="Slug">
                        <input v-model="form.slug"
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </FieldGroup>
                    <FieldGroup label="Website URL">
                        <input v-model="form.website_url" type="url"
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </FieldGroup>
                    <FieldGroup label="Logo URL">
                        <input v-model="form.logo_url" type="url"
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </FieldGroup>
                    <div class="flex justify-end gap-3 pt-2">
                        <button type="button" class="px-4 py-2 border border-border rounded-md text-sm hover:bg-accent"
                            @click="modal = false">Cancel</button>
                        <button type="submit"
                            class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">Save</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
interface Brand { id: string; name: string; slug: string; logo_url?: string; website_url?: string; product_count?: number }
const brands = ref<Brand[]>([])
const modal = ref(false)
const editing = ref<Brand | null>(null)
const form = reactive({ name: '', slug: '', website_url: '', logo_url: '' })

async function load() {
    const data = await api.get<{ items: Brand[] }>('/api/v1/products/brands')
    brands.value = data.items
}

function openCreate() { editing.value = null; Object.assign(form, { name: '', slug: '', website_url: '', logo_url: '' }); modal.value = true }
function openEdit(b: Brand) { editing.value = b; Object.assign(form, b); modal.value = true }

async function save() {
    if (editing.value) await api.put(`/api/v1/products/brands/${editing.value.id}`, form)
    else await api.post('/api/v1/products/brands', form)
    modal.value = false
    load()
}

async function del(b: Brand) {
    if (!confirm(`Delete brand "${b.name}"?`)) return
    await api.delete(`/api/v1/products/brands/${b.id}`)
    load()
}

onMounted(load)
</script>
