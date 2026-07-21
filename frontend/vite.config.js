// Vite bundler config: React plugin, dev server proxy to backend
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
      // Deliberately NOT a blanket "/auth" proxy: /auth/success must stay
      // client-side (React Router) since it carries the JWT after OAuth
      // completes. Proxying it to the backend would hit the same path as
      // the real GitHub OAuth callback and crash with MismatchingStateError.
      "/auth/login": "http://localhost:8000",
      "/auth/callback": "http://localhost:8000",
      "/auth/me": "http://localhost:8000",
      "/auth/logout": "http://localhost:8000",
      "/webhook": "http://localhost:8000",
    },
  },
});
