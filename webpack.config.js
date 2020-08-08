const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");

module.exports = {
  entry: "./app/js/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "app/assets"),
  },
  plugins: [new ManifestPlugin()],
};
