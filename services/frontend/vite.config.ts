import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: parseInt(process.env.VITE_PORT || '52209'),
    host: process.env.VITE_HOST || '0.0.0.0',
    strictPort: true,
    cors: true,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:52209',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  preview: {
    port: parseInt(process.env.VITE_PORT || '52209'),
    host: process.env.VITE_HOST || '0.0.0.0',
    strictPort: true,
  }
})
