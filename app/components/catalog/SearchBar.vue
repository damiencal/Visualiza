<script setup lang="ts">
interface Props {
  modelValue: string
  placeholder?: string
}

withDefaults(defineProps<Props>(), {
  placeholder: 'Buscar productos...',
})

const emit = defineEmits<{ 'update:modelValue': [v: string] }>()

const inputRef = ref<HTMLInputElement | null>(null)
const isFocused = ref(false)

function clear() {
  emit('update:modelValue', '')
  nextTick(() => inputRef.value?.focus())
}
</script>

<template>
  <div
    :class="[
      'flex items-center gap-3 px-4 py-2.5 rounded-2xl bg-white border transition-all duration-200',
      isFocused ? 'border-primary shadow-glow' : 'border-black/[0.08] shadow-soft',
    ]"
  >
    <Icon name="lucide:search" class="w-4 h-4 text-text-tertiary flex-shrink-0" />
    <input
      ref="inputRef"
      :value="modelValue"
      type="search"
      :placeholder="placeholder"
      class="flex-1 bg-transparent text-sm text-text-primary placeholder:text-text-tertiary outline-none"
      :aria-label="placeholder"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @focus="isFocused = true"
      @blur="isFocused = false"
    />
    <button
      v-if="modelValue"
      class="w-5 h-5 rounded-full bg-black/10 flex items-center justify-center hover:bg-black/20 transition-colors"
      aria-label="Limpiar búsqueda"
      @click="clear"
    >
      <Icon name="lucide:x" class="w-3 h-3" />
    </button>
  </div>
</template>
