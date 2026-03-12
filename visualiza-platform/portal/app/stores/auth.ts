import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
}

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const user = ref<User | null>(null);

  const isAuthenticated = computed(() => !!token.value);

  if (import.meta.client) {
    token.value = localStorage.getItem("visualiza_token");
    refreshToken.value = localStorage.getItem("visualiza_refresh");
    const stored = localStorage.getItem("visualiza_user");
    if (stored) user.value = JSON.parse(stored);
  }

  async function login(email: string, password: string) {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBaseUrl}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Login failed");
    }
    const data = await res.json();
    token.value = data.access_token;
    refreshToken.value = data.refresh_token;
    user.value = data.user;

    if (import.meta.client) {
      localStorage.setItem("visualiza_token", data.access_token);
      localStorage.setItem("visualiza_refresh", data.refresh_token);
      localStorage.setItem("visualiza_user", JSON.stringify(data.user));
    }
  }

  function logout() {
    token.value = null;
    refreshToken.value = null;
    user.value = null;
    if (import.meta.client) {
      localStorage.removeItem("visualiza_token");
      localStorage.removeItem("visualiza_refresh");
      localStorage.removeItem("visualiza_user");
    }
    const router = useRouter();
    router.push("/login");
  }

  return { token, user, isAuthenticated, login, logout };
});
