const webpack = require('webpack');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const purgecss = require('@fullhuman/postcss-purgecss');

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
      options[0].fileBlacklist.push(/\/domains-.*/);
      options[0].fileBlacklist.push(/\/users-.*/);
      options[0].fileBlacklist.push(/.*map$/);
      return options;
    });

    config.module
      .rule('css')
      .oneOf('normal')
      .use('postcss-loader')
      .tap((options) => {
        options.plugins.unshift(
          ...[
            require('cssnano'),
            // Shamelessly sourced from
            // https://github.com/ZeusWPI/g2-frontend/blob/6e6b5beddd17f878b63e44a45b27a919e4679755/postcss.config.js
            purgecss({
              content: [
                `./dist/**/*.html`,
                `./src/**/*.vue`,
                `./node_modules/vuetify/src/**/*.ts`,
                `./node_modules/uplot/dist/**`,
              ],
              variables: true,
              whitelist: [
                /**
                 * Vuetify
                 */
                'v-application',
                'v-application--wrap',
                'layout',
                'row',
                'col',
              ],
              whitelistPatterns: [
                /-(leave|enter|appear)(|-(to|from|active))$/,
                /^(?!(|.*?:)cursor-move).+-move$/,
                /^router-link(|-exact)-active$/,
                /data-v-.*/,

                /**
                 * Vuetify
                 */
                /^v-((?!application).)*$/,
                /^theme--*/,
                /.*-transition/,
                /^justify-*/,
                /^p*-[0-9]/,
                /^m*-[0-9]/,
                /^text--*/,
                /--text$/,
                /^row-*/,
                /^col-*/,
              ],
              whitelistPatternsChildren: [
                /**
                 * Vuetify
                 */
                /^v-((?!application).)*$/,
                /^theme--*/,
              ],
            }),
          ],
        );
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
