module.exports = {
  purge: {
    enabled: true,
    content: ['./templates/*.html',]
},
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    screens: {
      'sm':'1px',
      'md':'720px',
      'lg':'1024px',
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
