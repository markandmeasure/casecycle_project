import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Forward API requests to the backend during development
    proxy: { '/opportunities': 'http://localhost:8000' }
  }
})
