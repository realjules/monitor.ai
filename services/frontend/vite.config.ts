import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 50711,
    proxy: {
      '/api': {
        target: 'http://localhost:57763',
        changeOrigin: true,
      },
    },
  },
})
