/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        cairo: ['"Cairo"', "sans-serif"],
      },
      colors: {
        primary: {
          DEFAULT: "#3b82f6"
        }
      }
    }
  },
  plugins: []
};
