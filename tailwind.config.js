module.exports = {
  purge: false,
  content: [
    './templates/**/*.html', // Untuk memeriksa semua file HTML dalam folder templates
    './static/js/main.js',
    './app/**/*.py',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'custom-background': "url('../images/background.jpg')", // Path harus sesuai dengan lokasi file yang Anda berikan
      },
      // rotate: {
      //   '90': '90deg',
      // },
      // scale: {
      //   '100': '1',
      // }
    },
  },
  plugins: [],
}
