<template>
    <div class="max-w-3xl">
        <div class="flex items-center gap-3 mb-6">
            <NuxtLink :to="`/products/${id}`" class="text-muted-foreground hover:text-foreground">
                <Icon name="lucide:arrow-left" class="w-5 h-5" />
            </NuxtLink>
            <h1 class="text-2xl font-bold">Edit Product</h1>
        </div>
        <div v-if="loading" class="flex items-center justify-center py-16 text-muted-foreground">
            <Icon name="lucide:loader-circle" class="w-6 h-6 animate-spin mr-2" />
            Loading…
        </div>
        <ProductForm v-else :initial="product" :loading="saving" @submit="handleUpdate" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const route = useRoute()
const router = useRouter()
const api = useApi()
const id = route.params.id as string

const loading = ref(true)
const saving = ref(false)
const product = ref<Record<string, unknown>>({})

onMounted(async () => {
    product.value = await api.get(`/api/v1/products/${id}`)
    loading.value = false
})

async function handleUpdate(payload: Record<string, unknown>) {
    saving.value = true
    try {
        await api.put(`/api/v1/products/${id}`, payload)
        router.push(`/products/${id}`)
    } finally {
        saving.value = false
    }
}
</script>
