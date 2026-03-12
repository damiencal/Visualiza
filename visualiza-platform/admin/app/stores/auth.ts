import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useApi } from "~/composables/useApi";

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
  const isAdmin = computed(
    () => user.value?.role === "admin" || user.value?.role === "superadmin",
  );

  // Hydrate from localStorage on client
  if (import.meta.client) {
    token.value = localStorage.getItem("visualiza_admin_token");
    refreshToken.value = localStorage.getItem("visualiza_admin_refresh");
    const stored = localStorage.getItem("visualiza_admin_user");
    if (stored) user.value = JSON.parse(stored);
  }

  async function login(email: string, password: string) {
    const { $api } = useNuxtApp();
    const data = await ($api as ReturnType<typeof useApi>).post<{
      access_token: string;
      refresh_token: string;
      user: User;
    }>("/api/v1/auth/login", { email, password });

    token.value = data.access_token;
    refreshToken.value = data.refresh_token;
    user.value = data.user;

    if (import.meta.client) {
      localStorage.setItem("visualiza_admin_token", data.access_token);
      localStorage.setItem("visualiza_admin_refresh", data.refresh_token);
      localStorage.setItem("visualiza_admin_user", JSON.stringify(data.user));
    }
  }

  function logout() {
    token.value = null;
    refreshToken.value = null;
    user.value = null;
    if (import.meta.client) {
      localStorage.removeItem("visualiza_admin_token");
      localStorage.removeItem("visualiza_admin_refresh");
      localStorage.removeItem("visualiza_admin_user");
    }
    const router = useRouter();
    router.push("/login");
  }

  return { token, user, isAuthenticated, isAdmin, login, logout };
});
