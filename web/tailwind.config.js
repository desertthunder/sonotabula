import { iconsPlugin, getIconCollections } from "@egoist/tailwindcss-icons";

// 1-3: Background
// 4-6: Interactive
// 7-9 Borders
// 10-12: Text
const jade = {
  1: '#edf0ee',
  2: '#e5ece8',
  3: '#d5e6dc',
  4: '#c4e0d0',
  5: '#b1d7c1',
  6: '#99cbb0',
  7: '#79bb98',
  8: '#46a578',
  9: '#5bb98b',
  10: '#4fad80',
  11: '#006d44',
  12: '#1b3b2b',
  a1: '#265bef05',
  a2: '#066a790d',
  a3: '#0485551e',
  a4: '#028f4f30',
  a5: '#018a4544',
  a6: '#0387465e',
  a7: '#0183427f',
  a8: '#008548b5',
  a9: '#00964f9f',
  a10: '#018c4bac',
  a11: '#006d44',
  a12: '#012413e3',
  contrast: '#ffffff',
  surface: '#e2eae6cc',
  indicator: '#5bb98b',
  track: '#5bb98b'
};

const sage = {
  1: '#eeefec',
  2: '#e9ebe6',
  3: '#dfe1db',
  4: '#d6d9cf',
  5: '#cdd1c6',
  6: '#c4c9bb',
  7: '#b8beac',
  8: '#a4ab94',
  9: '#757e62',
  10: '#6b735a',
  11: '#4f5541',
  12: '#1d2311',
  a1: '#59288905',
  a2: '#0f110c09',
  a3: '#17190815',
  a4: '#27300622',
  a5: '#1c2a012b',
  a6: '#21300237',
  a7: '#25350147',
  a8: '#27350261',
  a9: '#1f2d0096',
  a10: '#1a26009f',
  a11: '#131a01ba',
  a12: '#0d1300ed',
  contrast: '#FFFFFF',
  surface: '#ffffffcc',
  indicator: '#757e62',
  track: '#757e62'
};


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
        jade,
        sage,
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
      collections: getIconCollections(["ri", "openmoji", "devicon", "skill-icons", "devicon-plain"]),
    }),
  ],
};
