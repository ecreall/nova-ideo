var path = require('path');
var webpack = require('webpack');
var glob = require('glob');
var _ = require('lodash');

//Env vars
var APP_URL = 'http://localhost:6543'
var WEBPACK_URL = 'http://localhost:8081'
var webpackPort = parseInt(WEBPACK_URL.split(':')[2]);
var webpackHost = WEBPACK_URL.split('://')[1].split(':')[0];

// For css hot reload to work, don't use ExtractTextPlugin
module.exports = {
    // devtool: '#cheap-module-eval-source-map',  // http://webpack.github.io/docs/configuration.html#devtool
    devtool: 'eval-source-map', // https://github.com/webpack/webpack-dev-server/issues/1090
    devServer: {
        inline: true,
        hot: true,
        headers: {
            "Access-Control-Allow-Origin": APP_URL,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
        },
        port: webpackPort,
        host: webpackHost,
        proxy: {
          '/static-react': {
            target: APP_URL
          }
        }
    },
    entry: {
        bundle: [
            'react-hot-loader/patch',
            '@babel/polyfill', // this is already in index.jsx but we need it to be first, otherwise it doesn't work on IE 11
            'webpack-dev-server/client?' + WEBPACK_URL,
            './js/app/index',
        ],
       novaideo: ['./css/novaideo.css', './css/latofonts.css']
    },
    output: {
        path: path.join(__dirname, 'build'),
        filename: '[name].js',
        publicPath: WEBPACK_URL + '/build/'
    },
    module: {
        rules: [
        {
            test: /\.jsx?(\?v=\d)?$/,
            use: {
              loader: 'babel-loader',
              options: {
                envName: 'development',
                plugins: [
                  '@babel/plugin-proposal-object-rest-spread',
                  '@babel/plugin-proposal-class-properties',
                  '@babel/plugin-transform-react-inline-elements',
                  'react-hot-loader/babel',
                  ['@babel/plugin-transform-runtime', { helpers: true }]
                ],
                presets: [["@babel/preset-env", { "modules": false, "targets": { "ie": 11 },
                                    "debug": true, "useBuiltIns": "entry",
                                    "exclude": ["web.timers", "web.immediate", "web.dom.iterable"] }],
                          "@babel/preset-react", "@babel/preset-flow"]
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
        }
]
    },
    resolve:{
        extensions:['.js', '.jsx']
    },
    mode: 'development',
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
    ]
};
