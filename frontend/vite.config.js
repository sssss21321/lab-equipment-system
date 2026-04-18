import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: '0.0.0.0',   // 监听所有网卡，方便局域网访问
    open: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',  // 本机开发时代理到后端
        changeOrigin: true,
      },
    },
  },
})
