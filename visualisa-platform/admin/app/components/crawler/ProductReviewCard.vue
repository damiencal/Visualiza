<template>
    <div class="bg-card border rounded-xl overflow-hidden transition-all cursor-pointer"
        :class="selected ? 'border-primary ring-2 ring-primary/20' : 'border-border hover:border-muted-foreground/40'"
        @click="$emit('toggle-select')">
        <!-- Image -->
        <div class="relative aspect-video bg-muted">
            <img v-if="result.image_url" :src="result.image_url" :alt="result.name" class="w-full h-full object-cover"
                loading="lazy" />
            <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground">
                <Icon name="lucide:image" class="w-8 h-8" />
            </div>
            <!-- Select indicator -->
            <div class="absolute top-2 left-2 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors"
                :class="selected ? 'bg-primary border-primary' : 'bg-white/80 border-gray-400'">
                <Icon v-if="selected" name="lucide:check" class="w-3 h-3 text-white" />
            </div>
            <!-- Source badge -->
            <span class="absolute top-2 right-2 px-2 py-0.5 bg-black/60 text-white text-xs rounded-full">
                {{ result.source_name }}
            </span>
        </div>

        <!-- Content -->
        <div class="p-4">
            <p class="font-medium text-sm line-clamp-2 mb-1">{{ result.name }}</p>
            <div class="flex items-center justify-between text-xs text-muted-foreground mb-3">
                <span class="capitalize">{{ result.surface_type }}</span>
                <span class="font-mono font-medium text-foreground">{{ formatPrice(result.price_dop) }}</span>
            </div>
            <a :href="result.source_url" target="_blank" rel="noopener noreferrer"
                class="text-xs text-blue-600 hover:underline truncate block mb-3" @click.stop>
                View source →
            </a>

            <!-- Action buttons -->
            <div class="flex gap-2">
                <button
                    class="flex-1 py-1.5 text-xs font-medium bg-green-100 text-green-700 rounded-md hover:bg-green-200 flex items-center justify-center gap-1"
                    @click.stop="$emit('approve')">
                    <Icon name="lucide:check" class="w-3.5 h-3.5" />
                    Approve
                </button>
                <button
                    class="flex-1 py-1.5 text-xs font-medium bg-red-100 text-red-700 rounded-md hover:bg-red-200 flex items-center justify-center gap-1"
                    @click.stop="$emit('reject')">
                    <Icon name="lucide:x" class="w-3.5 h-3.5" />
                    Reject
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    result: {
        id: string; name: string; price_dop: number; surface_type: string
        brand_name?: string; image_url?: string; source_url: string; source_name: string
    }
    selected: boolean
}>()

defineEmits<{ 'toggle-select': []; approve: []; reject: [] }>()

function formatPrice(v: number) {
    return new Intl.NumberFormat('es-DO', { style: 'currency', currency: 'DOP', maximumFractionDigits: 0 }).format(v)
}
</script>
