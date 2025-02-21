import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "static/js",
    rollupOptions: {
      input: {
        cart: path.resolve(__dirname, "static/js/cart.js"),
      },
      output: {
        entryFileNames: "[name]-bundle.js",
        format: "iife",
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
