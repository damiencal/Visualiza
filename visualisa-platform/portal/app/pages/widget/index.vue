<template>
    <div class="max-w-4xl">
        <div class="flex items-center justify-between mb-6">
            <div>
                <h1 class="text-2xl font-bold">Widget Configuration</h1>
                <p class="text-muted-foreground mt-1">Embed the Visualisa widget on your website or app.</p>
            </div>
        </div>

        <div v-if="loading" class="flex items-center justify-center py-16">
            <Icon name="lucide:loader-circle" class="w-6 h-6 animate-spin text-muted-foreground" />
        </div>

        <div v-else class="space-y-6">
            <!-- API Key card -->
            <div class="bg-card border border-border rounded-xl p-6">
                <h2 class="font-semibold mb-4">API Key</h2>
                <div class="flex items-center gap-3">
                    <code class="flex-1 px-3 py-2 bg-muted rounded-md text-sm font-mono break-all">
            {{ showKey ? profile?.api_key : maskKey(profile?.api_key) }}
          </code>
                    <button class="p-2 rounded border border-border hover:bg-accent" :title="showKey ? 'Hide' : 'Show'"
                        @click="showKey = !showKey">
                        <Icon :name="showKey ? 'lucide:eye-off' : 'lucide:eye'" class="w-4 h-4" />
                    </button>
                    <button class="p-2 rounded border border-border hover:bg-accent" title="Copy"
                        @click="copy(profile?.api_key ?? '')">
                        <Icon :name="copied ? 'lucide:check' : 'lucide:copy'" class="w-4 h-4" />
                    </button>
                </div>
                <div class="flex items-center justify-between mt-3">
                    <p class="text-xs text-muted-foreground">Never share your API key publicly.</p>
                    <button class="text-xs text-destructive hover:underline" @click="regenerateKey">
                        Regenerate key
                    </button>
                </div>
            </div>

            <!-- Embed snippet -->
            <div class="bg-card border border-border rounded-xl p-6">
                <h2 class="font-semibold mb-1">Embed Snippet</h2>
                <p class="text-sm text-muted-foreground mb-4">Copy this code and paste it before the <code
                        class="bg-muted px-1 rounded">&lt;/body&gt;</code> tag of your website.</p>
                <div class="relative">
                    <pre class="bg-muted rounded-lg p-4 text-xs overflow-x-auto">{{ embedCode }}</pre>
                    <button
                        class="absolute top-3 right-3 p-1.5 rounded bg-background border border-border hover:bg-accent"
                        @click="copy(embedCode)">
                        <Icon :name="copied ? 'lucide:check' : 'lucide:copy'" class="w-3.5 h-3.5" />
                    </button>
                </div>
            </div>

            <!-- Widget config form -->
            <div class="bg-card border border-border rounded-xl p-6">
                <h2 class="font-semibold mb-4">Appearance</h2>
                <form class="space-y-4 max-w-lg" @submit.prevent="saveConfig">
                    <div>
                        <label class="block text-sm font-medium mb-1">Primary Color</label>
                        <div class="flex items-center gap-3">
                            <input v-model="config.primary_color" type="color"
                                class="w-10 h-10 rounded cursor-pointer border border-input" />
                            <input v-model="config.primary_color" type="text"
                                class="px-3 py-2 border border-input rounded-md text-sm bg-background w-28 font-mono" />
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Button Label</label>
                        <input v-model="config.cta_text" type="text"
                            class="px-3 py-2 border border-input rounded-md text-sm bg-background w-full focus:outline-none focus:ring-2 focus:ring-ring"
                            placeholder="Get a Quote" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Allowed Domains</label>
                        <textarea v-model="domainsText"
                            class="px-3 py-2 border border-input rounded-md text-sm bg-background w-full focus:outline-none focus:ring-2 focus:ring-ring"
                            rows="3" placeholder="example.com&#10;subdomain.example.com" />
                        <p class="text-xs text-muted-foreground mt-1">One domain per line. Used for CORS origin
                            validation.</p>
                    </div>
                    <button type="submit"
                        class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                        :disabled="saving">
                        {{ saving ? 'Saving…' : 'Save Configuration' }}
                    </button>
                </form>
            </div>

            <!-- Deployments -->
            <div class="bg-card border border-border rounded-xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="font-semibold">Deployments</h2>
                    <button
                        class="flex items-center gap-2 px-3 py-2 border border-border rounded-md text-sm hover:bg-accent"
                        @click="openAddDeployment">
                        <Icon name="lucide:plus" class="w-4 h-4" />
                        Add Deployment
                    </button>
                </div>
                <p v-if="!deployments.length" class="text-sm text-muted-foreground">No deployments yet. Add your first
                    website deployment.</p>
                <div v-else class="space-y-3">
                    <div v-for="d in deployments" :key="d.id"
                        class="flex items-center justify-between p-3 bg-muted/30 rounded-lg">
                        <div>
                            <p class="font-medium text-sm">{{ d.site_name }}</p>
                            <a :href="d.site_url" target="_blank" rel="noopener noreferrer"
                                class="text-xs text-blue-600 hover:underline">{{ d.site_url }}</a>
                        </div>
                        <button
                            class="p-1.5 rounded hover:bg-destructive/10 text-muted-foreground hover:text-destructive"
                            @click="removeDeployment(d)">
                            <Icon name="lucide:trash-2" class="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Deployment Modal -->
        <div v-if="addModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
            @click.self="addModal = false">
            <div class="bg-card border border-border rounded-xl p-6 w-full max-w-md shadow-xl">
                <h2 class="font-semibold text-lg mb-4">Add Deployment</h2>
                <form class="space-y-4" @submit.prevent="saveDeployment">
                    <div>
                        <label class="block text-sm font-medium mb-1">Site Name *</label>
                        <input v-model="depForm.site_name" required
                            class="w-full px-3 py-2 border border-input rounded-md text-sm bg-background focus:outline-none focus:ring-2 focus:ring-ring"
                            placeholder="My Real Estate Site" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Site URL *</label>
                        <input v-model="depForm.site_url" required type="url"
                            class="w-full px-3 py-2 border border-input rounded-md text-sm bg-background focus:outline-none focus:ring-2 focus:ring-ring"
                            placeholder="https://example.com" />
                    </div>
                    <div class="flex justify-end gap-3">
                        <button type="button" class="px-4 py-2 border border-border rounded-md text-sm hover:bg-accent"
                            @click="addModal = false">Cancel</button>
                        <button type="submit"
                            class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">Add</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'default' })

