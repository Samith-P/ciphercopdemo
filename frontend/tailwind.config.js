/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'gradient': 'gradient 8s linear infinite',
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
  safelist: [
    {
      pattern: /from-(blue|green|purple|pink|red|yellow|orange)-(400|500|600)/,
    },
    {
      pattern: /to-(blue|green|purple|pink|red|yellow|orange)-(400|500|600)/,
    },
    {
      pattern: /border-(blue|green|purple|pink|red|yellow|orange)-(500)/,
    },
  ],
}
