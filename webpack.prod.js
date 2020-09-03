const { merge } = require("webpack-merge");
const common = require("./webpack.common");
const { BundleAnalyzerPlugin } = require("webpack-bundle-analyzer");

module.exports = merge(common, {
  mode: "production",
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: process.env.BUNDLE_ANALYZER_ENABLED ? "server" : "disabled",
      openAnalyzer: true,
      analyzerHost: "localhost",
      analyzerPort: 8888,
    }),
  ],
});
