module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true,
  },

  parser: '@typescript-eslint/parser',

  parserOptions: {
    project: 'tsconfig.json',
    sourceType: 'module',
    extraFileExtensions: ['.vue'],
    ecmaVersion: 2020,
  },

  plugins: [
    'eslint-plugin-import',
    'eslint-plugin-jsdoc',
    'eslint-plugin-prefer-arrow',
    '@typescript-eslint',
    '@typescript-eslint/tslint',
  ],

  root: true,

  extends: [
    'plugin:@typescript-eslint/recommended',
    'plugin:vue/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:vue/essential',
    'eslint:recommended',
    '@vue/typescript/recommended',
    '@vue/prettier',
    '@vue/prettier/@typescript-eslint',
  ],

  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
  },

  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)',
      ],
      env: {
        jest: true,
      },
    },
  ],
};
