const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const DotenvPlugin = require("dotenv-webpack");

const targetPath = path.resolve(__dirname, "app/assets/js_build");
module.exports.targetPath = targetPath;

module.exports = {
  entry: {
    "layouts/base": "./app/js/pages/layouts/base.js",
    "raffles/index": "./app/js/pages/raffles/index.js",
    "raffles/new": "./app/js/pages/raffles/new.js",
    "raffles/status": "./app/js/pages/raffles/status.js",
    "users/show": "./app/js/pages/users/show.js",
  },
  output: {
    filename: "[name].[contenthash].js",
    path: targetPath,
  },
  plugins: [
    new DotenvPlugin({ systemvars: true }),
    new CleanWebpackPlugin({ verbose: true, dry: false }),
    new ManifestPlugin({
      generate: (seed, files, entrypoints) => {
        // https://github.com/danethurber/webpack-manifest-plugin/issues/181
        // Generates a manifest in the format of { [entrypoint: string]: Array<string> }
        return entrypoints;
      },
    }),
  ],
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
  optimization: {
    splitChunks: {
      chunks: "all",
    },
  },
};
