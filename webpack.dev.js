const { merge } = require("webpack-merge");
const common = require("./webpack.common");
const { BundleAnalyzerPlugin } = require("webpack-bundle-analyzer");

module.exports = merge(common, {
  mode: "development",
  devtool: "inline-source-map",
  devServer: {
    contentBase: common.targetPath,
    writeToDisk: true,
  },
  plugins: [
    new BundleAnalyzerPlugin({
      openAnalyzer: false,
      analyzerHost: "localhost",
      analyzerPort: 8888,
    }),
  ],
});
