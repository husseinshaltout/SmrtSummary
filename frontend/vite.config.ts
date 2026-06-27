import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/static/frontend/',
  build: {
    outDir: '../SmrtSummary/static/frontend',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/accounts': 'http://127.0.0.1:8000',
    },
  },
});
