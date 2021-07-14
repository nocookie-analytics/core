module.exports = {
  content: [
    `./dist/**/*.html`,
    `./src/**/*.vue`,
    // `./node_modules/vuetify/src/**/*.ts`,
    `./node_modules/uplot/dist/uPlot.min.css`,
    './node_modules/vue2-daterange-picker/dist/vue2-daterange-picker.css',
  ],
  output: '/tmp/purged',
  variables: true,
  safelist: {
    standard: [
      /col-.*/,
      /row-.*/,
      'v-application',
      'v-application--wrap',
      'spacer',
      'button',
    ],
    deep: [
      /-(leave|enter|appear)(|-(to|from|active))$/,
      /^(?!(|.*?:)cursor-move).+-move$/,
      /^router-link(|-exact)-active$/,
      /data-v-.*/,
      /^layout.*/,
      /^container.*/,

      /^v-((?!application).)*$/,
      /^theme--light.*/,
      ///.*-transition/,
      /^justify-.*/,
      /^p-[0-9]/,
      /^m-[0-9]/,
      ///^text--*/,
      ///--text$/,
      /^row-.*/,
      ///^col-*/,
      ///^v-row-*/,
      ///^v-col-*/,
    ],
    greedy: [/v-list-item/, /v-input/, /v-data-table/],
    //greedy: [/v-list-item/, /v-data-table/],
    // greedy: [/d-flex/],
  },
};
