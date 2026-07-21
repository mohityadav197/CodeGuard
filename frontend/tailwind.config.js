// Tailwind CSS config: content paths for purging unused styles
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0B0F1A",
        accent: "#0ED3CF",
      },
    },
  },
  plugins: [],
};
