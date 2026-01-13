/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#22C55E',
          hover: '#14532D',
          secondary: '#34D399',
          neutral: '#6B7280',
          dark: '#000000',
          bg: '#F3F4F6',
          surface: '#FFFFFF',
        }
      }
    },
  },
  plugins: [],
}