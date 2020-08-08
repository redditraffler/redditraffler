const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");

module.exports = {
  mode: "development",
  entry: "./app/js/index.js",
  devServer: {
    contentBase: "./app/assets",
    writeToDisk: true,
  },
  output: {
    filename: "[name].[contenthash].js",
    path: path.resolve(__dirname, "app/assets"),
  },
  plugins: [new ManifestPlugin()],
};
