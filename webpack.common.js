const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

const targetPath = path.resolve(__dirname, "app/assets/js_build");
module.exports.targetPath = targetPath;

module.exports = {
  entry: {
    "layouts/base": "./app/js/pages/layouts/base.js",
    "raffles/new": "./app/js/pages/raffles/new.js",
  },
  output: {
    filename: "[name].[contenthash].js",
    path: targetPath,
  },
  plugins: [
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