const api = useApi()
const loading = ref(true)
const saving = ref(false)
const showKey = ref(false)
const copied = ref(false)
const addModal = ref(false)

interface Profile { api_key: string; widget_config: Record<string, unknown> }
interface Deployment { id: string; site_name: string; site_url: string }

const profile = ref<Profile | null>(null)
const deployments = ref<Deployment[]>([])
const config = reactive({ primary_color: '#7c3aed', cta_text: 'Get a Quote' })
const domainsText = ref('')
const depForm = reactive({ site_name: '', site_url: '' })

const embedCode = computed(() => {
    if (!profile.value?.api_key) return '<!-- Loading… -->'
    return `<script src="https://cdn.visualisa.web.do/widget.js"><\/script>
<visualisa-widget
  api-key="${profile.value.api_key}"
  lang="es"
><\/visualisa-widget>`
})

async function load() {
    const [prof, deps] = await Promise.all([
        api.get<Profile>('/api/v1/portal/widget/config'),
        api.get<{ items: Deployment[] }>('/api/v1/portal/widget/deployments'),
    ])
    profile.value = prof
    deployments.value = deps.items
    if (prof.widget_config) Object.assign(config, prof.widget_config)
    loading.value = false
}

async function saveConfig() {
    saving.value = true
    const domains = domainsText.value.split('\n').map((d) => d.trim()).filter(Boolean)
    await api.put('/api/v1/portal/widget/config', { ...config, allowed_domains: domains })
    saving.value = false
}

async function regenerateKey() {
    if (!confirm('Regenerating your API key will break existing widget deployments. Continue?')) return
    const data = await api.post<Profile>('/api/v1/portal/widget/regenerate-key', {})
    if (profile.value) profile.value.api_key = data.api_key
}

function maskKey(k?: string) {
    if (!k) return '—'
    return k.slice(0, 12) + '•'.repeat(24)
}

async function copy(text: string) {
    await navigator.clipboard.writeText(text)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
}

function openAddDeployment() {
    Object.assign(depForm, { site_name: '', site_url: '' })
    addModal.value = true
}

async function saveDeployment() {
    await api.post('/api/v1/portal/widget/deployments', depForm)
    addModal.value = false
    const deps = await api.get<{ items: Deployment[] }>('/api/v1/portal/widget/deployments')
    deployments.value = deps.items
}

async function removeDeployment(d: Deployment) {
    if (!confirm(`Remove deployment "${d.site_name}"?`)) return
    await api.delete(`/api/v1/portal/widget/deployments/${d.id}`)
    deployments.value = deployments.value.filter((dep) => dep.id !== d.id)
}

onMounted(load)
</script>
