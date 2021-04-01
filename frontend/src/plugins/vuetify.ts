import Vue from 'vue';
import Vuetify from 'vuetify';
import '@mdi/font/css/materialdesignicons.css';

Vue.use(Vuetify);

const appColors = {
  newOrleans: '#edd693',
  lighterNewOrleans: '#fff4d8',
  flamePea: '#e75f3b',
};

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    themes: {
      light: {
        secondary: appColors.lighterNewOrleans,
        primary: appColors.flamePea,
      },
    },
  },
});
