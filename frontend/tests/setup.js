import Vue from 'vue';
import Vuetify from 'vuetify';

global.requestAnimationFrame = (cb) => cb();
Vue.use(Vuetify);
