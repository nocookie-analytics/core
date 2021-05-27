const webpack = require('webpack');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');

module.exports = {
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
      const sassRule = config.module.rule('sass');
      sassRule.uses.clear();
      sassRule.use('null-loader').loader('null-loader');
    }
    config.module
      .rule('vue')
      .use('vue-loader')
      .loader('vue-loader')
      .tap((options) =>
        Object.assign(options, {
          transformAssetUrls: {
            'v-img': ['src', 'lazy-src'],
            'v-card': 'src',
            'v-card-media': 'src',
            'v-responsive': 'src',
          },
        }),
      );
  },
};
