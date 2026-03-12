import { useAuthStore } from "~/stores/auth";

const PUBLIC_PATHS = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/pricing",
];

export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore();
  const isPublic = PUBLIC_PATHS.some((p) => to.path.startsWith(p));
  if (!authStore.isAuthenticated && !isPublic) {
    return navigateTo("/login");
  }
});
