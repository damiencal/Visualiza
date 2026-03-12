<script setup lang="ts">
interface Props {
  target: number
  prefix?: string
  suffix?: string
  duration?: number
}

const props = withDefaults(defineProps<Props>(), {
  prefix: '',
  suffix: '',
  duration: 1200,
})

const el = ref<HTMLElement | null>(null)
const displayed = ref(0)
const { stop } = useIntersectionObserver(el, ([entry]) => {
  if (entry.isIntersecting) {
    animateTo(props.target)
    stop()
  }
})

function animateTo(end: number) {
  const start = 0
  const startTime = performance.now()
  function step(now: number) {
    const progress = Math.min((now - startTime) / props.duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    displayed.value = Math.floor(eased * end)
    if (progress < 1) requestAnimationFrame(step)
    else displayed.value = end
  }
  requestAnimationFrame(step)
}
</script>

<template>
  <span ref="el">{{ prefix }}{{ displayed.toLocaleString('es-DO') }}{{ suffix }}</span>
</template>
