/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../../templates/**/*.html",
    "../../main/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        saffron: { 500: '#ff9933', 600: '#e67a1a', 700: '#cc6600' },
        maroon: { 800: '#610000', 900: '#530000' },
        steel: { 800: '#1e293b', 900: '#0f172a' },
        gold: { 500: '#f59e0b', 600: '#d97706' }
      },
      fontFamily: {
        warrior: ['Cinzel', 'serif'],
        sanskrit: ['Noto Sans Devanagari', 'sans-serif']
      }
    }
  },
  plugins: [],
}
