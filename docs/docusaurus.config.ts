import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "Music Dashboard Docs",
  tagline: "A spotify integrated music library dashboard.",
  favicon: "/img/favicon.svg",
  url: "https://sonotabula.netlify.app",
  baseUrl: "/",
  projectName: "sonotablula",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },
  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          routeBasePath: "/",
          path: "md",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: "img/social-card.png",
    colorMode: {
      defaultMode: "dark",
      disableSwitch: true,
    },
    navbar: {
      title: "Music Dashboard",
      logo: {
        alt: "App Icon",
        src: "img/logo.svg",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "docsSidebar",
          position: "left",
          label: "Docs",
        },
        {
          href: "https://github.com/desertthunder/spotify-dashboard",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Social Links",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/desertthunder",
            },
            {
              label: "LinkedIn",
              href: "https://www.linkedin.com/in/owais-jamil/",
            },
            {
              label: "Twitter",
              href: "https://twitter.com/_desertthunder",
            },
          ],
        },
        {
          title: "Resources",
          items: [
            {
              label: "React",
              href: "https://react.dev",
            },
            {
              label: "Docusaurus",
              href: "https://docusaurus.io",
            },
            {
              label: "Spotify API Documentation",
              href: "https://developer.spotify.com/documentation/web-api/",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "My Blog",
              href: "https://desertthunder.github.io",
            },
            {
              label: "Digital Garden",
              href: "https://desertthunder.github.io/garden",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Owais J. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
