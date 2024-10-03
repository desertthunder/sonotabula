/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        prose: 'Noto Sans JP, sans-serif',
        headings: 'Rubik, sans-serif',
      },
      colors: {
        /**
         * Emerald 600
         *  */
        primary: '#047857',
        /**
         * Sky 500
         */
        secondary: '#0ea5e9',
        /**
         * Zinc 800
         */
        text: '#27272a',
        /**
         * Neutral 200
         */
        background: '#e5e5e5'
      }
    },
  },
  plugins: [],
};
