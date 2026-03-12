<template>
    <div class="w-full max-w-md p-8 bg-card rounded-xl shadow-lg border border-border">
        <div class="text-center mb-8">
            <div class="w-12 h-12 rounded-xl bg-primary flex items-center justify-center mx-auto mb-4">
                <span class="text-primary-foreground font-bold text-xl">V</span>
            </div>
            <h1 class="text-2xl font-bold">Create your account</h1>
            <p class="text-muted-foreground mt-1">Join thousands of DR real estate professionals</p>
        </div>

        <form class="space-y-4" @submit.prevent="handleRegister">
            <div>
                <label class="block text-sm font-medium mb-1">Full Name</label>
                <input v-model="form.full_name" type="text" required
                    class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
                <label class="block text-sm font-medium mb-1">Email</label>
                <input v-model="form.email" type="email" required autocomplete="email"
                    class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
                <label class="block text-sm font-medium mb-1">Password</label>
                <input v-model="form.password" type="password" required minlength="8" autocomplete="new-password"
                    class="w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
                <p class="text-xs text-muted-foreground mt-1">Minimum 8 characters</p>
            </div>

            <p v-if="error" class="text-sm text-destructive">{{ error }}</p>

            <button type="submit" :disabled="loading"
                class="w-full py-2 px-4 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50">
                {{ loading ? 'Creating account…' : 'Create Account' }}
            </button>
        </form>

        <p class="text-center text-sm text-muted-foreground mt-6">
            Already have an account?
            <NuxtLink to="/login" class="text-primary hover:underline font-medium">Sign in</NuxtLink>
        </p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: 'auth' })

const authStore = useAuthStore()
const router = useRouter()
const form = ref({ full_name: '', email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleRegister() {
    loading.value = true
    error.value = ''
    try {
        const config = useRuntimeConfig()
        const res = await fetch(`${config.public.apiBaseUrl}/api/v1/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...form.value, role: 'professional' }),
        })
        if (!res.ok) {
            const err = await res.json().catch(() => ({}))
            throw new Error(err.detail || 'Registration failed')
        }
        // Auto-login
        await authStore.login(form.value.email, form.value.password)
        router.push('/billing')
    } catch (e: unknown) {
        error.value = e instanceof Error ? e.message : 'Registration failed'
    } finally {
        loading.value = false
    }
}
</script>
