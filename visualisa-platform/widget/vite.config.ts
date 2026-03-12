import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, "src/main.ts"),
      name: "VisualisaWidget",
      fileName: "widget",
      formats: ["iife"],
    },
    rollupOptions: {
      output: {
        // Inline all CSS into the IIFE so a single script tag is enough
        assetFileNames: "widget.[ext]",
      },
    },
    minify: "esbuild",
  },
});
