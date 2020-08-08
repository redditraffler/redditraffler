const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");

module.exports = {
  mode: "development",
  entry: "./app/js/index.js",
  output: {
    filename: "[name].[contenthash].js",
    path: path.resolve(__dirname, "app/assets"),
  },
  plugins: [new ManifestPlugin()],
};
