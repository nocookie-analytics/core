const webpack = require('webpack');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const cssnano = require('cssnano');
const purgecss = require('@fullhuman/postcss-purgecss');
const purgecssConfig = require('./purgecss.conf');

module.exports = {
  assetsDir: 'static',
  configureWebpack: {
    plugins: [
      new CopyPlugin([
        {
          from: '**',
          context: './node_modules/flag-icon-css/flags/4x3/',
          to: './static/flags/',
        },
        {
          from: '**/*.svg',
          context: './node_modules/simple-icons/icons/',
          to: './static/brand-icons/',
        },
      ]),
      new VuetifyLoaderPlugin(),
      new webpack.IgnorePlugin({
        resourceRegExp: /moment$/,
      }),
    ],
  },

  chainWebpack: (config) => {
    config.plugin('prefetch').tap((options) => {
      options[0].fileBlacklist = options[0].fileBlacklist || [];
      options[0].fileBlacklist.push(/\/main-.*/);
      options[0].fileBlacklist.push(/\/domains.*/);
      options[0].fileBlacklist.push(/\/users-.*/);
      options[0].fileBlacklist.push(/\/.*analytics.*/);
      options[0].fileBlacklist.push(/.*map$/);
      return options;
    });

    config.module
      .rule('css')
      .oneOf('normal')
      .use('postcss-loader')
      .tap((options) => {
        options.plugins.unshift(...[cssnano, purgecss(purgecssConfig)]);
        return options;
      });

    if (process.env.NODE_ENV === 'test') {
      // https://github.com/vuejs/vue-cli/issues/4053#issuecomment-544641072
      for (const ruleName of ['sass', 'scss']) {
        const sassRule = config.module.rule(ruleName);
        sassRule.uses.clear();
        sassRule.use('null-loader').loader('null-loader');
      }
    }
  },
};
