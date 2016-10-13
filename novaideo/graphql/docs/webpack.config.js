var path = require('path')

module.exports = {
  entry: "./index.js",
  output: {
    path: path.join(__dirname, '..', 'build'),
    filename: "graphqldocs.bundle.js"
  },
  module: {
      loaders: [
          {
              exclude: /node_modules/,
              loaders: ['babel'],
          },
      ],
  },
  resolve: {
      extensions: ['', '.js', '.jsx'],
  },
}
