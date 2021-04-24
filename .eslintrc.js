module.exports = {
  env: {
    browser: true,
    es2020: true,
    jest: true,
  },
  extends: [
    "airbnb-base",
    "plugin:react/recommended",
    "plugin:jest-dom/recommended",
    "plugin:jsx-a11y/recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  plugins: ["react", "jsx-a11y", "@typescript-eslint"],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: 11,
    sourceType: "module",
    jsx: true,
  },
  settings: {
    react: {
      version: "detect",
    },
    "import/resolver": {
      webpack: {
        config: "webpack.common.js",
      },
    },
    "import/ignore": [/\.(scss|less|css)$/],
  },
  rules: {
    camelcase: "off",
    "import/prefer-default-export": "off",
    "import/extensions": "off",
    "import/no-extraneous-dependencies": ["error", { devDependencies: true }],
    "func-names": "off",
    "no-underscore-dangle": "off",
    "object-shorthand": ["error", "properties"],
    "no-use-before-define": "off",
    "@typescript-eslint/ban-ts-comment": "warn",
  },
};
