var path = require('path');
var webpack = require('webpack');

module.exports = {
  devtool: 'source-map',
  entry: {
//      'app': './js/app',
      'graphiql': './js/graphiql'
  },
  output: {
    path: path.join(__dirname, 'build'),
    filename: '[name].bundle.js',
    publicPath: '/static/'
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  module: {
    loaders: [
        {
            test: /\.jsx?$/,
            loader: 'babel',
            exclude: /node_modules/
        },
        { test: /\.css$/, loader: "style-loader!css-loader" },
        // inline base64 URLs for <=8k images, direct URLs for the rest
        { test: /\.(png|jpg)$/, loader: 'url-loader?limit=8192' }
    ]
  }
};
