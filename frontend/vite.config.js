import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Proxies /api during `vite dev` so the frontend always calls a relative
// path -- the built app (served by nginx) proxies the same path the same
// way, so no environment-specific API URL config is needed.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
