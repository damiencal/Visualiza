<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Categories</h1>
            <button
                class="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                @click="openCreate">
                <Icon name="lucide:plus" class="w-4 h-4" />
                Add Category
            </button>
        </div>

        <div class="bg-card border border-border rounded-xl overflow-hidden">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-border text-left">
                        <th class="py-3 px-4 font-medium text-muted-foreground">Name</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden md:table-cell">Slug</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground hidden lg:table-cell">Parent</th>
                        <th class="py-3 px-4 font-medium text-muted-foreground">Products</th>
                        <th class="py-3 px-4" />
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="cat in categories" :key="cat.id"
                        class="border-b border-border last:border-0 hover:bg-muted/30">
                        <td class="py-3 px-4 font-medium">{{ cat.name }}</td>
                        <td class="py-3 px-4 text-muted-foreground font-mono text-xs hidden md:table-cell">{{ cat.slug
                            }}</td>
                        <td class="py-3 px-4 text-muted-foreground hidden lg:table-cell">{{ cat.parent?.name ?? '—' }}
                        </td>
                        <td class="py-3 px-4">{{ cat.product_count ?? '—' }}</td>
                        <td class="py-3 px-4">
                            <div class="flex items-center justify-end gap-1">
                                <button class="p-1.5 rounded hover:bg-accent text-muted-foreground"
                                    @click="openEdit(cat)">
                                    <Icon name="lucide:pencil" class="w-4 h-4" />
                                </button>
                                <button
                                    class="p-1.5 rounded hover:bg-destructive/10 text-muted-foreground hover:text-destructive"
                                    @click="del(cat)">
                                    <Icon name="lucide:trash-2" class="w-4 h-4" />
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal -->
        <div v-if="modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
            @click.self="modal = false">
            <div class="bg-card border border-border rounded-xl p-6 w-full max-w-md shadow-xl">
                <h2 class="font-semibold text-lg mb-4">{{ editing ? 'Edit' : 'New' }} Category</h2>
                <form class="space-y-4" @submit.prevent="save">
                    <FieldGroup label="Name *">
                        <input v-model="form.name" required
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </FieldGroup>
                    <FieldGroup label="Slug">
                        <input v-model="form.slug"
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                    </FieldGroup>
                    <FieldGroup label="Parent Category">
                        <select v-model="form.parent_id"
                            class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none">
                            <option :value="null">— None —</option>
                            <option v-for="c in categories.filter(c => c.id !== editing?.id)" :key="c.id" :value="c.id">
                                {{ c.name }}</option>
                        </select>
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
interface Category { id: string; name: string; slug: string; parent?: { name: string }; parent_id?: string | null; product_count?: number }
const categories = ref<Category[]>([])
const modal = ref(false)
const editing = ref<Category | null>(null)
const form = reactive({ name: '', slug: '', parent_id: null as string | null })

async function load() {
    const data = await api.get<{ items: Category[] }>('/api/v1/products/categories')
    categories.value = data.items
}

function openCreate() { editing.value = null; Object.assign(form, { name: '', slug: '', parent_id: null }); modal.value = true }
function openEdit(c: Category) { editing.value = c; Object.assign(form, { name: c.name, slug: c.slug, parent_id: c.parent_id ?? null }); modal.value = true }

async function save() {
    if (editing.value) await api.put(`/api/v1/products/categories/${editing.value.id}`, form)
    else await api.post('/api/v1/products/categories', form)
    modal.value = false
    load()
}

async function del(c: Category) {
    if (!confirm(`Delete category "${c.name}"?`)) return
    await api.delete(`/api/v1/products/categories/${c.id}`)
    load()
}

onMounted(load)
</script>
