import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import dns from "dns";

dns.setDefaultResultOrder("verbatim");

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@libs": path.resolve(__dirname, "./src/libs"),
    },
  },
  server: {
    host: "0.0.0.0",
    hmr: {
      protocol: "wss",
      clientPort: 443,
      path: "hmr/",
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000", // Point directly to Django backend
        changeOrigin: true,
      },
    },
  },
});
