import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@libs": path.resolve(__dirname, "./src/libs"),
    },
  },
  server: {
    fs: {
      cachedChecks: false,
    },
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000", // Point directly to Django backend
        changeOrigin: true,
      },
    },
  },
});
