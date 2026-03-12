<script setup lang="ts">
const visualizerStore = useVisualizerStore()
const { generatedImage, aiAnalysis, isAnalyzing } = storeToRefs(visualizerStore)

async function runAnalysis() {
    await visualizerStore.analyzeWithAI()
}

const scoreColor = computed(() => {
    const s = aiAnalysis.value?.score ?? 0
    if (s >= 8) return 'text-emerald-600'
    if (s >= 5) return 'text-amber-500'
    return 'text-red-500'
})

const scoreBarColor = computed(() => {
    const s = aiAnalysis.value?.score ?? 0
    if (s >= 8) return 'bg-emerald-500'
    if (s >= 5) return 'bg-amber-400'
    return 'bg-red-500'
})

const scoreBarWidth = computed(() => `${((aiAnalysis.value?.score ?? 0) / 10) * 100}%`)
</script>

<template>
    <div class="flex flex-col h-full px-4 py-4 gap-4 overflow-y-auto overscroll-contain scrollbar-hide">
        <template v-if="generatedImage">
            <!-- Thumbnail of generated image -->
            <div class="rounded-xl overflow-hidden shadow-card">
                <img :src="generatedImage" alt="Diseño generado por IA" class="w-full h-36 object-cover" />
            </div>

            <!-- Analyze button -->
            <button :disabled="isAnalyzing" :class="[
                'w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold transition-all',
                isAnalyzing
                    ? 'bg-violet-100 text-violet-400'
                    : 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white shadow-md hover:opacity-90',
            ]" @click="runAnalysis">
                <Icon :name="isAnalyzing ? 'lucide:loader-2' : 'lucide:brain-circuit'"
                    :class="['w-4 h-4', isAnalyzing && 'animate-spin']" />
                {{ isAnalyzing ? 'Analizando diseño…' : aiAnalysis ? 'Volver a analizar' : 'Analizar con IA' }}
            </button>

            <!-- Results -->
            <template v-if="aiAnalysis">
                <!-- Score -->
                <div class="rounded-xl border border-black/[0.08] bg-white p-4 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-semibold text-text-primary">Puntuación</span>
                        <span :class="['text-2xl font-black tabular-nums', scoreColor]">
                            {{ aiAnalysis.score }}<span class="text-base font-normal text-text-tertiary">/10</span>
                        </span>
                    </div>
                    <div class="h-2 rounded-full bg-black/[0.07] overflow-hidden">
                        <div :class="['h-full rounded-full transition-all duration-700', scoreBarColor]"
                            :style="{ width: scoreBarWidth }" />
                    </div>
                </div>

                <!-- Summary -->
                <div class="rounded-xl border border-black/[0.08] bg-white p-4">
                    <p class="text-xs font-semibold text-text-tertiary uppercase tracking-wide mb-1.5">Resumen</p>
                    <p class="text-sm text-text-primary leading-relaxed">{{ aiAnalysis.summary }}</p>
                </div>

                <!-- Metrics grid -->
                <div class="grid grid-cols-1 gap-2">
                    <div v-for="(value, key) in { 'Armonía cromática': aiAnalysis.colorHarmony, 'Coherencia estilística': aiAnalysis.styleMatch, 'Cobertura de materiales': aiAnalysis.estimatedCoverage }"
                        :key="key" class="rounded-xl border border-black/[0.08] bg-white p-3">
                        <p class="text-xs font-semibold text-text-tertiary uppercase tracking-wide mb-1">{{ key }}</p>
                        <p class="text-sm text-text-primary">{{ value }}</p>
                    </div>
                </div>

                <!-- Suggestions -->
                <div class="rounded-xl border border-violet-200 bg-violet-50 p-4">
                    <p class="text-xs font-semibold text-violet-700 uppercase tracking-wide mb-2.5">Sugerencias</p>
                    <ul class="space-y-2">
                        <li v-for="(s, i) in aiAnalysis.suggestions" :key="i"
                            class="flex items-start gap-2 text-sm text-violet-900">
                            <Icon name="lucide:lightbulb" class="w-3.5 h-3.5 mt-0.5 text-violet-500 flex-shrink-0" />
                            {{ s }}
                        </li>
                    </ul>
                </div>
            </template>
        </template>
    </div>
</template>
