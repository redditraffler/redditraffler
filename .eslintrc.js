module.exports = {
  env: {
    browser: true,
    es2020: true,
  },
  extends: ["airbnb-base", "prettier"],
  parserOptions: {
    ecmaVersion: 11,
    sourceType: "module",
  },
  rules: {},
  settings: {
    "import/resolver": {
      webpack: {
        config: "webpack.common.js",
      },
    },
  },
};
