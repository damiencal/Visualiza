<script setup lang="ts">
interface InteriorStyle {
    id: string
    name: string
    description: string
    colors: [string, string]
    icon: string
}

const INTERIOR_STYLES: InteriorStyle[] = [
    {
        id: 'modern',
        name: 'Moderno',
        description: 'Líneas limpias y neutros',
        colors: ['#D1D5DB', '#6B7280'],
        icon: 'lucide:box',
    },
    {
        id: 'minimalist',
        name: 'Minimalista',
        description: 'Espacios despejados',
        colors: ['#F9FAFB', '#E5E7EB'],
        icon: 'lucide:minus-square',
    },
    {
        id: 'scandinavian',
        name: 'Escandinavo',
        description: 'Madera clara y calidez',
        colors: ['#FEF3C7', '#D4B896'],
        icon: 'lucide:trees',
    },
    {
        id: 'industrial',
        name: 'Industrial',
        description: 'Metales y texturas brutas',
        colors: ['#57534E', '#292524'],
        icon: 'lucide:wrench',
    },
    {
        id: 'mid-century',
        name: 'Mid-Century',
        description: 'Retro con maderas cálidas',
        colors: ['#FDBA74', '#C2410C'],
        icon: 'lucide:armchair',
    },
    {
        id: 'bohemian',
        name: 'Bohemio',
        description: 'Colorido y ecléctico',
        colors: ['#F9A8D4', '#7C3AED'],
        icon: 'lucide:flower-2',
    },
    {
        id: 'traditional',
        name: 'Clásico',
        description: 'Maderas ricas y ornamentos',
        colors: ['#B45309', '#78350F'],
        icon: 'lucide:crown',
    },
    {
        id: 'farmhouse',
        name: 'Rústico',
        description: 'Natural, madera y blanco',
        colors: ['#E7E5E4', '#A8A29E'],
        icon: 'lucide:warehouse',
    },
    {
        id: 'coastal',
        name: 'Costero',
        description: 'Azules, blancos y arenas',
        colors: ['#BAE6FD', '#0369A1'],
        icon: 'lucide:waves',
    },
    {
        id: 'art-deco',
        name: 'Art Déco',
        description: 'Geométrico y lujoso',
        colors: ['#FDE68A', '#92400E'],
        icon: 'lucide:gem',
    },
    {
        id: 'japandi',
        name: 'Japandi',
        description: 'Fusión japonesa y escandinava',
        colors: ['#D6D3D1', '#78716C'],
        icon: 'lucide:leaf',
    },
    {
        id: 'mediterranean',
        name: 'Mediterráneo',
        description: 'Terracota, azulejos y luz',
        colors: ['#FB923C', '#B91C1C'],
        icon: 'lucide:sun',
    },
]

const props = defineProps<{
    modelValue: boolean
    selectedStyle: string | null
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    'select': [styleId: string | null]
}>()

function selectStyle(styleId: string) {
    // Toggle off if already selected
    const newValue = props.selectedStyle === styleId ? null : styleId
    emit('select', newValue)
    emit('update:modelValue', false)
}

function close() {
    emit('update:modelValue', false)
}

function getGradient(colors: [string, string]) {
    return `linear-gradient(135deg, ${colors[0]} 0%, ${colors[1]} 100%)`
}
</script>

