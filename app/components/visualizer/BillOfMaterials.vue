<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const {
    bom,
    bomTotalDOP,
    bomTotalUSD,
    roomDimensions,
    wasteFactor,
    generatedImage,
    aiAnalysis,
    isAnalyzing,
    session,
} = storeToRefs(visualizerStore)

const { formatPrice } = useFormatPrice()

// Local copies for form binding
const dims = reactive({
    width: roomDimensions.value.width,
    length: roomDimensions.value.length,
    height: roomDimensions.value.height,
})

watch(
    dims,
    (v) => {
        roomDimensions.value = { ...v }
    },
    { deep: true },
)

watch(
    roomDimensions,
    (v) => {
        dims.width = v.width
        dims.length = v.length
        dims.height = v.height
    },
    { deep: true },
)

const showDims = ref(false)

async function runAnalysis() {
    await visualizerStore.analyzeWithAI()
}

const scoreColor = computed(() => {
    const s = aiAnalysis.value?.score ?? 0
    if (s >= 8) return 'text-emerald-600'
    if (s >= 5) return 'text-amber-500'
    return 'text-red-500'
})

const scoreBg = computed(() => {
    const s = aiAnalysis.value?.score ?? 0
    if (s >= 8) return 'bg-emerald-50 border-emerald-200'
    if (s >= 5) return 'bg-amber-50 border-amber-200'
    return 'bg-red-50 border-red-200'
})

const scoreBarWidth = computed(() => `${((aiAnalysis.value?.score ?? 0) / 10) * 100}%`)
const scoreBarColor = computed(() => {
    const s = aiAnalysis.value?.score ?? 0
    if (s >= 8) return 'bg-emerald-500'
    if (s >= 5) return 'bg-amber-400'
    return 'bg-red-500'
})

// Group BoM by currency for display
const bomDOP = computed(() => bom.value.filter((i) => i.currency === 'DOP'))
const bomUSD = computed(() => bom.value.filter((i) => i.currency === 'USD'))
</script>

<template>
    <div class="flex flex-col h-full">
        <!-- Empty state -->
        <div v-if="!bom.length" class="flex-1 flex flex-col items-center justify-center gap-3 px-6 py-10 text-center">
            <div class="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center">
                <Icon name="lucide:clipboard-list" class="w-7 h-7 text-primary" />
            </div>
            <div>
                <p class="text-sm font-semibold text-text-primary">Sin materiales aún</p>
                <p class="text-xs text-text-secondary mt-1">Selecciona superficies y aplica productos para generar el
                    presupuesto.</p>
            </div>
        </div>

        <template v-else>
            <!-- Room dimensions card -->
            <div class="px-4 pt-4">
                <button
                    class="w-full flex items-center justify-between gap-2 px-3.5 py-2.5 rounded-xl bg-black/[0.04] hover:bg-black/[0.07] transition-colors"
                    @click="showDims = !showDims">
                    <div class="flex items-center gap-2">
                        <Icon name="lucide:ruler" class="w-4 h-4 text-primary" />
                        <span class="text-sm font-medium text-text-primary">Dimensiones del espacio</span>
                    </div>
                    <Icon :name="showDims ? 'lucide:chevron-up' : 'lucide:chevron-down'"
                        class="w-4 h-4 text-text-tertiary transition-transform" />
                </button>

                <transition enter-active-class="transition-all duration-200 ease-out"
                    enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0"
                    leave-active-class="transition-all duration-150 ease-in"
                    leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-2">
                    <div v-if="showDims" class="mt-2 px-1 pb-1 space-y-3">
                        <!-- Grid of dimension inputs -->
                        <div class="grid grid-cols-3 gap-2">
                            <div v-for="field in ['width', 'length', 'height'] as const" :key="field">
                                <label class="block text-xs text-text-tertiary mb-1 capitalize">
                                    {{ field === 'width' ? 'Ancho' : field === 'length' ? 'Largo' : 'Alto' }}
                                </label>
                                <div class="relative">
                                    <input v-model.number="dims[field]" type="number" min="0.5" max="50" step="0.1"
                                        class="w-full text-sm border border-black/10 rounded-lg px-2 py-1.5 pr-7 focus:outline-none focus:ring-2 focus:ring-primary/30 bg-white" />
                                    <span
                                        class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-text-tertiary">m</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- BoM table -->
            <div class="flex-1 overflow-y-auto overscroll-contain scrollbar-hide px-4 py-3">
                <div class="space-y-2.5">
                    <div v-for="item in bom" :key="item.productId + item.surfaceId"
                        class="rounded-xl border border-black/[0.07] bg-white overflow-hidden">
                        <div class="flex items-center gap-3 px-3 py-2.5">
                            <!-- Texture thumbnail -->
                            <div class="w-10 h-10 rounded-lg overflow-hidden flex-shrink-0 bg-surface-100">
                                <img :src="item.product.images.texture || item.product.images.thumbnail"
                                    :alt="item.product.nameEs || item.product.name"
                                    class="w-full h-full object-cover" />
                            </div>
                            <div class="flex-1 min-w-0">
                                <p class="text-xs text-text-tertiary truncate">{{ item.product.brand.name }}</p>
                                <p class="text-sm font-semibold text-text-primary leading-tight line-clamp-1">
                                    {{ item.product.nameEs || item.product.name }}
                                </p>
                                <div class="flex items-center gap-1.5 mt-0.5">
                                    <span
                                        class="inline-flex items-center gap-1 text-xs text-text-secondary bg-black/[0.05] px-1.5 py-0.5 rounded-full">
                                        <Icon name="lucide:layers" class="w-3 h-3" />
                                        {{ item.surfaceLabel }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <!-- Stats row -->
                        <div
                            class="grid grid-cols-3 divide-x divide-black/[0.06] border-t border-black/[0.06] bg-black/[0.02]">
                            <div class="px-3 py-1.5 text-center">
                                <p class="text-xs text-text-tertiary">Área</p>
                                <p class="text-sm font-semibold text-text-primary">{{ item.areaM2 }} m²</p>
                            </div>
                            <div class="px-3 py-1.5 text-center">
                                <p class="text-xs text-text-tertiary">Cant.</p>
                                <p class="text-sm font-semibold text-text-primary">
                                    {{ item.quantity }}
                                    <span class="text-xs font-normal">{{ item.product.unit }}</span>
                                </p>
                            </div>
                            <div class="px-3 py-1.5 text-center">
                                <p class="text-xs text-text-tertiary">Total</p>
                                <p class="text-sm font-semibold text-primary">{{ formatPrice(item.totalPrice,
                                    item.currency) }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Totals footer -->
            <div class="px-4 pb-4 space-y-2 border-t border-black/[0.06] pt-3">
                <div v-if="bomTotalDOP > 0" class="flex items-center justify-between">
                    <span class="text-sm text-text-secondary">Total estimado (DOP)</span>
                    <span class="text-base font-bold text-text-primary">{{ formatPrice(bomTotalDOP, 'DOP') }}</span>
                </div>
                <div v-if="bomTotalUSD > 0" class="flex items-center justify-between">
                    <span class="text-sm text-text-secondary">Total estimado (USD)</span>
                    <span class="text-base font-bold text-text-primary">{{ formatPrice(bomTotalUSD, 'USD') }}</span>
                </div>
                <p class="text-xs text-text-tertiary">
                    * Incluye {{ Math.round(wasteFactor * 100) }}% de desperdicio. Precio referencial — consulta al
                    proveedor.
                </p>
            </div>
        </template>
    </div>
</template>
