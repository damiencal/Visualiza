import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
  compatibilityDate: "2025-05-01",
  devtools: { enabled: true },

  modules: [
    "@nuxtjs/tailwindcss",
    "@pinia/nuxt",
    "@nuxt/icon",
    "@vueuse/nuxt",
    "shadcn-nuxt",
  ],

  shadcn: {
    prefix: "",
    componentDir: "./components/ui",
  },

  runtimeConfig: {
    public: {
      apiBaseUrl:
        process.env.NUXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
      appUrl: process.env.NUXT_PUBLIC_APP_URL || "http://localhost:3002",
    },
  },

  app: {
    head: {
      title: "Visualisa — Professional Portal",
      meta: [
        {
          name: "description",
          content:
            "AI-powered renovation visualizer for DR real estate professionals",
        },
      ],
    },
  },
});
