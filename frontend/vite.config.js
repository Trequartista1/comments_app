import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    allowedHosts: ['perpetual-curiosity-production.up.railway.app'],
    host: true,
    port: 5173
  }
})