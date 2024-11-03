import { iconsPlugin, getIconCollections } from "@egoist/tailwindcss-icons";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: '"Inter Variable", sans-serif',
        titles: '"Karla Variable", sans-serif',
        headings: '"DM Sans Variable", sans-serif',
      },
      colors: {
        /**
         * Emerald 500
         *  */
        primary: "#10b981",
        /**
         * Sky 500
         */
        secondary: "#0ea5e9",
        /**
         * Rose 500
         */
        error: "#f43f5e",
        /**
         * Amber 500
         */
        warning: "#f59e0b",
        /**
         * Cyan 500
         */
        info: "#06b6d4",
        /**
         * Cyan 500
         */
        accent: "#06b6d4",
        /**
         * Neutral 950
         */
        text: "#0a0a0a",
        /**
         * Zinc 50
         */
        surface: "#fafafa",
      },
    },
  },
  plugins: [
    iconsPlugin({
      collections: getIconCollections([
        "ri",
        "openmoji",
        "devicon",
        "skill-icons",
        "devicon-plain",
        "fe",
      ]),
    }),
  ],
};
