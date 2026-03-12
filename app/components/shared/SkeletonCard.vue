<script setup lang="ts">
interface Props {
  type?: 'property' | 'product' | 'text'
  lines?: number
}

withDefaults(defineProps<Props>(), {
  type: 'property',
  lines: 3,
})
</script>

<template>
  <!-- Property card skeleton -->
  <div v-if="type === 'property'" class="glass-card overflow-hidden animate-pulse">
    <div class="skeleton h-52 w-full rounded-t-2xl rounded-b-none" />
    <div class="p-4 space-y-3">
      <div class="skeleton h-5 w-3/4 rounded-full" />
      <div class="skeleton h-4 w-1/2 rounded-full" />
      <div class="flex gap-3 mt-4">
        <div class="skeleton h-4 w-16 rounded-full" />
        <div class="skeleton h-4 w-16 rounded-full" />
        <div class="skeleton h-4 w-16 rounded-full" />
      </div>
      <div class="skeleton h-6 w-1/3 rounded-full mt-2" />
    </div>
  </div>

  <!-- Product card skeleton -->
  <div v-else-if="type === 'product'" class="glass-card overflow-hidden animate-pulse">
    <div class="skeleton h-44 w-full rounded-t-2xl rounded-b-none" />
    <div class="p-4 space-y-2">
      <div class="skeleton h-3 w-1/3 rounded-full" />
      <div class="skeleton h-5 w-2/3 rounded-full" />
      <div class="skeleton h-4 w-1/4 rounded-full mt-3" />
    </div>
  </div>

  <!-- Generic text skeleton -->
  <div v-else class="space-y-2 animate-pulse">
    <div
      v-for="i in lines"
      :key="i"
      class="skeleton h-4 rounded-full"
      :style="{ width: i === lines ? '60%' : '100%' }"
    />
  </div>
</template>
