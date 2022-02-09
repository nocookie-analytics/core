import 'regenerator-runtime/runtime';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import vuetify from './plugins/vuetify';
import './plugins/vee-validate';
import App from './App.vue';
import router from './router';
import store from '@/store';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';
import { initSentry } from './sentry';

Vue.config.productionTip = false;

initSentry();

new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
