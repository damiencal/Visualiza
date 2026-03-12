// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-01-01",
  nitro: {
    preset: "vercel",
  },
  runtimeConfig: {
    imagenApiKey: process.env.NUXT_IMAGEN_API_KEY ?? "",
  },
  future: { compatibilityVersion: 4 },
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxtjs/google-fonts",
    "@vueuse/nuxt",
    "@nuxt/icon",
    "@pinia/nuxt",
    "shadcn-nuxt",
  ],
  googleFonts: {
    families: {
      Inter: [300, 400, 500, 600, 700, 800],
    },
    display: "swap",
  },
  shadcn: {
    prefix: "",
    componentDir: "./app/components/ui",
  },
  css: ["~/assets/css/main.css"],
  app: {
    head: {
      title: "Visualisa — Visualisador Inmobiliario Interactivo",
      meta: [
        {
          name: "description",
          content:
            "Visualisa tu hogar ideal con productos reales de suplidores dominicanos.",
        },
        { name: "theme-color", content: "#F43F5E" },
        { name: "apple-mobile-web-app-capable", content: "yes" },
        { name: "apple-mobile-web-app-status-bar-style", content: "default" },
        { name: "apple-mobile-web-app-title", content: "Visualisa" },
        { name: "application-name", content: "Visualisa" },
        { name: "msapplication-TileColor", content: "#F43F5E" },
        { name: "msapplication-config", content: "/browserconfig.xml" },
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, viewport-fit=cover",
        },
      ],
      link: [
        { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        {
          rel: "apple-touch-icon",
          sizes: "180x180",
          href: "/apple-touch-icon.png",
        },
        { rel: "manifest", href: "/manifest.webmanifest" },
      ],
    },
  },
});