<template>
    <Teleport to="body">
        <!-- Backdrop -->
        <Transition name="backdrop">
            <div v-if="modelValue" class="fixed inset-0 z-40 bg-black/40 backdrop-blur-[3px]" aria-hidden="true"
                @click="close" />
        </Transition>

        <!-- Panel -->
        <Transition name="scale-up">
            <div v-if="modelValue"
                class="fixed z-50 inset-x-4 bottom-24 md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:w-[640px] bg-white/95 backdrop-blur-2xl rounded-3xl shadow-elevated border border-white/40 flex flex-col max-h-[70vh]"
                role="dialog" aria-modal="true" aria-label="Elegir estilo de interior">
                <!-- Header -->
                <div class="flex items-center justify-between px-5 pt-5 pb-4 border-b border-black/[0.06]">
                    <div>
                        <h2 class="text-base font-bold text-text-primary">Estilo de Interior</h2>
                        <p class="text-xs text-text-secondary mt-0.5">Elige el estilo que guiará la generación por IA
                        </p>
                    </div>
                    <!-- Clear + Close -->
                    <div class="flex items-center gap-2">
                        <button v-if="selectedStyle"
                            class="text-xs text-text-secondary hover:text-text-primary transition-colors px-2 py-1 rounded-lg hover:bg-black/[0.04]"
                            @click="emit('select', null); close()">
                            Quitar estilo
                        </button>
                        <button
                            class="w-8 h-8 rounded-full bg-black/5 hover:bg-black/10 transition-colors flex items-center justify-center"
                            aria-label="Cerrar" @click="close">
                            <Icon name="lucide:x" class="w-4 h-4 text-text-secondary" />
                        </button>
                    </div>
                </div>

                <!-- Grid -->
                <div class="overflow-y-auto p-4">
                    <div class="grid grid-cols-3 sm:grid-cols-4 gap-3">
                        <button v-for="style in INTERIOR_STYLES" :key="style.id" :class="[
                            'group relative flex flex-col rounded-2xl overflow-hidden border-2 transition-all duration-200 text-left',
                            selectedStyle === style.id
                                ? 'border-primary shadow-glow scale-[1.03]'
                                : 'border-transparent hover:border-black/10 hover:scale-[1.02]',
                        ]" @click="selectStyle(style.id)">
                            <!-- Preview swatch -->
                            <div class="w-full aspect-[4/3] relative"
                                :style="{ background: getGradient(style.colors) }">
                                <!-- Subtle texture overlay -->
                                <div class="absolute inset-0 opacity-20"
                                    style="background-image: url('data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Ccircle cx=\'2\' cy=\'2\' r=\'1\' fill=\'%23ffffff\'/%3E%3C/svg%3E'); background-repeat: repeat;" />
                                <!-- Icon centered -->
                                <div class="absolute inset-0 flex items-center justify-center">
                                    <div
                                        class="w-10 h-10 rounded-full bg-white/25 backdrop-blur-sm flex items-center justify-center shadow-sm">
                                        <Icon :name="style.icon" class="w-5 h-5 text-white drop-shadow-sm" />
                                    </div>
                                </div>
                                <!-- Selected check -->
                                <Transition name="fade">
                                    <div v-if="selectedStyle === style.id"
                                        class="absolute top-2 right-2 w-5 h-5 rounded-full bg-primary flex items-center justify-center shadow-glow">
                                        <Icon name="lucide:check" class="w-3 h-3 text-white" />
                                    </div>
                                </Transition>
                            </div>

                            <!-- Label -->
                            <div class="px-2.5 py-2 bg-white">
                                <p class="text-xs font-semibold text-text-primary leading-tight">{{ style.name }}</p>
                                <p class="text-[10px] text-text-secondary leading-tight mt-0.5">{{ style.description }}
                                </p>
                            </div>
                        </button>
                    </div>
                </div>

                <!-- Footer hint -->
                <div class="px-5 py-3 border-t border-black/[0.05] bg-black/[0.015] rounded-b-3xl">
                    <p class="text-[11px] text-text-tertiary text-center">
                        El estilo seleccionado se aplicará al generar con IA
                    </p>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<style scoped>
.backdrop-enter-active,
.backdrop-leave-active {
    transition: opacity 0.2s ease;
}

.backdrop-enter-from,
.backdrop-leave-to {
    opacity: 0;
}

.scale-up-enter-active {
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-up-leave-active {
    transition: all 0.18s ease-in;
}

.scale-up-enter-from {
    opacity: 0;
    transform: translateX(-50%) scale(0.92) translateY(12px);
}

.scale-up-leave-to {
    opacity: 0;
    transform: translateX(-50%) scale(0.95) translateY(8px);
}

/* On mobile (no translate-x) */
@media (max-width: 767px) {
    .scale-up-enter-from {
        opacity: 0;
        transform: scale(0.95) translateY(10px);
    }

    .scale-up-leave-to {
        opacity: 0;
        transform: scale(0.97) translateY(6px);
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
