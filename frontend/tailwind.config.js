/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#0a3ae0',
        secondary: {
          100: '#1e293b',
          200: '#334155',
        },
      },
    },
  },
  plugins: [],
};
