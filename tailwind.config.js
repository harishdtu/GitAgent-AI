/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        amber: {
          50: '#faf8f6',
          100: '#f5f1ed',
          200: '#ede9e5',
          300: '#e0d9ce',
          400: '#d1c4b0',
          500: '#c4b5a0',
          600: '#b89d85',
          700: '#92400e',
          800: '#78340f',
          900: '#5c2e0f',
          950: '#3d1f0a',
        },
      },
      fontFamily: {
        serif: ['Merriweather', 'serif'],
        mono: ['Source Code Pro', 'monospace'],
      },
    },
  },
  plugins: [],
}