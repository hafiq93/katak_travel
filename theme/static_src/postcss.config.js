module.exports = {
  plugins: [
    require('postcss-import'),
    require('postcss-simple-vars'), // This line is causing the error
    require('tailwindcss'),
    require('autoprefixer'),
  ],
};
