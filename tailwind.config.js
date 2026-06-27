/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
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
