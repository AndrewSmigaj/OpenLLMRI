import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // The repo root's .env holds the MUD's ports (one setting for compose, the backend and the app).
  // Only MUD_WS_* reaches the app's code; the file's other entries stay out of the bundle.
  envDir: '..',
  envPrefix: ['VITE_', 'MUD_WS_'],
  server: {
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true,
      interval: 500,
    },
  },
})
