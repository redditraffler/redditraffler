const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const DotenvPlugin = require("dotenv-webpack");

const targetPath = path.resolve(__dirname, "app/assets/dist/js");
module.exports.targetPath = targetPath;

module.exports = {
  entry: {
    "layouts/base": "./app/js/pages/layouts/base.js",
    "raffles/index": "./app/js/pages/raffles/index.js",
    "raffles/new": "./app/js/pages/raffles/new.js",
    "raffles/status": "./app/js/pages/raffles/status.js",
    "raffles/show": "./app/js/pages/raffles/show.js",
    "users/show": "./app/js/pages/users/show.js",
  },
  output: {
    filename: "[name].[contenthash].js",
    path: targetPath,
  },
  resolve: {
    alias: {
      "~": path.resolve(__dirname, "app/js"),
    },
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
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        enforce: "pre",
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "eslint-loader",
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
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
