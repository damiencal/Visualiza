<script setup lang="ts">
interface Props {
  modelValue: string
  brands: string[]
}

defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [v: string] }>()
</script>

<template>
  <div class="space-y-2">
    <p class="text-xs font-semibold text-text-tertiary uppercase tracking-wide px-1">Marca</p>
    <div class="flex flex-wrap gap-1.5">
      <button
        :class="['chip transition-all', modelValue === '' ? 'chip-active' : 'hover:bg-black/8']"
        @click="emit('update:modelValue', '')"
      >
        Todas
      </button>
      <button
        v-for="brand in brands"
        :key="brand"
        :class="['chip transition-all text-xs', modelValue === brand ? 'chip-active shadow-glow' : 'hover:bg-black/8']"
        @click="emit('update:modelValue', brand)"
      >
        {{ brand }}
      </button>
    </div>
  </div>
</template>
