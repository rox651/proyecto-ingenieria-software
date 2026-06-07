import { defineConfig } from "vitepress";

export default defineConfig({
  title: "VoiceLoop — Software Journey",
  description:
    "Bitácora de co-creación hombre-máquina del agente de voz asyncio VoiceLoop",
  base: "/proyecto-ingenieria-software/",
  themeConfig: {
    nav: [
      { text: "Inicio", link: "/" },
      { text: "Repositorio", link: "https://github.com/rox651/proyecto-ingenieria-software" },
    ],
    sidebar: [
      {
        text: "Software Journey",
        items: [
          { text: "Introducción", link: "/" },
          {
            text: "1. Bala Trazadora y Skills",
            link: "/journey/tracer-bullet",
          },
          {
            text: "2. Anatomía de la Complejidad",
            link: "/journey/anatomy",
          },
          {
            text: "3. Veredicto Retrospectivo",
            link: "/journey/retrospective",
          },
        ],
      },
    ],
    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/rox651/proyecto-ingenieria-software",
      },
    ],
  },
});
