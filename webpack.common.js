const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

const targetPath = path.resolve(__dirname, "app/assets/js_build");
module.exports.targetPath = targetPath;

module.exports = {
  entry: "./app/js/index.js",
  output: {
    filename: "[name].[contenthash].js",
    path: targetPath,
  },
  plugins: [
    new CleanWebpackPlugin({ verbose: true, dry: false }),
    new ManifestPlugin(),
  ],
};
