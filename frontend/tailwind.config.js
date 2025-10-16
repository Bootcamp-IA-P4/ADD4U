/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'worksans': ['Work Sans', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial'],
      },
      colors: {
        'brand-yellow': '#ffcf00',
        'brand-blue': '#38b6ff',
        'brand-green': '#32a842',
        'brand-beige': '#f8f4eb',
        'brand-white': '#ffffff',
        'brand-black': '#000000',
        'ink': '#000000',
        'muted': '#6B7280',
        'card': '#ffffff',
        'soft': '#f8f4eb',
        'ok': '#32a842',
        'warn': '#ffcf00',
        'err': '#EF4444',
      },
      boxShadow: {
        'soft': '0 10px 30px rgba(0,0,0,0.08)',
      },
    },
  },
  plugins: [],
}
