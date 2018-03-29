var path = require('path');
var webpack = require('webpack');
var glob = require('glob');
var _ = require('lodash');

var webpackPort = parseInt(process.env.WEBPACK_URL.split(':')[2]);
var webpackHost = process.env.WEBPACK_URL.split('://')[1].split(':')[0];

// For css hot reload to work, don't use ExtractTextPlugin
module.exports = {
    // devtool: '#cheap-module-eval-source-map',  // http://webpack.github.io/docs/configuration.html#devtool
    devtool: '#cheap-module-source-map', // https://github.com/webpack/webpack-dev-server/issues/1090
    devServer: {
        inline: true,
        hot: true,
        headers: {
            "Access-Control-Allow-Credentials": 'true'
        },
        port: webpackPort,
        host: webpackHost,
        proxy: {
          '/static-react': {
            target: "http://0.0.0.0:6543/"
          }
        }
    },
    entry: {
        bundle: [
            'babel-polyfill', // this is already in index.jsx but we need it to be first, otherwise it doesn't work on IE 11
            'webpack-dev-server/client?' + process.env.WEBPACK_URL,
            'react-hot-loader/patch',
            './js/app/index',
        ]
    },
    output: {
        path: path.join(__dirname, 'build'),
        filename: '[name].js',
        publicPath: process.env.WEBPACK_URL + '/build/'
    },
    module: {
        rules: [
        {
            test: /\.jsx?(\?v=\d)?$/,
            use: {
              loader: 'babel-loader',
              options: {
                forceEnv: 'development',
                plugins: [
                  'transform-object-rest-spread', 'transform-class-properties',
                  ['transform-runtime', { helpers: true, polyfill: false }]
                ],
                presets: [["env", { "modules": false, "targets": { "ie": 11 },
                                    "debug": true, "useBuiltIns": true,
                                    "exclude": ["web.timers", "web.immediate", "web.dom.iterable"] }],
                          "react", "flow"]
              }
            },
            include: [
              path.join(__dirname, 'js'),
            ]
        },
         {
            test: /\.scss$/,
            use: [
              { loader: "style-loader" },
              { loader: "css-loader", options: { sourceMap: true } },
              { loader: "sass-loader", options: { sourceMap: true } }
            ]
        },
        {
            test: /\.css$/,
            use: ['style-loader', 'css-loader']
        },
        {
            test: /\.(eot|woff|woff2|ttf|svg|png|jpe?g|gif)(\?\S*)?$/,
            use: 'url-loader?limit=100000&name=[name].[ext]'
        },
        {
          test: /\.(graphql|gql)$/,
          exclude: /node_modules/,
          use: 'graphql-tag/loader'
        },
        {
          test: /\.json$/,
          use: 'json-loader'
        },
]
    },
    resolve:{
        extensions:['.js', '.jsx']
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.DefinePlugin({
          'process.env': {
            NODE_ENV: JSON.stringify('development')
          }
        }),
    ]
};
