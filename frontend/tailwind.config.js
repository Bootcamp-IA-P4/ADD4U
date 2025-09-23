/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial'],
      },
      colors: {
        'cm-red': '#C8102E',
        'cm-red-dark': '#A20D25',
        'ink': '#111827',
        'muted': '#6B7280',
        'card': '#FFFFFF',
        'soft': '#F8F9FB',
        'ok': '#059669',
        'warn': '#D97706',
        'err': '#DC2626',
      },
      boxShadow: {
        'soft': '0 10px 30px rgba(17,24,39,0.08)',
      },
    },
  },
  plugins: [],
}
