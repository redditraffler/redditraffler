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
  settings: {
    "import/resolver": {
      webpack: {
        config: "webpack.common.js",
      },
    },
  },
  rules: {
    camelcase: "off",
    "import/prefer-default-export": "off",
    "func-names": "off",
    "no-underscore-dangle": "off",
    "object-shorthand": ["error", "properties"],
  },
};
