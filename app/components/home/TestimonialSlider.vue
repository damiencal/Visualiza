<script setup lang="ts">
const testimonials = [
  {
    id: 1,
    name: 'María Rodríguez',
    role: 'Compradora en Piantini',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&h=80&fit=crop',
    quote: 'Pude ver exactamente cómo quedarían los pisos de mármol antes de comprarlos. Me ahorré semanas de incertidumbre y tomé la mejor decisión para mi apartamento.',
    rating: 5,
  },
  {
    id: 2,
    name: 'Carlos Méndez',
    role: 'Inversionista, Punta Cana',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&h=80&fit=crop',
    quote: 'Como inversor, necesito visualizar rápidamente distintos acabados para mis propiedades. Visualisa me permite mostrar opciones reales a mis clientes en minutos.',
    rating: 5,
  },
  {
    id: 3,
    name: 'Ana Peña',
    role: 'Decoradora de interiores',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=80&h=80&fit=crop',
    quote: 'Los productos de Cerámica del Caribe y Pinturas Popular integrados directamente en el visualisador son un game changer. Mis clientes quedan fascinados.',
    rating: 5,
  },
]

const activeIndex = ref(0)
const intervalId = ref<ReturnType<typeof setInterval> | null>(null)

function startAutoplay() {
  intervalId.value = setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % testimonials.length
  }, 5000)
}

function stopAutoplay() {
  if (intervalId.value) clearInterval(intervalId.value)
}

onMounted(startAutoplay)
onUnmounted(stopAutoplay)
</script>

<template>
  <section class="py-12 sm:py-16 bg-gradient-to-br from-primary/5 via-white to-rose-50/60">
    <div class="max-w-3xl mx-auto px-4 sm:px-6">
      <div class="text-center mb-10">
        <p class="text-xs text-primary font-semibold uppercase tracking-wider mb-2">Testimonios</p>
        <h2 class="text-2xl sm:text-3xl font-bold text-text-primary">Lo que dicen nuestros usuarios</h2>
      </div>

      <div class="relative overflow-hidden">
        <TransitionGroup name="testimonial" tag="div" class="relative">
          <div
            v-for="(t, i) in testimonials"
            v-show="activeIndex === i"
            :key="t.id"
            class="glass-card p-8 text-center"
          >
            <!-- Stars -->
            <div class="flex justify-center gap-1 mb-4">
              <Icon
                v-for="star in t.rating"
                :key="star"
                name="lucide:star"
                class="w-4 h-4 text-amber-400 fill-amber-400"
              />
            </div>

            <!-- Quote -->
            <blockquote class="text-text-primary text-lg leading-relaxed italic mb-6">
              "{{ t.quote }}"
            </blockquote>

            <!-- Author -->
            <div class="flex items-center justify-center gap-3">
              <img
                :src="t.avatar"
                :alt="t.name"
                class="w-12 h-12 rounded-full object-cover ring-2 ring-primary/20"
              />
              <div class="text-left">
                <p class="font-semibold text-text-primary">{{ t.name }}</p>
                <p class="text-sm text-text-secondary">{{ t.role }}</p>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- Dots -->
      <div class="flex justify-center gap-2 mt-6">
        <button
          v-for="(t, i) in testimonials"
          :key="t.id"
          :class="[
            'rounded-full transition-all duration-300',
            activeIndex === i ? 'w-6 h-2 bg-primary' : 'w-2 h-2 bg-black/20',
          ]"
          :aria-label="`Ver testimonio ${i + 1}`"
          :aria-current="activeIndex === i ? 'true' : undefined"
          @click="activeIndex = i; stopAutoplay(); startAutoplay()"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.testimonial-enter-active,
.testimonial-leave-active {
  transition: all 0.4s ease;
  position: absolute;
  width: 100%;
}
.testimonial-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.testimonial-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}
</style>
