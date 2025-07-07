/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    fontFamily: {
      sans: ["Inter", "Nunito", "ui-sans-serif", "system-ui"],
    },
    extend: {
      colors: {
        primary: {
          50: '#fff5f5',
          100: '#ffe3e3',
          200: '#ffbdbd',
          300: '#ff9b9b',
          400: '#f86a6a',
          500: '#ef233c', // Zomato red
          600: '#d90429',
          700: '#a50021',
          800: '#6a040f',
          900: '#370617',
        },
        accent: {
          100: '#f1f8e9',
          200: '#b2dfdb',
          300: '#80cbc4',
          400: '#4db6ac',
          500: '#26a69a',
        },
        gray: {
          50: '#f8f9fa',
          100: '#f1f3f6',
          200: '#e9ecef',
          300: '#dee2e6',
          400: '#ced4da',
          500: '#adb5bd',
          600: '#6c757d',
          700: '#495057',
          800: '#343a40',
          900: '#212529',
        },
      },
      boxShadow: {
        card: '0 2px 16px 0 rgba(239,35,60,0.08)',
        nav: '0 2px 8px 0 rgba(239,35,60,0.06)',
      },
      borderRadius: {
        xl: '1.25rem',
      },
    },
  },
  plugins: [],
} 