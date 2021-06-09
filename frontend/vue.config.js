const webpack = require('webpack');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');

module.exports = {
  assetsDir: 'static',
  configureWebpack: {
    plugins: [
      new VuetifyLoaderPlugin(),
      new webpack.IgnorePlugin({
        resourceRegExp: /moment$/,
      }),
    ],
  },

  chainWebpack: (config) => {
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
