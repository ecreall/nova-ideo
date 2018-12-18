/*
Once you have made changes to this file, you have to run `supervisorctl restart dev:webpack` to see the effect.
*/

var path = require('path');
var webpack = require('webpack');
var MiniCssExtractPlugin = require("mini-css-extract-plugin");
var glob = require('glob');
var _ = require('lodash');

var general_entries = {
    bundle: ['./js/app/index'],
novaideo: ['./css/novaideo.css', './css/latofonts.css']
};

module.exports = {
    devtool: '#cheap-module-source-map',  // http://webpack.github.io/docs/configuration.html#devtool
    entry:general_entries,
    output: {
        path: path.join(__dirname, 'build'),
        filename: '[name].js',
        publicPath: '/novaideostatic-react/build/'
    },
    module: {
        rules: [
        {
            test: /\.jsx?(\?v=\d)?$/,
            use: {
              loader: 'babel-loader',
              options: {
                envName: 'production',  // babel default to development otherwise, this is to remove the __REACT_HOT_LOADER__ conditions in the code
                // We specify plugins and presets here to be able to transpile
                // dependencies that may have a .babelrc but doesn't do
                // an actual transpilation to ES5. The .babelrc
                // in this project is actually not used to transpile
                // dependencies if the dependency already has a .babelrc file,
                // we need plugins and presets here for that.
                // A dependency is transpiled only if it's in the include below.
                plugins: [
                  '@babel/plugin-proposal-object-rest-spread',
                  '@babel/plugin-proposal-class-properties',
                  '@babel/plugin-transform-react-inline-elements',
                  ['@babel/plugin-transform-runtime', { helpers: true}]
                ],
                presets: [["@babel/preset-env", { "modules": false, "targets": { "ie": 11 },
                                    "debug": false, "useBuiltIns": "entry",
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
              MiniCssExtractPlugin.loader,
              'css-loader',
              'sass-loader'
            ]
        },
        {
            test: /\.css$/,
            use: [
              MiniCssExtractPlugin.loader,
              'css-loader'
            ]
        },
        {
            test: /\.(eot|woff|woff2|ttf|svg|png|jpe?g|gif)(\?\S*)?$/,
            use: 'file-loader?name=[name].[ext]'
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
    mode: 'production',
    plugins: [
        new MiniCssExtractPlugin({ filename: "[name].css" }),
    ]
};
