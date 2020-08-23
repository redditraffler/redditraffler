const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const DotenvPlugin = require("dotenv-webpack");

const targetPath = path.resolve(__dirname, "app/assets/dist/js");
module.exports.targetPath = targetPath;

module.exports = {
  entry: {
    "layouts/base": "./app/js/pages/layouts/base.js",
    "base/index": "./app/js/pages/base/index.js",
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
      Assets: path.resolve(__dirname, "app/assets"),
    },
    extensions: [".js", ".jsx", ".css"],
    modules: ["node_modules"],
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
        enforce: "pre",
        test: /\.(s?)css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        enforce: "pre",
        test: /\.s[ca]ss$/i,
        use: ["sass-loader"],
      },
      {
        enforce: "pre",
        test: /\.js(x?)$/,
        exclude: /node_modules/,
        loader: "eslint-loader",
      },
      {
        test: /\.js(x?)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
            plugins: ["@babel/plugin-transform-runtime"],
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
