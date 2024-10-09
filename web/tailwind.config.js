import { iconsPlugin, getIconCollections } from "@egoist/tailwindcss-icons";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: '"Inter Variable", sans-serif',
        prose: '"Noto Sans JP Variable", sans-serif',
        headings: '"Rubik Variable", sans-serif',
      },
      colors: {
        /**
         * Emerald 600
         *  */
        primary: "#047857",
        /**
         * Sky 500
         */
        secondary: "#0ea5e9",
        /**
         * Zinc 800
         */
        text: "#27272a",
        /**
         * Neutral 200
         */
        background: "#e5e5e5",
      },
    },
  },
  plugins: [
    iconsPlugin({
      collections: getIconCollections(["ri"]),
    }),
  ],
};
