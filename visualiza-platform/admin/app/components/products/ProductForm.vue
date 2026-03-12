<template>
    <form class="bg-card border border-border rounded-xl p-6 space-y-5" @submit.prevent="$emit('submit', form)">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FieldGroup label="Name *">
                <input v-model="form.name" required class="field" type="text" />
            </FieldGroup>
            <FieldGroup label="SKU">
                <input v-model="form.sku" class="field" type="text" />
            </FieldGroup>
            <FieldGroup label="Price (DOP) *">
                <input v-model.number="form.price_dop" required class="field" type="number" min="0" step="0.01" />
            </FieldGroup>
            <FieldGroup label="Price (USD)">
                <input v-model.number="form.price_usd" class="field" type="number" min="0" step="0.01" />
            </FieldGroup>
            <FieldGroup label="Unit">
                <select v-model="form.unit" class="field">
                    <option value="m2">m²</option>
                    <option value="ft2">ft²</option>
                    <option value="linear_m">linear m</option>
                    <option value="unit">unit</option>
                    <option value="gallon">gallon</option>
                    <option value="box">box</option>
                </select>
            </FieldGroup>
            <FieldGroup label="Surface Type *">
                <select v-model="form.surface_type" required class="field">
                    <option value="floor">Floor</option>
                    <option value="wall">Wall</option>
                    <option value="ceiling">Ceiling</option>
                    <option value="countertop">Countertop</option>
                    <option value="door">Door</option>
                    <option value="window">Window</option>
                    <option value="exterior">Exterior</option>
                    <option value="other">Other</option>
                </select>
            </FieldGroup>
            <FieldGroup label="Status *">
                <select v-model="form.status" required class="field">
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="pending_review">Pending Review</option>
                </select>
            </FieldGroup>
            <FieldGroup label="Source URL">
                <input v-model="form.source_url" class="field" type="url" />
            </FieldGroup>
        </div>

        <FieldGroup label="Description">
            <textarea v-model="form.description" class="field" rows="3" />
        </FieldGroup>

        <FieldGroup label="Image URL">
            <input v-model="form.image_url" class="field" type="url" />
        </FieldGroup>

        <div class="flex justify-end gap-3 pt-2">
            <button type="button" class="px-4 py-2 border border-border rounded-md text-sm hover:bg-accent"
                @click="$router.back()">
                Cancel
            </button>
            <button type="submit"
                class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 disabled:opacity-50"
                :disabled="loading">
                {{ loading ? 'Saving…' : 'Save Product' }}
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

const props = defineProps<{
    initial?: Record<string, unknown>
    loading?: boolean
}>()

defineEmits<{ submit: [payload: Record<string, unknown>] }>()

const form = reactive({
    name: '',
    sku: '',
    price_dop: 0,
    price_usd: undefined as number | undefined,
    unit: 'm2',
    surface_type: 'floor',
    status: 'active',
    description: '',
    image_url: '',
    source_url: '',
})

watch(
    () => props.initial,
    (v) => {
        if (v) Object.assign(form, v)
    },
    { immediate: true }
)
</script>

<style scoped>
.field {
    @apply w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring;
}
</style>
