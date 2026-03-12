<template>
    <div class="w-full max-w-md p-8 bg-card rounded-xl shadow-lg border border-border">
        <div class="text-center mb-8">
            <div class="w-12 h-12 rounded-xl bg-primary flex items-center justify-center mx-auto mb-4">
                <span class="text-primary-foreground font-bold text-xl">V</span>
            </div>
            <h1 class="text-2xl font-bold">Visualiza Admin</h1>
            <p class="text-muted-foreground mt-1">Sign in to manage the platform</p>
        </div>

        <form class="space-y-4" @submit.prevent="handleLogin">
            <div>
                <label class="block text-sm font-medium mb-1">Email</label>
                <input v-model="form.email" type="email" required autocomplete="email"
                    class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    placeholder="admin@visualiza.do" />
            </div>
            <div>
                <label class="block text-sm font-medium mb-1">Password</label>
                <input v-model="form.password" type="password" required autocomplete="current-password"
                    class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>

            <p v-if="error" class="text-sm text-destructive">{{ error }}</p>

            <button type="submit"
                class="w-full py-2 px-4 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50"
                :disabled="loading">
                {{ loading ? 'Signing in…' : 'Sign in' }}
            </button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'

definePageMeta({ layout: 'auth' })

const authStore = useAuthStore()
const router = useRouter()

const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
    loading.value = true
    error.value = ''
    try {
        await authStore.login(form.value.email, form.value.password)
        router.push('/')
    } catch (e: unknown) {
        error.value = e instanceof Error ? e.message : 'Login failed'
    } finally {
        loading.value = false
    }
}
</script>
