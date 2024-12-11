/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './main/templates/main/**/*.html'
  ],
  theme: {
    extend: {
      colors : {
        "Background": "#181818",
        "Primary-Text": "#E0E0E0",
        "Secondary-Text-Color": "#B0B0B0",
        "Accent-Button-Color": "#FF6347",
        "Link-Color": "#4CAF50",
        "Border-Color": "#333333",
        "Highlight-Color": "#FFD700"
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'sans-serif'],
        body: ['Source Sans Pro', 'Nunito', 'sans-serif'],
        code: ['Roboto Mono', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
}

