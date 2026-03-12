<template>
    <div class="max-w-3xl">
        <div class="flex items-center gap-3 mb-6">
            <NuxtLink to="/products" class="text-muted-foreground hover:text-foreground">
                <Icon name="lucide:arrow-left" class="w-5 h-5" />
            </NuxtLink>
            <h1 class="text-2xl font-bold">Add Product</h1>
        </div>
        <ProductForm @submit="handleCreate" :loading="saving" />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'admin' })

const api = useApi()
const router = useRouter()
const saving = ref(false)

async function handleCreate(payload: Record<string, unknown>) {
    saving.value = true
    try {
        await api.post('/api/v1/products', payload)
        router.push('/products')
    } finally {
        saving.value = false
    }
}
</script>
