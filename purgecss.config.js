module.exports = {
    content: ['templates/*.html'],
    css: ['static/tailwind.css'],
    defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
    output: 'build/css',
  };