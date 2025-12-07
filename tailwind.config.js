/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: 'var(--bg-primary)',
        secondary: 'var(--bg-secondary)',
        tertiary: 'var(--bg-tertiary)',
        'text-primary': 'var(--text-primary)',
        'text-secondary': 'var(--text-secondary)',
        'text-muted': 'var(--text-muted)',
        'accent-teal': 'var(--accent-teal)',
        'accent-teal-dark': 'var(--accent-teal-dark)',
        'accent-purple': 'var(--accent-purple)',
        'accent-purple-dark': 'var(--accent-purple-dark)',
        'accent-pink': 'var(--accent-pink)',
        'accent-gold': 'var(--accent-gold)',
        'accent-green': 'var(--accent-green)',
      },
    },
  },
  plugins: [],
};
